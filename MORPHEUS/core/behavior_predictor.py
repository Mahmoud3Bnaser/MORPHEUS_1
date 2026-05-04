"""
MORPHEUS-X Intelligence Engine
Module: behavior_predictor.py

Predicts likely malware behavior based on API combinations and static indicators.
This module uses high-signal combinations of suspicious APIs to infer behavior
patterns without executing the file.
"""

from __future__ import annotations

from typing import Any, Dict, List


# High-signal behavior patterns: combinations of APIs that strongly indicate specific behaviors
BEHAVIOR_PATTERNS: Dict[str, Dict[str, Any]] = {
    "process_injection": {
        "confidence": "high",
        "severity": "critical",
        "description": "File likely performs process injection for code execution or evasion",
        "api_combinations": [
            ["VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread"],
            ["NtCreateThreadEx", "NtWriteVirtualMemory"],
            ["QueueUserAPC", "SetThreadContext", "ResumeThread"],
            ["OpenProcess", "VirtualAllocEx", "WriteProcessMemory"],
        ],
        "indicators": ["process_injection"],
    },
    "persistence": {
        "confidence": "high",
        "severity": "high",
        "description": "File likely establishes persistence through registry or services",
        "api_combinations": [
            ["RegCreateKeyW", "RegSetValueExW"],
            ["RegCreateKeyA", "RegSetValueExA"],
            ["CreateServiceW", "StartServiceW"],
            ["RegSetValueW", "RegSetValueW"],  # Multiple registry writes
        ],
        "indicators": ["persistence"],
    },
    "command_execution": {
        "confidence": "high",
        "severity": "high",
        "description": "File likely executes external commands or scripts",
        "api_combinations": [
            ["CreateProcessA", "CreateProcessW"],
            ["ShellExecuteA", "ShellExecuteW"],
            ["WinExec"],
            ["CreateProcessW", "CreatePipeW"],
        ],
        "indicators": ["command_execution"],
    },
    "data_exfiltration": {
        "confidence": "medium",
        "severity": "high",
        "description": "File likely sends data over the network",
        "api_combinations": [
            ["InternetOpenA", "HttpSendRequestA"],
            ["InternetOpenW", "HttpSendRequestW"],
            ["WinHttpOpen", "WinHttpSendRequest"],
            ["socket", "send"],
            ["URLDownloadToFileA", "URLDownloadToFileW"],
        ],
        "indicators": ["network_communication"],
    },
    "privilege_escalation": {
        "confidence": "medium",
        "severity": "high",
        "description": "File likely attempts to escalate privileges",
        "api_combinations": [
            ["OpenProcessToken", "DuplicateTokenEx"],
            ["AdjustTokenPrivileges"],
            ["ImpersonateLoggedOnUser"],
        ],
        "indicators": ["privilege_escalation"],
    },
    "sandbox_evasion": {
        "confidence": "medium",
        "severity": "medium",
        "description": "File likely attempts to detect and evade sandbox/debugger",
        "api_combinations": [
            ["IsDebuggerPresent", "Sleep"],
            ["CheckRemoteDebuggerPresent"],
            ["OutputDebugStringA", "OutputDebugStringW"],
            ["NtQueryInformationProcess"],
        ],
        "indicators": ["anti_debug"],
    },
    "file_operations": {
        "confidence": "medium",
        "severity": "medium",
        "description": "File likely performs suspicious file operations",
        "api_combinations": [
            ["CreateFileA", "WriteFile", "DeleteFileA"],
            ["CreateFileW", "WriteFile", "DeleteFileW"],
            ["CopyFileA", "CopyFileW"],
            ["MoveFileA", "MoveFileW"],
        ],
        "indicators": ["file_operations"],
    },
    "dll_injection": {
        "confidence": "medium",
        "severity": "high",
        "description": "File likely loads malicious DLLs",
        "api_combinations": [
            ["LoadLibraryA", "GetProcAddress"],
            ["LoadLibraryW", "GetProcAddress"],
            ["LoadLibraryExA", "GetProcAddress"],
            ["LoadLibraryExW", "GetProcAddress"],
        ],
        "indicators": ["dll_injection"],
    },
    "cryptography": {
        "confidence": "low",
        "severity": "medium",
        "description": "File likely uses cryptographic functions",
        "api_combinations": [
            ["CryptEncrypt", "CryptDecrypt"],
            ["CryptHashData"],
            ["CryptDeriveKey"],
        ],
        "indicators": ["cryptography"],
    },
}


def extract_imported_apis(analysis_result: Dict[str, Any]) -> List[str]:
    """
    Extract list of imported APIs from analysis result.

    Args:
        analysis_result: JSON output from analyzer.py

    Returns:
        List of API names.
    """
    apis = []

    # Get high-confidence APIs
    high_confidence = analysis_result.get("high_confidence_suspicious_apis", [])
    for api_item in high_confidence:
        if isinstance(api_item, dict):
            apis.append(api_item.get("name", ""))
        else:
            apis.append(str(api_item))

    # Get all suspicious APIs
    suspicious = analysis_result.get("suspicious_apis", [])
    for api_item in suspicious:
        if isinstance(api_item, dict):
            apis.append(api_item.get("name", ""))
        else:
            apis.append(str(api_item))

    # Get imports
    imports = analysis_result.get("imports", [])
    for imp in imports:
        if isinstance(imp, dict):
            functions = imp.get("functions", [])
            for func in functions:
                if isinstance(func, dict):
                    apis.append(func.get("name", ""))
                else:
                    apis.append(str(func))
        else:
            apis.append(str(imp))

    return list(set(apis))  # Remove duplicates


