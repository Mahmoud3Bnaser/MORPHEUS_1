"""
MORPHEUS-X Similarity Engine
Person 3: Detection Engineering - Malware Similarity Analysis

Analyzes similarity between malware samples using multiple metrics:
- String similarity
- API similarity
- Behavior similarity
- Behavioral pattern correlation
- Overall similarity scoring

Key Functions:
- calculate_similarity()      → Compare two samples
- compare_strings()           → String pattern comparison
- compare_apis()              → API import comparison
- compare_behaviors()         → Predicted behavior comparison
- calculate_overall_score()   → Composite similarity score
- find_similar_samples()      → Batch comparison
- cluster_samples()           → Group similar samples
- visualize_similarity()      → Generate similarity graph (optional)
"""

import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from difflib import SequenceMatcher


def calculate_similarity(
    analysis1: Dict,
    analysis2: Dict,
    behavior1: Dict = None,
    behavior2: Dict = None,
    weights: Dict = None,
) -> Dict:
    """
    Calculate comprehensive similarity between two malware samples.

    Args:
        analysis1: First sample's analysis result
        analysis2: Second sample's analysis result
        behavior1: Optional behavior prediction for first sample
        behavior2: Optional behavior prediction for second sample
        weights: Custom scoring weights (string, api, behavior, etc.)

    Returns:
        Detailed similarity report with metrics and score
    """
    # Default weights
    if weights is None:
        weights = {
            "strings": 0.25,
            "apis": 0.30,
            "behaviors": 0.25,
            "metadata": 0.10,
            "sections": 0.10,
        }

    report = {
        "sample1": {
            "name": analysis1.get("file_name", "unknown"),
            "md5": analysis1.get("hashes", {}).get("md5", "unknown"),
            "sha256": analysis1.get("hashes", {}).get("sha256", "unknown"),
        },
        "sample2": {
            "name": analysis2.get("file_name", "unknown"),
            "md5": analysis2.get("hashes", {}).get("md5", "unknown"),
            "sha256": analysis2.get("hashes", {}).get("sha256", "unknown"),
        },
        "metrics": {},
        "analysis": {},
        "created_at": datetime.now().isoformat(),
    }

    # Calculate individual metrics
    string_sim = compare_strings(
        analysis1.get("suspicious_strings", []),
        analysis2.get("suspicious_strings", []),
    )
    report["metrics"]["string_similarity"] = string_sim["score"]
    report["analysis"]["strings"] = string_sim

    api_sim = compare_apis(
        analysis1.get("imports", []),
        analysis2.get("imports", []),
    )
    report["metrics"]["api_similarity"] = api_sim["score"]
    report["analysis"]["apis"] = api_sim

    section_sim = compare_sections(
        analysis1.get("sections", []),
        analysis2.get("sections", []),
    )
    report["metrics"]["section_similarity"] = section_sim["score"]
    report["analysis"]["sections"] = section_sim

    metadata_sim = compare_metadata(analysis1, analysis2)
    report["metrics"]["metadata_similarity"] = metadata_sim["score"]
    report["analysis"]["metadata"] = metadata_sim

    # Behavior comparison if available
    if behavior1 and behavior2:
        behavior_sim = compare_behaviors(behavior1, behavior2)
        report["metrics"]["behavior_similarity"] = behavior_sim["score"]
        report["analysis"]["behaviors"] = behavior_sim

    # Calculate overall score
    overall_score = calculate_overall_score(report["metrics"], weights)
    report["overall_similarity_score"] = overall_score
    report["similarity_level"] = _get_similarity_level(overall_score)

    # Generate recommendations
    report["recommendations"] = _generate_recommendations(report)

    return report


