# MORPHEUS-X - Complete Commands Guide

## 📋 Summary: All Commands to Run Your Project

---

## 🚀 **QUICK START (Recommended)**

### **Option 1: Windows Command Prompt (Easiest)**

```cmd
cd d:\Project\MORPHEUS
run_gui.bat
```

### **Option 2: PowerShell**

```powershell
cd d:\Project\MORPHEUS
.\run_gui.ps1
```

### **Option 3: Direct Command (All Platforms)**

```bash
cd d:\Project\MORPHEUS
streamlit run app.py
```

---

## 📖 DETAILED COMMAND REFERENCE

### **1️⃣ Initial Setup (First Time Only)**

#### Install Virtual Environment

```bash
cd d:\Project\MORPHEUS
python -m venv .venv
```

#### Activate Virtual Environment

**Windows CMD:**

```cmd
.venv\Scripts\activate.bat
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Verify Installation

```bash
python -c "import streamlit; print('Streamlit installed')"
streamlit --version
```

---

### **2️⃣ Running the GUI (Every Time)**

#### **METHOD A: Using Batch File (Windows CMD)**

```cmd
cd d:\Project\MORPHEUS
run_gui.bat
```

**What it does:**

- Activates virtual environment
- Checks dependencies
- Installs missing packages if needed
- Starts Streamlit dashboard
- Opens at `http://localhost:8501`

---

#### **METHOD B: Using PowerShell Script**

```powershell
cd d:\Project\MORPHEUS
.\run_gui.ps1
```

**What it does:**

- Same as batch file
- Better error messages in PowerShell
- More detailed output

---

#### **METHOD C: Direct Streamlit Command (Fastest)**

```bash
cd d:\Project\MORPHEUS
streamlit run app.py
```

**If venv not activated:**

```bash
cd d:\Project\MORPHEUS
.venv\Scripts\activate.bat
streamlit run app.py
```

---

### **3️⃣ GUI Setup & Cleanup**

#### Run Interactive Setup Menu

```bash
python gui_setup.py
```

**Options:**

```
1. Clean up test data (remove test files, demo rules)
2. Setup directories (create data folders)
3. Verify installation (check packages)
4. Create configuration (generate config file)
5. Run all setup steps (complete setup)
6. Exit
```

#### Option 1: Clean Up Test Data

```bash
python gui_setup.py
# Select: 1
# Type: yes
```

Removes:

- Test Python files
- Demo YARA rules
- Sample output files
- Temporary files

---

### **4️⃣ Testing & Verification**

#### Check Python Version

```bash
python --version
```

#### Check Streamlit

```bash
streamlit --version
```

#### List Installed Packages

```bash
pip list
```

#### Check Specific Package

```bash
pip show streamlit
pip show pefile
pip show plotly
```

#### Test Imports

```bash
python -c "from core.analyzer import analyze_file; print('Analyzer loaded')"
python -c "import streamlit; import plotly; print('All GUI packages loaded')"
```

---

### **5️⃣ File Analysis (CLI - If Needed)**

#### Analyze File via Python

```python
from core.analyzer import analyze_file
from core.risk_engine import calculate_risk_score

# Analyze a file
analysis = analyze_file("path/to/file.exe")
risk_result = calculate_risk_score(analysis)

print(f"Risk Score: {risk_result['risk_score']}/100")
print(f"Risk Level: {risk_result['risk_level']}")
print(f"Verdict: {risk_result['verdict']}")
```

---

### **6️⃣ Advanced Commands**

#### Run Streamlit with Debug Logging

```bash
streamlit run app.py --logger.level=debug
```

#### Run Streamlit on Custom Port

```bash
streamlit run app.py --server.port 8502
```

#### Run Streamlit with Custom Config

```bash
streamlit run app.py --config .streamlit/config.toml
```

#### Generate YARA Rules (CLI)

```python
from core.yara_generator import generate_yara_rule, export_rule_to_file

# Generate rule
analysis = analyze_file("file.exe")
rule = generate_yara_rule(analysis, rule_name="my_malware")
export_rule_to_file(rule, "rules/my_malware.yar")
```

---

## 🔄 **TYPICAL WORKFLOW**

### First Time Setup

```cmd
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
.venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Clean up test data
python gui_setup.py
# Select: 1, then yes
```

### Every Time You Run

```cmd
# Method 1: Fastest
cd d:\Project\MORPHEUS
streamlit run app.py

# OR Method 2: Auto-setup
run_gui.bat

# OR Method 3: PowerShell
.\run_gui.ps1
```

### Stop the Server

```
Press: Ctrl+C
```

---

## ✅ **TROUBLESHOOTING COMMANDS**

### Reactivate Virtual Environment

```cmd
.venv\Scripts\activate.bat
```

### Reinstall Dependencies

```bash
pip install -r requirements.txt --force-reinstall
```

### Clear Streamlit Cache

```bash
streamlit cache clear
```

### Check Port 8501 Usage (Windows)

```cmd
netstat -ano | findstr :8501
```

### Kill Process on Port 8501 (Windows)

```cmd
taskkill /PID <PID> /F
```

### Check Port 8501 Usage (Linux/macOS)

```bash
lsof -i :8501
```

---

## 📁 **PROJECT STRUCTURE**

```
d:\Project\MORPHEUS\
├── app.py                          ← Main Streamlit app
├── gui_utils.py                    ← Visualization utilities
├── report_generator.py             ← PDF report generation
├── gui_setup.py                    ← Setup/cleanup utility
├── run_gui.bat                     ← Windows launcher
├── run_gui.ps1                     ← PowerShell launcher
├── .streamlit/config.toml          ← Streamlit configuration
├── .venv/                          ← Virtual environment
├── core/                           ← Analysis modules
│   ├── analyzer.py
│   ├── risk_engine.py
│   ├── behavior_predictor.py
│   ├── mitre_mapper.py
│   ├── yara_generator.py
│   └── similarity_engine.py
├── data/
│   ├── uploads/                    ← Upload folder
│   ├── reports/                    ← Generated reports
│   └── analysis_results/
├── docs/                           ← Documentation
├── rules/                          ← YARA rules
├── tests/                          ← Test files
├── requirements.txt                ← Python dependencies
└── README.md                       ← Project readme
```

---

## 🎯 **BROWSER ACCESS**

After running the GUI, open one of these URLs:

```
http://localhost:8501
```

Or if accessing from another computer:

```
http://192.168.1.45:8501          (Your LAN IP)
http://102.184.116.26:8501        (External IP - if available)
```

---

## 🆘 **ERROR SOLUTIONS**

### Error: "streamlit command not found"

```bash
# Activate venv first
.venv\Scripts\activate.bat
# Then run
streamlit run app.py
```

### Error: "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

### Error: "Port 8501 already in use"

```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Error: "Virtual environment not found"

```bash
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Error: "Permission denied on run_gui.ps1"

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\run_gui.ps1
```

---

## 📊 **PERFORMANCE TIPS**

### Speed up startup:

```bash
# Clear Streamlit cache
streamlit cache clear

# Use direct command (faster)
streamlit run app.py
```

### Reduce file size for analysis:

- Use smaller PE files initially
- Test with < 5 MB files first
- Larger files take longer to analyze

### Monitor performance:

```bash
streamlit run app.py --client.showErrorDetails=true
```

---

## 🔒 **SECURITY NOTES**

### Don't expose to internet:

```bash
# Dashboard is NOT password protected by default
# Only use on local network or isolated machine
```

### Run in isolated environment:

- Use VM or sandbox for malware
- Never run real malware on host machine
- Keep analysis results secure

---

## 📝 **SAMPLE WORKFLOW**

### Step 1: Launch Dashboard

```cmd
cd d:\Project\MORPHEUS
streamlit run app.py
```

### Step 2: Browser Opens

```
http://localhost:8501 opens automatically
```

### Step 3: Upload File

- Click "📤 Analysis" page
- Upload a PE file

### Step 4: View Results

- See risk score
- View charts and tables
- Check behaviors

### Step 5: Generate Report

- Go to "📄 Reports"
- Select report format
- Download PDF

### Step 6: Stop Server

```
Press Ctrl+C in terminal
```

---

## 💾 **SAVING YOUR WORK**

### Backup Analysis History

```bash
# Analyses are saved in session automatically
# Exported as PDF from Reports page
```

### Save Reports

```bash
# Reports page generates PDF files
# Save to your desired location
```

---

## 🔄 **COMMON COMMAND SEQUENCES**

### First Time (Complete Setup)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python gui_setup.py
streamlit run app.py
```

### Regular Use (One Command)

```cmd
streamlit run app.py
```

### With Auto-Launcher

```cmd
run_gui.bat
```

### With PowerShell

```powershell
.\run_gui.ps1
```

---

## ✨ **CHEAT SHEET**

| Task              | Command                                   |
| ----------------- | ----------------------------------------- |
| Setup venv        | `python -m venv .venv`                    |
| Activate (CMD)    | `.venv\Scripts\activate.bat`              |
| Activate (PS)     | `.\venv\Scripts\Activate.ps1`             |
| Install deps      | `pip install -r requirements.txt`         |
| Run GUI (fast)    | `streamlit run app.py`                    |
| Run GUI (auto)    | `run_gui.bat` or `.\run_gui.ps1`          |
| Cleanup test data | `python gui_setup.py` then select 1       |
| Check status      | `streamlit --version`                     |
| Stop server       | `Ctrl+C`                                  |
| Clear cache       | `streamlit cache clear`                   |
| Custom port       | `streamlit run app.py --server.port 8502` |

---

## 🎉 **YOU'RE READY!**

Choose one method and run:

### **Fastest Way** ⚡

```bash
streamlit run app.py
```

### **Easiest Way** 🖱️

```cmd
run_gui.bat
```

### **PowerShell Way** 💻

```powershell
.\run_gui.ps1
```

---

**Version**: 1.0.0  
**Last Updated**: May 2, 2026  
**Status**: ✅ Ready to Run
