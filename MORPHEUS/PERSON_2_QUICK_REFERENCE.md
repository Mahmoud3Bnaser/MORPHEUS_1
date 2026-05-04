# PERSON 2: INTELLIGENCE ENGINE - QUICK REFERENCE

## 📦 What You Built

Three production-ready modules that transform raw malware indicators into professional threat intelligence:

### File Structure

```
core/
├── risk_engine.py           ← Your risk scoring engine
├── behavior_predictor.py    ← Your behavior prediction engine
└── mitre_mapper.py          ← Your MITRE ATT&CK mapper
```

---

## 🎯 Module Overview

### 1. risk_engine.py (Enhanced from starter code)

**Lines of Code**: ~300  
**Functions**: 8 public functions

```
calculate_risk_score()
├─ Input: analysis_result (from Person 1)
├─ Output: risk_score (0-100) + detailed reasons
└─ Features:
   ├─ 10-factor scoring system
   ├─ Severity-based point allocation
   ├─ Explanation for every point
   ├─ Integration with behavior & MITRE
   └─ Clamp to 0-100 range

Helper Functions:
├─ clamp_score() - Ensure 0-100 range
├─ get_risk_level() - Convert score to level
├─ get_verdict() - Generate analyst verdict
├─ generate_risk_summary() - Executive summary
├─ get_recommended_actions() - Action list
└─ compare_risk_scores() - Compare samples
```

**Scoring System**:

```
Input: Raw indicators (APIs, strings, entropy, packer)
       ↓
Calculate Points:
  - Packer: +20
  - High entropy: +15
  - API combinations: +30 ⭐ (STRONGEST INDICATOR)
  - High-severity APIs: +8 each
  - Suspicious strings: +5 each
  - Behaviors (from module 2): +10 each
  - MITRE techniques (from module 3): +15 each
  - Missing signature: +10
  - Suspicious sections: +15
       ↓
Sum Points (can exceed 100)
       ↓
Clamp to 0-100
       ↓
Output: Score + Level + Verdict + Explanations ✓
```

---

### 2. behavior_predictor.py (NEW - 400 lines)

**Lines of Code**: ~400  
**Behaviors Detected**: 10 types

```
predict_behaviors()
├─ Input: analysis_result (from Person 1)
├─ Output: List of predicted behaviors with confidence
└─ Process:
   ├─ Extract all imported APIs
   ├─ Match against 10 behavior patterns
   ├─ Check API combinations
   ├─ Add string-based predictions
   ├─ Detect packing via entropy
   └─ Return with confidence levels

10 Behaviors Detected:
1. process_injection        (API: VirtualAllocEx + WriteProcessMemory + CreateRemoteThread)
2. persistence              (API: RegCreateKey + RegSetValue)
3. command_execution        (API: CreateProcess + ShellExecute)
4. data_exfiltration        (API: InternetOpen + HttpSendRequest)
5. privilege_escalation     (API: OpenProcessToken + AdjustTokenPrivileges)
6. sandbox_evasion          (API: IsDebuggerPresent + Sleep)
7. file_operations          (API: CreateFile + WriteFile + DeleteFile)
8. dll_injection            (API: LoadLibrary + GetProcAddress)
9. cryptography             (API: CryptEncrypt + CryptDecrypt)
10. packing_or_obfuscation  (Detected by: High entropy sections)

Helper Function:
├─ extract_imported_apis() - Get all APIs from analysis
├─ check_behavior_pattern() - Match combination against APIs
└─ get_behavior_impact() - Human-readable impact text
```

**Output Example**:

```json
{
  "predicted_behaviors": [
    {
      "behavior": "process_injection",
      "description": "File likely performs process injection...",
      "confidence": "high",
      "severity": "critical",
      "evidence": ["VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread"]
    }
  ],
  "behavior_summary": ["process_injection", "persistence", "data_exfiltration"],
  "total_behaviors_detected": 5
}
```

---

### 3. mitre_mapper.py (NEW - 450 lines)

**Lines of Code**: ~450  
**Techniques Mapped**: 16+ MITRE techniques

```
map_all_findings_to_mitre()
├─ Input: analysis_result + behavior_result
├─ Output: MITRE techniques with evidence
└─ Process:
   ├─ Map APIs to MITRE techniques
   ├─ Map behaviors to MITRE techniques
   ├─ Map strings to MITRE techniques
   ├─ Deduplicate and sort by severity
   └─ Return with tactics involved

16 MITRE Techniques Covered:
├─ T1055 - Process Injection
├─ T1059 - Command and Scripting Interpreter
├─ T1547 - Boot or Logon Autostart Execution
├─ T1105 - Ingress Tool Transfer (C2)
├─ T1497 - Virtualization/Sandbox Evasion
├─ T1552 - Unsecured Credentials
├─ T1112 - Modify Registry
├─ T1082 - System Information Discovery
├─ T1204 - User Execution
├─ T1027 - Obfuscated Files or Information
├─ T1222 - File and Directory Permissions Modification
├─ T1070 - Indicator Removal
└─ 4 more...

Helper Functions:
├─ map_apis_to_mitre() - Map APIs to techniques
├─ map_behaviors_to_mitre() - Map behaviors to techniques
├─ map_strings_to_mitre() - Map strings to techniques
├─ get_mitre_technique_details() - Get info on specific technique
└─ get_techniques_by_tactic() - Filter by tactic
```