def compare_strings(
    strings1: List[str], strings2: List[str], threshold: float = 0.6
) -> Dict:
    """
    Compare suspicious strings between two samples.

    Returns similarity metrics and matching strings.
    """
    result = {
        "score": 0.0,
        "total_strings_sample1": len(strings1),
        "total_strings_sample2": len(strings2),
        "matching_strings": [],
        "unique_to_sample1": [],
        "unique_to_sample2": [],
        "confidence": "medium",
    }

    if not strings1 or not strings2:
        result["score"] = 0.0 if strings1 or strings2 else 1.0
        return result

    strings1_set = set(str(s).lower() for s in strings1 if isinstance(s, str))
    strings2_set = set(str(s).lower() for s in strings2 if isinstance(s, str))

    # Exact matches
    exact_matches = strings1_set & strings2_set
    result["matching_strings"] = list(exact_matches)

    # Unique strings
    result["unique_to_sample1"] = list(strings1_set - strings2_set)[:10]
    result["unique_to_sample2"] = list(strings2_set - strings1_set)[:10]

    # Calculate score
    if exact_matches:
        match_ratio = len(exact_matches) / max(
            len(strings1_set), len(strings2_set)
        )
        result["score"] = min(1.0, match_ratio * 1.5)
        result["confidence"] = "high" if match_ratio > 0.7 else "medium"
    else:
        # Try fuzzy matching
        fuzzy_matches = 0
        for s1 in list(strings1_set)[:30]:
            for s2 in list(strings2_set)[:30]:
                ratio = SequenceMatcher(None, s1, s2).ratio()
                if ratio >= threshold:
                    fuzzy_matches += 1

        if fuzzy_matches > 0:
            result["score"] = min(
                0.7,
                fuzzy_matches / max(len(strings1_set), len(strings2_set)) * 2,
            )
            result["confidence"] = "medium"

    return result


def compare_apis(imports1: List[Dict], imports2: List[Dict]) -> Dict:
    """
    Compare imported APIs and DLLs between two samples.

    Returns similarity metrics.
    """
    result = {
        "score": 0.0,
        "total_dlls_sample1": len(imports1),
        "total_dlls_sample2": len(imports2),
        "matching_dlls": [],
        "matching_apis": [],
        "high_signal_overlap": False,
        "confidence": "medium",
    }

    if not imports1 or not imports2:
        result["score"] = 0.0 if imports1 or imports2 else 1.0
        return result

    # Extract DLL names
    dlls1 = set()
    apis1 = set()
    for imp in imports1:
        if isinstance(imp, dict):
            dll_name = imp.get("dll", "").lower()
            if dll_name:
                dlls1.add(dll_name)
            for func in imp.get("functions", []):
                if isinstance(func, dict):
                    apis1.add(func.get("name", "").lower())
                else:
                    apis1.add(str(func).lower())

    dlls2 = set()
    apis2 = set()
    for imp in imports2:
        if isinstance(imp, dict):
            dll_name = imp.get("dll", "").lower()
            if dll_name:
                dlls2.add(dll_name)
            for func in imp.get("functions", []):
                if isinstance(func, dict):
                    apis2.add(func.get("name", "").lower())
                else:
                    apis2.add(str(func).lower())

    # Matching analysis
    dll_matches = dlls1 & dlls2
    api_matches = apis1 & apis2

    result["matching_dlls"] = list(dll_matches)
    result["matching_apis"] = list(api_matches)[:15]

    # Calculate scores
    dll_score = (
        len(dll_matches) / max(len(dlls1), len(dlls2))
        if max(len(dlls1), len(dlls2)) > 0
        else 0
    )
    api_score = (
        len(api_matches) / max(len(apis1), len(apis2))
        if max(len(apis1), len(apis2)) > 0
        else 0
    )

    # Weight API score more heavily (more specific)
    result["score"] = dll_score * 0.3 + api_score * 0.7

    # Check for critical API overlap
    critical_apis = {"VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread",
                     "CreateProcessA", "CreateProcessW"}
    critical_overlap = len(
        {api.lower() for api in critical_apis} & api_matches
    )
    result["high_signal_overlap"] = critical_overlap >= 2

    if api_matches:
        result["confidence"] = "high" if api_score > 0.6 else "medium"

    return result


