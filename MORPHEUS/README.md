# MORPHEUS-X: Intelligent Malware Analysis Framework

[![Status](https://img.shields.io/badge/status-Production%20Ready-green)]()
[![Tests](https://img.shields.io/badge/tests-All%20Passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-Comprehensive-blue)]()

A comprehensive, three-stage automated malware analysis system that combines **static analysis**, **behavioral intelligence**, and **detection engineering** into a unified threat analysis pipeline.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start-30-seconds)
2. [GUI Dashboard](#-gui-dashboard-new)
3. [System Architecture](#system-architecture)
4. [Module Overview](#module-overview)
5. [Installation](#installation)
6. [Usage Examples](#usage-examples)
7. [API Reference](#api-reference)
8. [Feature Comparison](#feature-comparison)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start (30 seconds)

### Analyze a File

```python
from core.analyzer import analyze_file
from core.risk_engine import calculate_risk_score

# Step 1: Analyze the file (Static Analysis)
analysis = analyze_file("suspicious.exe")

# Step 2: Calculate risk score (Behavior Intelligence)
risk_result = calculate_risk_score(analysis)

print(f"Risk: {risk_result['risk_score']}/100")
print(f"Level: {risk_result['risk_level']}")
print(f"Verdict: {risk_result['verdict']}")
```

### Generate YARA Rule

```python
from core.yara_generator import generate_yara_rule, export_rule_to_file

# Generate detection rule
rule = generate_yara_rule(analysis, rule_name="my_malware")

# Export to file
export_rule_to_file(rule, "rules/my_malware.yar")
```

### Check Malware Similarity

```python
from core.similarity_engine import calculate_similarity

# Compare two samples
report = calculate_similarity(sample1_analysis, sample2_analysis)

print(f"Similarity: {report['overall_similarity_score']:.0%}")
```

---

## � GUI Dashboard (NEW!)

MORPHEUS-X now includes a modern **Streamlit-based web dashboard** with intuitive visualizations and comprehensive reporting.

### 🚀 Quick Launch

```bash
# Windows
run_gui.bat

# PowerShell
.\run_gui.ps1

# Manual
streamlit run app.py
```

The dashboard opens at: **http://localhost:8501**

### 📊 Dashboard Features

**Analysis Page**

- 📤 Upload PE files for analysis
- 📊 Real-time risk assessment gauge
- 🎯 Detected behaviors with confidence levels
- 🗺️ MITRE ATT&CK technique mapping
- 🔍 Suspicious APIs and strings
- 📈 PE section entropy analysis

**Dashboard Page**

- 📊 Risk distribution charts
- 📈 Risk score trends
- 📋 Complete analysis history
- 📊 Comparison statistics

**Similarity Page**

- 🔍 Compare two malware samples
- 📊 Multi-dimensional similarity scoring
- 🎯 Common characteristics detection
- 👪 Malware family identification

**Reports Page**

- 📄 PDF report generation
- 📋 Multiple report formats (Summary, Detailed, Executive)
- 📊 Professional formatting
- 💾 Download capabilities

### 📚 Documentation

- **Quick Start**: [GUI_QUICK_START.md](GUI_QUICK_START.md)
- **Full Guide**: [GUI_README.md](GUI_README.md)
- **Setup**: `python gui_setup.py`

### 🖼️ Dashboard Preview

```
┌─────────────────────────────────────────────────────┐
│ 🔍 MORPHEUS-X Malware Analysis Dashboard           │
├─────────────────────────────────────────────────────┤
│ 📊 Navigation: 🏠 | 📤 | 📊 | 🔍 | 📄 | ℹ️         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Risk Score: ████████░░  85/100 🔴 CRITICAL       │
│                                                     │
│  📋 Key Metrics:                                   │
│  • File Size: 512 KB                              │
│  • Behaviors: 8 detected                          │
│  • MITRE Techniques: 12 mapped                    │
│  • Risk Factors: 7 identified                     │
│                                                     │
│  📊 Charts: [Risk Distribution] [Trends] [APIs]   │
│                                                     │
│  📄 Reports: [Generate] [Download]                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## �🏗️ System Architecture

MORPHEUS-X uses a three-stage analysis pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: STATIC ANALYZER                                       │
│  ─────────────────────────────────────────────────────────────  │
│  Analyzes PE file structure, imports, strings, entropy           │
│  └─→ Output: Structured analysis with indicators                │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: BEHAVIOR INTELLIGENCE ENGINE                          │
│  ─────────────────────────────────────────────────────────────  │
│  ├─ Risk Scoring (10-factor scoring system → 0-100)             │
│  ├─ Behavior Prediction (10 malware behaviors detected)         │
│  └─ MITRE Mapping (16+ ATT&CK techniques mapped)                │
│  └─→ Output: Risk score, behaviors, MITRE techniques           │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3: DETECTION ENGINEERING                                 │
│  ─────────────────────────────────────────────────────────────  │
│  ├─ YARA Rule Generation (multi-vector rules)                   │
│  └─ Similarity Analysis (find variants & families)              │
│  └─→ Output: Detection rules + similarity reports               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Module Overview

### Stage 1: Static Analyzer

**Files**: `core/analyzer.py`, `core/string_extractor.py`, `core/suspicious_api_detector.py`, `core/entropy.py`

Analyzes PE file structure, imports, strings, and entropy. Produces structured JSON with all technical indicators.

**Example Output**:

```json
{
  "file_name": "sample.exe",
  "md5": "5d41402abc4b2a76b9719d911017c592",
  "imports": [
    {
      "dll": "kernel32.dll",
      "functions": ["VirtualAllocEx", "WriteProcessMemory"]
    },
    { "dll": "advapi32.dll", "functions": ["RegCreateKeyW"] }
  ],
  "suspicious_strings": ["powershell.exe", "cmd.exe"],
  "sections": [
    { "name": ".text", "entropy": 7.2 },
    { "name": ".data", "entropy": 3.5 }
  ]
}
```

### Stage 2: Behavior Intelligence Engine

**Files**: `core/risk_engine.py`, `core/behavior_predictor.py`, `core/mitre_mapper.py`  
**Documentation**: `docs/behavior/`

Analyzes raw indicators and produces professional threat intelligence:

- **Risk Scoring**: 10-factor system producing 0-100 risk score
- **Behavior Prediction**: Detects 10 types of malware behaviors
- **MITRE Mapping**: Maps findings to 16+ ATT&CK techniques

**Example Output**:

```json
{
  "risk_score": 95,
  "risk_level": "critical",
  "predicted_behaviors": [
    "process_injection",
    "persistence",
    "data_exfiltration"
  ],
  "mitre_techniques": [
    { "id": "T1055", "name": "Process Injection", "severity": "high" }
  ]
}
```

### Stage 3: Detection Engineering

**Files**: `core/yara_generator.py`, `core/similarity_engine.py`  
**Documentation**: `docs/detection/`

Generates detection rules and analyzes malware relationships:

- **YARA Generation**: Multi-vector detection rules (5 independent metrics)
- **Similarity Analysis**: 5-metric composite scoring for variant detection
- **Batch Operations**: Clustering and batch similarity search

---

## 💾 Installation

### Prerequisites

- Python 3.7+
- Windows (for PE file analysis)

### Quick Setup (Automated)

**Option 1: PowerShell (Recommended)**

```bash
cd d:\Project\MORPHEUS
.\setup.ps1
```

**Option 2: Command Prompt**

```bash
cd d:\Project\MORPHEUS
setup.bat
```

### Manual Setup

If the automated scripts don't work:

```bash
cd d:\Project\MORPHEUS

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

**Important: Run from the project root directory (d:\Project\MORPHEUS), NOT from the tests folder!**

```bash
# Tests should be run from: d:\Project\MORPHEUS
python tests/test_static.py
python tests/test_behavior.py
python tests/test_detection.py
```

Expected output: All tests should pass with ✅

---

## 📚 Usage Examples

### Complete Analysis Pipeline

```python
from core.analyzer import analyze_file
from core.behavior_predictor import predict_behaviors
from core.mitre_mapper import map_all_findings_to_mitre
from core.risk_engine import calculate_risk_score, get_recommended_actions
from core.yara_generator import generate_combined_rule, export_rule_to_file

# Stage 1: Static Analysis
analysis = analyze_file("suspicious.exe")

# Stage 2: Behavior Intelligence
behaviors = predict_behaviors(analysis)
mitre_findings = map_all_findings_to_mitre(analysis, behaviors)
risk_result = calculate_risk_score(analysis, behaviors, mitre_findings)

# Stage 3: Detection Engineering
rule = generate_combined_rule(analysis, behaviors)
export_rule_to_file(rule, "rules/detection.yar")

print(f"Risk: {risk_result['risk_score']}/100 [{risk_result['risk_level']}]")
```

### Find Similar Malware

```python
from core.similarity_engine import find_similar_samples, cluster_samples

# Find variants
similar = find_similar_samples(target_analysis, all_samples, threshold=0.65)

# Group into families
families = cluster_samples(all_samples, threshold=0.65)
```

---

## 📖 API Reference

### Core Functions

```python
# Stage 1: Static Analysis
from core.analyzer import analyze_file
analysis = analyze_file("file_path")

# Stage 2: Behavior Intelligence
from core.risk_engine import calculate_risk_score
from core.behavior_predictor import predict_behaviors
from core.mitre_mapper import map_all_findings_to_mitre

risk = calculate_risk_score(analysis)
behaviors = predict_behaviors(analysis)
mitre = map_all_findings_to_mitre(analysis, behaviors)

# Stage 3: Detection Engineering
from core.yara_generator import generate_yara_rule, export_rule_to_file
from core.similarity_engine import calculate_similarity, find_similar_samples

rule = generate_yara_rule(analysis)
export_rule_to_file(rule, "rules/rule.yar")
similarity = calculate_similarity(analysis1, analysis2)
```

---

## 📊 Feature Comparison

| Feature                 | Static | Behavior            | Detection     |
| ----------------------- | ------ | ------------------- | ------------- |
| **Risk Scoring**        | ❌     | ✅ (10-factor)      | ❌            |
| **Behavior Prediction** | ❌     | ✅ (10 behaviors)   | ❌            |
| **MITRE Mapping**       | ❌     | ✅ (16+ techniques) | ❌            |
| **YARA Generation**     | ❌     | ❌                  | ✅ (5-vector) |
| **Similarity Analysis** | ❌     | ❌                  | ✅ (5-metric) |
| **Production Ready**    | ✅     | ✅                  | ✅            |

---

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'core'"

**Problem**: You're running the test from the wrong directory

```bash
cd d:\Project\MORPHEUS\tests
python test_static.py            # ❌ ERROR!
```

**Solution**: Always run from the **project root**

```bash
cd d:\Project\MORPHEUS
python tests/test_static.py      # ✅ CORRECT
```

**Why**: The test files import `from core.analyzer import analyze_file`, which expects `core/` to be at the parent directory level. Running from the tests folder breaks this path.

### "can't open file 'D:\\Project\\MORPHEUS\\tests\\tests\\test_static.py'"

**Problem**: You typed the path twice

```bash
python tests/tests/test_static.py  # ❌ Double path
```

**Solution**: Use the correct path once

```bash
python tests/test_static.py        # ✅ CORRECT
```

### "Python command not found"

**Problem**: Python isn't installed or not in PATH

**Solution**:

1. Check Python installation:

```bash
python --version
```

2. If not found, install Python 3.7+ from python.org
3. Restart PowerShell after installation

### "pefile module not found"

**Problem**: Dependencies not installed

**Solution**: Install from project root with virtual environment active

```bash
cd d:\Project\MORPHEUS
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### "Can't find data/uploads folder"

**Problem**: The folder doesn't exist yet

**Solution**: Create it manually

```bash
mkdir data
mkdir data\uploads
```

### "Virtual environment not activating"

**Problem**: Wrong activation command or directory

**Solution**: Run from project root

```bash
cd d:\Project\MORPHEUS
.\.venv\Scripts\activate          # For PowerShell
# or
.venv\Scripts\activate.bat        # For Command Prompt
```

---

## 📖 Getting Started Guide

See [HOW_TO_RUN.txt](HOW_TO_RUN.txt) for:

- ✅ Step-by-step setup instructions
- ✅ How to run the project correctly
- ✅ Common mistakes and fixes
- ✅ Complete example session
- ✅ Troubleshooting reference

### "YARA rule syntax invalid"

**Solution**: Use `generate_combined_rule()` for automatic validation

### "File not found: data/uploads/"

**Solution**: Create directories: `mkdir data\uploads`

---

## 📁 Project Structure

```
MORPHEUS-X/
├── core/                  # Analysis modules
│   ├── analyzer.py       # Stage 1: Static Analysis
│   ├── risk_engine.py    # Stage 2: Risk Scoring
│   ├── behavior_predictor.py
│   ├── mitre_mapper.py
│   ├── yara_generator.py # Stage 3: YARA Generation
│   └── similarity_engine.py
├── docs/                 # Documentation
│   ├── behavior/         # Behavior Intelligence docs
│   └── detection/        # Detection Engineering docs
├── tests/                # Test suites
│   ├── test_static.py
│   ├── test_behavior.py
│   └── test_detection.py
├── rules/                # Generated YARA rules
└── data/
    └── uploads/          # Sample files
```

---

## 📖 Documentation

- [Behavior Intelligence Guide](docs/behavior/GUIDE.md)
- [Behavior Intelligence Quick Reference](docs/behavior/QUICK_REFERENCE.md)
- [Detection Engineering Guide](docs/detection/GUIDE.md)
- [Detection Engineering Quick Reference](docs/detection/QUICK_REFERENCE.md)

---

## 🧪 Testing

**⚠️ Important: Always run tests from the project root directory!**

```bash
# Navigate to project root
cd d:\Project\MORPHEUS

# Activate virtual environment
.\.venv\Scripts\activate

# Run tests
python tests/test_static.py      # Stage 1: Static Analysis
python tests/test_behavior.py    # Stage 2: Behavior Intelligence
python tests/test_detection.py   # Stage 3: Detection Engineering

# Run full verification
python setup_and_verify.py       # Complete system check
```

**❌ Don't do this:**

```bash
cd d:\Project\MORPHEUS\tests
python test_static.py            # ❌ ERROR: Can't find 'core' module
```

**✅ Do this instead:**

```bash
cd d:\Project\MORPHEUS
python tests/test_static.py      # ✅ Works correctly
```

See [HOW_TO_RUN.txt](HOW_TO_RUN.txt) for detailed setup and troubleshooting guide.

---

## 📈 Statistics

| Component             | Lines      | Functions | Status       |
| --------------------- | ---------- | --------- | ------------ |
| Static Analyzer       | 300+       | 12+       | ✅           |
| Behavior Intelligence | 1,150+     | 26+       | ✅           |
| Detection Engineering | 1,200+     | 26+       | ✅           |
| **Total**             | **2,650+** | **64+**   | **✅ READY** |

---

## ✅ Status

**MORPHEUS-X is Production Ready** ✅

- ✅ All 3 stages implemented
- ✅ 64+ production functions
- ✅ Comprehensive test coverage
- ✅ Full documentation
- ✅ Ready for deployment

**Version**: 1.0.0 - Production Ready  
**Last Updated**: May 1, 2026
