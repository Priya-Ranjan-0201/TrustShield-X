"""Production Android Component Intelligence Engine (Phase 3.7 Part 1A.9).

Discovers, normalizes, enriches, connects, and stores metadata describing Android application components.
Zero malware scoring, threat verdicts, or security alerts.
"""

import time
from typing import List, Dict, Any, Optional, Set
from app.services.component_catalog import lookup_component_type
from app.schemas.manifest_intelligence_models import ManifestIntelligenceDTO, ComponentDTO
from app.schemas.component_intelligence_models import (
    EnrichedComponentDTO,
    EnrichedIntentFilterDTO,
    ComponentRelationshipDTO,
    ProcessIntelligenceDTO,
    ComponentStatisticsDTO,
    ComponentIntelligenceResultDTO,
    ExportStatus,
    ProcessType,
)


class ComponentIntelligenceService:
    """Master Android Component Intelligence Normalization & Analysis Engine."""

    def analyze_components(
        self,
        manifest_dto: ManifestIntelligenceDTO,
    ) -> ComponentIntelligenceResultDTO:
        start_time = time.time()

        all_raw_components: List[Tuple[ComponentDTO, str]] = []
        for a in manifest_dto.activities:
            all_raw_components.append((a, "ACTIVITY"))
        for s in manifest_dto.services:
            all_raw_components.append((s, "SERVICE"))
        for r in manifest_dto.receivers:
            all_raw_components.append((r, "RECEIVER"))
        for p in manifest_dto.providers:
            all_raw_components.append((p, "PROVIDER"))

        enriched_components: List[EnrichedComponentDTO] = []
        relationships: List[ComponentRelationshipDTO] = []
        process_map: Dict[str, Tuple[ProcessType, int]] = {}

        stat_activities = 0
        stat_services = 0
        stat_receivers = 0
        stat_providers = 0
        stat_intent_filters = 0
        stat_launchers = 0
        stat_foreground = 0
        stat_exported = 0
        stat_non_exported = 0
        stat_deep_links = 0

        pkg_name = manifest_dto.package_name or "com.app"

        for raw_c, c_type_str in all_raw_components:
            comp_name = raw_c.name
            filters_dto: List[EnrichedIntentFilterDTO] = []

            is_comp_launcher = False
            has_intent_filter = len(raw_c.intent_filters) > 0

            for if_raw in raw_c.intent_filters:
                stat_intent_filters += 1
                is_launcher = (
                    "android.intent.action.MAIN" in if_raw.actions
                    and "android.intent.category.LAUNCHER" in if_raw.categories
                )
                if is_launcher:
                    is_comp_launcher = True
                    stat_launchers += 1

                is_deep_link = any(
                    s.lower() in ("http", "https") for s in if_raw.schemes
                )
                if is_deep_link:
                    stat_deep_links += 1

                filters_dto.append(
                    EnrichedIntentFilterDTO(
                        actions=if_raw.actions,
                        categories=if_raw.categories,
                        schemes=if_raw.schemes,
                        hosts=if_raw.hosts,
                        ports=if_raw.ports,
                        mime_types=if_raw.mime_types,
                        priority=if_raw.priority,
                        auto_verify=False,
                        is_deep_link=is_deep_link,
                        is_launcher=is_launcher,
                    )
                )

            # Export status resolution
            if raw_c.exported is True:
                exp_status = ExportStatus.EXPLICIT_EXPORTED
                stat_exported += 1
            elif raw_c.exported is False:
                exp_status = ExportStatus.NON_EXPORTED
                stat_non_exported += 1
            elif has_intent_filter:
                exp_status = ExportStatus.IMPLICIT_EXPORTED
                stat_exported += 1
            else:
                exp_status = ExportStatus.DEFAULT_EXPORTED
                stat_non_exported += 1

            # Process resolution
            proc_name = raw_c.process or f"{pkg_name}:default"
            if raw_c.process:
                proc_type = ProcessType.CUSTOM if ":" in raw_c.process else ProcessType.SHARED
            else:
                proc_type = ProcessType.DEFAULT

            if proc_name not in process_map:
                process_map[proc_name] = (proc_type, 0)
            p_type, p_count = process_map[proc_name]
            process_map[proc_name] = (p_type, p_count + 1)

            # Component Type counters & Foreground Service check
            is_fg = False
            if c_type_str == "ACTIVITY":
                stat_activities += 1
            elif c_type_str == "SERVICE":
                stat_services += 1
                if raw_c.foreground_service_type:
                    is_fg = True
                    stat_foreground += 1
            elif c_type_str == "RECEIVER":
                stat_receivers += 1
            elif c_type_str == "PROVIDER":
                stat_providers += 1

            # Relationship graph
            relationships.append(
                ComponentRelationshipDTO(
                    parent_component=pkg_name,
                    child_component=comp_name,
                    relationship_type=f"app_contains_{c_type_str.lower()}",
                )
            )

            enriched_components.append(
                EnrichedComponentDTO(
                    name=comp_name,
                    component_type=c_type_str,
                    exported_status=exp_status,
                    is_enabled=raw_c.enabled,
                    permission=raw_c.permission,
                    process_name=proc_name,
                    process_type=proc_type,
                    is_launcher=is_comp_launcher,
                    is_foreground=is_fg,
                    is_isolated=raw_c.multiprocess is False,
                    authorities=raw_c.authorities,
                    launch_mode=raw_c.launch_mode,
                    task_affinity=raw_c.task_affinity,
                    theme=raw_c.theme,
                    intent_filters=filters_dto,
                )
            )

        process_dtos = [
            ProcessIntelligenceDTO(
                process_name=name,
                process_type=ptype,
                component_count=count,
            )
            for name, (ptype, count) in process_map.items()
        ]

        stats = ComponentStatisticsDTO(
            total_components=len(enriched_components),
            activities_count=stat_activities,
            services_count=stat_services,
            receivers_count=stat_receivers,
            providers_count=stat_providers,
            intent_filters_count=stat_intent_filters,
            launcher_activities_count=stat_launchers,
            foreground_services_count=stat_foreground,
            exported_count=stat_exported,
            non_exported_count=stat_non_exported,
            deep_link_count=stat_deep_links,
        )

        parse_time_ms = int((time.time() - start_time) * 1000)

        return ComponentIntelligenceResultDTO(
            components=enriched_components,
            relationships=relationships,
            processes=process_dtos,
            statistics=stats,
            parsing_time_ms=parse_time_ms,
        )
