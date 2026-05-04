"""
PERSON 2: INTELLIGENCE ENGINE - USAGE EXAMPLES

This file shows exactly how to use your three modules in real code.
"""

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Using Risk Engine Alone
# ════════════════════════════════════════════════════════════════════════════

from core.risk_engine import calculate_risk_score, get_recommended_actions

# Assume analysis_result comes from Person 1's analyzer
analysis_result = {
    "packer_indicators": {"packer_suspected": True, "reasons": ["UPX detected"]},
    "sections": [
        {"name": ".text", "entropy": 7.2},
        {"name": ".data", "entropy": 3.5},
    ],
    "high_confidence_suspicious_apis": [
        {"name": "VirtualAllocEx", "severity": "high"},
        {"name": "WriteProcessMemory", "severity": "high"},
    ],
    "suspicious_strings": ["powershell.exe", "cmd.exe"],
    "high_signal_combinations": [
        ["VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread"]
    ],
    "is_pe": True,
    "is_signed": False,
}

# Calculate risk (without behaviors/MITRE)
risk_result = calculate_risk_score(analysis_result)

print(f"Risk Score: {risk_result['risk_score']}/100")
print(f"Risk Level: {risk_result['risk_level']}")
print(f"Verdict: {risk_result['verdict']}")
print("\nTop Reasons:")
for reason in risk_result['risk_reasons'][:3]:
    print(f"  +{reason['points']} points: {reason['reason']}")


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: Using Behavior Predictor
# ════════════════════════════════════════════════════════════════════════════

from core.behavior_predictor import predict_behaviors, get_behavior_impact

# Use the same analysis_result with imports
analysis_result_with_imports = {
    **analysis_result,
    "imports": [
        {
            "dll": "kernel32.dll",
            "functions": [
                {"name": "VirtualAllocEx"},
                {"name": "WriteProcessMemory"},
                {"name": "CreateRemoteThread"},
            ],
        },
        {
            "dll": "advapi32.dll",
            "functions": [
                {"name": "RegCreateKeyW"},
                {"name": "RegSetValueExW"},
            ],
        },
    ],
    "suspicious_strings": ["powershell.exe", "http://malicious.com"],
}

# Predict behaviors
behavior_result = predict_behaviors(analysis_result_with_imports)

print(f"\nDetected {behavior_result['total_behaviors_detected']} behaviors:")
for behavior in behavior_result['predicted_behaviors']:
    print(f"\n  • {behavior['behavior'].upper()}")
    print(f"    Confidence: {behavior['confidence']}")
    print(f"    Severity: {behavior['severity']}")
    print(f"    Impact: {get_behavior_impact(behavior['behavior'])}")


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Using MITRE Mapper
# ════════════════════════════════════════════════════════════════════════════

from core.mitre_mapper import (
    map_all_findings_to_mitre,
    get_mitre_technique_details,
    get_techniques_by_tactic,
)

# Map everything to MITRE
mitre_result = map_all_findings_to_mitre(
    analysis_result_with_imports,
    behavior_result,
)

print(f"\nMapped {mitre_result['total_techniques_mapped']} MITRE techniques:")
for technique in mitre_result['mitre_techniques'][:3]:
    print(f"\n  {technique['technique_id']}: {technique['name']}")
    print(f"  Tactic: {technique['tactic']}")
    print(f"  Evidence: {technique['evidence']}")

# Get details on a specific technique
t1055_details = get_mitre_technique_details("T1055")
print(f"\nT1055 Details: {t1055_details['name']}")
print(f"Description: {t1055_details['description']}")

# Get all persistence techniques
persistence_techs = get_techniques_by_tactic("Persistence")
print(f"\nPersistence Techniques: {[t['technique_id'] for t in persistence_techs]}")


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: COMPLETE WORKFLOW - All Modules Together
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("COMPLETE INTELLIGENCE ENGINE WORKFLOW")
print("="*70)

# Step 1: Get analysis from Person 1
print("\n[STEP 1] Receiving analysis from Person 1...")
sample_file = "suspicious.exe"

# Step 2: Predict behaviors
print("[STEP 2] Predicting behaviors...")
behaviors = predict_behaviors(analysis_result_with_imports)
print(f"  → Detected {behaviors['total_behaviors_detected']} behaviors")

# Step 3: Map to MITRE
print("[STEP 3] Mapping to MITRE ATT&CK...")
mitre_findings = map_all_findings_to_mitre(
    analysis_result_with_imports,
    behaviors,
)
print(f"  → Mapped {mitre_findings['total_techniques_mapped']} techniques")

# Step 4: Calculate final risk (with all intelligence)
print("[STEP 4] Calculating final risk score...")
final_risk = calculate_risk_score(
    analysis_result_with_imports,
    behaviors,
    mitre_findings,
)
print(f"  → Risk Score: {final_risk['risk_score']}/100 [{final_risk['risk_level'].upper()}]")

# Step 5: Generate recommendations
print("[STEP 5] Generating recommendations...")
recommendations = get_recommended_actions(final_risk, final_risk['risk_level'])
print(f"  → {len(recommendations)} recommended actions")

# Step 6: Summary
print("\n" + "="*70)
print("FINAL INTELLIGENCE REPORT")
print("="*70)
print(f"\nFile: {sample_file}")
print(f"Risk Score: {final_risk['risk_score']}/100 - {final_risk['risk_level'].upper()}")
print(f"Verdict: {final_risk['verdict']}\n")

