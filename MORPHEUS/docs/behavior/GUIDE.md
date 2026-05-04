# MORPHEUS-X: Behavior Intelligence Engine Documentation

## 📋 Overview

The Behavior Intelligence Engine is responsible for building the **intelligence layer** - the brain that analyzes malware DNA and produces professional threat intelligence.

This module receives raw analysis data from the **Static Analyzer** and produces:

- ✅ Risk scores with explanations
- ✅ Predicted malware behaviors
- ✅ MITRE ATT&CK technique mappings
- ✅ Recommended actions

---

## 🧠 Three Core Modules

### 1️⃣ **risk_engine.py** - Risk Scoring & Verdict

**Purpose**: Calculate a 0-100 risk score and generate analyst-friendly verdicts

**Key Functions**:

```python
calculate_risk_score(analysis_result, behavior_result, mitre_result)
  ↓ Returns: risk_score, risk_level, verdict, reasons (with explanations)

generate_risk_summary(risk_result)
  ↓ Returns: Professional summary text

get_recommended_actions(risk_result, level)
  ↓ Returns: List of actions based on risk level

compare_risk_scores(score1, score2)
  ↓ Returns: Comparison analysis
```

**Scoring Logic** (what adds points):

- Packer indicators: **+20 points**
- High entropy sections: **+15 points**
- High-signal API combinations: **+30 points** (MOST IMPORTANT)
- High-severity APIs: **+8 points each** (max +30)
- Suspicious strings: **+5 points each** (max +20)
- Predicted critical behaviors: **+10 points each** (max +25)
- Critical MITRE techniques: **+15 points each** (max +30)
- Missing signature: **+10 points**
- Suspicious section names: **+15 points**
- Invalid PE format: **+5 points**

**Risk Levels**:

- 0-30: 🟢 **LOW** - Safe file
- 31-60: 🟡 **MEDIUM** - Review recommended
- 61-80: 🔴 **HIGH** - Dangerous, isolate
- 81-100: 🔴 **CRITICAL** - Highly malicious

---

### 2️⃣ **behavior_predictor.py** - Behavior Prediction Engine

**Purpose**: Predict malware behavior from API combinations without executing the file

**Key Functions**:

```python
predict_behaviors(analysis_result)
  ↓ Returns: List of predicted behaviors with confidence levels

get_behavior_impact(behavior_name)
  ↓ Returns: Human-readable impact description
```

**10 Behavior Types Predicted**:

1. **process_injection** (HIGH RISK)
   - APIs: VirtualAllocEx, WriteProcessMemory, CreateRemoteThread
   - Impact: Malware hides in other processes

2. **persistence** (HIGH RISK)
   - APIs: RegCreateKeyW, RegSetValueExW, CreateServiceW
   - Impact: Survives reboot

3. **command_execution** (HIGH RISK)
   - APIs: CreateProcessA/W, ShellExecuteA/W
   - Impact: Execute arbitrary commands

4. **data_exfiltration** (HIGH RISK)
   - APIs: InternetOpenW, HttpSendRequestW, URLDownloadToFileW
   - Impact: Send data to attackers

5. **privilege_escalation** (HIGH RISK)
   - APIs: OpenProcessToken, AdjustTokenPrivileges
   - Impact: Gain higher privileges

6. **sandbox_evasion** (MEDIUM RISK)
   - APIs: IsDebuggerPresent, Sleep, NtQueryInformationProcess
   - Impact: Detect and evade analysis

7. **file_operations** (MEDIUM RISK)
   - APIs: CreateFileA/W, WriteFile, DeleteFileA/W
   - Impact: Modify/delete files

8. **dll_injection** (HIGH RISK)
   - APIs: LoadLibraryA/W, GetProcAddress
   - Impact: Load malicious DLLs

9. **cryptography** (MEDIUM RISK)
   - APIs: CryptEncrypt, CryptDecrypt
   - Impact: Hide activities with encryption

10. **packing_or_obfuscation** (HIGH RISK)
    - Detected by: High entropy sections
    - Impact: Compressed/encrypted to avoid detection

---

### 3️⃣ **mitre_mapper.py** - MITRE ATT&CK Framework Mapping

**Purpose**: Map findings to real-world attack techniques from MITRE ATT&CK

**Key Functions**:

```python
map_all_findings_to_mitre(analysis_result, behavior_result)
  ↓ Returns: MITRE techniques with evidence and severity

map_apis_to_mitre(apis)
  ↓ Returns: Techniques mapped to specific APIs

map_behaviors_to_mitre(behaviors)
  ↓ Returns: Techniques mapped to behaviors

get_mitre_technique_details(technique_id)
  ↓ Returns: Details of a specific technique (e.g., T1055)

get_techniques_by_tactic(tactic_name)
  ↓ Returns: All techniques using a specific tactic
```

