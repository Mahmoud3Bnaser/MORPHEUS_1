# MORPHEUS-X GUI Dashboard

## 🎯 Overview

The MORPHEUS-X GUI Dashboard is a modern, web-based interface built with Streamlit for comprehensive malware analysis. It provides an intuitive, visual approach to malware analysis with real-time dashboards, detailed reports, and powerful visualization tools.

---

## ✨ Features

### 📊 Dashboard Pages

#### 1. **🏠 Home Page**

- Welcome and system overview
- Quick statistics on total analyses
- Average risk scores
- Framework information
- System architecture diagram

#### 2. **📤 Analysis Page**

- **File Upload**: Upload PE executable files (.exe, .dll, .sys)
- **Real-time Analysis**: Comprehensive static and behavioral analysis
- **Risk Assessment**: Visual risk gauge (0-100 scale)
- **File Details**:
  - Basic file information
  - Hash values (MD5, SHA1, SHA256)
  - PE section analysis
  - Entropy calculations
- **Behavior Detection**: Predicted malware behaviors with confidence scores
- **MITRE Mapping**: ATT&CK techniques mapped with confidence levels
- **API Analysis**: Suspicious API imports detection
- **String Analysis**: Suspicious strings extracted from the file

#### 3. **📊 Dashboard Page**

- Historical analysis overview
- Risk level distribution (pie chart)
- Risk score trends over time
- Detailed analysis history table
- Statistics (total analyses, average risk, critical samples)

#### 4. **🔍 Similarity Page**

- Compare two malware samples
- Similarity scoring across multiple dimensions
- Common characteristics detection
- Malware family identification

#### 5. **📄 Reports Page**

- **Report Generation**: Create comprehensive PDF reports
- **Multiple Formats**:
  - Summary Report: Quick overview
  - Detailed Report: Complete technical analysis
  - Executive Summary: High-level findings
- **Report Sections**:
  - Title page
  - Executive summary
  - Technical analysis with file metadata
  - Risk factor breakdown
  - Detected indicators
  - MITRE ATT&CK techniques
  - Detailed findings

#### 6. **ℹ️ About Page**

- System information
- Architecture details
- Feature list
- Technology stack

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Windows, Linux, or macOS

### Installation

1. **Install Dependencies**

```bash
cd d:\Project\MORPHEUS
pip install -r requirements.txt
```

The following packages will be installed:

- `streamlit` - Web framework
- `plotly` - Interactive visualizations
- `pandas` - Data manipulation
- `reportlab` - PDF generation
- `pefile` - PE file analysis
- `yara-python` - YARA rule support
- `pillow` - Image processing

2. **Verify Installation**

```bash
streamlit --version
python -c "import streamlit; print('Streamlit installed successfully')"
```

### Launching the Dashboard

