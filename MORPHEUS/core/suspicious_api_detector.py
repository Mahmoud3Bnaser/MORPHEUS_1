"""
MORPHEUS-X Static Malware DNA Engine
Module: suspicious_api_detector.py

Detects suspicious Windows API imports and classifies them by malware behavior
category using severity and confidence levels.

This module avoids treating common APIs as highly suspicious unless they appear
in stronger malware-related combinations.
"""

from __future__ import annotations

from typing import Dict, List, Set


SUSPICIOUS_APIS: Dict[str, Dict[str, object]] = {
    "process_injection": {
        "severity": "high",
        "confidence": "high",
        "apis": [
            "OpenProcess",
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread",
            "NtWriteVirtualMemory",
            "NtCreateThreadEx",
            "QueueUserAPC",
            "SetThreadContext",
            "GetThreadContext",
            "ResumeThread",
        ],
    },
    "command_execution": {
        "severity": "high",
        "confidence": "high",
        "apis": [
            "CreateProcessA",
            "CreateProcessW",
            "ShellExecuteA",
            "ShellExecuteW",
            "WinExec",
            "system",
        ],
    },
    "persistence": {
        "severity": "high",
        "confidence": "medium",
        "apis": [
            "RegCreateKeyA",
            "RegCreateKeyW",
            "RegSetValueA",
            "RegSetValueW",
            "RegSetValueExA",
            "RegSetValueExW",
            "CreateServiceA",
            "CreateServiceW",
            "StartServiceA",
            "StartServiceW",
            "OpenSCManagerA",
            "OpenSCManagerW",
        ],
    },
    "network": {
        "severity": "medium",
        "confidence": "medium",
        "apis": [
            "InternetOpenA",
            "InternetOpenW",
            "InternetConnectA",
            "InternetConnectW",
            "HttpOpenRequestA",
            "HttpOpenRequestW",
            "HttpSendRequestA",
            "HttpSendRequestW",
            "WinHttpOpen",
            "WinHttpConnect",
            "WinHttpSendRequest",
            "URLDownloadToFileA",
            "URLDownloadToFileW",
            "connect",
            "send",
            "recv",
            "socket",
        ],
    },
    "anti_debug": {
        "severity": "medium",
        "confidence": "medium",
        "apis": [
            "IsDebuggerPresent",
            "CheckRemoteDebuggerPresent",
            "OutputDebugStringA",
            "OutputDebugStringW",
            "NtQueryInformationProcess",
        ],
    },
    "crypto": {
        "severity": "medium",
        "confidence": "medium",
        "apis": [
            "CryptAcquireContextA",
            "CryptAcquireContextW",
            "CryptEncrypt",
            "CryptDecrypt",
            "CryptGenRandom",
            "BCryptEncrypt",
            "BCryptDecrypt",
        ],
    },
    "memory_manipulation": {
        "severity": "low",
        "confidence": "low",
        "apis": [
            "VirtualAlloc",
            "VirtualProtect",
            "HeapCreate",
            "HeapAlloc",
            "RtlMoveMemory",
            "memcpy",
        ],
    },
    "file_system": {
        "severity": "low",
        "confidence": "low",
        "apis": [
            "CreateFileA",
            "CreateFileW",
            "WriteFile",
            "ReadFile",
            "DeleteFileA",
            "DeleteFileW",
            "CopyFileA",
            "CopyFileW",
            "MoveFileA",
            "MoveFileW",
            "FindFirstFileA",
            "FindFirstFileW",
        ],
    },
    "timing_evasion": {
        "severity": "low",
        "confidence": "low",
        "apis": [
            "Sleep",
            "GetTickCount",
            "QueryPerformanceCounter",
        ],
    },
}


HIGH_SIGNAL_COMBINATIONS = [
    {
        "name": "classic_process_injection_chain",
        "category": "process_injection",
        "severity": "critical",
        "confidence": "high",
        "required_apis": [
            "OpenProcess",
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread",
        ],
        "description": "Classic remote process injection API chain detected.",
    },
    {
        "name": "memory_write_thread_creation_chain",
        "category": "process_injection",
        "severity": "critical",
        "confidence": "high",
        "required_apis": [
            "WriteProcessMemory",
            "CreateRemoteThread",
        ],
        "description": "Memory writing with remote thread creation detected.",
    },
    {
        "name": "download_and_execute_pattern",
        "category": "downloader",
        "severity": "high",
        "confidence": "medium",
        "required_apis": [
            "URLDownloadToFileA",
            "CreateProcessA",
        ],
        "description": "Possible download-and-execute behavior detected.",
    },
    {
        "name": "service_persistence_pattern",
        "category": "persistence",
        "severity": "high",
        "confidence": "high",
        "required_apis": [
            "CreateServiceA",
            "StartServiceA",
        ],
        "description": "Possible Windows service persistence behavior detected.",
    },
]


def normalize_api_name(api_name: str) -> str:
    return api_name.strip() if api_name else ""


def flatten_imports(imports: List[Dict[str, object]]) -> Set[str]:
    api_names: Set[str] = set()

    for imported_dll in imports:
        functions = imported_dll.get("functions", [])

        if not isinstance(functions, list):
            continue

        for function_name in functions:
            if isinstance(function_name, str):
                api_names.add(normalize_api_name(function_name))

    return api_names


def detect_suspicious_apis(imports: List[Dict[str, object]]) -> List[Dict[str, str]]:
    imported_apis = flatten_imports(imports)
    findings: List[Dict[str, str]] = []

    for category, category_data in SUSPICIOUS_APIS.items():
        severity = str(category_data["severity"])
        confidence = str(category_data["confidence"])
        suspicious_api_list = category_data["apis"]

        for suspicious_api in suspicious_api_list:
            if suspicious_api in imported_apis:
                findings.append(
                    {
                        "api": suspicious_api,
                        "category": category,
                        "severity": severity,
                        "confidence": confidence,
                    }
                )

    return findings


def detect_high_signal_combinations(
    imported_apis: Set[str],
) -> List[Dict[str, object]]:
    combinations: List[Dict[str, object]] = []

    for rule in HIGH_SIGNAL_COMBINATIONS:
        required_apis = set(rule["required_apis"])

        if required_apis.issubset(imported_apis):
            combinations.append(
                {
                    "name": rule["name"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "confidence": rule["confidence"],
                    "matched_apis": sorted(required_apis),
                    "description": rule["description"],
                }
            )

    return combinations


def summarize_api_categories(findings: List[Dict[str, str]]) -> Dict[str, int]:
    summary: Dict[str, int] = {}

    for finding in findings:
        category = finding.get("category", "unknown")
        summary[category] = summary.get(category, 0) + 1

    return summary


def filter_high_confidence_findings(
    findings: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    return [
        finding
        for finding in findings
        if finding.get("confidence") in {"medium", "high"}
    ]


def analyze_imported_apis(imports: List[Dict[str, object]]) -> Dict[str, object]:
    imported_apis = flatten_imports(imports)
    findings = detect_suspicious_apis(imports)
    high_confidence_findings = filter_high_confidence_findings(findings)
    combinations = detect_high_signal_combinations(imported_apis)

    return {
        "total_suspicious_apis": len(findings),
        "total_high_confidence_suspicious_apis": len(high_confidence_findings),
        "suspicious_apis": findings,
        "high_confidence_suspicious_apis": high_confidence_findings,
        "category_summary": summarize_api_categories(findings),
        "high_signal_combinations": combinations,
        "total_high_signal_combinations": len(combinations),
    }