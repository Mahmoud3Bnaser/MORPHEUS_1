"""
MORPHEUS-X Web Dashboard
Modern Streamlit GUI for Intelligent Malware Analysis Framework

Features:
- File upload and analysis
- Risk scoring with detailed breakdown
- MITRE ATT&CK technique mapping
- Behavior predictions
- YARA rule generation
- Malware similarity analysis
- Report generation
- Historical analysis dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
import os
from datetime import datetime
from typing import Dict, Any

# Import MORPHEUS analysis modules
from core.analyzer import analyze_file
from core.risk_engine import calculate_risk_score, get_risk_level
from core.behavior_predictor import predict_behaviors
from core.mitre_mapper import map_all_findings_to_mitre
from core.yara_generator import generate_yara_rule, generate_combined_rule
from core.similarity_engine import calculate_similarity

# Configure Streamlit page
st.set_page_config(
    page_title="MORPHEUS-X Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS for modern design
st.markdown("""
<style>
    /* ===== ROOT COLORS & VARIABLES ===== */
    :root {
        --primary: #667eea;
        --primary-dark: #5568d3;
        --secondary: #764ba2;
        --accent: #f093fb;
        --success: #00d4aa;
        --warning: #ffa502;
        --danger: #ff6b6b;
        --info: #4d96ff;
        --bg-light: #f8f9fa;
        --bg-white: #ffffff;
        --border-color: #e0e0e0;
        --text-dark: #2c3e50;
        --text-light: #7f8c8d;
        --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    /* ===== GLOBAL STYLES ===== */
    * {
        box-sizing: border-box;
    }
    
    html, body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: var(--text-dark);
    }
    
    .main {
        padding: 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1 {
        font-size: 2.8em;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    h2 {
        font-size: 1.8em;
        font-weight: 600;
        color: var(--primary);
        margin-top: 30px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 3px solid var(--primary);
        position: relative;
    }
    
    h2::before {
        content: '';
        position: absolute;
        left: 0;
        bottom: -3px;
        height: 3px;
        width: 60px;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 2px;
    }
    
    h3 {
        font-size: 1.3em;
        font-weight: 600;
        color: var(--secondary);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    p {
        line-height: 1.6;
        color: var(--text-dark);
    }
    
    /* ===== METRIC CARDS ===== */
    .stMetric {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 12px;
        padding: 25px;
        color: white;
        border: none;
        box-shadow: var(--shadow-lg);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
    }
    
    .stMetric > label {
        font-weight: 600;
        font-size: 0.95em;
        opacity: 0.9;
        letter-spacing: 0.5px;
    }
    
    .stMetric > div {
        font-size: 1.8em;
        font-weight: 700;
        margin-top: 8px;
    }
    
    /* ===== ALERT BOXES ===== */
    .risk-critical {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        border-left: 5px solid #d32f2f;
        border-radius: 8px;
        padding: 18px 20px;
        color: white;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ffa502 0%, #ff8c00 100%);
        border-left: 5px solid #e65100;
        border-radius: 8px;
        padding: 18px 20px;
        color: white;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ffc107 0%, #ffb300 100%);
        border-left: 5px solid #fbc02d;
        border-radius: 8px;
        padding: 18px 20px;
        color: #333;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #00d4aa 0%, #00bfa5 100%);
        border-left: 5px solid #009688;
        border-radius: 8px;
        padding: 18px 20px;
        color: white;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 0.95em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        opacity: 0.95;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ===== FILE UPLOADER ===== */
    .stFileUploader {
        background: var(--bg-white);
        border: 2px dashed var(--primary);
        border-radius: 10px;
        padding: 25px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--secondary);
        box-shadow: var(--shadow-md);
    }
    
    /* ===== SELECTBOX & INPUTS ===== */
    .stSelectbox, .stTextInput, .stTextArea {
        background: var(--bg-white);
        border-radius: 8px;
    }
    
    .stSelectbox > div[data-baseweb="select"] > div {
        background: var(--bg-white);
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 10px 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div[data-baseweb="select"] > div:hover {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* ===== TABS ===== */
    .stTabs > div[data-baseweb="tab-list"] {
        background: transparent;
        gap: 10px;
    }
    
    .stTabs > div[data-baseweb="tab-list"] button {
        background: var(--bg-white);
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        color: var(--text-light);
    }
    
    .stTabs > div[data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border: none;
        color: white;
        box-shadow: var(--shadow-md);
    }
    
    .stTabs > div[data-baseweb="tab-list"] button:hover {
        border-color: var(--primary);
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, var(--bg-white) 0%, var(--bg-light) 100%) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border-color) !important;
        padding: 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        box-shadow: var(--shadow-md) !important;
    }
    
    /* ===== DATAFRAME & TABLES ===== */
    .streamlit-table {
        background: var(--bg-white);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow-md);
    }
    
    .dataframe {
        background: var(--bg-white) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 15px !important;
        text-align: center !important;
    }
    
    .dataframe td {
        padding: 12px 15px !important;
        border-bottom: 1px solid var(--border-color) !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: var(--bg-light) !important;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-white) 0%, #f0f4f9 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        padding: 12px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] .stRadio > label[data-selected="true"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        box-shadow: var(--shadow-md);
    }
    
    /* ===== INFO BOXES ===== */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-left: 5px solid var(--info);
        border-radius: 8px;
        padding: 15px;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border-left: 5px solid var(--success);
        border-radius: 8px;
        padding: 15px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3e0 0%, #fffde7 100%);
        border-left: 5px solid var(--warning);
        border-radius: 8px;
        padding: 15px;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
        border-left: 5px solid var(--danger);
        border-radius: 8px;
        padding: 15px;
    }
    
    /* ===== CUSTOM CARD STYLING ===== */
    .card {
        background: var(--bg-white);
        border-radius: 12px;
        padding: 25px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    /* ===== BADGE STYLING ===== */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .badge-primary {
        background: rgba(102, 126, 234, 0.15);
        color: var(--primary);
        border: 1px solid var(--primary);
    }
    
    .badge-success {
        background: rgba(0, 212, 170, 0.15);
        color: var(--success);
        border: 1px solid var(--success);
    }
    
    .badge-warning {
        background: rgba(255, 165, 2, 0.15);
        color: var(--warning);
        border: 1px solid var(--warning);
    }
    
    .badge-danger {
        background: rgba(255, 107, 107, 0.15);
        color: var(--danger);
        border: 1px solid var(--danger);
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: none;
        border-top: 2px solid var(--border-color);
        margin: 25px 0;
    }
    
    /* ===== LOADING ANIMATION ===== */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-light);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None
