"""
MORPHEUS-X YARA Rule Generator
Person 3: Detection Engineering - YARA Rule Generation

Generates YARA rules from malware DNA for threat detection.
YARA rules can be used to detect variants of analyzed malware.

Key Functions:
- generate_yara_rule()          → Create YARA rule from analysis
- generate_strings_rule()       → Generate rule from suspicious strings
- generate_api_rule()           → Generate rule from API patterns
- generate_combined_rule()      → Create comprehensive rule
- export_rule_to_file()         → Save rule to .yar format
- download_rule()               → Prepare rule for download
"""

import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime


def generate_yara_rule(
    analysis_result: Dict,
    rule_name: str = None,
    include_strings: bool = True,
    include_sections: bool = True,
    include_metadata: bool = True,
) -> Dict:
    """
    Generate a complete YARA rule from analysis result.

    Args:
        analysis_result: Dictionary from Person 1's analyzer
        rule_name: Custom rule name (auto-generated if None)
        include_strings: Include string-based detections
        include_sections: Include section-based detections
        include_metadata: Include YARA metadata

    Returns:
        Dictionary containing YARA rule components
    """
    if not rule_name:
        case_id = analysis_result.get("case_id", "UNKNOWN")
        rule_name = f"malware_{case_id.replace('-', '_').lower()}"

    rule_components = {
        "rule_name": rule_name,
        "rule_type": "complete",
        "strings": [],
        "conditions": [],
        "metadata": {},
    }

    # Generate metadata
    if include_metadata:
        rule_components["metadata"] = _generate_metadata(analysis_result)

    # Generate string patterns
    if include_strings:
        strings_section = _generate_strings_section(analysis_result)
        rule_components["strings"].extend(strings_section["patterns"])
        rule_components["conditions"].extend(strings_section["conditions"])

    # Generate section-based patterns
    if include_sections:
        section_section = _generate_section_patterns(analysis_result)
        rule_components["strings"].extend(section_section["patterns"])
        rule_components["conditions"].extend(section_section["conditions"])

    # Generate API patterns
    api_section = _generate_api_patterns(analysis_result)
    if api_section["patterns"]:
        rule_components["strings"].extend(api_section["patterns"])
        rule_components["conditions"].extend(api_section["conditions"])

    # Compile final condition
    if rule_components["conditions"]:
        rule_components["final_condition"] = _compile_condition(
            rule_components["conditions"]
        )
    else:
        rule_components["final_condition"] = "none"

    rule_components["generated_at"] = datetime.now().isoformat()
    rule_components["yara_rule_text"] = _render_yara_rule(rule_components)
    rule_components["complexity_score"] = _calculate_rule_complexity(rule_components)

    return rule_components


def _generate_metadata(analysis_result: Dict) -> Dict:
    """Generate YARA metadata section."""
    return {
        "author": "MORPHEUS Detection Engineering",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": analysis_result.get("case_id", "UNKNOWN"),
        "file_name": analysis_result.get("file_name", "unknown"),
        "md5": analysis_result.get("hashes", {}).get("md5", "unknown"),
        "sha256": analysis_result.get("hashes", {}).get("sha256", "unknown"),
        "risk_level": analysis_result.get("risk_level", "unknown"),
        "description": f"Detection rule for malware variant: {analysis_result.get('file_name', 'unknown')}",
    }


def _generate_strings_section(analysis_result: Dict) -> Dict:
    """
    Generate YARA string patterns from suspicious strings.

    Returns dict with 'patterns' (list of strings) and 'conditions' (rules)
    """
    result = {"patterns": [], "conditions": []}
    suspicious_strings = analysis_result.get("suspicious_strings", [])

    if not suspicious_strings:
        return result

    # Group strings by confidence
    high_conf_strings = [
        s
        for s in suspicious_strings
        if isinstance(s, str) and len(s) > 4
    ][:10]
    medium_conf_strings = [
        s
        for s in suspicious_strings
        if isinstance(s, str) and len(s) > 3
    ][10:20]

    # High confidence string patterns (most specific)
    if high_conf_strings:
        for i, string in enumerate(high_conf_strings, 1):
            if _is_valid_yara_string(string):
                var_name = f"str_hc_{i}"
                result["patterns"].append(
                    {
                        "name": var_name,
                        "type": "wide",
                        "value": string,
                        "confidence": "high",
                    }
                )

    # Medium confidence strings
    if medium_conf_strings:
        for i, string in enumerate(medium_conf_strings, 1):
            if _is_valid_yara_string(string):
                var_name = f"str_mc_{i}"
                result["patterns"].append(
                    {
                        "name": var_name,
                        "type": "wide",
                        "value": string,
                        "confidence": "medium",
                    }
                )

    # Add conditions
    if result["patterns"]:
        high_count = len([p for p in result["patterns"] if p["confidence"] == "high"])
        medium_count = len([p for p in result["patterns"] if p["confidence"] == "medium"])

        result["conditions"].append(
            f"{high_count} of (str_hc_*) or {max(1, medium_count//2)} of (str_mc_*)"
        )

    return result


