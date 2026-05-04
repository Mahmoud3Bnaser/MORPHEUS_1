"""
MORPHEUS-X Static Malware DNA Engine
Module: analyzer.py

Main static analysis module.

This module analyzes Windows PE files and extracts structured malware DNA:
file metadata, hashes, PE headers, sections, entropy, imports, suspicious APIs,
strings, suspicious strings, and packer indicators.
"""

from __future__ import annotations
from core.risk_engine import calculate_risk_score

import hashlib
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest import result

import pefile

from core.entropy import analyze_entropy, calculate_entropy
from core.string_extractor import analyze_strings
from core.suspicious_api_detector import analyze_imported_apis

ENGINE_NAME = "MORPHEUS Static Malware DNA Engine"
ENGINE_VERSION = "1.0.0"
SCHEMA_VERSION = "1.0"

SUSPICIOUS_SECTION_NAMES = {
    "upx0",
    "upx1",
    "upx2",
    ".aspack",
    ".adata",
    ".packed",
    ".petite",
    ".mpress",
    ".themida",
    ".vmp0",
    ".vmp1",
}



def read_file_bytes(file_path: str) -> bytes:
    """
    Read file bytes safely.

    Args:
        file_path: Path to target file.

    Returns:
        Raw file bytes.
    """
    with open(file_path, "rb") as file:
        return file.read()


def calculate_hashes(data: bytes) -> Dict[str, str]:
    """
    Calculate common malware-analysis hashes.

    Args:
        data: Raw file bytes.

    Returns:
        MD5, SHA1, and SHA256 hashes.
    """
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def get_file_info(file_path: str, data: bytes) -> Dict[str, Any]:
    """
    Extract basic file information.

    Args:
        file_path: Path to target file.
        data: Raw file bytes.

    Returns:
        File metadata dictionary.
    """
    path = Path(file_path)

    return {
        "file_name": path.name,
        "file_path": str(path),
        "file_extension": path.suffix.lower(),
        "file_size_bytes": len(data),
        "file_size_kb": round(len(data) / 1024, 2),
    }


def is_pe_file(data: bytes) -> bool:
    """
    Check if file starts with MZ signature.

    Args:
        data: Raw file bytes.

    Returns:
        True if file appears to be PE.
    """
    return data[:2] == b"MZ"


def safe_decode(value: Optional[bytes]) -> str:
    """
    Decode bytes safely.

    Args:
        value: Bytes value.

    Returns:
        Decoded string.
    """
    if not value:
        return ""

    return value.decode(errors="ignore").strip("\x00").strip()


def extract_pe_headers(pe: pefile.PE) -> Dict[str, Any]:
    """
    Extract important PE header fields.

    Args:
        pe: Parsed PE object.

    Returns:
        PE header dictionary.
    """
    timestamp = pe.FILE_HEADER.TimeDateStamp

    return {
        "machine": hex(pe.FILE_HEADER.Machine),
        "number_of_sections": pe.FILE_HEADER.NumberOfSections,
        "timestamp_raw": timestamp,
        "timestamp_readable": time.strftime(
            "%Y-%m-%d %H:%M:%S UTC", time.gmtime(timestamp)
        ),
        "characteristics": hex(pe.FILE_HEADER.Characteristics),
        "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
        "image_base": hex(pe.OPTIONAL_HEADER.ImageBase),
        "subsystem": pe.OPTIONAL_HEADER.Subsystem,
        "dll_characteristics": hex(pe.OPTIONAL_HEADER.DllCharacteristics),
    }

def extract_section_permissions(characteristics: int) -> Dict[str, bool]:
    """
    Extract readable PE section permissions from section characteristics.

    Args:
        characteristics: PE section characteristics integer.

    Returns:
        Dictionary showing read, write, and execute permissions.
    """
    return {
        "read": bool(characteristics & 0x40000000),
        "write": bool(characteristics & 0x80000000),
        "execute": bool(characteristics & 0x20000000),
    }