```bash
cd d:\Project\MORPHEUS
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 📋 Usage Guide

### Basic Workflow

1. **Start the Application**

   ```bash
   streamlit run app.py
   ```

2. **Navigate to Analysis Page**
   - Click "📤 Analysis" in the sidebar

3. **Upload a PE File**
   - Click "Upload a PE executable file"
   - Select a suspicious file (.exe, .dll, .sys)

4. **View Results**
   - Risk score and assessment
   - File metadata and hashes
   - Detected behaviors
   - MITRE techniques
   - Suspicious APIs and strings

5. **Generate Report**
   - Navigate to "📄 Reports"
   - Select report format
   - Click "Generate & Download Report"

6. **Compare Samples**
   - Upload multiple files
   - Use "🔍 Similarity" page
   - Compare characteristics

---

## 🎨 Dashboard Features

### Visualizations

#### Risk Gauge

- Visual representation of risk score (0-100)
- Color-coded severity levels:
  - 🟢 **Low** (0-34): Green
  - 🟡 **Medium** (35-59): Yellow
  - 🟠 **High** (60-79): Orange
  - 🔴 **Critical** (80-100): Red

#### Risk Factor Breakdown

- Bar chart showing contribution of each risk factor
- Color intensity indicates factor severity
- Helps identify primary risk drivers

#### Behavior Radar Chart

- Multi-dimensional behavior visualization
- Confidence levels for each detected behavior
- Comparison across behavior categories

#### MITRE Tactics Distribution

- Pie/bar chart of identified techniques
- Grouped by attack tactic
- Confidence scoring for each

#### Entropy Analysis

- Section-by-section entropy visualization
- Identifies suspicious sections with high entropy
- Packer detection support

#### API Frequency Chart

- Most common suspicious API imports
- Ranked by frequency
- Risk level indicators

### Data Tables

#### File Details Table

- Hashes (MD5, SHA1, SHA256)
- File metadata
- Import information
- Section information

#### Behaviors Table

- Detected behaviors
- Categories and classifications
- Confidence percentages
- Descriptions

#### MITRE Techniques Table

- Technique IDs
- Names and descriptions
- Associated tactics
- Confidence levels

#### Suspicious APIs Table

- DLL names
- Function names
- Risk levels

#### Strings Table

- Suspicious strings found
- Categorization
- Frequency information

---

## 📊 Analysis Details

### Risk Scoring System

Risk scores are calculated using a 10-factor system (0-100 scale):

1. **Packer Indicators** - Presence of packing/obfuscation
2. **Entropy Scores** - High entropy sections suggest encryption
3. **Suspicious Imports** - Number and risk of API imports
4. **Section Analysis** - Suspicious PE sections
5. **String Indicators** - Suspicious strings in the binary
6. **Entry Point** - Non-standard entry points
7. **Digital Signature** - Missing or invalid signatures
8. **File Size Anomalies** - Unusual file sizes
9. **Known Malicious Patterns** - Matches to known indicators
10. **API Behavior** - Dangerous API combinations

### Behavior Prediction

The system predicts 10+ malware behaviors:

- **Dropper** - Drops additional malware
- **Downloader** - Downloads additional files
- **Injector** - Performs code injection
- **Keylogger** - Captures keyboard input
- **Ransomware** - Encrypts user files
- **Rootkit** - Hides malware presence
- **Worm** - Self-replicating capability
- **Trojan** - Backdoor access
- **C2 Communication** - Command and control
- **Privilege Escalation** - UAC bypass attempts

### MITRE ATT&CK Mapping

Techniques are mapped to MITRE ATT&CK tactics:

- Discovery
- Execution
- Persistence
- Defense Evasion
- Credential Access
- Lateral Movement
- Exfiltration
- Command and Control
- Impact

---

## 📈 Performance Metrics

### Analysis Speed

- Small files (<1 MB): 2-5 seconds
- Medium files (1-10 MB): 5-15 seconds
- Large files (10+ MB): 15-30 seconds

### Scalability

- Supports multiple concurrent analyses
- History tracking for unlimited samples
- In-memory session management

---

## 🔧 Configuration

### Streamlit Config (.streamlit/config.toml)

```toml
[theme]
primaryColor = "#667eea"        # Primary UI color
backgroundColor = "#ffffff"      # Page background
textColor = "#262730"           # Text color