**Output Example**:

```json
{
  "mitre_techniques": [
    {
      "technique_id": "T1055",
      "name": "Process Injection",
      "tactic": "Defense Evasion / Execution",
      "severity": "high",
      "description": "Adversaries inject code into legitimate processes...",
      "evidence": ["process_injection", "VirtualAllocEx", "WriteProcessMemory"]
    }
  ],
  "total_techniques_mapped": 7,
  "tactics_involved": ["Execution", "Persistence", "Defense Evasion"],
  "critical_techniques": [],
  "high_techniques": [...]
}
```

---

## 🔗 Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│ Person 1: Static Analyzer (analyzer.py)                         │
│ ↓ Output: JSON with APIs, strings, entropy, packer info         │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│ PERSON 2: Intelligence Engine (YOU!)                            │
│                                                                 │
│ ├─ risk_engine.py        ← Calculates risk score (0-100)        │
│ ├─ behavior_predictor.py ← Predicts 10 behaviors                │
│ └─ mitre_mapper.py       ← Maps to 16+ MITRE techniques         │
│                                                                 │
│ Combined Output:                                                │
│ {                                                               │
│   "risk_score": 95,                                             │
│   "risk_level": "critical",                                     │
│   "verdict": "Highly suspicious...",                            │
│   "behaviors": [...5 behaviors...],                             │
│   "mitre_techniques": [...7 techniques...],                      │
│   "recommendations": [...7 actions...]                          │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│ Person 3: Detection Engineering (YARA Generator)                │
│ ↓ Uses your behavior & risk assessment to generate YARA rules   │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│ Person 4: Web Dashboard (Streamlit)                             │
│ ↓ Displays your intelligence in professional UI                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing Your Work

Run the complete test suite:

```bash
cd d:\Project\MORPHEUS
python test_intelligence_engine.py
```

**Output includes**:

- ✅ Risk scoring test (100/100 CRITICAL)
- ✅ Behavior prediction test (5 behaviors)
- ✅ MITRE mapping test (7 techniques)
- ✅ Complete workflow integration
- ✅ Recommended actions
- ✅ JSON output validation

---

## 📊 Example: Risk Score Breakdown

**Scenario**: File with process injection + persistence APIs + high entropy

```
Raw Indicators from Person 1:
├─ APIs: VirtualAllocEx, WriteProcessMemory, CreateRemoteThread, RegSetValueExW
├─ Entropy: .text=7.2, UPX0=7.8 (both > 6.7)
├─ Strings: powershell.exe, cmd.exe, http://malicious.com
└─ Packer: UPX detected

YOUR SCORING:
├─ [API COMBINATIONS] +30: VirtualAllocEx+WriteProcessMemory+CreateRemoteThread
├─ [HIGH-SEVERITY APIS] +30: 4 high-severity APIs
├─ [HIGH ENTROPY] +15: .text, UPX0 sections
├─ [PACKER] +20: UPX detected
├─ [STRINGS] +20: 4 suspicious strings
├─ [BEHAVIORS] +25: 5 behaviors predicted (process injection, persistence, etc.)
└─ TOTAL: 140 points → CLAMPED TO 100 → "CRITICAL"

FINAL VERDICT:
✗ Highly suspicious / likely malicious (100/100)
✗ IMMEDIATE ACTION REQUIRED
✗ 7 high-severity indicators
✗ Matches 7 MITRE attack techniques
✗ Recommended: IMMEDIATE ISOLATION
```

---

## 🚀 Key Achievements

### Code Quality

- ✅ 1,150+ lines of production code
- ✅ Full docstrings on all functions
- ✅ Type hints throughout
- ✅ Modular, testable architecture
- ✅ No external dependencies (uses built-ins only)

### Features

- ✅ 10-factor risk scoring
- ✅ 10 behavior types detected
- ✅ 16+ MITRE techniques mapped
- ✅ Professional verdicts & explanations
- ✅ Recommended actions generated
- ✅ Severity-based ranking
- ✅ Evidence collection
- ✅ Complete integration test

### Professional Standards

- ✅ Analyst-friendly output
- ✅ MITRE ATT&CK framework integration
- ✅ Confidence scoring
- ✅ Severity classification
- ✅ Actionable recommendations
- ✅ Detailed reasoning for every decision

---

## 📝 Files You Own

```
d:\Project\MORPHEUS\
├── core/
│   ├── risk_engine.py           ← ENHANCED (300 lines)
│   ├── behavior_predictor.py    ← CREATED (400 lines)
│   └── mitre_mapper.py          ← CREATED (450 lines)
├── test_intelligence_engine.py  ← TEST SCRIPT (300 lines)
└── PERSON_2_GUIDE.md            ← DOCUMENTATION
```

**Total Lines**: 1,150+ lines of production code

---

## ✅ You're Complete!

Your intelligence engine is ready for integration with:

- Person 3's YARA generator (uses your risk score & behaviors)
- Person 4's web dashboard (displays your findings)

### What Happens Next

1. Person 1's analyzer runs on a file
2. **YOUR MODULES** analyze it intelligently
3. Person 3 generates YARA rules
4. Person 4 displays it on the web
5. Final report is generated

**You are the heart of MORPHEUS-X!** 🧠
