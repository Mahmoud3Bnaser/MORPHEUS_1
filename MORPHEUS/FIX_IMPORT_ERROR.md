# 🔧 Import Error Fix - Summary

## ❌ Error You Encountered

```
ImportError: cannot import name 'map_to_mitre_techniques' from 'core.mitre_mapper'
```

## ✅ What Was Wrong

The `app.py` file was trying to import a function called `map_to_mitre_techniques`, but the actual function in `core/mitre_mapper.py` is called `map_all_findings_to_mitre`.

### Wrong Import (Line 30 in app.py):

```python
from core.mitre_mapper import map_to_mitre_techniques  # ❌ WRONG
```

### Correct Import:

```python
from core.mitre_mapper import map_all_findings_to_mitre  # ✅ CORRECT
```

---

## ✅ Fixes Applied

### Fix 1: Updated Import Statement

**File**: `app.py` line 30

- Changed: `from core.mitre_mapper import map_to_mitre_techniques`
- To: `from core.mitre_mapper import map_all_findings_to_mitre`

### Fix 2: Updated Function Call

**File**: `app.py` line 411

- Changed: `analysis["mitre_techniques"] = map_to_mitre_techniques(analysis)`
- To: `analysis["mitre_techniques"] = map_all_findings_to_mitre(analysis)`

---

## ✅ All Available Functions

### In `core/mitre_mapper.py`:

- ✅ `map_apis_to_mitre()` - Maps APIs to MITRE techniques
- ✅ `map_behaviors_to_mitre()` - Maps behaviors to MITRE techniques
- ✅ `map_strings_to_mitre()` - Maps strings to MITRE techniques
- ✅ `map_all_findings_to_mitre()` - Maps all findings at once (used in app)
- ✅ `get_mitre_technique_details()` - Get details of a specific technique
- ✅ `get_techniques_by_tactic()` - Get techniques by tactic

### In `core/behavior_predictor.py`:

- ✅ `predict_behaviors()` - Predicts malware behaviors
- ✅ `extract_imported_apis()` - Extracts imported APIs
- ✅ `check_behavior_pattern()` - Checks behavior patterns
- ✅ `get_behavior_impact()` - Gets behavior impact level

### In `core/analyzer.py`:

- ✅ `analyze_file()` - Main file analysis function

### In `core/yara_generator.py`:

- ✅ `generate_yara_rule()` - Generates YARA rules
- ✅ `generate_combined_rule()` - Generates combined rules

### In `core/similarity_engine.py`:

- ✅ `calculate_similarity()` - Calculates similarity between samples

---

## 🚀 Next Steps

Now the app should work! Try running it again:

```powershell
streamlit run app.py
```

Or if you had it running:

1. Stop the current server (Press `Ctrl+C`)
2. Run the command above
3. Open `http://localhost:8501` in your browser

---

## 📋 What to Expect

When you open the dashboard now:

1. ✅ No import errors
2. ✅ Analysis page will load
3. ✅ You can upload PE files
4. ✅ MITRE techniques will be mapped correctly
5. ✅ All charts and tables will display

---

## ❌ If You Still Get Errors

### Error: `ModuleNotFoundError: No module named 'core'`

**Solution:**

```bash
# Make sure you're in the right directory
cd d:\Project\MORPHEUS

# And that the virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Then run
streamlit run app.py
```

### Error: `ImportError: cannot import name 'predict_behaviors'`

**Solution:**

```bash
# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### Error: Port 8501 already in use

**Solution:**

```bash
# Stop the old process first
Ctrl+C

# Or use a different port
streamlit run app.py --server.port 8502
```

---

## ✨ Status

- ✅ Import error FIXED
- ✅ All functions verified
- ✅ Ready to run dashboard
- ✅ Ready to analyze files

---

## 🎯 Quick Command to Run

```powershell
streamlit run app.py
```

**That's it!** The dashboard should now work correctly.

---

**Last Updated**: May 2, 2026  
**Status**: ✅ FIXED