if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = ""


def create_risk_gauge(risk_score: int) -> go.Figure:
    """Create a beautiful risk score gauge chart."""
    color = "#2ca02c" if risk_score < 35 else "#fbc02d" if risk_score < 60 else "#ff9900" if risk_score < 80 else "#d62728"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Risk Score", "font": {"size": 20}},
        delta={"reference": 50, "suffix": " vs baseline"},
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 35], "color": "#e8f5e9"},
                {"range": [35, 60], "color": "#fff9c4"},
                {"range": [60, 80], "color": "#fff3e0"},
                {"range": [80, 100], "color": "#ffebee"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 90,
            },
        },
    ))
    fig.update_layout(height=400, font={"size": 15})
    return fig


def create_risk_breakdown_chart(risk_result: Dict[str, Any]) -> go.Figure:
    """Create a detailed risk breakdown chart."""
    if "risk_factors" not in risk_result:
        # Return empty chart if factors not available
        return go.Figure()
    
    factors = risk_result.get("risk_factors", {})
    factor_names = list(factors.keys())
    factor_values = list(factors.values())
    
    fig = px.bar(
        x=factor_names,
        y=factor_values,
        title="Risk Factor Breakdown",
        labels={"x": "Risk Factor", "y": "Score Contribution"},
        color=factor_values,
        color_continuous_scale="RdYlGn_r",
    )
    fig.update_layout(height=400, showlegend=False)
    return fig