print("Predicted Behaviors:")
for b in behaviors['predicted_behaviors'][:3]:
    print(f"  ✓ {b['behavior']} ({b['confidence']})")

print(f"\nMITRE Techniques:")
for t in mitre_findings['mitre_techniques'][:3]:
    print(f"  ✓ {t['technique_id']} - {t['name']}")

print(f"\nRecommended Actions:")
for action in recommendations[:3]:
    print(f"  → {action}")


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Exporting to JSON (for Person 4's web dashboard)
# ════════════════════════════════════════════════════════════════════════════

import json
from pathlib import Path

# Create complete intelligence report
complete_report = {
    "case_id": "MX-0001",
    "file_name": "suspicious.exe",
    "analysis_timestamp": "2026-05-01T12:00:00Z",
    
    # Risk Assessment (from risk_engine.py)
    "risk_assessment": {
        "score": final_risk['risk_score'],
        "level": final_risk['risk_level'],
        "verdict": final_risk['verdict'],
        "reasons": final_risk['risk_reasons'],
    },
    
    # Behavior Prediction (from behavior_predictor.py)
    "behavior_analysis": {
        "behaviors": behaviors['predicted_behaviors'],
        "summary": behaviors['behavior_summary'],
        "total": behaviors['total_behaviors_detected'],
    },
    
    # MITRE Mapping (from mitre_mapper.py)
    "mitre_analysis": {
        "techniques": mitre_findings['mitre_techniques'],
        "tactics": mitre_findings['tactics_involved'],
        "total": mitre_findings['total_techniques_mapped'],
    },
    
    # Recommendations (from risk_engine.py)
    "recommendations": recommendations,
}

# Save to JSON (Person 4 will read this)
report_path = Path("data/reports/MX-0001_intelligence_report.json")
report_path.parent.mkdir(parents=True, exist_ok=True)

with open(report_path, 'w') as f:
    json.dump(complete_report, f, indent=2)

print(f"\n✅ Intelligence report saved to: {report_path}")


# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Comparing Two Samples
# ════════════════════════════════════════════════════════════════════════════

from core.risk_engine import compare_risk_scores

# Assume we analyzed two samples
sample1_risk = 95
sample2_risk = 45

comparison = compare_risk_scores(sample1_risk, sample2_risk)

print(f"\nSample Comparison:")
print(f"  Sample 1: {sample1_risk}/100 [{comparison['level1']}]")
print(f"  Sample 2: {sample2_risk}/100 [{comparison['level2']}]")
print(f"  Difference: {comparison['difference']} points")
print(f"  Riskier: Sample {1 if comparison['riskier'] == 'first' else 2}")


# ════════════════════════════════════════════════════════════════════════════
# KEY USAGE PATTERNS
# ════════════════════════════════════════════════════════════════════════════

"""
PATTERN 1: Risk Scoring Only
────────────────────────────
result = calculate_risk_score(analysis_result)
Use when: You only need risk score quickly


PATTERN 2: Risk + Behaviors
─────────────────────────
behaviors = predict_behaviors(analysis_result)
result = calculate_risk_score(analysis_result, behaviors)
Use when: You want behavior insights


PATTERN 3: Full Intelligence
────────────────────────────
behaviors = predict_behaviors(analysis_result)
mitre = map_all_findings_to_mitre(analysis_result, behaviors)
result = calculate_risk_score(analysis_result, behaviors, mitre)
Use when: You want complete threat intelligence (RECOMMENDED)


PATTERN 4: MITRE Only
─────────────────────
mitre = map_all_findings_to_mitre(analysis_result)
techniques = mitre['mitre_techniques']
Use when: You only care about MITRE mapping


PATTERN 5: Behavior + MITRE (Skip Risk Scoring)
────────────────────────────────────────────
behaviors = predict_behaviors(analysis_result)
mitre = map_all_findings_to_mitre(analysis_result, behaviors)
Use when: You need behavior + MITRE but not risk scoring
"""


# ════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING
# ════════════════════════════════════════════════════════════════════════════

try:
    # Make sure analysis_result has required fields
    if not analysis_result.get("imports"):
        print("Warning: Missing imports - behavior prediction may be limited")
    
    if not analysis_result.get("suspicious_strings"):
        print("Warning: Missing strings - some behaviors may not be detected")
    
    # Gracefully handle missing fields
    result = calculate_risk_score(analysis_result, behaviors, mitre_findings)
    print("✓ Risk scoring successful")
    
except Exception as e:
    print(f"Error in risk scoring: {e}")
    # Fallback to basic scoring
    result = calculate_risk_score(analysis_result)
    print("✓ Fallback to basic scoring")


# ════════════════════════════════════════════════════════════════════════════
# TESTING YOUR MODULES
# ════════════════════════════════════════════════════════════════════════════

"""
Run the test suite:

$ cd d:\Project\MORPHEUS
$ python test_intelligence_engine.py

This will:
✓ Test risk_engine.py
✓ Test behavior_predictor.py
✓ Test mitre_mapper.py
✓ Test integration
✓ Show example output
✓ Validate JSON format
"""

print("\n" + "="*70)
print("✅ PERSON 2 INTELLIGENCE ENGINE - ALL EXAMPLES COMPLETE")
print("="*70)
