"""
MORPHEUS-X Intelligence Engine
Module: mitre_mapper.py

Maps malware analysis findings to MITRE ATT&CK techniques.
This module creates a bridge between technical indicators and real-world attack frameworks.

MITRE ATT&CK is a knowledge base of adversary tactics and techniques
based on real-world observations.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set


# MITRE ATT&CK Framework Mapping
# Maps APIs, behaviors, and indicators to MITRE techniques
MITRE_TECHNIQUES: Dict[str, Dict[str, Any]] = {
    "T1055": {
        "name": "Process Injection",
        "tactic": "Defense Evasion / Execution",
        "severity": "high",
        "apis": [
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread",
            "NtWriteVirtualMemory",
            "NtCreateThreadEx",
            "QueueUserAPC",
            "SetThreadContext",
            "GetThreadContext",
            "ResumeThread",
            "OpenProcess",
        ],
        "behaviors": ["process_injection"],
        "description": "Adversaries inject code into legitimate processes to evade security mechanisms",
    },
    "T1059": {
        "name": "Command and Scripting Interpreter",
        "tactic": "Execution",
        "severity": "high",
        "apis": [
            "CreateProcessA",
            "CreateProcessW",
            "ShellExecuteA",
            "ShellExecuteW",
            "WinExec",
            "system",
        ],
        "behaviors": ["command_execution"],
        "description": "Adversaries execute commands through command-line interfaces",
    },
    "T1547": {
        "name": "Boot or Logon Autostart Execution",
        "tactic": "Persistence",
        "severity": "high",
        "apis": [
            "RegCreateKeyA",
            "RegCreateKeyW",
            "RegSetValueA",
            "RegSetValueW",
            "RegSetValueExA",
            "RegSetValueExW",
            "CreateServiceA",
            "CreateServiceW",
        ],
        "behaviors": ["persistence"],
        "strings": [
            "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "Run",
            "RunOnce",
        ],
        "description": "Adversary ensures malware runs automatically on system startup",
    },
    "T1105": {
        "name": "Ingress Tool Transfer",
        "tactic": "Command and Control",
        "severity": "high",
        "apis": [
            "InternetOpenA",
            "InternetOpenW",
            "InternetConnectA",
            "InternetConnectW",
            "HttpOpenRequestA",
            "HttpOpenRequestW",
            "HttpSendRequestA",
            "HttpSendRequestW",
            "URLDownloadToFileA",
            "URLDownloadToFileW",
            "socket",
            "send",
            "recv",
            "connect",
            "WinHttpOpen",
            "WinHttpConnect",
            "WinHttpSendRequest",
        ],
        "behaviors": ["data_exfiltration"],
        "strings": ["http://", "https://", "ftp://", "POST /", "GET /"],
        "description": "Adversaries transfer tools or malware over the network",
    },
    "T1497": {
        "name": "Virtualization/Sandbox Evasion",
        "tactic": "Defense Evasion",
        "severity": "medium",
        "apis": [
            "IsDebuggerPresent",
            "CheckRemoteDebuggerPresent",
            "OutputDebugStringA",
            "OutputDebugStringW",
            "NtQueryInformationProcess",
            "QueryPerformanceCounter",
            "GetTickCount",
            "Sleep",
        ],
        "behaviors": ["sandbox_evasion"],
        "description": "Adversaries detect and evade analysis environments to prevent detection",
    },
    "T1552": {
        "name": "Unsecured Credentials",
        "tactic": "Credential Access",
        "severity": "high",
        "apis": ["RegOpenKeyA", "RegOpenKeyW", "RegQueryValueA", "RegQueryValueW"],
        "behaviors": ["credential_access"],
        "strings": ["password", "username", "api_key", "token"],
        "description": "Adversaries extract credentials stored in memory or files",
    },
    "T1112": {
        "name": "Modify Registry",
        "tactic": "Defense Evasion",
        "severity": "high",
        "apis": [
            "RegSetValueA",
            "RegSetValueW",
            "RegSetValueExA",
            "RegSetValueExW",
            "RegDeleteKeyA",
            "RegDeleteKeyW",
        ],
        "behaviors": ["persistence"],
        "description": "Adversaries modify registry to change system behavior or disable security",
    },
    "T1082": {
        "name": "System Information Discovery",
        "tactic": "Discovery",
        "severity": "medium",
        "apis": [
            "GetSystemInfo",
            "GetComputerNameA",
            "GetComputerNameW",
            "GetUserNameA",
            "GetUserNameW",
            "GetProcessorCount",
        ],
        "behaviors": ["reconnaissance"],
        "description": "Adversaries gather information about the system they are on",
    },
    "T1204": {
        "name": "User Execution",
        "tactic": "Execution",
        "severity": "medium",
        "apis": ["ShellExecuteA", "ShellExecuteW", "CreateProcessA", "CreateProcessW"],
        "behaviors": ["command_execution"],
        "description": "Adversaries rely on user interaction to execute malware",
    },
    "T1027": {
        "name": "Obfuscated Files or Information",
        "tactic": "Defense Evasion",
        "severity": "high",
        "apis": ["CryptEncrypt", "CryptDecrypt", "CryptHashData"],
        "behaviors": ["packing_or_obfuscation"],
        "description": "Adversaries obscure malware to avoid detection and analysis",
    },
    "T1222": {
        "name": "File and Directory Permissions Modification",
        "tactic": "Defense Evasion",
        "severity": "medium",
        "apis": ["SetFileAttributesA", "SetFileAttributesW"],
        "behaviors": ["file_operations"],
        "description": "Adversaries modify file permissions to maintain access",
    },
    "T1070": {
        "name": "Indicator Removal",
        "tactic": "Defense Evasion",
        "severity": "high",
        "apis": ["DeleteFileA", "DeleteFileW", "SHDeleteValueA", "SHDeleteValueW"],
        "behaviors": ["file_operations"],
        "description": "Adversaries remove artifacts or traces of their activities",
    },
}


def map_apis_to_mitre(apis: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Map imported APIs to MITRE ATT&CK techniques.

    Args:
        apis: List of imported API names

    Returns:
        Dictionary mapping MITRE technique IDs to details.
    """
    api_set = set(api.lower() for api in apis)
    mitre_findings = {}

    for technique_id, technique_data in MITRE_TECHNIQUES.items():
        technique_apis = set(
            api.lower() for api in technique_data.get("apis", [])
        )

        # Check if any APIs match
        matching_apis = api_set.intersection(technique_apis)

        if matching_apis:
            if technique_id not in mitre_findings:
                mitre_findings[technique_id] = {
                    "technique_id": technique_id,
                    "name": technique_data.get("name", "Unknown"),
                    "tactic": technique_data.get("tactic", "Unknown"),
                    "severity": technique_data.get("severity", "unknown"),
                    "description": technique_data.get("description", ""),
                    "evidence": list(matching_apis),
                }

    return mitre_findings