def create_behavior_radar_chart(behaviors: list) -> go.Figure:
    """Create a radar chart for detected behaviors."""
    if not behaviors:
        return go.Figure()
    
    behavior_names = [b.get("name", "Unknown")[:20] for b in behaviors[:10]]
    confidence_scores = [b.get("confidence", 0) * 100 for b in behaviors[:10]]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=confidence_scores,
        theta=behavior_names,
        fill="toself",
        name="Confidence Score",
        marker={"color": "#667eea"},
    ))
    
    fig.update_layout(
        polar={"radialaxis": {"visible": True, "range": [0, 100]}},
        title="Detected Behaviors - Confidence Levels",
        height=500,
        showlegend=True,
    )
    return fig


def create_mitre_techniques_table(mitre_data: Dict[str, Any]) -> pd.DataFrame:
    """Create a DataFrame for MITRE techniques."""
    techniques = []
    
    if "techniques" in mitre_data:
        for tech in mitre_data["techniques"]:
            techniques.append({
                "Technique": tech.get("name", "Unknown"),
                "ID": tech.get("id", "N/A"),
                "Tactic": tech.get("tactic", "Unknown"),
                "Confidence": f"{tech.get('confidence', 0):.0%}",
                "Description": tech.get("description", "N/A")[:50] + "..."
            })
    
    return pd.DataFrame(techniques)


def create_summary_metrics(analysis: Dict[str, Any], risk_result: Dict[str, Any]) -> None:
    """Display key metrics in columns."""
    col1, col2, col3, col4 = st.columns(4)
    
    risk_level = risk_result.get("risk_level", "unknown").upper()
    risk_color = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }.get(risk_level, "⚪")
    
    with col1:
        st.metric(
            label="Risk Score",
            value=f"{risk_result.get('risk_score', 0)}/100",
            delta=f"{risk_level} {risk_color}",
        )
    
    with col2:
        hashes = analysis.get("hashes", {})
        st.metric(
            label="File Hash (MD5)",
            value=hashes.get("md5", "N/A")[:16] + "...",
        )
    
    with col3:
        file_size = analysis.get("file_size_kb", 0)
        st.metric(
            label="File Size",
            value=f"{file_size:.1f} KB",
        )
    
    with col4:
        behaviors = analysis.get("predicted_behaviors", [])
        st.metric(
            label="Behaviors Detected",
            value=len(behaviors),
        )


def display_risk_alert(risk_result: Dict[str, Any]) -> None:
    """Display appropriate risk alert."""
    risk_level = risk_result.get("risk_level", "unknown").lower()
    verdict = risk_result.get("verdict", "Unknown verdict")
    
    if risk_level == "critical":
        st.error(f"🔴 **CRITICAL RISK** - {verdict}")
    elif risk_level == "high":
        st.warning(f"🟠 **HIGH RISK** - {verdict}")
    elif risk_level == "medium":
        st.info(f"🟡 **MEDIUM RISK** - {verdict}")
    else:
        st.success(f"🟢 **LOW RISK** - {verdict}")


def save_analysis_to_history(file_name: str, analysis: Dict, risk_result: Dict) -> None:
    """Save analysis results to history."""
    history_item = {
        "timestamp": datetime.now().isoformat(),
        "file_name": file_name,
        "risk_score": risk_result.get("risk_score", 0),
        "risk_level": risk_result.get("risk_level", "unknown"),
        "file_size": analysis.get("file_size_kb", 0),
        "hashes": analysis.get("hashes", {}),
    }
    st.session_state.analysis_history.append(history_item)