def compare_behaviors(behavior1: Dict, behavior2: Dict) -> Dict:
    """
    Compare predicted behaviors between two samples.

    Returns behavior similarity metrics.
    """
    result = {
        "score": 0.0,
        "behaviors_sample1": [],
        "behaviors_sample2": [],
        "matching_behaviors": [],
        "behavior_count_sample1": 0,
        "behavior_count_sample2": 0,
        "shared_severity": [],
    }

    behaviors_set1 = set()
    behaviors_set2 = set()

    for behavior in behavior1.get("predicted_behaviors", []):
        behavior_name = behavior.get("behavior", "").lower()
        if behavior_name:
            behaviors_set1.add(behavior_name)
        result["behaviors_sample1"].append(
            {
                "name": behavior_name,
                "severity": behavior.get("severity", "unknown"),
            }
        )

    for behavior in behavior2.get("predicted_behaviors", []):
        behavior_name = behavior.get("behavior", "").lower()
        if behavior_name:
            behaviors_set2.add(behavior_name)
        result["behaviors_sample2"].append(
            {
                "name": behavior_name,
                "severity": behavior.get("severity", "unknown"),
            }
        )

    result["behavior_count_sample1"] = len(behaviors_set1)
    result["behavior_count_sample2"] = len(behaviors_set2)

    # Matching behaviors
    matching = behaviors_set1 & behaviors_set2
    result["matching_behaviors"] = list(matching)

    # Calculate score
    if max(len(behaviors_set1), len(behaviors_set2)) > 0:
        result["score"] = len(matching) / max(len(behaviors_set1), len(behaviors_set2))

    # Analyze severity overlap
    severity_scores = {}
    for b1 in result["behaviors_sample1"]:
        for b2 in result["behaviors_sample2"]:
            if b1["name"] == b2["name"]:
                sev = b1.get("severity", "unknown")
                if sev not in severity_scores:
                    severity_scores[sev] = 0
                severity_scores[sev] += 1

    result["shared_severity"] = [
        {"severity": sev, "count": count} for sev, count in severity_scores.items()
    ]

    return result


def compare_sections(sections1: List[Dict], sections2: List[Dict]) -> Dict:
    """
    Compare PE sections between samples.

    Returns section similarity metrics.
    """
    result = {
        "score": 0.0,
        "section_count_sample1": len(sections1),
        "section_count_sample2": len(sections2),
        "matching_sections": [],
        "entropy_similarity": 0.0,
    }

    if not sections1 or not sections2:
        return result

    # Compare section names
    names1 = {s.get("name", "").lower() for s in sections1}
    names2 = {s.get("name", "").lower() for s in sections2}
    matching_names = names1 & names2
    result["matching_sections"] = list(matching_names)

    # Compare entropy profiles
    entropies1 = [s.get("entropy", 0) for s in sections1]
    entropies2 = [s.get("entropy", 0) for s in sections2]

    if entropies1 and entropies2:
        avg_entropy1 = sum(entropies1) / len(entropies1)
        avg_entropy2 = sum(entropies2) / len(entropies2)
        entropy_diff = abs(avg_entropy1 - avg_entropy2)
        result["entropy_similarity"] = max(0, 1 - (entropy_diff / 8))

    # Calculate overall score
    name_score = (
        len(matching_names) / max(len(names1), len(names2))
        if max(len(names1), len(names2)) > 0
        else 0
    )
    result["score"] = (name_score * 0.4) + (result["entropy_similarity"] * 0.6)

    return result


def compare_metadata(analysis1: Dict, analysis2: Dict) -> Dict:
    """
    Compare file metadata attributes.

    Returns metadata similarity metrics.
    """
    result = {
        "score": 0.0,
        "file_size_similarity": 0.0,
        "packer_match": False,
        "is_pe_match": False,
    }

    # File size comparison
    size1 = analysis1.get("file_size_bytes", 0)
    size2 = analysis2.get("file_size_bytes", 0)

    if size1 and size2:
        size_ratio = min(size1, size2) / max(size1, size2)
        result["file_size_similarity"] = size_ratio
    else:
        result["file_size_similarity"] = 0.5

    # Packer match
    packer1 = analysis1.get("packer_indicators", {}).get("packer_suspected", False)
    packer2 = analysis2.get("packer_indicators", {}).get("packer_suspected", False)
    result["packer_match"] = packer1 == packer2

    # PE format match
    pe1 = analysis1.get("is_pe", False)
    pe2 = analysis2.get("is_pe", False)
    result["is_pe_match"] = pe1 == pe2

    # Calculate score
    score = 0
    if result["packer_match"]:
        score += 0.3
    if result["is_pe_match"]:
        score += 0.2
    score += result["file_size_similarity"] * 0.5

    result["score"] = min(1.0, score)

    return result


