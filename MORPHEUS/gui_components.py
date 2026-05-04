"""
MORPHEUS-X Modern GUI Enhancement
Layout and component utilities for modern design
"""

import streamlit as st


class ModernComponents:
    """Collection of modern UI components for Streamlit."""
    
    @staticmethod
    def header_section(title: str, subtitle: str = "", icon: str = ""):
        """Create a modern header section with gradient background."""
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 12px; padding: 40px; color: white; text-align: center; 
                        margin-bottom: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
                <h2 style="margin: 0 0 10px 0; color: white; border: none;">{icon} {title}</h2>
                <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">{subtitle}</p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def info_card(title: str, content: str, icon: str = "ℹ️", color: str = "#667eea"):
        """Create an information card with border and icon."""
        st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
                        border-left: 5px solid {color}; transition: all 0.3s ease;">
                <h4 style="margin-top: 0; color: {color};">{icon} {title}</h4>
                <p style="margin: 0;">{content}</p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def stat_card(label: str, value: str, icon: str = ""):
        """Create a modern statistics card."""
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 12px; padding: 25px; color: white; 
                        text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        transition: all 0.3s ease;">
                <p style="margin: 0 0 10px 0; opacity: 0.9; font-size: 0.9em;">{icon} {label}</p>
                <h3 style="margin: 0; font-size: 2em;">{value}</h3>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def alert_box(message: str, alert_type: str = "info"):
        """Create a modern alert box."""
        colors = {
            "info": ("#e3f2fd", "#2196F3", "ℹ️"),
            "success": ("#e8f5e9", "#4CAF50", "✅"),
            "warning": ("#fff3e0", "#FF9800", "⚠️"),
            "error": ("#ffebee", "#F44336", "❌"),
        }
        
        bg_color, border_color, icon = colors.get(alert_type, colors["info"])
        
        st.markdown(f"""
            <div style="background-color: {bg_color}; border-left: 5px solid {border_color}; 
                        border-radius: 8px; padding: 15px; margin: 10px 0;">
                <p style="margin: 0; color: #333; font-weight: 500;">
                    {icon} {message}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def section_divider(text: str = ""):
        """Create a modern section divider."""
        if text:
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin: 30px 0;">
                    <div style="flex: 1; height: 2px; background: linear-gradient(90deg, transparent, #667eea, transparent);"></div>
                    <span style="padding: 0 15px; color: #667eea; font-weight: 600; font-size: 0.95em;">{text}</span>
                    <div style="flex: 1; height: 2px; background: linear-gradient(90deg, transparent, #667eea, transparent);"></div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="height: 2px; background: linear-gradient(90deg, transparent, #667eea, transparent); margin: 25px 0;"></div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def feature_grid(features: list):
        """Create a grid of feature cards."""
        cols = st.columns(min(3, len(features)))
        for idx, (title, content, icon) in enumerate(features):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div style="background: white; border-radius: 12px; padding: 25px; 
                                box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 5px solid #667eea;
                                transition: all 0.3s ease; margin-bottom: 20px;">
                        <h4 style="margin-top: 0; color: #667eea;">{icon} {title}</h4>
                        <p style="margin: 0; color: #666;">{content}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def progress_bar(label: str, value: int, max_value: int = 100, color: str = "#667eea"):
        """Create a modern progress bar."""
        percentage = (value / max_value) * 100
        st.markdown(f"""
            <div style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-weight: 600; color: #2c3e50;">{label}</span>
                    <span style="color: #7f8c8d;">{value}/{max_value}</span>
                </div>
                <div style="background: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {color} 0%, {color}dd 100%); 
                                width: {percentage}%; height: 100%; transition: width 0.3s ease;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def badge(text: str, badge_type: str = "primary"):
        """Create a modern badge."""
        colors = {
            "primary": ("#667eea", "#e8eef7"),
            "success": ("#00d4aa", "#e6f9f5"),
            "warning": ("#ffa502", "#fff3e0"),
            "danger": ("#ff6b6b", "#ffe6e6"),
            "info": ("#4d96ff", "#e3f2fd"),
        }
        
        text_color, bg_color = colors.get(badge_type, colors["primary"])
        
        return f"""
            <span style="display: inline-block; background-color: {bg_color}; color: {text_color}; 
                         padding: 6px 12px; border-radius: 20px; font-size: 0.85em; 
                         font-weight: 600; margin-right: 8px; border: 1px solid {text_color};">
                {text}
            </span>
        """
    
    @staticmethod
    def code_block(code: str, language: str = "python"):
        """Create a modern code block."""
        st.markdown(f"""
            <pre style="background: #2c3e50; color: #ecf0f1; padding: 20px; border-radius: 8px; 
                        overflow-x: auto; font-family: 'Courier New', monospace;">
                <code>{code}</code>
            </pre>
        """, unsafe_allow_html=True)


class ModernLayouts:
    """Modern layout patterns for Streamlit apps."""
    
    @staticmethod
    def two_column_layout(left_title: str, left_content: callable, right_title: str, right_content: callable):
        """Create a two-column layout with modern styling."""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 25px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;">
                    <h3 style="margin-top: 0; color: #667eea;">{left_title}</h3>
            """, unsafe_allow_html=True)
            left_content()
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 25px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;">
                    <h3 style="margin-top: 0; color: #667eea;">{right_title}</h3>
            """, unsafe_allow_html=True)
            right_content()
            st.markdown("</div>", unsafe_allow_html=True)
    
    @staticmethod
    def tab_layout(tabs: dict):
        """Create modern tabs layout."""
        tab_list = st.tabs(list(tabs.keys()))
        
        for tab, (tab_name, tab_content) in zip(tab_list, tabs.items()):
            with tab:
                tab_content()


# Color theme definitions
class ColorTheme:
    """Modern color themes for the application."""
    
    PRIMARY = "#667eea"
    PRIMARY_DARK = "#5568d3"
    SECONDARY = "#764ba2"
    ACCENT = "#f093fb"
    SUCCESS = "#00d4aa"
    WARNING = "#ffa502"
    DANGER = "#ff6b6b"
    INFO = "#4d96ff"
    
    LIGHT_BG = "#f8f9fa"
    WHITE = "#ffffff"
    BORDER = "#e0e0e0"
    TEXT_DARK = "#2c3e50"
    TEXT_LIGHT = "#7f8c8d"
    
    # Gradients
    PRIMARY_GRADIENT = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    WARM_GRADIENT = "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"
    COOL_GRADIENT = "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)"


# Helper functions for common patterns
def modern_metric_row(metrics: list):
    """Display multiple modern metric cards in a row."""
    cols = st.columns(len(metrics))
    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.metric(label, value)


def modern_alert(message: str, alert_type: str = "info"):
    """Display a modern alert message."""
    ModernComponents.alert_box(message, alert_type)


def modern_divider(text: str = ""):
    """Display a modern divider."""
    ModernComponents.section_divider(text)