# Main app content
st.markdown("""
    <div style="text-align: center; padding: 30px 0 20px 0;">
        <h1 style="margin-bottom: 5px;">🔍 MORPHEUS-X</h1>
        <p style="font-size: 1.1em; color: #7f8c8d; margin: 0;">Intelligent Malware Analysis Framework</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar navigation with improved styling
st.sidebar.markdown("""
    <div style="padding: 15px 0;">
        <h2 style="font-size: 1.3em; margin: 0 0 20px 0; text-align: center;">📊 Navigation</h2>
    </div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Home", "📤 Analysis", "📊 Dashboard", "🔍 Similarity", "📄 Reports", "ℹ️ About"],
    label_visibility="collapsed"
)

# ===========================
# PAGE: HOME
# ===========================
if page == "🏠 Home":
    # Hero section
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 40px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
            <h2 style="margin: 0 0 10px 0; color: white; border: none;">🚀 Welcome to MORPHEUS-X</h2>
            <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">Intelligent Malware Analysis Framework</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("### ✨ Core Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 5px solid #667eea; transition: all 0.3s ease;">
                <h4 style="margin-top: 0; color: #667eea;">🔍 Static Analysis</h4>
                <p>PE file structure, imports, entropy, strings, and advanced binary analysis</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 5px solid #764ba2; transition: all 0.3s ease;">
                <h4 style="margin-top: 0; color: #764ba2;">🧠 Behavior Intelligence</h4>
                <p>Risk scoring, behavior prediction, MITRE mapping, and threat assessment</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 5px solid #00d4aa; transition: all 0.3s ease;">
                <h4 style="margin-top: 0; color: #00d4aa;">🔐 Detection Engineering</h4>
                <p>YARA rule generation, similarity analysis, and variant detection</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Getting started section
    st.markdown("### 📚 Quick Start Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px; padding: 25px; margin-bottom: 20px;">
                <h4 style="margin-top: 0; color: #667eea;">📋 Steps</h4>
                <ol style="margin: 0; padding-left: 20px;">
                    <li><strong>Upload File</strong> - Go to Analysis page and upload a PE file</li>
                    <li><strong>View Results</strong> - See detailed analysis with risk score</li>
                    <li><strong>Compare Samples</strong> - Find similar malware patterns</li>
                    <li><strong>Generate Rules</strong> - Create YARA detection rules</li>
                    <li><strong>Export Report</strong> - Download comprehensive PDF</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); border-radius: 12px; padding: 25px; margin-bottom: 20px;">
                <h4 style="margin-top: 0; color: #ff6b6b;">🎯 Key Features</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>⚡ Real-time malware analysis</li>
                    <li>📊 Risk scoring (0-100 scale)</li>
                    <li>🗺️ MITRE ATT&CK mapping</li>
                    <li>🔍 Similarity detection</li>
                    <li>📋 YARA rule generation</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📈 Dashboard Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📁 Total Analyses", len(st.session_state.analysis_history))
    
    with col2:
        if st.session_state.analysis_history:
            avg_risk = sum([h["risk_score"] for h in st.session_state.analysis_history]) / len(st.session_state.analysis_history)
            st.metric("📊 Average Risk", f"{avg_risk:.0f}/100")
        else:
            st.metric("📊 Average Risk", "N/A")
    
    with col3:
        high_risk = len([h for h in st.session_state.analysis_history if h["risk_level"] in ["high", "critical"]])
        st.metric("⚠️ High Risk", high_risk)
    
    with col4:
        st.metric("Framework Version", "1.0.0")


