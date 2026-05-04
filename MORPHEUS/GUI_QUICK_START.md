# MORPHEUS-X GUI - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
cd d:\Project\MORPHEUS
pip install -r requirements.txt
```

### Step 2: Launch the Dashboard

**Option A: Using Batch File (Windows)**

```bash
run_gui.bat
```

**Option B: Using PowerShell (Windows)**

```powershell
.\run_gui.ps1
```

**Option C: Direct Command**

```bash
streamlit run app.py
```

### Step 3: Open in Browser

The dashboard automatically opens at: `http://localhost:8501`

If not, manually navigate to that URL in your browser.

---

## 📊 Using the Dashboard

### Home Page

- Overview of MORPHEUS-X system
- Statistics on analyses performed
- Framework information

### Analysis Page

1. Click **"📤 Analysis"** in sidebar
2. Click **"Upload a PE executable file"**
3. Select a suspicious Windows executable (.exe, .dll, .sys)
4. Wait for analysis to complete (~5-30 seconds)
5. View results:
   - **Risk Score**: Gauge showing threat level
   - **File Details**: Hashes, metadata
   - **Behaviors**: Detected malware behaviors
   - **MITRE Techniques**: ATT&CK framework mapping
   - **APIs**: Suspicious imports
   - **Strings**: Suspicious strings in binary

### Dashboard Page

- View all previous analyses
- Charts showing risk distribution
- Risk trends over time
- Full analysis history

### Similarity Page

1. Analyze at least 2 files
2. Click **"🔍 Similarity"**
3. Select file to compare
4. Click **"🔍 Compare Files"**
5. View similarity report and characteristics

### Reports Page

1. After analyzing a file
2. Click **"📄 Reports"**
3. Select report format:
   - **Summary Report**: Quick 2-3 page overview
   - **Detailed Report**: Complete 5-8 page analysis
   - **Executive Summary**: 1-page business summary
4. Click **"📥 Generate & Download Report"**
5. Report preview shows with data

---

## 🎯 Common Tasks

### Task 1: Quick File Analysis

```
1. Open app → go to "Analysis"
2. Upload file
3. Check Risk Score
4. Check Behaviors section
5. Review verdict
```

### Task 2: Compare Two Malware Samples

```
1. Upload first file → analyze
2. Upload second file → analyze
3. Go to "Similarity"
4. Select second file
5. Click "Compare Files"
6. Review similarity percentage
```

### Task 3: Generate PDF Report

```
1. Analyze a file
2. Go to "Reports"
3. Select "Detailed Report"
4. Click "Generate & Download"
5. View report preview
6. Download PDF
```

### Task 4: View Analysis History

```
1. Go to "Dashboard"
2. See all previous analyses
3. View risk distribution chart
4. View risk trends
5. Click on entries to view details
```

---

## 📈 Understanding Results

### Risk Score (0-100)

| Score  | Level    | Color     | Meaning          |
| ------ | -------- | --------- | ---------------- |
| 0-34   | Low      | 🟢 Green  | Minimal threat   |
| 35-59  | Medium   | 🟡 Yellow | Potential issues |
| 60-79  | High     | 🟠 Orange | Likely malicious |
| 80-100 | Critical | 🔴 Red    | Highly malicious |

### Confidence Scores

- **90-100%**: Very confident
- **70-89%**: Confident
- **50-69%**: Moderate confidence
- **Below 50%**: Low confidence

### Behaviors

Common malware behaviors detected:

- **Dropper**: Drops additional malware
- **Downloader**: Downloads files
- **Injector**: Injects code
- **Keylogger**: Captures keystrokes
- **Ransomware**: Encrypts files
- **Rootkit**: Hides presence
- **Trojan**: Backdoor access
- **Worm**: Self-replicating

---

## ⚙️ Troubleshooting

### Dashboard Won't Start

**Error**: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**:

```bash
pip install streamlit
```

### File Upload Fails

**Issue**: Can't upload files

**Solutions**:

1. Check file is valid PE (.exe, .dll, .sys)
2. File size under 200 MB?
3. Check file isn't corrupted
4. Try refreshing browser

### No Results After Upload

**Issue**: Analysis page shows no results

**Solutions**:

1. Wait longer - analysis in progress
2. Check browser console for errors (F12)
3. Try different file
4. Restart Streamlit: `Ctrl+C` then `streamlit run app.py`

### Charts Not Displaying

**Issue**: Visualizations not showing

**Solutions**:

1. Refresh page (F5)
2. Check if JavaScript enabled
3. Try different browser
4. Install plotly: `pip install plotly --upgrade`

### Slow Performance

**Issue**: Analysis or UI is slow

**Solutions**:

1. Close other applications
2. Analyze smaller files first
3. Clear browser cache
4. Restart Streamlit

---

## 🔒 Security Notes

### ⚠️ IMPORTANT

- **Never** run on exposed network
- **Always** analyze in isolated VMs
- **Don't** execute uploaded files
- **Use** only for static analysis

### Best Practices

1. Keep malware samples secure
2. Limit dashboard access
3. Use strong passwords if deployed
4. Monitor analysis logs
5. Regular backups of findings

---

## 📁 Directory Structure

```
MORPHEUS/
├── app.py                    ← Main dashboard
├── gui_utils.py              ← Charts and visualization
├── report_generator.py       ← PDF reports
├── gui_setup.py              ← Setup and cleanup
├── run_gui.bat               ← Windows launcher
├── run_gui.ps1               ← PowerShell launcher
├── .streamlit/
│   └── config.toml          ← Streamlit config
├── core/                     ← Analysis modules
├── data/uploads              ← Uploaded files
├── data/reports              ← Generated reports
└── docs/                     ← Documentation
```

---

## 🆘 Getting Help

### Check Documentation

- Read `GUI_README.md` for detailed guide
- Check `PERSON_*_GUIDE.md` for component guides
- Review `QUICK_REFERENCE.md` files

### Enable Debug Mode

```bash
streamlit run app.py --logger.level=debug
```

### Check Logs

```bash
tail -f .streamlit/logs/
```

---

## 🧹 Cleaning Up

To remove test data before analyzing real malware:

```bash
python gui_setup.py
# Select option 1: Clean up test data
```

This removes:

- Test files
- Demo rules
- Sample outputs
- Temporary files

---

## 💾 Saving Analysis Results

### Automatic Storage

- All analyses saved in session
- History visible in Dashboard page

### Export Analysis

- Generate PDF report (Reports page)
- Download report with all findings

### Backup Analysis

```python
import json
# Analysis data automatically saved in session state
```

---

## 🚀 Advanced Features

### Custom Upload Location

Edit in `app.py`:

```python
temp_file_path = "your_custom_path/file.exe"
```

### Custom Report Template

Edit `report_generator.py`:

```python
# Modify report sections and styling
```

### Add Custom Visualizations

Edit `gui_utils.py`:

```python
# Add new chart methods to VisualizationEngine class
```

---

## 📝 Next Steps

After analyzing files:

1. **Review Reports** - Download PDF reports
2. **Create Rules** - Generate YARA detection rules
3. **Compare Samples** - Find malware families
4. **Export Data** - Share findings
5. **Iterate** - Analyze more samples

---

## ✅ Checklist

Before analyzing real malware:

- [ ] Installed all dependencies
- [ ] Dashboard starts without errors
- [ ] Cleaned up test data
- [ ] Have isolated analysis environment
- [ ] Backed up any important data
- [ ] Read security notes
- [ ] Ready to upload first sample

---

## 📞 Support Resources

- **Documentation**: See `/docs` folder
- **Guides**: See `PERSON_*_GUIDE.md` files
- **References**: See `*_QUICK_REFERENCE.md` files
- **Streamlit Docs**: https://docs.streamlit.io

---

**Status**: ✅ Ready to Analyze  
**Version**: 1.0.0  
**Last Updated**: May 2026