def _generate_section_patterns(analysis_result: Dict) -> Dict:
    """Generate patterns based on PE section characteristics."""
    result = {"patterns": [], "conditions": []}
    sections = analysis_result.get("sections", [])

    if not sections:
        return result

    # Look for suspicious sections
    suspicious_section_names = []
    high_entropy_sections = []

    for section in sections:
        name = section.get("name", "")
        entropy = section.get("entropy", 0)

        # UPX, .packed, etc.
        if any(x in name for x in ["UPX", ".packed", ".rsrc"]):
            suspicious_section_names.append(name)

        # Very high entropy
        if entropy > 7.0:
            high_entropy_sections.append({"name": name, "entropy": entropy})

    # Add section name patterns
    for i, sec_name in enumerate(suspicious_section_names[:5], 1):
        result["patterns"].append(
            {
                "name": f"sec_name_{i}",
                "type": "section",
                "value": sec_name,
                "confidence": "high",
            }
        )

    if result["patterns"]:
        result["conditions"].append(f"1 of (sec_name_*)")

    return result


def _generate_api_patterns(analysis_result: Dict) -> Dict:
    """Generate patterns from suspicious API combinations."""
    result = {"patterns": [], "conditions": []}

    high_signal = analysis_result.get("high_signal_combinations", [])
    high_conf_apis = analysis_result.get("high_confidence_suspicious_apis", [])

    # High-signal API combinations
    api_keywords = []
    for combo in high_signal[:5]:
        if isinstance(combo, list):
            # Create pattern names from API names
            api_keywords.extend(
                [api.lower() if isinstance(api, str) else "" for api in combo]
            )

    # High confidence APIs
    for api in high_conf_apis[:5]:
        if isinstance(api, dict):
            api_keywords.append(api.get("name", "").lower())
        elif isinstance(api, str):
            api_keywords.append(api.lower())

    # Add as hex patterns (API hash/obfuscation detection)
    if api_keywords:
        result["patterns"].append(
            {
                "name": "apis_detected",
                "type": "api",
                "value": api_keywords,
                "confidence": "high",
            }
        )
        result["conditions"].append("2 or more apis_detected")

    return result


def generate_strings_rule(suspicious_strings: List[str], rule_name: str = None) -> Dict:
    """
    Generate a simple YARA rule based on suspicious strings only.

    Args:
        suspicious_strings: List of suspicious strings found in malware
        rule_name: Optional custom rule name

    Returns:
        YARA rule dictionary
    """
    if not rule_name:
        rule_name = "malware_strings_detection"

    rule = {
        "rule_name": rule_name,
        "rule_type": "strings",
        "strings": [],
        "metadata": {
            "author": "MORPHEUS Detection Engineering",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": "String-based malware detection rule",
        },
    }

    # Filter and add strings
    valid_strings = [s for s in suspicious_strings if _is_valid_yara_string(s)][:20]

    for i, string in enumerate(valid_strings, 1):
        rule["strings"].append({"name": f"str_{i}", "value": string, "type": "wide"})

    rule["condition"] = f"{max(1, len(valid_strings)//2)} of them"
    rule["yara_rule_text"] = _render_yara_rule(rule)

    return rule


def generate_api_rule(imports: List[Dict], rule_name: str = None) -> Dict:
    """
    Generate YARA rule based on imported APIs.

    Args:
        imports: List of imported DLLs and functions
        rule_name: Optional custom rule name

    Returns:
        YARA rule dictionary
    """
    if not rule_name:
        rule_name = "malware_api_pattern"

    rule = {
        "rule_name": rule_name,
        "rule_type": "api",
        "strings": [],
        "metadata": {
            "author": "MORPHEUS Detection Engineering",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": "API import pattern detection rule",
        },
    }

    api_list = []
    for dll_entry in imports:
        if isinstance(dll_entry, dict):
            functions = dll_entry.get("functions", [])
            for func in functions[:3]:
                if isinstance(func, dict):
                    api_list.append(func.get("name", ""))
                else:
                    api_list.append(str(func))

    for i, api in enumerate(api_list[:15], 1):
        rule["strings"].append({"name": f"api_{i}", "value": api, "type": "api"})

    rule["condition"] = f"{max(2, len(api_list)//3)} of them"
    rule["yara_rule_text"] = _render_yara_rule(rule)

    return rule


def generate_combined_rule(
    analysis_result: Dict, behavior_result: Dict = None, rule_name: str = None
) -> Dict:
    """
    Generate comprehensive YARA rule combining multiple detection vectors.

    Args:
        analysis_result: Output from Person 1's analyzer
        behavior_result: Optional output from Person 2's behavior predictor
        rule_name: Optional custom rule name

    Returns:
        Comprehensive YARA rule
    """
    main_rule = generate_yara_rule(analysis_result, rule_name)

    # Add behavior-based detections if available
    if behavior_result:
        behaviors = behavior_result.get("predicted_behaviors", [])
        behavior_strings = []

        for behavior in behaviors:
            behavior_name = behavior.get("behavior", "")
            if behavior_name:
                behavior_strings.append(f"// Behavior: {behavior_name}")

        if behavior_strings:
            main_rule["behavior_annotations"] = behavior_strings

    main_rule["complexity_score"] = _calculate_rule_complexity(main_rule)

    return main_rule