def extract_sections(pe: pefile.PE) -> List[Dict[str, Any]]:
    """
    Extract PE section information.

    Args:
        pe: Parsed PE object.

    Returns:
        List of section dictionaries.
    """
    sections: List[Dict[str, Any]] = []

    for section in pe.sections:
        section_name = safe_decode(section.Name)
        section_data = section.get_data()
        entropy_result = analyze_entropy(section_data)

        sections.append(
    {
        "name": section_name,
        "virtual_address": hex(section.VirtualAddress),
        "virtual_size": section.Misc_VirtualSize,
        "raw_size": section.SizeOfRawData,
        "entropy": entropy_result["entropy"],
        "entropy_classification": entropy_result["classification"],
        "suspicious_entropy": entropy_result["suspicious"],
        "characteristics": hex(section.Characteristics),
        "permissions": extract_section_permissions(section.Characteristics),
    }
)

    return sections


def extract_imports(pe: pefile.PE) -> List[Dict[str, Any]]:
    """
    Extract imported DLLs and functions.

    Args:
        pe: Parsed PE object.

    Returns:
        List of imported DLL dictionaries.
    """
    imports: List[Dict[str, Any]] = []

    if not hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        return imports

    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll_name = safe_decode(entry.dll)
        functions: List[str] = []

        for imported_symbol in entry.imports:
            if imported_symbol.name:
                functions.append(safe_decode(imported_symbol.name))
            else:
                functions.append(f"ordinal_{imported_symbol.ordinal}")

        imports.append(
            {
                "dll": dll_name,
                "functions": functions,
                "total_functions": len(functions),
            }
        )

    return imports


def calculate_average_entropy(sections: List[Dict[str, Any]]) -> float:
    """
    Calculate average section entropy.

    Args:
        sections: Extracted PE sections.

    Returns:
        Average entropy.
    """
    if not sections:
        return 0.0

    total_entropy = sum(float(section["entropy"]) for section in sections)

    return round(total_entropy / len(sections), 4)