def map_behaviors_to_mitre(behaviors: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Map predicted behaviors to MITRE ATT&CK techniques.

    Args:
        behaviors: List of behavior names from behavior_predictor

    Returns:
        Dictionary mapping MITRE technique IDs to details.
    """
    behavior_set = set(b.lower() for b in behaviors)
    mitre_findings = {}

    for technique_id, technique_data in MITRE_TECHNIQUES.items():
        technique_behaviors = set(
            b.lower() for b in technique_data.get("behaviors", [])
        )

        # Check if behaviors match
        matching_behaviors = behavior_set.intersection(technique_behaviors)

        if matching_behaviors:
            if technique_id not in mitre_findings:
                mitre_findings[technique_id] = {
                    "technique_id": technique_id,
                    "name": technique_data.get("name", "Unknown"),
                    "tactic": technique_data.get("tactic", "Unknown"),
                    "severity": technique_data.get("severity", "unknown"),
                    "description": technique_data.get("description", ""),
                    "evidence": list(matching_behaviors),
                }

    return mitre_findings


def map_strings_to_mitre(strings: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Map suspicious strings to MITRE ATT&CK techniques.

    Args:
        strings: List of suspicious strings from analyzer

    Returns:
        Dictionary mapping MITRE technique IDs to details.
    """
    strings_lower = set(s.lower() for s in strings) if strings else set()
    mitre_findings = {}

    for technique_id, technique_data in MITRE_TECHNIQUES.items():
        technique_strings = technique_data.get("strings", [])

        if not technique_strings:
            continue

        matching_strings = [
            s for s in technique_strings if any(s.lower() in str_item.lower() for str_item in strings_lower)
        ]

        if matching_strings:
            if technique_id not in mitre_findings:
                mitre_findings[technique_id] = {
                    "technique_id": technique_id,
                    "name": technique_data.get("name", "Unknown"),
                    "tactic": technique_data.get("tactic", "Unknown"),
                    "severity": technique_data.get("severity", "unknown"),
                    "description": technique_data.get("description", ""),
                    "evidence": matching_strings,
                }

    return mitre_findings


def map_all_findings_to_mitre(
    analysis_result: Dict[str, Any],
    behavior_result: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Map all findings (APIs, behaviors, strings) to MITRE ATT&CK techniques.

    This is the main entry point that combines all mapping sources.

    Args:
        analysis_result: JSON output from analyzer.py
        behavior_result: Output from behavior_predictor.py (optional)

    Returns:
        Dictionary with complete MITRE ATT&CK mapping.
    """
    all_mitre_findings: Dict[str, Dict[str, Any]] = {}

    # Extract APIs
    apis = []
    for imp in analysis_result.get("imports", []):
        if isinstance(imp, dict):
            for func in imp.get("functions", []):
                if isinstance(func, dict):
                    apis.append(func.get("name", ""))
                else:
                    apis.append(str(func))

    # Map APIs to MITRE
    api_mitre = map_apis_to_mitre(apis)
    all_mitre_findings.update(api_mitre)

    # Map behaviors if provided
    if behavior_result:
        behaviors = [b.get("behavior", "") for b in behavior_result.get("predicted_behaviors", [])]
        behavior_mitre = map_behaviors_to_mitre(behaviors)
        all_mitre_findings.update(behavior_mitre)

    # Map strings
    strings = analysis_result.get("suspicious_strings", [])
    string_mitre = map_strings_to_mitre(strings)
    all_mitre_findings.update(string_mitre)

    # Sort by severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}
    sorted_findings = sorted(
        all_mitre_findings.values(),
        key=lambda x: severity_order.get(x.get("severity", "unknown"), 5),
    )

    return {
        "mitre_techniques": sorted_findings,
        "total_techniques_mapped": len(sorted_findings),
        "critical_techniques": [
            t for t in sorted_findings if t.get("severity") == "critical"
        ],
        "high_techniques": [
            t for t in sorted_findings if t.get("severity") == "high"
        ],
        "tactics_involved": list(
            set(t.get("tactic", "Unknown") for t in sorted_findings)
        ),
    }


def get_mitre_technique_details(technique_id: str) -> Dict[str, Any] | None:
    """
    Get detailed information about a specific MITRE technique.

    Args:
        technique_id: MITRE technique ID (e.g., "T1055")

    Returns:
        Technique details or None if not found.
    """
    return MITRE_TECHNIQUES.get(technique_id)


def get_techniques_by_tactic(tactic: str) -> List[Dict[str, Any]]:
    """
    Get all MITRE techniques that use a specific tactic.

    Args:
        tactic: Tactic name (e.g., "Execution", "Persistence")

    Returns:
        List of techniques using that tactic.
    """
    techniques = []
    for technique_id, data in MITRE_TECHNIQUES.items():
        if tactic.lower() in data.get("tactic", "").lower():
            techniques.append({
                "technique_id": technique_id,
                "name": data.get("name", ""),
                "tactic": data.get("tactic", ""),
                "severity": data.get("severity", "unknown"),
            })
    return techniques