def _compile_condition(conditions: List[str]) -> str:
    """Compile multiple conditions into a single YARA condition string."""
    if not conditions:
        return "none"
    if len(conditions) == 1:
        return conditions[0]

    # Smart combining: prefer specificity
    return f"({' and '.join(conditions)})"


def _is_valid_yara_string(s: str) -> bool:
    """Check if string is valid for YARA rule."""
    if not isinstance(s, str) or not s:
        return False

    # Skip very short strings
    if len(s) < 3:
        return False

    # Skip strings with too many special chars
    special_chars = sum(1 for c in s if not c.isalnum() and c not in " _-.")
    if special_chars > len(s) * 0.7:
        return False

    return True


def _calculate_rule_complexity(rule: Dict) -> int:
    """Calculate complexity score (0-100) of a YARA rule."""
    score = 0

    # Base score
    strings = rule.get("strings", [])
    score += min(20, len(strings) * 2)

    # Condition complexity
    conditions = rule.get("conditions", [])
    score += min(30, len(conditions) * 5)

    # Metadata complexity
    metadata = rule.get("metadata", {})
    score += min(20, len(metadata) * 2)

    # Type diversity
    rule_type = rule.get("rule_type", "")
    score += 20 if rule_type == "complete" else 10

    return min(100, score)


def _render_yara_rule(rule_dict: Dict) -> str:
    """
    Render YARA rule dictionary as valid YARA syntax.

    Returns YARA rule as formatted string.
    """
    lines = []

    # Rule header
    rule_name = rule_dict.get("rule_name", "malware_detection")
    lines.append(f"rule {rule_name}")
    lines.append("{")

    # Metadata section
    metadata = rule_dict.get("metadata", {})
    if metadata:
        lines.append("    meta:")
        for key, value in metadata.items():
            # Escape quotes in value
            value_str = str(value).replace('"', '\\"')
            lines.append(f'        {key} = "{value_str}"')
        lines.append("")

    # Strings section
    strings = rule_dict.get("strings", [])
    if strings:
        lines.append("    strings:")
        for string_item in strings:
            name = string_item.get("name", "unknown")
            value = string_item.get("value", "")
            string_type = string_item.get("type", "wide")

            if string_type == "api":
                lines.append(f'        ${name} = "{value}"')
            elif string_type == "section":
                lines.append(f'        ${name} = "{value}"')
            elif string_type == "wide":
                # Escape special chars
                escaped = str(value).replace('"', '\\"')
                lines.append(f'        ${name} = "{escaped}" wide')
            else:
                lines.append(f'        ${name} = "{value}"')

        lines.append("")

    # Condition section
    lines.append("    condition:")
    condition = rule_dict.get("final_condition") or rule_dict.get("condition", "none")
    lines.append(f"        {condition}")

    lines.append("}")

    return "\n".join(lines)


def export_rule_to_file(
    rule: Dict, file_path: str, format: str = "yar"
) -> Tuple[bool, str]:
    """
    Export YARA rule to file.

    Args:
        rule: YARA rule dictionary
        file_path: Path to save rule file
        format: Export format ('yar', 'json')

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        if format == "yar":
            content = rule.get("yara_rule_text", "")
            with open(file_path, "w") as f:
                f.write(content)

        elif format == "json":
            with open(file_path, "w") as f:
                json.dump(rule, f, indent=2)

        else:
            return False, f"Unsupported format: {format}"

        return True, f"Rule exported successfully to {file_path}"

    except Exception as e:
        return False, f"Export failed: {str(e)}"


def download_rule(rule: Dict, format: str = "yar") -> Dict:
    """
    Prepare YARA rule for download.

    Args:
        rule: YARA rule dictionary
        format: Format for download ('yar', 'json')

    Returns:
        Download package with metadata
    """
    download_package = {
        "success": True,
        "rule_name": rule.get("rule_name", "malware_detection"),
        "format": format,
        "created_at": datetime.now().isoformat(),
    }

    if format == "yar":
        download_package["content"] = rule.get("yara_rule_text", "")
        download_package["filename"] = f"{rule.get('rule_name', 'rule')}.yar"
        download_package["content_type"] = "text/plain"

    elif format == "json":
        download_package["content"] = json.dumps(rule, indent=2)
        download_package["filename"] = f"{rule.get('rule_name', 'rule')}.json"
        download_package["content_type"] = "application/json"

    else:
        download_package["success"] = False
        download_package["error"] = f"Unsupported format: {format}"

    download_package["size_bytes"] = len(download_package.get("content", ""))

    return download_package
