"""Production DEX Structure Intelligence Engine (Phase 3.7 Part 1A.13).

Parses Dalvik Executable (Multi-DEX) files to extract structural metadata:
- Header metadata
- Package tree hierarchy & depth
- Class definitions & flags
- Method signatures & prototype offsets
- Field declarations & access flags
- String inventory
- Type graph
- Complexity statistics

Zero bytecode execution, zero malware detection, zero security verdicts.
"""

import os
import io
import time
import struct
import hashlib
import zipfile
from typing import List, Dict, Any, Optional, Tuple, Set
from app.schemas.dex_structure_models import (
    DEXHeaderDTO,
    PackageNodeDTO,
    ClassStructureDTO,
    MethodStructureDTO,
    FieldStructureDTO,
    StringEntryDTO,
    TypeEntryDTO,
    DEXStructureStatisticsDTO,
    DEXStructureResultDTO,
)


class DEXStructureService:
    """Master DEX Structure Intelligence Engine."""

    def parse_dex_header(self, data: bytes) -> Optional[DEXHeaderDTO]:
        """Parses standard 112-byte DEX file header."""
        if len(data) < 112:
            return None

        try:
            magic = data[0:8].decode("ascii", errors="replace")
            dex_ver = magic[4:7] if len(magic) >= 7 else "035"
            checksum = struct.unpack("<I", data[8:12])[0]
            sha1 = data[12:32].hex()
            file_size = struct.unpack("<I", data[32:36])[0]
            header_size = struct.unpack("<I", data[36:40])[0]
            endian_tag = struct.unpack("<I", data[40:44])[0]
            link_size = struct.unpack("<I", data[44:48])[0]
            link_offset = struct.unpack("<I", data[48:52])[0]
            map_offset = struct.unpack("<I", data[52:56])[0]
            string_count = struct.unpack("<I", data[56:60])[0]
            string_off = struct.unpack("<I", data[60:64])[0]
            type_count = struct.unpack("<I", data[64:68])[0]
            proto_count = struct.unpack("<I", data[72:76])[0]
            field_count = struct.unpack("<I", data[80:84])[0]
            method_count = struct.unpack("<I", data[88:92])[0]
            class_count = struct.unpack("<I", data[96:100])[0]
            data_size = struct.unpack("<I", data[100:104])[0]
            data_offset = struct.unpack("<I", data[104:108])[0]

            return DEXHeaderDTO(
                dex_version=dex_ver,
                magic=magic,
                checksum=checksum,
                sha1=sha1,
                file_size=file_size,
                header_size=header_size,
                endian_tag=endian_tag,
                link_size=link_size,
                link_offset=link_offset,
                map_offset=map_offset,
                string_count=string_count,
                type_count=type_count,
                proto_count=proto_count,
                field_count=field_count,
                method_count=method_count,
                class_count=class_count,
                data_size=data_size,
                data_offset=data_offset,
            )
        except Exception:
            return None

    def analyze_dex_structure(
        self,
        dex_files_bytes: List[Tuple[str, bytes]],
    ) -> DEXStructureResultDTO:
        start_time = time.time()

        headers: List[DEXHeaderDTO] = []
        classes: List[ClassStructureDTO] = []
        methods: List[MethodStructureDTO] = []
        fields: List[FieldStructureDTO] = []
        strings_dict: Dict[str, StringEntryDTO] = {}
        types_dict: Dict[str, TypeEntryDTO] = {}
        packages_dict: Dict[str, Dict[str, int]] = {}

        for dex_name, dex_bytes in dex_files_bytes:
            hdr = self.parse_dex_header(dex_bytes)
            if hdr:
                headers.append(hdr)

            # High-performance passive inspection using androguard if available
            try:
                from androguard.core.bytecodes.dvd import DalvikVMFormat
                d = DalvikVMFormat(dex_bytes)

                # Extract Strings
                for idx, s_item in enumerate(d.get_strings()):
                    s_val = str(s_item)
                    s_hash = hashlib.sha256(s_val.encode("utf-8", errors="replace")).hexdigest()
                    if s_val not in strings_dict:
                        strings_dict[s_val] = StringEntryDTO(
                            string_value=s_val[:1024],
                            length=len(s_val),
                            string_hash=s_hash,
                            offset=idx * 4,
                            referenced_count=1,
                        )

                # Extract Classes, Methods, Fields, Types
                for c in d.get_classes():
                    c_name_raw = c.get_name()  # Lcom/example/App;
                    formatted_cname = c_name_raw.lstrip("L").rstrip(";").replace("/", ".")
                    simple_cname = formatted_cname.split(".")[-1]
                    pkg_name = ".".join(formatted_cname.split(".")[:-1]) or "default"

                    superclass_raw = c.get_superclassname()
                    formatted_super = superclass_raw.lstrip("L").rstrip(";").replace("/", ".") if superclass_raw else "java.lang.Object"

                    # Package tracking
                    if pkg_name not in packages_dict:
                        packages_dict[pkg_name] = {"classes": 0, "methods": 0}
                    packages_dict[pkg_name]["classes"] += 1

                    types_dict[formatted_cname] = TypeEntryDTO(type_name=formatted_cname, kind="OBJECT")

                    class_dto = ClassStructureDTO(
                        full_name=formatted_cname,
                        simple_name=simple_cname,
                        package_name=pkg_name,
                        superclass=formatted_super,
                        interfaces=[i.lstrip("L").rstrip(";").replace("/", ".") for i in c.get_interfaces()],
                        access_flags=c.get_access_flags(),
                        is_abstract="abstract" in c.get_access_flags_string(),
                        is_final="final" in c.get_access_flags_string(),
                        is_public="public" in c.get_access_flags_string(),
                        is_inner="$" in simple_cname,
                        source_file=c.get_source_file(),
                    )
                    classes.append(class_dto)

                    # Extract Methods
                    for m in c.get_methods():
                        packages_dict[pkg_name]["methods"] += 1
                        m_name = m.get_name()
                        ret_type = m.get_triple()[2]
                        param_types = [p for p in m.get_triple()[1]]
                        m_access = m.get_access_flags_string()

                        m_code = m.get_code()
                        reg_count = m_code.get_registers_size() if m_code else 0
                        ins_count = len(m_code.get_bc().get_instructions()) if m_code else 0

                        method_dto = MethodStructureDTO(
                            method_name=m_name,
                            class_name=formatted_cname,
                            package_name=pkg_name,
                            return_type=ret_type,
                            parameter_types=param_types,
                            access_flags=m.get_access_flags(),
                            is_constructor=m_name in ("<init>", "<clinit>"),
                            is_static="static" in m_access,
                            is_abstract="abstract" in m_access,
                            is_native="native" in m_access,
                            register_count=reg_count,
                            instruction_count=ins_count,
                        )
                        methods.append(method_dto)

                    # Extract Fields
                    for f in c.get_fields():
                        f_name = f.get_name()
                        f_type = f.get_descriptor()
                        f_access = f.get_access_flags_string()

                        field_dto = FieldStructureDTO(
                            field_name=f_name,
                            class_name=formatted_cname,
                            package_name=pkg_name,
                            field_type=f_type,
                            access_flags=f.get_access_flags(),
                            is_static="static" in f_access,
                            is_final="final" in f_access,
                        )
                        fields.append(field_dto)
            except Exception:
                pass

        # Build Package Tree
        package_nodes: List[PackageNodeDTO] = []
        for pkg_name, counts in packages_dict.items():
            parent = ".".join(pkg_name.split(".")[:-1]) if "." in pkg_name else None
            depth = len(pkg_name.split(".")) if pkg_name != "default" else 0
            package_nodes.append(
                PackageNodeDTO(
                    package_name=pkg_name,
                    parent_package=parent,
                    depth=depth,
                    class_count=counts["classes"],
                    method_count=counts["methods"],
                )
            )

        # Statistics
        total_pkgs = len(package_nodes)
        total_cls = len(classes)
        total_meths = len(methods)
        total_flds = len(fields)
        total_strs = len(strings_dict)
        avg_meths = round(total_meths / total_cls, 2) if total_cls > 0 else 0.0

        largest_pkg = max(packages_dict.items(), key=lambda x: x[1]["classes"])[0] if packages_dict else None
        largest_cls = max(classes, key=lambda c: len(c.full_name)).full_name if classes else None

        stats = DEXStructureStatisticsDTO(
            total_packages=total_pkgs,
            total_classes=total_cls,
            total_methods=total_meths,
            total_fields=total_flds,
            total_strings=total_strs,
            avg_methods_per_class=avg_meths,
            largest_package=largest_pkg,
            largest_class=largest_cls,
        )

        parse_time_ms = int((time.time() - start_time) * 1000)

        return DEXStructureResultDTO(
            headers=headers,
            packages=package_nodes,
            classes=classes,
            methods=methods,
            fields=fields,
            strings=list(strings_dict.values()),
            types=list(types_dict.values()),
            statistics=stats,
            parsing_time_ms=parse_time_ms,
        )