def calculate_overall_score(
    metrics: Dict, weights: Dict = None
) -> float:
    """
    Calculate weighted overall similarity score.

    Args:
        metrics: Dictionary of similarity scores
        weights: Custom weights for each metric

    Returns:
        Overall similarity score (0.0 - 1.0)
    """
    if weights is None:
        weights = {
            "string_similarity": 0.25,
            "api_similarity": 0.30,
            "behavior_similarity": 0.25,
            "metadata_similarity": 0.10,
            "section_similarity": 0.10,
        }

    total_weight = 0
    weighted_sum = 0

    for metric_name, weight in weights.items():
        if metric_name in metrics:
            weighted_sum += metrics[metric_name] * weight
            total_weight += weight

    if total_weight == 0:
        return 0.0

    return weighted_sum / total_weight


def find_similar_samples(
    target_analysis: Dict, all_samples: List[Dict], threshold: float = 0.5
) -> Dict:
    """
    Find similar samples from a list using batch comparison.

    Args:
        target_analysis: Reference sample to compare
        all_samples: List of samples to search
        threshold: Minimum similarity score (0-1)

    Returns:
        List of similar samples with scores
    """
    results = {
        "target_sample": target_analysis.get("file_name", "unknown"),
        "total_samples_compared": len(all_samples),
        "matches_found": [],
        "threshold": threshold,
        "search_completed_at": datetime.now().isoformat(),
    }

    similarities = []

    for sample in all_samples:
        # Skip the target itself
        if sample.get("hashes", {}).get("md5") == target_analysis.get("hashes", {}).get(
            "md5"
        ):
            continue

        # Quick similarity check (lightweight)
        quick_sim = _quick_similarity(target_analysis, sample)

        if quick_sim >= threshold:
            similarities.append(
                {
                    "sample": sample.get("file_name", "unknown"),
                    "md5": sample.get("hashes", {}).get("md5", "unknown"),
                    "similarity_score": quick_sim,
                }
            )

    # Sort by similarity score
    similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
    results["matches_found"] = similarities[:20]

    return results


def cluster_samples(
    all_samples: List[Dict], threshold: float = 0.6
) -> Dict:
    """
    Cluster similar malware samples.

    Args:
        all_samples: List of analysis results
        threshold: Similarity threshold for clustering

    Returns:
        Clusters of similar samples
    """
    clusters = {
        "total_samples": len(all_samples),
        "clusters": [],
        "unclustered": [],
        "created_at": datetime.now().isoformat(),
    }

    if len(all_samples) < 2:
        clusters["unclustered"] = all_samples
        return clusters

    used = set()

    for i, sample in enumerate(all_samples):
        if i in used:
            continue

        cluster = {
            "cluster_id": f"cluster_{len(clusters['clusters'])}",
            "members": [
                {
                    "sample": sample.get("file_name", "unknown"),
                    "md5": sample.get("hashes", {}).get("md5", "unknown"),
                    "score": 1.0,
                }
            ],
        }

        # Find similar samples
        for j in range(i + 1, len(all_samples)):
            if j in used:
                continue

            sim = _quick_similarity(sample, all_samples[j])
            if sim >= threshold:
                cluster["members"].append(
                    {
                        "sample": all_samples[j].get("file_name", "unknown"),
                        "md5": all_samples[j].get("hashes", {}).get("md5", "unknown"),
                        "score": sim,
                    }
                )
                used.add(j)

        clusters["clusters"].append(cluster)
        used.add(i)

    # Unclustered samples
    for i, sample in enumerate(all_samples):
        if i not in used:
            clusters["unclustered"].append(
                {
                    "sample": sample.get("file_name", "unknown"),
                    "md5": sample.get("hashes", {}).get("md5", "unknown"),
                }
            )

    return clusters