def check_behavior_pattern(
    apis: List[str], pattern: Dict[str, Any]
) -> bool:
    """
    Check if imported APIs match a behavior pattern.

    Args:
        apis: List of imported API names
        pattern: Behavior pattern with api_combinations

    Returns:
        True if pattern matches.
    """
    combinations = pattern.get("api_combinations", [])

    for combo in combinations:
        # Check if all APIs in the combination are present
        if all(api in apis for api in combo):
            return True

    return False


def predict_behaviors(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict malware behaviors based on API combinations.

    Args:
        analysis_result: JSON output from analyzer.py

    Returns:
        Dictionary with predicted behaviors and confidence levels.
    """
    apis = extract_imported_apis(analysis_result)
    predicted_behaviors = []
    behavior_summary = []

    # Check each behavior pattern
    for behavior_name, pattern_info in BEHAVIOR_PATTERNS.items():
        if check_behavior_pattern(apis, pattern_info):
            # Find which combination matched
            matched_apis = []
            for combo in pattern_info.get("api_combinations", []):
                if all(api in apis for api in combo):
                    matched_apis = combo
                    break

            predicted_behaviors.append(
                {
                    "behavior": behavior_name,
                    "description": pattern_info.get("description", ""),
                    "confidence": pattern_info.get("confidence", "unknown"),
                    "severity": pattern_info.get("severity", "unknown"),
                    "evidence": matched_apis,
                }
            )

            behavior_summary.append(behavior_name)

    # Add string-based behavior predictions
    strings = analysis_result.get("suspicious_strings", [])
    strings_lower = [s.lower() for s in strings] if strings else []

    if any("powershell" in s or "cmd.exe" in s for s in strings_lower):
        if "command_execution" not in behavior_summary:
            predicted_behaviors.append(
                {
                    "behavior": "command_execution",
                    "description": "File contains command execution strings (powershell, cmd.exe)",
                    "confidence": "medium",
                    "severity": "high",
                    "evidence": [s for s in strings if any(x in s.lower() for x in ["powershell", "cmd.exe"])],
                }
            )

    if any("http" in s or "ftp" in s or "url" in s.lower() for s in strings_lower):
        if "data_exfiltration" not in behavior_summary:
            predicted_behaviors.append(
                {
                    "behavior": "data_exfiltration",
                    "description": "File contains network communication strings",
                    "confidence": "medium",
                    "severity": "high",
                    "evidence": [s for s in strings if any(x in s.lower() for x in ["http", "ftp", "url"])],
                }
            )

    if any("hkey_" in s.lower() or "software\\microsoft" in s.lower() for s in strings_lower):
        if "persistence" not in behavior_summary:
            predicted_behaviors.append(
                {
                    "behavior": "persistence",
                    "description": "File contains registry persistence strings",
                    "confidence": "medium",
                    "severity": "high",
                    "evidence": [
                        s
                        for s in strings
                        if any(x in s.lower() for x in ["hkey_", "software\\microsoft"])
                    ],
                }
            )

    # Check for packing (high entropy = potential evasion)
    sections = analysis_result.get("sections", [])
    high_entropy_sections = [
        s.get("name")
        for s in sections
        if float(s.get("entropy", 0.0)) >= 6.7
    ]

    if high_entropy_sections:
        predicted_behaviors.append(
            {
                "behavior": "packing_or_obfuscation",
                "description": "File likely contains packed or obfuscated code",
                "confidence": "high",
                "severity": "high",
                "evidence": high_entropy_sections,
            }
        )

    return {
        "predicted_behaviors": predicted_behaviors,
        "behavior_summary": list(set(behavior_summary)),
        "total_behaviors_detected": len(predicted_behaviors),
    }


def get_behavior_impact(behavior: str) -> str:
    """
    Get human-readable impact description for a behavior.

    Args:
        behavior: Behavior name (e.g., "process_injection")

    Returns:
        Impact description.
    """
    impacts = {
        "process_injection": "Malware can hide code in other processes and evade detection",
        "persistence": "Malware can survive system reboot and remain installed",
        "command_execution": "Malware can execute arbitrary commands on the system",
        "data_exfiltration": "Malware can send data to remote servers",
        "privilege_escalation": "Malware can gain higher system privileges",
        "sandbox_evasion": "Malware can detect and evade analysis environments",
        "file_operations": "Malware can modify or delete files on the system",
        "dll_injection": "Malware can inject malicious code into legitimate processes",
        "cryptography": "Malware uses encryption to hide its activities",
        "packing_or_obfuscation": "Malware is likely compressed/encrypted to avoid detection",
    }
    return impacts.get(behavior, "Unknown behavior impact")
