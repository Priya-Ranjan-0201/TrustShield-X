"""Production Intent & Deep Link Intelligence Engine (Phase 3.7 Part 1A.10).

Discovers, normalizes, enriches, builds navigation graphs, and stores metadata describing Android intent filters and deep links.
Zero malware scoring, threat verdicts, or security alerts.
"""

import time
from typing import List, Dict, Any, Optional, Set
from app.services.intent_catalog import lookup_intent_action
from app.schemas.manifest_intelligence_models import ManifestIntelligenceDTO
from app.schemas.intent_intelligence_models import (
    EnrichedActionDTO,
    EnrichedCategoryDTO,
    EnrichedDeepLinkDTO,
    NavigationNodeDTO,
    IntentStatisticsDTO,
    IntentIntelligenceResultDTO,
    ActionType,
)


class IntentIntelligenceService:
    """Master Intent & Deep Link Intelligence Normalization Engine."""

    def analyze_intents(
        self,
        manifest_dto: ManifestIntelligenceDTO,
    ) -> IntentIntelligenceResultDTO:
        start_time = time.time()

        actions_map: Dict[str, EnrichedActionDTO] = {}
        categories_map: Dict[str, EnrichedCategoryDTO] = {}
        deep_links_list: List[EnrichedDeepLinkDTO] = []
        navigation_nodes: List[NavigationNodeDTO] = []

        stat_filters = 0
        stat_actions = 0
        stat_categories = 0
        stat_deep_links = 0
        stat_launchers = 0
        stat_browsable = 0
        stat_app_links = 0
        stat_custom_schemes = 0
        stat_http = 0
        stat_https = 0
        stat_mime = 0

        all_components = (
            manifest_dto.activities
            + manifest_dto.services
            + manifest_dto.receivers
            + manifest_dto.providers
        )

        for comp in all_components:
            comp_name = comp.name
            for if_obj in comp.intent_filters:
                stat_filters += 1

                # Actions processing
                for action in if_obj.actions:
                    norm_act = action.strip()
                    if norm_act not in actions_map:
                        stat_actions += 1
                        meta = lookup_intent_action(norm_act)
                        act_type = (
                            ActionType.SYSTEM
                            if meta.get("is_system_only", False) or meta.get("is_known", False)
                            else ActionType.CUSTOM
                        )
                        actions_map[norm_act] = EnrichedActionDTO(
                            action_name=norm_act,
                            action_type=act_type,
                            purpose=meta.get("purpose"),
                            is_system_only=meta.get("is_system_only", False),
                        )

                # Categories processing
                has_browsable = False
                has_launcher = False
                for cat in if_obj.categories:
                    norm_cat = cat.strip()
                    if norm_cat not in categories_map:
                        stat_categories += 1
                        is_l = norm_cat == "android.intent.category.LAUNCHER"
                        is_b = norm_cat == "android.intent.category.BROWSABLE"
                        is_d = norm_cat == "android.intent.category.DEFAULT"
                        categories_map[norm_cat] = EnrichedCategoryDTO(
                            category_name=norm_cat,
                            is_launcher=is_l,
                            is_browsable=is_b,
                            is_default=is_d,
                        )

                    if norm_cat == "android.intent.category.BROWSABLE":
                        has_browsable = True
                        stat_browsable += 1
                    if norm_cat == "android.intent.category.LAUNCHER":
                        has_launcher = True
                        stat_launchers += 1

                # Deep Links processing
                if if_obj.schemes:
                    for scheme in if_obj.schemes:
                        norm_scheme = scheme.lower().strip()
                        if norm_scheme == "http":
                            stat_http += 1
                        elif norm_scheme == "https":
                            stat_https += 1
                        else:
                            stat_custom_schemes += 1

                        is_app_link = norm_scheme in ("http", "https") and has_browsable
                        if is_app_link:
                            stat_app_links += 1

                        hosts = if_obj.hosts or [None]
                        for host in hosts:
                            stat_deep_links += 1
                            deep_link_dto = EnrichedDeepLinkDTO(
                                component_name=comp_name,
                                scheme=norm_scheme,
                                host=host,
                                port=if_obj.ports[0] if if_obj.ports else None,
                                path=None,
                                mime_type=if_obj.mime_types[0] if if_obj.mime_types else None,
                                is_app_link=is_app_link,
                                is_browsable=has_browsable,
                                auto_verify=False,
                            )
                            deep_links_list.append(deep_link_dto)

                            # Navigation node graph link
                            for action in if_obj.actions:
                                navigation_nodes.append(
                                    NavigationNodeDTO(
                                        source_component="EXTERNAL_INTENT",
                                        intent_action=action,
                                        target_scheme=norm_scheme,
                                        target_host=host,
                                        destination_component=comp_name,
                                    )
                                )

                if if_obj.mime_types:
                    stat_mime += len(if_obj.mime_types)

        stats = IntentStatisticsDTO(
            total_intent_filters=stat_filters,
            total_actions=len(actions_map),
            total_categories=len(categories_map),
            total_deep_links=stat_deep_links,
            launcher_count=stat_launchers,
            browsable_count=stat_browsable,
            app_links_count=stat_app_links,
            custom_uri_schemes_count=stat_custom_schemes,
            http_links_count=stat_http,
            https_links_count=stat_https,
            mime_filters_count=stat_mime,
        )

        parse_time_ms = int((time.time() - start_time) * 1000)

        return IntentIntelligenceResultDTO(
            actions=list(actions_map.values()),
            categories=list(categories_map.values()),
            deep_links=deep_links_list,
            navigation_nodes=navigation_nodes,
            statistics=stats,
            parsing_time_ms=parse_time_ms,
        )