[client]
maxUploadSize = 200             # Max upload size in MB
```

### Customization

To customize the dashboard:

1. **Colors**: Edit `COLORS` dictionary in `app.py`
2. **Page Layout**: Modify `st.columns()` settings
3. **Chart Types**: Change Plotly chart configurations
4. **Report Template**: Edit `report_generator.py`

---

## 📝 Report Generation

### Report Formats

#### Summary Report

- Quick overview (2-3 pages)
- Key findings only
- Risk assessment
- Recommendations

#### Detailed Report

- Comprehensive analysis (5-8 pages)
- All findings and indicators
- Technical deep-dive
- MITRE mapping details

#### Executive Summary

- Business-focused (1 page)
- Risk level and recommendations
- No technical details

### Report Sections

1. **Title Page** - File name, date, classification
2. **Executive Summary** - Risk level, verdict, key findings
3. **Technical Analysis** - File metadata, hashes, PE structure
4. **Risk Breakdown** - Risk factors and scores
5. **Detected Indicators** - Behaviors, APIs, strings
6. **MITRE Techniques** - ATT&CK framework mapping
7. **Detailed Findings** - PE sections, strings, imports

---

## 🔐 Security Notes

### Safe Analysis

1. **Isolated Environment**: Always analyze files in isolated VMs
2. **No Execution**: Static analysis only - no code execution
3. **Safe Storage**: Keep analyzed files in secure locations
4. **Access Control**: Restrict dashboard access to authorized users

### Best Practices

- Analyze suspicious files in a sandbox environment
- Don't run dashboard on exposed networks
- Regularly backup analysis history
- Use authentication for production deployments

---

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

#### File Upload Not Working

- Check file is PE format (.exe, .dll, .sys)
- Verify file size is under 200 MB limit
- Check file permissions

#### Charts Not Displaying

- Ensure plotly is installed: `pip install plotly`
- Check browser JavaScript is enabled
- Try refreshing the page

#### Slow Analysis

- Reduce file size
- Analyze in stages (upload smaller files)
- Check system resources (RAM, CPU)

### Debug Mode

Enable debug logging:

```bash
streamlit run app.py --logger.level=debug
```

---

## 📚 Integration

### With External Systems

#### YARA Rule Generation

```python
from core.yara_generator import generate_yara_rule

analysis = analyze_file("file.exe")
yara_rule = generate_yara_rule(analysis, rule_name="my_malware")
```

#### Custom Behavior Predictor

```python
from core.behavior_predictor import predict_behaviors

behaviors = predict_behaviors(analysis)
```

#### Similarity Analysis

```python
from core.similarity_engine import calculate_similarity

similarity = calculate_similarity(sample1, sample2)
```

---

## 🚀 Deployment

### Local Development

```bash
streamlit run app.py
```

### Production Deployment

#### Docker

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

#### Cloud Deployment

- Heroku
- AWS
- Google Cloud
- Azure

---

## 📊 Data Management

### Session State

- Analysis history stored in memory
- Persists during session only
- Cleared on page refresh

### Persistent Storage

To save analysis history:

```python
import json
with open("analysis_history.json", "w") as f:
    json.dump(st.session_state.analysis_history, f)
```

### Export Data

- Export as JSON
- Export as CSV
- Download PDF reports

---

## 🔄 Updates & Maintenance

### Regular Updates

```bash
pip install --upgrade streamlit plotly pandas
```

### Performance Optimization

- Clear browser cache periodically
- Manage analysis history size
- Monitor dashboard resource usage

---

## 📞 Support

### Documentation

- See `docs/` folder for detailed guides
- Check `PERSON_*_GUIDE.md` files
- Review `QUICK_REFERENCE.md` files

### Getting Help

- Check troubleshooting section
- Review log files
- Check Streamlit documentation: https://docs.streamlit.io

---

## 📄 License

MORPHEUS-X is provided under MIT License.

---

## 🙏 Acknowledgments

Built with:

- **Streamlit** - Interactive web framework
- **Plotly** - Interactive visualizations
- **pefile** - PE file parsing
- **YARA** - Pattern matching engine
- **ReportLab** - PDF generation

---

## 📋 File Structure

```
MORPHEUS/
├── app.py                 # Main Streamlit application
├── gui_utils.py          # Visualization utilities
├── report_generator.py    # PDF report generation
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── core/                 # Analysis modules
│   ├── analyzer.py
│   ├── risk_engine.py
│   ├── behavior_predictor.py
│   ├── mitre_mapper.py
│   ├── yara_generator.py
│   └── similarity_engine.py
├── data/
│   └── uploads/          # File upload directory
├── docs/                 # Documentation
├── rules/                # Generated YARA rules
├── tests/                # Test files
└── requirements.txt      # Python dependencies
```

---

**Last Updated**: May 2026  
**Version**: 1.0.0  
**Status**: Production Ready
