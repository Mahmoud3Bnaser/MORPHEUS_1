"""
PERSON 3: DETECTION ENGINEERING - USAGE EXAMPLES

This file shows exactly how to use your YARA Generator and Similarity Engine
in real code. Copy-paste and adapt these examples for your use cases.
"""

import json

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Simple YARA Rule from Suspicious Strings
# ════════════════════════════════════════════════════════════════════════════

from core.yara_generator import generate_strings_rule

# Assume we have a list of suspicious strings from an analysis
suspicious_strings = [
    "powershell.exe",
    "cmd.exe",
    "http://malicious.com",
    "C:\\Windows\\Temp\\",
    "WriteProcessMemory",
    "VirtualAllocEx",
]

# Generate simple string-based rule
string_rule = generate_strings_rule(
    suspicious_strings=suspicious_strings,
    rule_name="simple_malware_detection"
)

print("=" * 80)
print("EXAMPLE 1: Simple String-Based YARA Rule")
print("=" * 80)
print(f"Rule Name: {string_rule['rule_name']}")
print(f"Rule Type: {string_rule['rule_type']}")
print(f"Strings in rule: {len(string_rule['strings'])}")
print(f"\nGenerated YARA Rule:\n")
print(string_rule['yara_rule_text'])
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: YARA Rule from API Patterns
# ════════════════════════════════════════════════════════════════════════════

from core.yara_generator import generate_api_rule

# Simulated imports from Person 1's analyzer
imports = [
    {
        "dll": "kernel32.dll",
        "functions": [
            {"name": "VirtualAllocEx"},
            {"name": "WriteProcessMemory"},
            {"name": "CreateRemoteThread"},
            {"name": "CreateProcess"},
        ],
    },
    {
        "dll": "advapi32.dll",
        "functions": [
            {"name": "RegCreateKeyW"},
            {"name": "RegSetValueExW"},
        ],
    },
    {
        "dll": "ws2_32.dll",
        "functions": [
            {"name": "socket"},
            {"name": "connect"},
            {"name": "send"},
        ],
    },
]

# Generate API pattern rule
api_rule = generate_api_rule(imports=imports, rule_name="trojan_injection_apis")

print("=" * 80)
print("EXAMPLE 2: API Pattern-Based YARA Rule")
print("=" * 80)
print(f"Rule Name: {api_rule['rule_name']}")
print(f"Rule Type: {api_rule['rule_type']}")
print(f"APIs detected: {len(api_rule['strings'])}")
print(f"\nGenerated YARA Rule:\n")
print(api_rule['yara_rule_text'])
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Complete Multi-Vector YARA Rule
# ════════════════════════════════════════════════════════════════════════════

from core.yara_generator import generate_yara_rule

