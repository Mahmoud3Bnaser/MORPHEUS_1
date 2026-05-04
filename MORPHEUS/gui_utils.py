"""
MORPHEUS-X GUI Utilities
Visualization and charting helper functions for Streamlit dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any, Tuple


class VisualizationEngine:
    """Engine for creating visualization charts for the dashboard."""
    
    # Color palette for consistency
    COLORS = {
        "critical": "#d62728",
        "high": "#ff9900",
        "medium": "#fbc02d",
        "low": "#2ca02c",
        "primary": "#667eea",
        "secondary": "#764ba2",
        "accent": "#ff7f0e",
    }
    
    @staticmethod
    def create_risk_distribution_chart(risk_data: List[Dict[str, Any]]) -> go.Figure:
        """Create a pie chart for risk distribution."""
        risk_counts = {}
        for item in risk_data:
            level = item.get("risk_level", "unknown")
            risk_counts[level] = risk_counts.get(level, 0) + 1
        
        labels = list(risk_counts.keys())
        values = list(risk_counts.values())
        colors = [VisualizationEngine.COLORS.get(label, "#999999") for label in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker={"colors": colors},
            textposition="inside",
            textinfo="label+percent",
        )])
        
        fig.update_layout(
            title="Risk Level Distribution",
            height=400,
            showlegend=True,
        )
        
        return fig
    
    @staticmethod
    def create_timeline_chart(history_data: pd.DataFrame) -> go.Figure:
        """Create a timeline chart of risk scores."""
        if history_data.empty:
            return go.Figure()
        
        fig = px.scatter(
            history_data,
            x="timestamp",
            y="risk_score",
            size="risk_score",
            color="risk_level",
            hover_name="file_name",
            title="Risk Score Timeline",
            labels={"timestamp": "Analysis Time", "risk_score": "Risk Score"},
            color_discrete_map=VisualizationEngine.COLORS,
        )
        
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def create_behavior_heatmap(behaviors: List[Dict[str, Any]]) -> go.Figure:
        """Create a heatmap of behavior categories and confidence."""
        if not behaviors:
            return go.Figure()
        
        # Group by category
        categories = {}
        for behavior in behaviors:
            category = behavior.get("category", "Unknown")
            confidence = behavior.get("confidence", 0) * 100
            
            if category not in categories:
                categories[category] = []
            categories[category].append(confidence)
        
        # Create heatmap data
        category_names = list(categories.keys())
        avg_confidences = [sum(conf) / len(conf) for conf in categories.values()]
        
        fig = go.Figure(data=go.Bar(
            x=category_names,
            y=avg_confidences,
            marker={"color": avg_confidences, "colorscale": "Reds"},
            text=[f"{c:.0f}%" for c in avg_confidences],
            textposition="auto",
        ))
        
        fig.update_layout(
            title="Behavior Categories - Average Confidence",
            xaxis_title="Behavior Category",
            yaxis_title="Confidence (%)",
            height=400,
        )
        
        return fig
    
    @staticmethod
    def create_api_frequency_chart(apis: List[Dict[str, Any]]) -> go.Figure:
        """Create a chart of most frequent suspicious APIs."""
        if not apis:
            return go.Figure()
        
        # Count API frequencies
        api_counts = {}
        for api in apis[:15]:  # Top 15
            func = api.get("function", "Unknown")
            api_counts[func] = api_counts.get(func, 0) + 1
        
        sorted_apis = sorted(api_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        func_names = [api[0][:25] for api in sorted_apis]
        counts = [api[1] for api in sorted_apis]
        
        fig = go.Figure(data=go.Bar(
            y=func_names,
            x=counts,
            orientation="h",
            marker={"color": counts, "colorscale": "Oranges"},
        ))
        
        fig.update_layout(
            title="Most Frequent Suspicious APIs",
            xaxis_title="Frequency",
            yaxis_title="API Function",
            height=400,
            yaxis={"tickfont": {"size": 10}},
        )
        
        return fig
    
    @staticmethod
    def create_file_entropy_chart(sections: List[Dict[str, Any]]) -> go.Figure:
        """Create a chart showing entropy levels across PE sections."""
        if not sections:
            return go.Figure()
        
        section_names = [s.get("name", "Unknown")[:8] for s in sections]
        entropies = [s.get("entropy", 0) for s in sections]
        colors = ["#d62728" if e > 7.5 else "#ff9900" if e > 6.5 else "#2ca02c" for e in entropies]
        
        fig = go.Figure(data=go.Bar(
            x=section_names,
            y=entropies,
            marker={"color": colors},
            text=[f"{e:.2f}" for e in entropies],
            textposition="auto",
        ))
        
        fig.update_layout(
            title="Section Entropy Analysis",
            xaxis_title="PE Section",
            yaxis_title="Entropy (bits)",
            height=400,
            yaxis={"range": [0, 8.5]},
        )
        
        # Add threshold line
        fig.add_hline(y=7.5, line_dash="dash", line_color="red", annotation_text="High entropy threshold")
        
        return fig
    
    @staticmethod
    def create_mitre_tactic_chart(techniques: List[Dict[str, Any]]) -> go.Figure:
        """Create a chart of MITRE tactics."""
        if not techniques:
            return go.Figure()
        
        # Group by tactic
        tactics = {}
        for tech in techniques:
            tactic = tech.get("tactic", "Unknown")
            tactics[tactic] = tactics.get(tactic, 0) + 1
        
        sorted_tactics = sorted(tactics.items(), key=lambda x: x[1], reverse=True)
        tactic_names = [t[0] for t in sorted_tactics]
        counts = [t[1] for t in sorted_tactics]
        
        fig = go.Figure(data=go.Bar(
            x=tactic_names,
            y=counts,
            marker={"color": VisualizationEngine.COLORS["primary"]},
            text=counts,
            textposition="auto",
        ))
        
        fig.update_layout(
            title="MITRE ATT&CK Tactics Distribution",
            xaxis_title="Tactic",
            yaxis_title="Technique Count",
            height=400,
        )
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    @staticmethod
    def create_comparison_radar(
        sample1_behaviors: List[Dict],
        sample2_behaviors: List[Dict]
    ) -> go.Figure:
        """Create a radar chart comparing two samples."""
        categories = ["Dropper", "Downloader", "Injector", "Keylogger", "Ransomware", "Rootkit"]
        
        sample1_scores = []
        sample2_scores = []
        
        for category in categories:
            s1_score = next((b.get("confidence", 0) * 100 for b in sample1_behaviors 
                           if category.lower() in b.get("name", "").lower()), 0)
            s2_score = next((b.get("confidence", 0) * 100 for b in sample2_behaviors 
                           if category.lower() in b.get("name", "").lower()), 0)
            
            sample1_scores.append(s1_score)
            sample2_scores.append(s2_score)
        
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=sample1_scores,
                theta=categories,
                fill="toself",
                name="Sample 1",
                marker={"color": VisualizationEngine.COLORS["primary"]},
            ),
            go.Scatterpolar(
                r=sample2_scores,
                theta=categories,
                fill="toself",
                name="Sample 2",
                marker={"color": VisualizationEngine.COLORS["secondary"]},
            )
        ])
        
        fig.update_layout(
            polar={"radialaxis": {"visible": True, "range": [0, 100]}},
            title="Malware Characteristics Comparison",
            height=500,
        )
        
        return fig
    
    @staticmethod
    def create_risk_factor_breakdown(risk_factors: Dict[str, float]) -> go.Figure:
        """Create a detailed risk factor breakdown chart."""
        if not risk_factors:
            return go.Figure()
        
        factors = sorted(risk_factors.items(), key=lambda x: x[1], reverse=True)
        factor_names = [f[0].replace("_", " ").title()[:20] for f in factors]
        factor_values = [f[1] for f in factors]
        
        fig = go.Figure(data=go.Bar(
            x=factor_names,
            y=factor_values,
            marker={"color": factor_values, "colorscale": "RdYlGn_r"},
            text=[f"{v:.1f}" for v in factor_values],
            textposition="auto",
        ))
        
        fig.update_layout(
            title="Risk Score Factor Contribution",
            xaxis_title="Risk Factor",
            yaxis_title="Score Contribution",
            height=400,
            xaxis={"tickangle": 45},
        )
        
        return fig


class TableGenerator:
    """Generate formatted tables for the dashboard."""
    
    @staticmethod
    def create_analysis_summary_table(analysis: Dict[str, Any]) -> pd.DataFrame:
        """Create a summary table of key analysis details."""
        hashes = analysis.get("hashes", {})
        
        data = {
            "Attribute": [
                "File Name",
                "File Size",
                "MD5 Hash",
                "SHA256 Hash",
                "Is PE",
                "Is Signed",
                "Packer Detected",
                "Entry Point",
            ],
            "Value": [
                analysis.get("file_name", "N/A"),
                f"{analysis.get('file_size_kb', 0):.1f} KB",
                hashes.get("md5", "N/A")[:32] + "...",
                hashes.get("sha256", "N/A")[:32] + "...",
                str(analysis.get("is_pe", False)),
                str(analysis.get("is_signed", False)),
                str(analysis.get("packer_indicators", {}).get("packer_suspected", False)),
                analysis.get("entry_point", "N/A"),
            ]
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_behaviors_table(behaviors: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create a table of detected behaviors."""
        data = []
        
        for behavior in behaviors:
            data.append({
                "Behavior": behavior.get("name", "Unknown"),
                "Category": behavior.get("category", "Unknown"),
                "Confidence": f"{behavior.get('confidence', 0):.0%}",
                "Description": behavior.get("description", "N/A")[:40] + "...",
            })
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_mitre_table(techniques: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create a table of MITRE techniques."""
        data = []
        
        for tech in techniques:
            data.append({
                "ID": tech.get("id", "N/A"),
                "Technique": tech.get("name", "Unknown"),
                "Tactic": tech.get("tactic", "Unknown"),
                "Confidence": f"{tech.get('confidence', 0):.0%}",
            })
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_suspicious_strings_table(strings: List[str], limit: int = 15) -> pd.DataFrame:
        """Create a table of suspicious strings."""
        data = {
            "String": strings[:limit],
            "Type": ["Suspicious"] * min(limit, len(strings)),
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_suspicious_apis_table(apis: List[Dict[str, Any]], limit: int = 15) -> pd.DataFrame:
        """Create a table of suspicious APIs."""
        data = []
        
        for api in apis[:limit]:
            data.append({
                "DLL": api.get("dll", "Unknown"),
                "Function": api.get("function", "Unknown"),
                "Risk Level": api.get("risk_level", "Unknown").upper(),
            })
        
        return pd.DataFrame(data)