def _quick_similarity(analysis1: Dict, analysis2: Dict) -> float:
    """Quick lightweight similarity check for batch operations."""
    score = 0

    # API similarity (strongest signal)
    api_sim = compare_apis(
        analysis1.get("imports", []),
        analysis2.get("imports", []),
    )
    score += api_sim["score"] * 0.4

    # String similarity
    string_sim = compare_strings(
        analysis1.get("suspicious_strings", []),
        analysis2.get("suspicious_strings", []),
    )
    score += string_sim["score"] * 0.3

    # Section similarity
    section_sim = compare_sections(
        analysis1.get("sections", []),
        analysis2.get("sections", []),
    )
    score += section_sim["score"] * 0.2

    # Metadata
    metadata_sim = compare_metadata(analysis1, analysis2)
    score += metadata_sim["score"] * 0.1

    return min(1.0, score)


def _get_similarity_level(score: float) -> str:
    """Convert score to human-readable similarity level."""
    if score >= 0.9:
        return "NEAR_IDENTICAL"
    elif score >= 0.7:
        return "HIGHLY_SIMILAR"
    elif score >= 0.5:
        return "MODERATELY_SIMILAR"
    elif score >= 0.3:
        return "SOMEWHAT_SIMILAR"
    else:
        return "DISSIMILAR"


def _generate_recommendations(report: Dict) -> List[str]:
    """Generate actionable recommendations based on similarity analysis."""
    recommendations = []
    overall_score = report.get("overall_similarity_score", 0)
    similarity_level = report.get("similarity_level", "")

    if overall_score >= 0.9:
        recommendations.append("⚠️ CRITICAL: These samples appear nearly identical!")
        recommendations.append("🔍 Samples are likely variants of the same malware family.")
        recommendations.append("🛡️ Deploy identical detection rules for both samples.")

    elif overall_score >= 0.7:
        recommendations.append("⚠️ ALERT: High similarity detected between samples.")
        recommendations.append(
            "📊 Samples likely share common malware source or toolkit."
        )
        recommendations.append("🎯 Consider consolidated threat response.")

    elif overall_score >= 0.5:
        recommendations.append("📌 Moderate similarity suggests potential connection.")
        recommendations.append("🔗 Samples may be part of same campaign.")

    # API-specific recommendations
    api_score = report.get("metrics", {}).get("api_similarity", 0)
    if api_score > 0.7:
        recommendations.append("⚙️ Similar API patterns: Check for process injection or data theft.")

    # Behavior-specific recommendations
    behavior_analysis = report.get("analysis", {}).get("behaviors", {})
    matching_behaviors = behavior_analysis.get("matching_behaviors", [])
    if matching_behaviors:
        recommendations.append(f"🚨 Both samples exhibit: {', '.join(matching_behaviors)}")

    return recommendations


def visualize_similarity(
    similarity_report: Dict, output_format: str = "dict"
) -> Dict:
    """
    Generate similarity visualization data.

    Args:
        similarity_report: Output from calculate_similarity()
        output_format: 'dict' for data structure or 'graph' for graph metadata

    Returns:
        Visualization data
    """
    viz = {
        "sample1": similarity_report["sample1"]["name"],
        "sample2": similarity_report["sample2"]["name"],
        "metrics": similarity_report["metrics"],
        "overall_score": similarity_report["overall_similarity_score"],
        "similarity_level": similarity_report["similarity_level"],
        "nodes": [],
        "edges": [],
    }

    # Create nodes for visualization
    node_id = 0
    metric_nodes = {}

    for metric_name, score in similarity_report["metrics"].items():
        metric_nodes[metric_name] = {
            "id": node_id,
            "label": metric_name.replace("_", " ").title(),
            "value": score,
            "size": int(score * 100) + 20,
        }
        viz["nodes"].append(metric_nodes[metric_name])
        node_id += 1

    # Add edges (connections between metrics)
    for metric_name in metric_nodes:
        viz["edges"].append(
            {
                "source": metric_nodes[metric_name]["id"],
                "target": 0,  # Connect to first metric as center
                "weight": similarity_report["metrics"].get(metric_name, 0),
            }
        )

    return viz