def detect_packer_indicators(
    sections: List[Dict[str, Any]],
    imports: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Detect basic packer indicators.

    Args:
        sections: Extracted PE sections.
        imports: Extracted imports.

    Returns:
        Packer indicator dictionary.
    """
    reasons: List[str] = []

    average_entropy = calculate_average_entropy(sections)
    total_imported_functions = sum(
        int(imported_dll.get("total_functions", 0)) for imported_dll in imports
    )

    high_entropy_sections = [
        section["name"]
        for section in sections
        if float(section.get("entropy", 0.0)) >= 7.0
    ]

    suspicious_section_names = [
        section["name"]
        for section in sections
        if section["name"].lower() in SUSPICIOUS_SECTION_NAMES
    ]

    if average_entropy >= 6.7:
        reasons.append("High average section entropy detected")

    if high_entropy_sections:
        reasons.append(
            f"High entropy sections detected: {', '.join(high_entropy_sections)}"
        )

    if total_imported_functions <= 5:
        reasons.append("Very low imported function count detected")

    if suspicious_section_names:
        reasons.append(
            f"Suspicious section names detected: {', '.join(suspicious_section_names)}"
        )

    return {
        "packer_suspected": len(reasons) > 0,
        "average_entropy": average_entropy,
        "total_imported_functions": total_imported_functions,
        "high_entropy_sections": high_entropy_sections,
        "suspicious_section_names": suspicious_section_names,
        "reasons": reasons,
    }


def build_summary(
    is_pe: bool,
    sections: List[Dict[str, Any]],
    imports: List[Dict[str, Any]],
    suspicious_api_results: Dict[str, Any],
    string_results: Dict[str, Any],
    packer_indicators: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build final analysis summary.

    Args:
        is_pe: PE status.
        sections: Extracted sections.
        imports: Extracted imports.
        suspicious_api_results: API detection results.
        string_results: String analysis results.
        packer_indicators: Packer detection results.

    Returns:
        Summary dictionary.
    """
    return {
        "is_pe": is_pe,
        "total_sections": len(sections),
        "total_imported_dlls": len(imports),
        "total_suspicious_apis": suspicious_api_results.get(
    "total_suspicious_apis", 0
),
"total_high_confidence_suspicious_apis": suspicious_api_results.get(
    "total_high_confidence_suspicious_apis", 0
),
"total_high_signal_combinations": suspicious_api_results.get(
    "total_high_signal_combinations", 0
),
        "total_strings": string_results.get("total_strings", 0),
        "total_suspicious_strings": string_results.get(
            "total_suspicious_strings", 0
        ),
        "packer_suspected": packer_indicators.get("packer_suspected", False),
    }


def analyze_file(file_path: str) -> Dict[str, Any]:
    """
    Analyze a file and return structured static malware DNA.

    Args:
        file_path: Path to target file.

    Returns:
        Structured analysis result dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    data = read_file_bytes(file_path)
    file_info = get_file_info(file_path, data)
    hashes = calculate_hashes(data)
    pe_status = is_pe_file(data)

    result: Dict[str, Any] = {
    "analysis_metadata": build_analysis_metadata(),
    "file_info": file_info,
    "hashes": hashes,
    "is_pe": pe_status,
    "pe_headers": {},
    "sections": [],
    "imports": [],
    "suspicious_apis": [],
    "high_confidence_suspicious_apis": [],
    "api_category_summary": {},
    "high_signal_combinations": [],
    "strings": [],
    "suspicious_strings": [],
    "packer_indicators": {},
    "summary": {},
    "errors": [],
    "risk": {},
}

    string_results = analyze_strings(data)

    result["strings"] = string_results["strings"]
    result["suspicious_strings"] = string_results["suspicious_strings"]

    if not pe_status:
        result["errors"].append("File does not appear to be a Windows PE file")
        result["summary"] = {
            "is_pe": False,
            "total_strings": string_results.get("total_strings", 0),
            "total_suspicious_strings": string_results.get(
                "total_suspicious_strings", 0
            ),
        }
        return result

    try:
        pe = pefile.PE(file_path)
        result["hashes"]["imphash"] = pe.get_imphash()

        result["pe_headers"] = extract_pe_headers(pe)
        result["sections"] = extract_sections(pe)
        result["imports"] = extract_imports(pe)

        suspicious_api_results = analyze_imported_apis(result["imports"])
        packer_indicators = detect_packer_indicators(
            result["sections"],
            result["imports"],
        )

        result["suspicious_apis"] = suspicious_api_results["suspicious_apis"]
        result["high_confidence_suspicious_apis"] = suspicious_api_results[
            "high_confidence_suspicious_apis"
        ]
        result["api_category_summary"] = suspicious_api_results["category_summary"]
        result["high_signal_combinations"] = suspicious_api_results[
            "high_signal_combinations"
        ]

        result["packer_indicators"] = packer_indicators
        result["packer_indicators"] = packer_indicators

        result["summary"] = build_summary(
            is_pe=pe_status,
            sections=result["sections"],
            imports=result["imports"],
            suspicious_api_results=suspicious_api_results,
            string_results=string_results,
            packer_indicators=packer_indicators,
        )
        result["risk"] = calculate_risk_score(result)

        pe.close()

    except pefile.PEFormatError as error:
        result["errors"].append(f"PE parsing error: {str(error)}")

    result["risk"] = calculate_risk_score(result)

    return result

def build_analysis_metadata() -> Dict[str, Any]:
    """
    Build metadata for the analysis result.

    Returns:
        Analysis metadata dictionary.
    """
    return {
        "engine": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "analysis_type": "static",
        "schema_version": SCHEMA_VERSION,
        "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }