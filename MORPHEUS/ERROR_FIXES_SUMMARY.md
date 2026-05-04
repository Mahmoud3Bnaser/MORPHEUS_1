# ✅ ERROR FIXES & SOLUTION GUIDE

## 🐛 Errors You Encountered

### Error 1: "run_gui.bat is not recognized"

```
run_gui.bat : The term 'run_gui.bat' is not recognized as the name of a cmdlet...
```

**Cause:** In PowerShell, you need to use `.\` prefix to run batch files

**Solution:** Use one of these:

```powershell
.\run_gui.bat          # Correct way in PowerShell
# OR
cmd /c run_gui.bat     # Alternative
# OR use PowerShell script instead:
.\run_gui.ps1
```

---

### Error 2: "Unexpected token '}' in PowerShell script"

```
At D:\Project\MORPHEUS\run_gui.ps1:24 char:5
+     } else {
+     ~
Unexpected token '}' in expression or statement.
```

**Cause:** PowerShell syntax error with inline `if` statement formatting

**Solution:** ✅ **FIXED** - Updated `run_gui.ps1` with correct syntax

---

### Error 3: Confusing Command Entry

```
run_gui.bat          # Windows
>> .\run_gui.ps1     # PowerShell
>> streamlit run app.py
```

**Cause:** You were mixing commands and PowerShell was treating them as multi-line input

**Solution:** Run ONE command at a time, see below ⬇️

---

## ✅ What Was Fixed

### ✅ Fixed: `run_gui.ps1`

- Fixed: Changed `& $venv_path` to `. $venv_path` (correct dot-sourcing)
- Fixed: Changed `& python -m pip` to `python -m pip` (removed unnecessary call operator)
- Fixed: Added `$ErrorActionPreference = "Continue"` for better error handling
- Fixed: Improved error messaging and formatting

---

## 🎯 **CORRECT COMMANDS TO RUN YOUR PROJECT**

### **The Easiest Way (Recommended)** ✨

#### **Windows Command Prompt (CMD)**

```cmd
cd d:\Project\MORPHEUS
streamlit run app.py
```

#### **Windows PowerShell**

```powershell
cd d:\Project\MORPHEUS
streamlit run app.py
```

**Result:** Dashboard opens at `http://localhost:8501`

---

### **Alternative Method 1: Use Batch File**

#### **Windows Command Prompt**

```cmd
cd d:\Project\MORPHEUS
run_gui.bat
```

---

### **Alternative Method 2: Use PowerShell Script**

#### **Windows PowerShell**

```powershell
cd d:\Project\MORPHEUS
.\run_gui.ps1
```

---

## 🚀 **STEP-BY-STEP FIRST TIME SETUP**

### Step 1: Open Terminal/PowerShell

```powershell
# Navigate to project
cd d:\Project\MORPHEUS
```

### Step 2: Activate Virtual Environment

```powershell
# Activate venv (only if not already activated)
.\.venv\Scripts\Activate.ps1

# You should see (.venv) at the start of your prompt:
# (.venv) PS D:\Project\MORPHEUS>
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Run the Dashboard

```powershell
streamlit run app.py
```

### Step 5: Browser Opens

✅ Dashboard automatically opens at: `http://localhost:8501`

---

## 📋 **WHAT EACH COMMAND DOES**

### Command 1: `streamlit run app.py`

```
✅ Fastest way to start
✅ Launches dashboard immediately
✅ Best for everyday use
⏱️ Takes 3-5 seconds to start
```

### Command 2: `run_gui.bat`

```
✅ Handles setup automatically
✅ Checks virtual environment
✅ Installs missing packages
⏱️ Takes 10-20 seconds first time, 3-5 seconds after
```

### Command 3: `.\run_gui.ps1`

```
✅ Same as batch file but for PowerShell
✅ Better error messages
⏱️ Takes 10-20 seconds first time, 3-5 seconds after
```

---

## 🎯 **QUICK REFERENCE TABLE**

| Goal                 | Command                           | Notes                         |
| -------------------- | --------------------------------- | ----------------------------- |
| Start immediately    | `streamlit run app.py`            | Fastest                       |
| Start with checks    | `run_gui.bat`                     | Recommended for first time    |
| Start (PowerShell)   | `.\run_gui.ps1`                   | Fixed version                 |
| Install dependencies | `pip install -r requirements.txt` | One-time setup                |
| Clean test data      | `python gui_setup.py`             | Before analyzing real malware |
| Check version        | `streamlit --version`             | Verify installation           |
| Stop server          | `Ctrl+C`                          | Stops the dashboard           |

---

## 💻 **COMPLETE FIRST-TIME WORKFLOW**

```powershell
# 1. Open PowerShell
# Navigate to project
cd d:\Project\MORPHEUS

# 2. If not yet activated, activate venv
.\.venv\Scripts\Activate.ps1

# 3. Install all packages
pip install -r requirements.txt

# 4. (Optional) Clean test data
python gui_setup.py
# Select: 1, then type: yes

# 5. Start the dashboard
streamlit run app.py

# 6. Browser opens at http://localhost:8501
# 7. Start analyzing! 🎉
```

---

## 🔑 **KEY POINTS**

### ✅ DO

- ✅ Use `streamlit run app.py` for quick start
- ✅ Use `.\run_gui.ps1` in PowerShell
- ✅ Use `run_gui.bat` in Command Prompt
- ✅ Keep virtual environment activated
- ✅ Check dashboard at `http://localhost:8501`

### ❌ DON'T

- ❌ Don't use `run_gui.bat` in PowerShell without `.\`
- ❌ Don't mix multiple commands on one line
- ❌ Don't forget to activate virtual environment
- ❌ Don't try to run multiple dashboards on same port

---

## 🌐 **ACCESS DASHBOARD**

Once running, open your browser:

```
http://localhost:8501
```

Or from another computer on same network:

```
http://192.168.1.45:8501
```

---

## 🛑 **STOPPING THE SERVER**

In the terminal where it's running:

```
Press: Ctrl+C
```

This will:

- Stop the Streamlit server
- Close the dashboard
- Return to command prompt

---

## ⚡ **QUICK START (JUST 3 STEPS)**

**Step 1:** Open PowerShell

```powershell
cd d:\Project\MORPHEUS
```

**Step 2:** Run the app

```powershell
streamlit run app.py
```

**Step 3:** Browser opens automatically at `http://localhost:8501` ✅

---

## 📝 **EXAMPLE SESSION**

```powershell
(.venv) PS D:\Project\MORPHEUS> streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.45:8501
  External URL: http://102.184.116.26:8501

  Uvicorn server started on 0.0.0.0:8501

# ✅ Now open browser and go to http://localhost:8501
# 🎉 Dashboard is ready to use!
```

---

## 🐛 **IF SOMETHING GOES WRONG**

### Dashboard won't start?

```powershell
# 1. Make sure venv is activated
.\.venv\Scripts\Activate.ps1

# 2. Check dependencies
pip install -r requirements.txt

# 3. Try again
streamlit run app.py
```

### Port 8501 already in use?

```powershell
# Use different port
streamlit run app.py --server.port 8502
```

### Module not found error?

```powershell
# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

---

## ✨ **NOW YOU'RE READY!**

Choose your method and run:

### **Fastest** ⚡

```powershell
streamlit run app.py
```

### **Easiest** 🖱️ (Windows)

```cmd
run_gui.bat
```

### **PowerShell** 💻

```powershell
.\run_gui.ps1
```

---

**All errors are now fixed! 🎉**

**Status**: ✅ Ready to Use  
**Last Updated**: May 2, 2026  
**Version**: 1.0.0