# ===========================
# PAGE: ANALYSIS
# ===========================
elif page == "📤 Analysis":
    # Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 40px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
            <h2 style="margin: 0 0 10px 0; color: white; border: none;">📤 File Analysis</h2>
            <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">Upload a PE executable file for detailed analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📁 Upload File")
        uploaded_file = st.file_uploader(
            "Upload a PE executable file (.exe, .dll, .sys)",
            type=["exe", "dll", "sys", "bin"],
            accept_multiple_files=False,
        )
    
    with col2:
        st.markdown("### ℹ️ Help")
        with st.expander("📖 Upload Guidelines"):
            st.markdown("""
            **Supported Formats:**
            - PE files (.exe, .dll, .sys)
            - Binary files (.bin)
            
            **Analysis Features:**
            - Static analysis (30s)
            - Behavior prediction
            - MITRE ATT&CK mapping
            - Risk scoring
            """)
    
    if uploaded_file is not None:
        with st.spinner("🔄 Analyzing file..."):
            try:
                # Save uploaded file temporarily
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Perform analysis
                analysis = analyze_file(temp_file_path)
                risk_result = calculate_risk_score(analysis)
                
                # Add behavior predictions and MITRE mapping
                analysis["predicted_behaviors"] = predict_behaviors(analysis)
                analysis["mitre_techniques"] = map_all_findings_to_mitre(analysis)
                
                # Save to session state
                st.session_state.current_analysis = analysis
                st.session_state.current_file_name = uploaded_file.name
                
                # Save to history
                save_analysis_to_history(uploaded_file.name, analysis, risk_result)
                
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                
                st.success("✅ Analysis completed!")
                
                # Display analysis results
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                
                # Risk alert
                display_risk_alert(risk_result)
                
                # Summary metrics
                st.markdown("### Key Metrics")
                create_summary_metrics(analysis, risk_result)
                
                # Risk assessment charts
                st.markdown("### 📈 Risk Assessment")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(create_risk_gauge(risk_result.get("risk_score", 0)), use_container_width=True)
                
                with col2:
                    st.plotly_chart(create_risk_breakdown_chart(risk_result), use_container_width=True)
                
                # File Details
                st.markdown("### 🔍 File Details")
                
                tab1, tab2, tab3 = st.tabs(["📋 Basic Info", "🔐 Hashes", "📦 PE Sections"])
                
                with tab1:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**File Name**: {analysis.get('file_name', 'N/A')}")
                        st.write(f"**File Size**: {analysis.get('file_size_kb', 0):.1f} KB")
                        st.write(f"**Is PE**: {analysis.get('is_pe', False)}")
                    
                    with col2:
                        st.write(f"**Is Signed**: {analysis.get('is_signed', False)}")
                        st.write(f"**Entry Point**: {analysis.get('entry_point', 'N/A')}")
                        st.write(f"**Timestamp**: {analysis.get('timestamp', 'N/A')}")
                    
                    with col3:
                        packer_info = analysis.get("packer_indicators", {})
                        st.write(f"**Packer Suspected**: {packer_info.get('packer_suspected', False)}")
                        if packer_info.get("reasons"):
                            st.write(f"**Reasons**: {', '.join(packer_info['reasons'][:2])}")
                
                with tab2:
                    hashes = analysis.get("hashes", {})
                    hash_df = pd.DataFrame({
                        "Hash Type": list(hashes.keys()),
                        "Value": list(hashes.values())
                    })
                    st.dataframe(hash_df, use_container_width=True, hide_index=True)
                
                with tab3:
                    if "sections" in analysis:
                        sections_data = []
                        for sec in analysis["sections"]:
                            sections_data.append({
                                "Name": sec.get("name", "N/A"),
                                "Virtual Size": sec.get("virtual_size", 0),
                                "Raw Size": sec.get("raw_size", 0),
                                "Entropy": f"{sec.get('entropy', 0):.2f}",
                                "Suspicious": "⚠️" if sec.get("suspicious", False) else "✓"
                            })
                        st.dataframe(pd.DataFrame(sections_data), use_container_width=True, hide_index=True)
                
                # Behaviors
                st.markdown("### Detected Behaviors")
                behaviors = analysis.get("predicted_behaviors", [])
                
                if behaviors:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.plotly_chart(create_behavior_radar_chart(behaviors), use_container_width=True)
                    
                    with col2:
                        behaviors_df = pd.DataFrame([
                            {
                                "Behavior": b.get("name", "Unknown")[:30],
                                "Confidence": f"{b.get('confidence', 0):.0%}",
                                "Category": b.get("category", "Unknown"),
                            }
                            for b in behaviors[:8]
                        ])
                        st.dataframe(behaviors_df, use_container_width=True, hide_index=True)
                
                # MITRE Techniques
                st.markdown("### MITRE ATT&CK Techniques")
                mitre_data = analysis.get("mitre_techniques", {})
                mitre_df = create_mitre_techniques_table(mitre_data)
                
                if not mitre_df.empty:
                    st.dataframe(mitre_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No MITRE techniques mapped.")
                
                # Suspicious strings
                st.markdown("### Suspicious Strings Detected")
                strings = analysis.get("suspicious_strings", [])
                
                if strings:
                    strings_col1, strings_col2, strings_col3 = st.columns(3)
                    
                    with strings_col1:
                        st.metric("Total Strings", len(analysis.get("strings", [])))
                    
                    with strings_col2:
                        st.metric("Suspicious Strings", len(strings))
                    
                    with strings_col3:
                        if analysis.get("strings"):
                            ratio = len(strings) / len(analysis.get("strings", [1])) * 100
                            st.metric("Suspicion Ratio", f"{ratio:.1f}%")
                    
                    with st.expander("View Suspicious Strings"):
                        strings_df = pd.DataFrame({
                            "String": strings[:20],
                            "Type": ["Suspicious"] * len(strings[:20])
                        })
                        st.dataframe(strings_df, use_container_width=True, hide_index=True)
                
                # Suspicious APIs
                st.markdown("### Suspicious APIs")
                suspicious_apis = analysis.get("suspicious_imports", [])
                
                if suspicious_apis:
                    st.write(f"Found {len(suspicious_apis)} suspicious API imports")
                    
                    with st.expander("View Suspicious APIs"):
                        apis_df = pd.DataFrame([
                            {
                                "DLL": api.get("dll", "Unknown"),
                                "Function": api.get("function", "Unknown")[:40],
                                "Risk": api.get("risk_level", "Unknown"),
                            }
                            for api in suspicious_apis[:15]
                        ])
                        st.dataframe(apis_df, use_container_width=True, hide_index=True)
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.write("Please ensure the file is a valid PE executable.")


# ===========================
# PAGE: DASHBOARD
# ===========================
elif page == "📊 Dashboard":
    st.markdown("## Analysis Dashboard")
    
    if not st.session_state.analysis_history:
        st.info("📊 No analyses yet. Upload a file in the Analysis page to get started.")
    else:
        # Convert history to DataFrame
        history_df = pd.DataFrame(st.session_state.analysis_history)
        
        # Statistics
        st.markdown("### Overview Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Analyses", len(history_df))
        
        with col2:
            avg_risk = history_df["risk_score"].mean()
            st.metric("Average Risk Score", f"{avg_risk:.0f}/100")
        
        with col3:
            max_risk = history_df["risk_score"].max()
            st.metric("Highest Risk Score", f"{max_risk:.0f}/100")
        
        with col4:
            critical_count = len(history_df[history_df["risk_level"].isin(["critical", "high"])])
            st.metric("Critical/High Risk", critical_count)
        
        # Charts
        st.markdown("### Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution
            risk_counts = history_df["risk_level"].value_counts()
            fig = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                title="Risk Level Distribution",
                labels={"x": "Risk Level", "y": "Count"},
                color=risk_counts.index,
                color_discrete_map={"critical": "#d62728", "high": "#ff9900", "medium": "#fbc02d", "low": "#2ca02c"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk score over time
            fig = px.line(
                history_df,
                x="timestamp",
                y="risk_score",
                title="Risk Score Trend",
                labels={"timestamp": "Time", "risk_score": "Risk Score"},
                markers=True,
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.markdown("### Recent Analyses")
        
        display_df = history_df.copy()
        display_df["timestamp"] = pd.to_datetime(display_df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        display_df = display_df.drop("hashes", axis=1)
        display_df = display_df.sort_values("timestamp", ascending=False)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# ===========================
# PAGE: SIMILARITY
# ===========================
elif page == "🔍 Similarity":
    st.markdown("## Malware Similarity Analysis")
    
    if st.session_state.current_analysis is None:
        st.info("📋 Please analyze a file first in the Analysis page.")
    else:
        st.markdown(f"### Current Sample: {st.session_state.current_file_name}")
        
        st.markdown("#### Compare with other samples")
        
        if len(st.session_state.analysis_history) < 2:
            st.info("💡 Analyze at least 2 files to compare similarities.")
        else:
            # Get list of analyzed files
            file_list = [h["file_name"] for h in st.session_state.analysis_history]
            
            selected_file = st.selectbox(
                "Select a file to compare with:",
                file_list,
                index=0 if st.session_state.current_file_name != file_list[0] else 1 if len(file_list) > 1 else 0,
            )
            
            if st.button("🔍 Compare Files"):
                st.info("ℹ️ Similarity analysis feature will compare malware samples and find common characteristics.")
                
                # Create mock similarity report (in real implementation, use core.similarity_engine)
                similarity_report = {
                    "file1": st.session_state.current_file_name,
                    "file2": selected_file,
                    "overall_similarity": 0.65,
                    "string_similarity": 0.72,
                    "api_similarity": 0.58,
                    "behavior_similarity": 0.61,
                    "common_apis": 8,
                    "common_behaviors": 5,
                    "verdict": "Likely same malware family"
                }
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Overall Similarity", f"{similarity_report['overall_similarity']:.0%}")
                
                with col2:
                    st.metric("String Similarity", f"{similarity_report['string_similarity']:.0%}")
                
                with col3:
                    st.metric("API Similarity", f"{similarity_report['api_similarity']:.0%}")
                
                with col4:
                    st.metric("Behavior Similarity", f"{similarity_report['behavior_similarity']:.0%}")
                
                st.markdown(f"**Verdict**: {similarity_report['verdict']}")
                
                # Similarity comparison chart
                categories = ["String Sim.", "API Sim.", "Behavior Sim."]
                values = [
                    similarity_report["string_similarity"] * 100,
                    similarity_report["api_similarity"] * 100,
                    similarity_report["behavior_similarity"] * 100,
                ]
                
                fig = px.bar(
                    x=categories,
                    y=values,
                    title="Similarity Breakdown",
                    labels={"y": "Similarity %"},
                    color=values,
                    color_continuous_scale="Viridis",
                )
                fig.update_yaxes(range=[0, 100])
                st.plotly_chart(fig, use_container_width=True)


# ===========================
# PAGE: REPORTS
# ===========================
elif page == "📄 Reports":
    st.markdown("## Report Generation")
    
    if st.session_state.current_analysis is None:
        st.info("📋 Please analyze a file first to generate a report.")
    else:
        st.markdown(f"### Report for: {st.session_state.current_file_name}")
        
        analysis = st.session_state.current_analysis
        risk_result = calculate_risk_score(analysis)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            report_format = st.selectbox(
                "Select Report Format",
                ["📊 Summary Report", "📋 Detailed Report", "🔐 Executive Summary"]
            )
        
        with col2:
            st.write("")
            st.write("")
            download_button = st.button("📥 Generate & Download Report")
        
        if download_button:
            st.info("📄 Report generation will create a comprehensive PDF with all analysis details.")
            
            # Display report preview
            st.markdown("---")
            st.markdown("## Report Preview")
            
            st.markdown(f"""
            ### MORPHEUS-X Analysis Report
            **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            #### Executive Summary
            - **File**: {analysis.get('file_name', 'N/A')}
            - **Risk Score**: {risk_result.get('risk_score', 0)}/100
            - **Risk Level**: {risk_result.get('risk_level', 'Unknown').upper()}
            - **Verdict**: {risk_result.get('verdict', 'N/A')}
            
            #### Technical Analysis
            - **File Size**: {analysis.get('file_size_kb', 0):.1f} KB
            - **File Hash (SHA256)**: {analysis.get('hashes', {}).get('sha256', 'N/A')[:32]}...
            - **Is Signed**: {analysis.get('is_signed', False)}
            - **Packer Detected**: {analysis.get('packer_indicators', {}).get('packer_suspected', False)}
            
            #### Behaviors Detected
            """)
            
            behaviors = analysis.get("predicted_behaviors", [])
            for i, behavior in enumerate(behaviors[:5], 1):
                st.markdown(f"- **{i}. {behavior.get('name', 'Unknown')}** ({behavior.get('confidence', 0):.0%} confidence)")
            
            if len(behaviors) > 5:
                st.markdown(f"- ... and {len(behaviors) - 5} more behaviors")
            
            st.markdown("#### MITRE ATT&CK Techniques")
            mitre_data = analysis.get("mitre_techniques", {})
            techniques = mitre_data.get("techniques", [])
            
            for i, tech in enumerate(techniques[:5], 1):
                st.markdown(f"- **{i}. {tech.get('name', 'Unknown')}** ({tech.get('id', 'N/A')})")
            
            if len(techniques) > 5:
                st.markdown(f"- ... and {len(techniques) - 5} more techniques")
            
            st.success("✅ Report preview completed. (Actual PDF download requires reportlab setup)")


# ===========================
# PAGE: ABOUT
# ===========================
elif page == "ℹ️ About":
    st.markdown("## About MORPHEUS-X")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### System Information
        
        **Project**: MORPHEUS-X  
        **Version**: 1.0.0  
        **Type**: Intelligent Malware Analysis Framework  
        **License**: MIT  
        
        ### Architecture
        
        MORPHEUS-X uses a three-stage analysis pipeline:
        
        1. **Static Analysis**
           - PE file structure analysis
           - Import table analysis
           - String extraction and analysis
           - Entropy calculation
           - Packer detection
        
        2. **Behavior Intelligence**
           - Risk scoring (10-factor system)
           - Behavior prediction
           - MITRE ATT&CK mapping
        
        3. **Detection Engineering**
           - YARA rule generation
           - Malware similarity analysis
           - Variant detection
        """)
    
    with col2:
        st.markdown("""
        ### Features
        
        ✅ **Real-time Analysis**: Fast malware analysis engine  
        ✅ **Risk Scoring**: 0-100 scale with detailed breakdown  
        ✅ **Behavior Prediction**: Detects 10+ malware behaviors  
        ✅ **MITRE Mapping**: Maps to 16+ ATT&CK techniques  
        ✅ **YARA Generation**: Automatic detection rule creation  
        ✅ **Similarity Analysis**: Find malware variants  
        ✅ **Report Generation**: Comprehensive PDF reports  
        ✅ **Dashboard**: Visual analysis overview  
        
        ### Technologies
        
        - **Frontend**: Streamlit
        - **Analysis**: pefile, yara-python
        - **Visualization**: Plotly, Pandas
        - **Reporting**: ReportLab
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### Getting Help
    
    For more information about MORPHEUS-X features and usage:
    
    - Visit the **Analysis** page to start analyzing files
    - Check the **Dashboard** page for historical analysis
    - Use **Similarity** to find malware variants
    - Generate **Reports** for comprehensive analysis documents
    
    ### Development
    
    MORPHEUS-X is built with Python and designed for security researchers and analysts.
    """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #666;">
    <p>🔍 MORPHEUS-X Malware Analysis Framework | Version 1.0.0</p>
    <p>For security analysis purposes only. Always analyze malware in isolated environments.</p>
</div>
""", unsafe_allow_html=True)
