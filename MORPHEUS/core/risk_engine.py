"""
MORPHEUS-X Intelligence Engine
Module: risk_engine.py

Calculates a static malware risk score based on extracted file indicators.
The goal is to produce a clear analyst-friendly verdict, not just raw data.

This module works with behavior_predictor.py and mitre_mapper.py to provide
complete threat intelligence analysis.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def clamp_score(score: int) -> int:
    return max(0, min(score, 100))


def get_risk_level(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 35:
        return "medium"
    return "low"


def get_verdict(score: int, level: str) -> str:
    """
    Get analyst-friendly verdict based on risk score and level.

    Args:
        score: Risk score (0-100)
        level: Risk level (critical, high, medium, low)

    Returns:
        Human-readable verdict.
    """
    if level == "critical":
        return f"Highly suspicious / likely malicious ({score}/100) - IMMEDIATE ACTION REQUIRED"
    if level == "high":
        return f"Suspicious / requires immediate analyst review ({score}/100)"
    if level == "medium":
        return f"Potentially suspicious / review recommended ({score}/100)"
    return f"Low risk / no strong malware behavior detected ({score}/100)"


def generate_risk_summary(risk_result: Dict[str, Any]) -> str:
    """
    Generate executive summary of risk findings.

    Args:
        risk_result: Output from calculate_risk_score

    Returns:
        Professional summary text.
    """
    score = risk_result.get("risk_score", 0)
    level = risk_result.get("risk_level", "unknown")
    reasons = risk_result.get("risk_reasons", [])

    summary = f"\n{'='*60}\n"
    summary += f"MALWARE RISK ASSESSMENT REPORT\n"
    summary += f"{'='*60}\n\n"
    summary += f"RISK SCORE: {score}/100 [{level.upper()}]\n"
    summary += f"VERDICT: {risk_result.get('verdict', 'Unknown')}\n\n"

    summary += "KEY FINDINGS:\n"
    summary += "-" * 60 + "\n"

    for i, reason in enumerate(reasons[:5], 1):  # Top 5 reasons
        summary += f"\n{i}. {reason.get('reason', 'Unknown')}\n"
        summary += f"   Points: +{reason.get('points', 0)}\n"
        summary += f"   Category: {reason.get('category', 'unknown')}\n"
        summary += f"   Explanation: {reason.get('explanation', 'N/A')}\n"
        
        evidence = reason.get('evidence', [])
        if evidence:
            summary += f"   Evidence: {evidence[:3]}\n"

    summary += f"\n{'='*60}\n"
    return summary


def get_recommended_actions(risk_result: Dict[str, Any], level: str) -> List[str]:
    """
    Get recommended actions based on risk level.

    Args:
        risk_result: Output from calculate_risk_score
        level: Risk level

    Returns:
        List of recommended actions.
    """
    actions = {
        "critical": [
            "🚨 IMMEDIATELY ISOLATE the infected system from network",
            "🚨 DO NOT execute the file under any circumstances",
            "🚨 Preserve the file for forensic analysis",
            "🚨 Notify SOC/Security team immediately",
            "🚨 Generate YARA rules and deploy to detection systems",
            "🚨 Check for similar samples in your environment",
            "🚨 Review system logs for indicators of compromise",
        ],
        "high": [
            "⚠️ Quarantine the file immediately",
            "⚠️ Perform detailed reverse engineering analysis",
            "⚠️ Generate and test detection rules",
            "⚠️ Check for sample propagation",
            "⚠️ Review system and network logs",
            "⚠️ Notify relevant security teams",
        ],
        "medium": [
            "⏱️ Schedule analysis for this sample",
            "⏱️ Monitor for any suspicious behavior",
            "⏱️ Consider generating detection rules",
            "⏱️ Keep sample for correlation analysis",
        ],
        "low": [
            "✓ File appears to be benign",
            "✓ No immediate action required",
            "✓ Continue normal operations",
        ],
    }

    return actions.get(level, [])


def compare_risk_scores(score1: int, score2: int) -> Dict[str, Any]:
    """
    Compare two risk scores and provide analysis.

    Args:
        score1: First risk score
        score2: Second risk score

    Returns:
        Comparison analysis.
    """
    return {
        "score1": score1,
        "score2": score2,
        "difference": abs(score1 - score2),
        "riskier": "first" if score1 > score2 else "second" if score2 > score1 else "equal",
        "level1": get_risk_level(score1),
        "level2": get_risk_level(score2),
    }


def calculate_risk_score(
    analysis_result: Dict[str, Any],
    behavior_result: Optional[Dict[str, Any]] = None,
    mitre_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Calculate malware risk score with detailed reasoning.

    Scores range from 0-100:
    - 0-30: Low Risk
    - 31-60: Medium Risk
    - 61-80: High Risk
    - 81-100: Critical Risk

    Args:
        analysis_result: JSON output from analyzer.py
        behavior_result: Output from behavior_predictor.py (optional)
        mitre_result: Output from mitre_mapper.py (optional)

    Returns:
        Dictionary with risk_score, risk_level, verdict, and detailed reasons.
    """
    score = 0
    reasons: List[Dict[str, Any]] = []

    packer = analysis_result.get("packer_indicators", {})
    suspicious_strings = analysis_result.get("suspicious_strings", [])
    high_confidence_apis = analysis_result.get("high_confidence_suspicious_apis", [])
    high_signal_combinations = analysis_result.get("high_signal_combinations", [])
    sections = analysis_result.get("sections", [])

    # 1. Packer Detection (High Risk Indicator)
    if packer.get("packer_suspected"):
        score += 20
        reasons.append(
            {
                "points": 20,
                "category": "packing",
                "reason": "Packer indicators detected",
                "severity": "high",
                "evidence": packer.get("reasons", []),
                "explanation": "Packing/encryption suggests code hiding and evasion tactics",
            }
        )

    # 2. High Entropy Sections (Strong Packing Indicator)
    high_entropy_sections = [
        {"name": section.get("name"), "entropy": float(section.get("entropy", 0.0))}
        for section in sections
        if float(section.get("entropy", 0.0)) >= 6.7
    ]

    if high_entropy_sections:
        score += 15
        reasons.append(
            {
                "points": 15,
                "category": "entropy",
                "reason": "High entropy sections detected",
                "severity": "high",
                "evidence": high_entropy_sections,
                "explanation": "High entropy indicates encrypted/compressed code, typical of malware",
            }
        )

    # 3. High-Signal API Combinations (CRITICAL)
    if high_signal_combinations:
        points = min(len(high_signal_combinations) * 30, 50)
        score += points
        reasons.append(
            {
                "points": points,
                "category": "api_combinations",
                "reason": "High-signal malware behavior combinations detected",
                "severity": "critical",
                "evidence": high_signal_combinations,
                "explanation": "Specific API combinations strongly indicate malware behavior",
            }
        )

    # 4. High-Severity Suspicious APIs
    high_severity_apis = [
        item
        for item in high_confidence_apis
        if item.get("severity") in {"high", "critical"}
    ]

    if high_severity_apis:
        points = min(len(high_severity_apis) * 8, 30)
        score += points
        reasons.append(
            {
                "points": points,
                "category": "apis",
                "reason": "High-confidence suspicious APIs detected",
                "severity": "high",
                "evidence": [api.get("name", "unknown") for api in high_severity_apis],
                "explanation": f"Found {len(high_severity_apis)} dangerous APIs (process injection, persistence, etc.)",
            }
        )

    # 5. Suspicious Strings
    if suspicious_strings:
        points = min(len(suspicious_strings) * 5, 20)
        score += points
        reasons.append(
            {
                "points": points,
                "category": "strings",
                "reason": "Suspicious strings detected",
                "severity": "medium",
                "evidence": suspicious_strings[:10],
                "explanation": f"Found {len(suspicious_strings)} suspicious strings (commands, URLs, registry paths, etc.)",
            }
        )

    # 6. Predicted Behaviors (from behavior_predictor)
    if behavior_result and "predicted_behaviors" in behavior_result:
        behaviors = behavior_result.get("predicted_behaviors", [])
        critical_behaviors = [
            b for b in behaviors if b.get("severity") in {"critical", "high"}
        ]

        if critical_behaviors:
            points = min(len(critical_behaviors) * 10, 25)
            score += points
            reasons.append(
                {
                    "points": points,
                    "category": "predicted_behavior",
                    "reason": "Critical behaviors predicted",
                    "severity": "high",
                    "evidence": [b.get("behavior", "unknown") for b in critical_behaviors],
                    "explanation": f"Predicted {len(critical_behaviors)} dangerous behaviors based on API patterns",
                }
            )

    # 7. MITRE Techniques (from mitre_mapper)
    if mitre_result and "critical_techniques" in mitre_result:
        critical_techniques = mitre_result.get("critical_techniques", [])
        high_techniques = mitre_result.get("high_techniques", [])

        if critical_techniques:
            points = min(len(critical_techniques) * 15, 30)
            score += points
            reasons.append(
                {
                    "points": points,
                    "category": "mitre_techniques",
                    "reason": "Critical MITRE ATT&CK techniques identified",
                    "severity": "critical",
                    "evidence": [t.get("technique_id") for t in critical_techniques],
                    "explanation": f"Matches {len(critical_techniques)} critical attack techniques",
                }
            )

    # 8. File Format Issues
    if not analysis_result.get("is_pe", False):
        score += 5
        reasons.append(
            {
                "points": 5,
                "category": "file_format",
                "reason": "File is not a valid Windows PE executable",
                "severity": "low",
                "evidence": ["Invalid PE structure"],
                "explanation": "Non-standard format may indicate obfuscation or manipulation",
            }
        )

    # 9. No Digital Signature
    if not analysis_result.get("is_signed", False):
        score += 10
        reasons.append(
            {
                "points": 10,
                "category": "signature",
                "reason": "File is not digitally signed",
                "severity": "medium",
                "evidence": ["No valid digital signature found"],
                "explanation": "Unsigned executables are more commonly malicious",
            }
        )

    # 10. Suspicious Section Names
    suspicious_sections = [
        s.get("name")
        for s in sections
        if s.get("name", "").lower() in {
            "upx0", "upx1", "upx2", ".aspack", ".adata", ".packed", 
            ".petite", ".mpress", ".themida", ".vmp0", ".vmp1"
        }
    ]

    if suspicious_sections:
        score += 15
        reasons.append(
            {
                "points": 15,
                "category": "section_names",
                "reason": "Suspicious packer section names detected",
                "severity": "high",
                "evidence": suspicious_sections,
                "explanation": f"Section names {suspicious_sections} are known packer signatures",
            }
        )

    # Clamp final score to 0-100
    final_score = clamp_score(score)
    level = get_risk_level(final_score)

    # Sort reasons by points (highest first)
    reasons_sorted = sorted(reasons, key=lambda x: x.get("points", 0), reverse=True)

    return {
        "risk_score": final_score,
        "risk_level": level,
        "verdict": get_verdict(final_score, level),
        "risk_reasons": reasons_sorted,
        "score_breakdown": {
            "total_points_considered": sum(r.get("points", 0) for r in reasons),
            "total_indicators": len(reasons),
            "high_severity_count": len(
                [r for r in reasons if r.get("severity") in {"high", "critical"}]
            ),
        },
    }