# Complete analysis result from Person 1
complete_analysis = {
    "case_id": "MX-0042",
    "file_name": "ransomware.exe",
    "file_size_bytes": 524288,
    "hashes": {
        "md5": "5d41402abc4b2a76b9719d911017c592",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    "is_pe": True,
    "is_signed": False,
    "packer_indicators": {
        "packer_suspected": True,
        "reasons": ["UPX section detected", "Very low import count"],
    },
    "sections": [
        {
            "name": ".text",
            "entropy": 7.2,
            "characteristics": "EXECUTE | READ",
        },
        {
            "name": "UPX0",
            "entropy": 7.8,
            "characteristics": "EXECUTE | READ | WRITE",
        },
        {
            "name": ".rsrc",
            "entropy": 5.1,
            "characteristics": "READ",
        },
    ],
    "suspicious_strings": [
        "C:\\Users\\%s\\AppData\\",
        "SYSTEM\\CurrentControlSet\\Services",
        "cmd.exe /c",
        "powershell.exe -encodedcommand",
        ".onion",
        "bitcoin:",
    ],
    "high_confidence_suspicious_apis": [
        {"name": "VirtualAllocEx", "severity": "high"},
        {"name": "WriteProcessMemory", "severity": "high"},
        {"name": "CreateRemoteThread", "severity": "high"},
    ],
    "high_signal_combinations": [
        ["VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread"],
        ["RegCreateKeyW", "RegSetValueExW"],
    ],
    "imports": imports,  # From example 2
}

# Generate comprehensive YARA rule
comprehensive_rule = generate_yara_rule(
    analysis_result=complete_analysis,
    rule_name="ransomware_lockbit_family",
    include_strings=True,
    include_sections=True,
    include_metadata=True,
)

print("=" * 80)
print("EXAMPLE 3: Complete Multi-Vector YARA Rule")
print("=" * 80)
print(f"Rule Name: {comprehensive_rule['rule_name']}")
print(f"Rule Type: {comprehensive_rule['rule_type']}")
print(f"Complexity Score: {comprehensive_rule['complexity_score']}/100")
print(f"Total Strings: {len(comprehensive_rule['strings'])}")
print(f"Total Conditions: {len(comprehensive_rule['conditions'])}")
print(f"\nGenerated YARA Rule:\n")
print(comprehensive_rule['yara_rule_text'][:500] + "...\n")


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Export YARA Rule to File
# ════════════════════════════════════════════════════════════════════════════

from core.yara_generator import export_rule_to_file

# Export to .yar format
success, message = export_rule_to_file(
    rule=comprehensive_rule,
    file_path="rules/ransomware_lockbit.yar",
    format="yar"
)

print("=" * 80)
print("EXAMPLE 4: Export YARA Rule")
print("=" * 80)
print(f"Export Status: {'✓ Success' if success else '✗ Failed'}")
print(f"Message: {message}")

# Also export as JSON
success_json, msg_json = export_rule_to_file(
    rule=comprehensive_rule,
    file_path="rules/ransomware_lockbit.json",
    format="json"
)
print(f"JSON Export: {'✓ Success' if success_json else '✗ Failed'}")
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Download Rule Package
# ════════════════════════════════════════════════════════════════════════════

from core.yara_generator import download_rule

# Prepare rule for download
download_package = download_rule(comprehensive_rule, format="yar")

print("=" * 80)
print("EXAMPLE 5: Download YARA Rule Package")
print("=" * 80)
print(f"Filename: {download_package['filename']}")
print(f"Content Type: {download_package['content_type']}")
print(f"Size: {download_package['size_bytes']} bytes")
print(f"Success: {download_package['success']}")
print(f"\nFirst 200 chars of content:")
print(download_package['content'][:200])
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Compare Two Malware Samples for Similarity
# ════════════════════════════════════════════════════════════════════════════

from core.similarity_engine import calculate_similarity

# Second sample for comparison
sample2_analysis = {
    "case_id": "MX-0043",
    "file_name": "ransomware_variant.exe",
    "file_size_bytes": 512000,
    "hashes": {
        "md5": "098f6bcd4621d373cade4e832627b4f6",
        "sha256": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    },
    "is_pe": True,
    "is_signed": False,
    "packer_indicators": {
        "packer_suspected": True,
        "reasons": ["UPX section detected"],
    },
    "sections": complete_analysis["sections"],  # Similar sections
    "suspicious_strings": [
        "C:\\Users\\%s\\AppData\\",  # Same as sample 1
        "SYSTEM\\CurrentControlSet\\Services",  # Same as sample 1
        "cmd.exe /c",  # Same as sample 1
        "http://c2.example.com",  # Different
    ],
    "high_confidence_suspicious_apis": complete_analysis[
        "high_confidence_suspicious_apis"
    ],  # Same APIs
    "high_signal_combinations": complete_analysis["high_signal_combinations"],
    "imports": imports,
}

# Calculate similarity
similarity_report = calculate_similarity(
    analysis1=complete_analysis,
    analysis2=sample2_analysis,
)

print("=" * 80)
print("EXAMPLE 6: Malware Similarity Analysis")
print("=" * 80)
print(f"Sample 1: {similarity_report['sample1']['name']} ({similarity_report['sample1']['md5']})")
print(f"Sample 2: {similarity_report['sample2']['name']} ({similarity_report['sample2']['md5']})")
print()
print(f"Overall Similarity Score: {similarity_report['overall_similarity_score']:.2%}")
print(f"Similarity Level: {similarity_report['similarity_level']}")
print()
print("Individual Metrics:")
for metric, score in similarity_report['metrics'].items():
    bar = "█" * int(score * 20)
    print(f"  {metric:.<35} {score:.2%} {bar}")
print()
print("Recommendations:")
for rec in similarity_report['recommendations']:
    print(f"  {rec}")
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 7: Find Similar Samples from Database
# ════════════════════════════════════════════════════════════════════════════

from core.similarity_engine import find_similar_samples

# Simulated database of samples
database_samples = [
    sample2_analysis,  # 82% similar
    {
        "case_id": "MX-0100",
        "file_name": "trojan_banker.exe",
        "file_size_bytes": 256000,
        "hashes": {"md5": "hash1", "sha256": "hash1"},
        "is_pe": True,
        "suspicious_strings": ["https://bank.com"],
        "imports": [],
    },
]

# Search for similar samples
search_results = find_similar_samples(
    target_analysis=complete_analysis,
    all_samples=database_samples,
    threshold=0.50,  # Find samples 50%+ similar
)

print("=" * 80)
print("EXAMPLE 7: Find Similar Samples (Threat Intelligence)")
print("=" * 80)
print(f"Target Sample: {search_results['target_sample']}")
print(f"Total Compared: {search_results['total_samples_compared']}")
print(f"Threshold: {search_results['threshold']:.0%}")
print()
print("Matches Found:")
if search_results['matches_found']:
    for match in search_results['matches_found']:
        print(
            f"  • {match['sample']:.<35} {match['similarity_score']:.2%} match"
        )
else:
    print("  (No similar samples found)")
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 8: Cluster Malware Samples into Families
# ════════════════════════════════════════════════════════════════════════════

from core.similarity_engine import cluster_samples

# Create extended database
extended_database = [
    complete_analysis,
    sample2_analysis,
    {
        "case_id": "MX-0050",
        "file_name": "ransomware_v2.exe",
        "file_size_bytes": 520000,
        "hashes": {"md5": "hash2", "sha256": "hash2"},
        "is_pe": True,
        "suspicious_strings": complete_analysis["suspicious_strings"],
        "imports": imports,
        "sections": complete_analysis["sections"],
    },
    {
        "case_id": "MX-0051",
        "file_name": "different_malware.exe",
        "file_size_bytes": 100000,
        "hashes": {"md5": "hash3", "sha256": "hash3"},
        "is_pe": True,
        "suspicious_strings": ["http://different.com"],
        "imports": [],
        "sections": [],
    },
]

# Cluster samples
clusters = cluster_samples(all_samples=extended_database, threshold=0.65)

print("=" * 80)
print("EXAMPLE 8: Malware Clustering (Family Detection)")
print("=" * 80)
print(f"Total Samples: {clusters['total_samples']}")
print(f"Clusters Found: {len(clusters['clusters'])}")
print()

for cluster in clusters["clusters"]:
    print(f"{cluster['cluster_id']} ({len(cluster['members'])} members):")
    for member in cluster["members"]:
        confidence = "█" * int(member["score"] * 10)
        print(f"  ├─ {member['sample']:.<35} {member['score']:.0%} {confidence}")
    print()

if clusters['unclustered']:
    print(f"Unclustered Samples ({len(clusters['unclustered'])}):")
    for sample in clusters['unclustered']:
        print(f"  • {sample['sample']}")
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 9: Full Pipeline - Analyze, Generate Rule, Find Similar
# ════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("EXAMPLE 9: Complete Detection Engineering Pipeline")
print("=" * 80)
print("""
Typical workflow:
  1. Person 1 (Static Analyzer) analyzes file → analysis_result
  2. Person 2 (Intelligence Engine) predicts behaviors → behavior_result
  3. Person 3 (Detection Engineering) does:
     a) Generate YARA rule for detection
     b) Find similar samples for threat intelligence
     c) Cluster family members
""")
print()

# Step 1: Generate detection rule
print("Step 1: Generate Detection Rule")
rule = generate_yara_rule(complete_analysis, rule_name="new_threat_family_v1")
print(f"  ✓ Generated rule: {rule['rule_name']}")
print(f"  ✓ Complexity: {rule['complexity_score']}/100")
print()

# Step 2: Export for deployment
print("Step 2: Export for Deployment")
success, msg = export_rule_to_file(rule, "rules/deployment.yar")
print(f"  ✓ Exported: {msg}")
print()

# Step 3: Search threat intelligence database
print("Step 3: Threat Intelligence Search")
search = find_similar_samples(complete_analysis, extended_database, threshold=0.60)
print(f"  ✓ Found {len(search['matches_found'])} related samples")
for match in search['matches_found'][:3]:
    print(f"    - {match['sample']}: {match['similarity_score']:.0%}")
print()

# Step 4: Cluster related samples
print("Step 4: Threat Family Clustering")
families = cluster_samples(extended_database, threshold=0.65)
print(f"  ✓ Identified {len(families['clusters'])} malware families")
print()

print("Pipeline Complete! Detection rule ready for deployment.")
print()


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 10: Custom Similarity Weights
# ════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("EXAMPLE 10: Custom Similarity Weights")
print("=" * 80)
print("""
Customize how different metrics contribute to overall similarity.
Default weights emphasize API patterns (30%) as most reliable signal.
""")
print()

# Default weights
default_report = calculate_similarity(complete_analysis, sample2_analysis)
print(f"Default Weights: {default_report['overall_similarity_score']:.2%}")

# Custom weights - emphasize strings more
custom_weights = {
    "string_similarity": 0.40,  # Boost strings
    "api_similarity": 0.20,     # Lower APIs
    "behavior_similarity": 0.20,
    "metadata_similarity": 0.10,
    "section_similarity": 0.10,
}

custom_report = calculate_similarity(
    complete_analysis,
    sample2_analysis,
    weights=custom_weights
)
print(f"Custom Weights (40% Strings): {custom_report['overall_similarity_score']:.2%}")

# Custom weights - emphasize APIs even more
api_focused_weights = {
    "string_similarity": 0.10,
    "api_similarity": 0.60,  # Heavily weight APIs
    "behavior_similarity": 0.15,
    "metadata_similarity": 0.10,
    "section_similarity": 0.05,
}

api_report = calculate_similarity(
    complete_analysis,
    sample2_analysis,
    weights=api_focused_weights
)
print(f"API-Focused Weights (60% APIs): {api_report['overall_similarity_score']:.2%}")
print()
print("✓ Adjust weights based on your threat intelligence priorities!")