**MITRE Techniques You Map To** (16 total, here's a sample):

| Technique ID | Name                              | Tactic          | APIs                                                   |
| ------------ | --------------------------------- | --------------- | ------------------------------------------------------ |
| **T1055**    | Process Injection                 | Defense Evasion | VirtualAllocEx, WriteProcessMemory, CreateRemoteThread |
| **T1059**    | Command and Scripting Interpreter | Execution       | CreateProcessA/W, ShellExecuteA/W                      |
| **T1547**    | Boot or Logon Autostart Execution | Persistence     | RegCreateKeyW, RegSetValueExW                          |
| **T1105**    | Ingress Tool Transfer             | C2              | InternetOpenW, URLDownloadToFileW                      |
| **T1497**    | Virtualization/Sandbox Evasion    | Defense Evasion | IsDebuggerPresent                                      |
| **T1112**    | Modify Registry                   | Defense Evasion | RegSetValueW, RegDeleteKeyW                            |
| **T1027**    | Obfuscated Files                  | Defense Evasion | CryptEncrypt, High Entropy                             |

---

## 🔄 How They Work Together

```
Analysis Result (from Static Analyzer)
    ↓
    ├─→ [risk_engine.py]
    │   └─→ Calculate initial risk score: 50 points
    │
    ├─→ [behavior_predictor.py]
    │   └─→ Predict behaviors: Process Injection, Persistence, C2 Comm
    │
    ├─→ [mitre_mapper.py]
    │   └─→ Map to MITRE: T1055, T1547, T1105
    │
    └─→ [risk_engine.py with behavior + MITRE]
        └─→ Final risk score: 95/100 [CRITICAL]
            + Explanations for each point
            + Recommended actions
            + MITRE technique mappings
```

---

## 💻 How to Use These Modules

### Simple Usage Example:

```python
from core.risk_engine import calculate_risk_score
from core.behavior_predictor import predict_behaviors
from core.mitre_mapper import map_all_findings_to_mitre

# Step 1: Get analysis from Static Analyzer
analysis = analyzer.analyze_file("suspicious.exe")

# Step 2: Predict behaviors
behaviors = predict_behaviors(analysis)

# Step 3: Map to MITRE
mitre_findings = map_all_findings_to_mitre(analysis, behaviors)

# Step 4: Calculate risk (with all intelligence)
risk_result = calculate_risk_score(analysis, behaviors, mitre_findings)

print(f"Risk Score: {risk_result['risk_score']}/100")
print(f"Risk Level: {risk_result['risk_level']}")
print(f"Verdict: {risk_result['verdict']}")

# Step 5: Get recommended actions
from core.risk_engine import get_recommended_actions
actions = get_recommended_actions(risk_result, risk_result['risk_level'])
for action in actions:
    print(action)
```

---

## 📊 Output Structure

### Risk Engine Output:

```json
{
  "risk_score": 95,
  "risk_level": "critical",
  "verdict": "Highly suspicious / likely malicious (95/100) - IMMEDIATE ACTION REQUIRED",
  "risk_reasons": [
    {
      "points": 30,
      "category": "api_combinations",
      "reason": "High-signal malware behavior combinations detected",
      "severity": "critical",
      "evidence": [
        ["VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread"]
      ],
      "explanation": "Specific API combinations strongly indicate malware behavior"
    }
  ],
  "score_breakdown": {
    "total_points_considered": 95,
    "total_indicators": 7,
    "high_severity_count": 5
  }
}
```

### Behavior Predictor Output:

```json
{
  "predicted_behaviors": [
    {
      "behavior": "process_injection",
      "description": "File likely performs process injection for code execution or evasion",
      "confidence": "high",
      "severity": "critical",
      "evidence": ["VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread"]
    }
  ],
  "behavior_summary": ["process_injection", "persistence", "data_exfiltration"],
  "total_behaviors_detected": 5
}
```

### MITRE Mapper Output:

```json
{
  "mitre_techniques": [
    {
      "technique_id": "T1055",
      "name": "Process Injection",
      "tactic": "Defense Evasion / Execution",
      "severity": "high",
      "description": "Adversaries inject code into legitimate processes...",
      "evidence": ["process_injection"]
    }
  ],
  "total_techniques_mapped": 7,
  "tactics_involved": [
    "Execution",
    "Persistence",
    "Defense Evasion",
    "Command and Control"
  ]
}
```

---

## 🚀 What You've Built

### Module 1: risk_engine.py

- ✅ 10-factor risk scoring system
- ✅ Intelligent point calculation
- ✅ Professional verdict generation
- ✅ Detailed explanations for every point
- ✅ Risk level classification
- ✅ Recommended actions based on severity
- ✅ Score comparison utilities

### Module 2: behavior_predictor.py

- ✅ 10 behavior patterns recognized
- ✅ API combination detection
- ✅ Confidence scoring
- ✅ Severity classification
- ✅ String-based behavior detection
- ✅ Entropy-based packing detection
- ✅ Human-readable impact descriptions

### Module 3: mitre_mapper.py

- ✅ 16+ MITRE techniques mapped
- ✅ Multi-source mapping (APIs, behaviors, strings)
- ✅ Evidence collection
- ✅ Severity assignment
- ✅ Tactic grouping
- ✅ Real-world attack framework integration

---

## 💡 Key Features

1. **Explainability**: Every point has a reason
2. **Actionability**: Recommends what to do
3. **Professional**: MITRE framework for analyst credibility
4. **Automated**: No manual analysis needed
5. **Modular**: Each module works independently
6. **Scalable**: Easy to add new behaviors/techniques

---

## 🔌 Integration Points

Your modules integrate with:

- **Input**: Static Analyzer's output (JSON)
- **Output**: Goes to Detection Engineering and web dashboard

The JSON format is standardized so all modules can work together seamlessly.

---

## 📝 Next Steps

After you complete these modules:

- Detection Engineering uses your intelligence output for YARA generation
- Web dashboard displays your findings in professional reports

Your work is the **foundation** of the entire intelligence pipeline! 🧠
