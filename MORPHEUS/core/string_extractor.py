"""
MORPHEUS-X Static Malware DNA Engine
Module: string_extractor.py

Extracts readable ASCII and UTF-16LE strings from binary files and identifies
high-signal suspicious strings with false-positive reduction.
"""

from __future__ import annotations

import re
from typing import Dict, List


DEFAULT_MIN_LENGTH = 4
MAX_RETURNED_STRINGS = 5000


SUSPICIOUS_STRING_PATTERNS: Dict[str, List[str]] = {
    "command_execution": [
        "cmd.exe",
        "powershell",
        "powershell.exe",
        "wscript.exe",
        "cscript.exe",
        "rundll32.exe",
        "mshta.exe",
        "schtasks.exe",
        "regsvr32.exe",
    ],
    "network_indicator": [
        "http://",
        "https://",
        "ftp://",
        "User-Agent:",
        "POST /",
        "GET /",
        "Mozilla/",
    ],
    "registry_persistence": [
        "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "CurrentVersion\\RunOnce",
        "CurrentVersion\\RunServices",
    ],
    "suspicious_paths": [
        "\\AppData\\Roaming\\",
        "\\AppData\\Local\\Temp\\",
        "\\Windows\\Temp\\",
        "\\ProgramData\\",
    ],
    "anti_analysis": [
        "IsDebuggerPresent",
        "CheckRemoteDebuggerPresent",
        "NtQueryInformationProcess",
        "VirtualBox",
        "VMware",
        "VBoxGuest",
        "VBoxService",
        "sandbox",
        "debugger",
        "wireshark",
        "procmon",
        "procexp",
    ],
    "credential_access": [
        "password=",
        "passwd=",
        "login=",
        "credential",
        "Authorization:",
        "Bearer ",
        "Cookie:",
    ],
}


BENIGN_SUBSTRINGS = [
    "http://schemas.microsoft.com",
    "https://schemas.microsoft.com",
    "http://www.w3.org",
    "https://www.w3.org",
    "microsoft.com/fwlink",
    "api-ms-win-",
    "ext-ms-win-",
]


def extract_ascii_strings(data: bytes, min_length: int = DEFAULT_MIN_LENGTH) -> List[str]:
    if not data:
        return []

    pattern = rb"[\x20-\x7E]{" + str(min_length).encode() + rb",}"
    matches = re.findall(pattern, data)

    return [match.decode("ascii", errors="ignore").strip() for match in matches]


def extract_utf16le_strings(data: bytes, min_length: int = DEFAULT_MIN_LENGTH) -> List[str]:
    if not data:
        return []

    pattern = rb"(?:[\x20-\x7E]\x00){" + str(min_length).encode() + rb",}"
    matches = re.findall(pattern, data)

    strings: List[str] = []

    for match in matches:
        decoded = match.decode("utf-16le", errors="ignore").strip()
        if len(decoded) >= min_length:
            strings.append(decoded)

    return strings


def extract_strings(data: bytes, min_length: int = DEFAULT_MIN_LENGTH) -> List[str]:
    ascii_strings = extract_ascii_strings(data, min_length)
    utf16_strings = extract_utf16le_strings(data, min_length)

    unique_strings = sorted(set(ascii_strings + utf16_strings))

    return unique_strings[:MAX_RETURNED_STRINGS]


def is_probably_benign_string(value: str) -> bool:
    lowered = value.lower()

    for benign in BENIGN_SUBSTRINGS:
        if benign.lower() in lowered:
            return True

    return False


def detect_suspicious_strings(strings: List[str]) -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    seen = set()

    for extracted_string in strings:
        if is_probably_benign_string(extracted_string):
            continue

        lowered_string = extracted_string.lower()

        for category, patterns in SUSPICIOUS_STRING_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in lowered_string:
                    key = (extracted_string, category, pattern)

                    if key not in seen:
                        findings.append(
                            {
                                "string": extracted_string,
                                "category": category,
                                "matched_pattern": pattern,
                            }
                        )
                        seen.add(key)

                    break

    return findings


def analyze_strings(data: bytes, min_length: int = DEFAULT_MIN_LENGTH) -> Dict[str, object]:
    strings = extract_strings(data, min_length)
    suspicious_strings = detect_suspicious_strings(strings)

    return {
        "total_strings": len(strings),
        "strings": strings,
        "suspicious_strings": suspicious_strings,
        "total_suspicious_strings": len(suspicious_strings),
    }