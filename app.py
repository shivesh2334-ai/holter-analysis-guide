import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Philips Holter Monitor Analysis Guide",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00539B;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #00539B;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .task-card {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00539B;
        margin-bottom: 20px;
    }
    .tip-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🫀 Philips Holter 1810 Series Analysis Guide</div>', unsafe_allow_html=True)
st.markdown("**Comprehensive guide for cardiac monitoring analysis using Philips Holter 2010 Plus/1810 Series**")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Analysis Task:",
    [
        "🏠 Home",
        "🔍 Quick Task Finder",
        "💓 Atrial Fibrillation Detection",
        "⚡ Arrhythmia Analysis",
        "📊 ST Segment Analysis",
        "🔋 Pacemaker Analysis",
        "📈 HRV Analysis",
        "📝 Report Generation",
        "⚙️ Settings & Rules",
        "🎓 Scanning Modes",
        "📚 Reference Guide"
    ]
)

# Main content based on selection
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Quick Access")
        st.info("**Most Common Tasks:**")
        st.markdown("""
        - Detecting AF → Use **Rules** Tab
        - Reviewing Events → Use **Events** Tab
        - Creating Reports → Use **Report** Tab
        - Measuring Intervals → Use **Caliper** Tool
        """)
    
    with col2:
        st.markdown("### 🔧 Main Toolbar Functions")
        st.success("**Available Tabs:**")
        st.markdown("""
        - **Display**: Main viewing interface
        - **SO**: Strip Overview
        - **Class**: Event classification
        - **Detail**: Detailed event analysis
        - **Review**: Recording review
        - **Events**: Event management
        """)
    
    with col3:
        st.markdown("### 📖 About This App")
        st.warning("**Purpose:**")
        st.markdown("""
        This guide helps clinicians efficiently use the Philips Holter 1810 Series for:
        - Accurate arrhythmia detection
        - Proper software configuration
        - Report generation
        - Clinical decision support
        """)
    
    st.markdown("---")
    
    # System Overview
    st.markdown('<div class="sub-header">System Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🖥️ Software Capabilities")
        st.markdown("""
        The Philips Zymed Holter 2010 Plus / 1810 Series provides:
        - **Automatic Arrhythmia Detection**: Atrial ectopy, AF, atrial tachycardia/bradycardia
        - **Advanced Analysis**: HRV, ST segment, pacemaker analysis
        - **Multiple Scanning Modes**: Page, QuickScan, Retrospective, Superimposition
        - **12-Lead ECG Generation**: Using EASI hookup configuration
        - **Customizable Reports**: With full editing capabilities
        """)
    
    with col2:
        st.markdown("#### 📊 Key Features")
        st.markdown("""
        - **Recording Duration**: Up to 7 days continuous monitoring
        - **Sampling Rate**: 200 Hz for high-quality data
        - **Channel Support**: 3 channels (Ch1, Ch2, Ch3)
        - **Export Options**: PDF, HL7, ZPT Report Viewer
        - **Network Integration**: Compatible with EMR/HIS systems
        """)

elif page == "🔍 Quick Task Finder":
    st.markdown('<div class="sub-header">Quick Task Finder</div>', unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("🔎 Search for a task or arrhythmia type:", placeholder="e.g., detect AF, measure QT interval, generate report")
    
    # Task database
    tasks = {
        "Detect Atrial Fibrillation": {
            "tabs": ["Rules", "Events", "Detail"],
            "steps": [
                "Open the **Rules** menu from the toolbar",
                "Adjust AF detection settings: Number of beats analyzed and R-R interval variability",
                "Set Auto Stops to stop at AF episodes",
                "Start the scan in **Retrospective** or **Page** mode",
                "Review detected AF episodes in **Events** tab",
                "Verify episodes in **Detail** view with all 12 leads"
            ],
            "tips": "Use R-R interval variability to increase sensitivity for paroxysmal AF"
        },
        "Measure QT Interval": {
            "tabs": ["Caliper", "Display"],
            "steps": [
                "Select **Caliper** tool from toolbar",
                "Navigate to a clear QRS complex in **Display** view",
                "Place first caliper at Q wave onset",
                "Place second caliper at T wave end",
                "Read measurement displayed on screen"
            ],
            "tips": "Use lead II or V5 for best QT measurements"
        },
        "Generate Report": {
            "tabs": ["Report", "Review"],
            "steps": [
                "Complete the scan and event review",
                "Click **Report** tab",
                "Select report template",
                "Review automatically generated content",
                "Add physician comments if needed",
                "Export as PDF, HL7, or ZPT format"
            ],
            "tips": "Reports can be edited after generation using ZPT Report Viewer"
        },
        "Classify Arrhythmias": {
            "tabs": ["Class", "Events", "Detail"],
            "steps": [
                "Open **Class** tab to view all detected events",
                "Review event categories (VPB, APB, AF, etc.)",
                "Use **Detail** view to examine individual beats",
                "Reclassify events if needed",
                "Save classification changes"
            ],
            "tips": "Use keyboard shortcuts for faster classification"
        },
        "ST Segment Analysis": {
            "tabs": ["ST", "Graph", "Review"],
            "steps": [
                "Click **ST** tab in toolbar",
                "Set ST measurement points (J-point, ST80)",
                "Define ST deviation thresholds",
                "Review ST trend graphs in **Graph** tab",
                "Correlate ST changes with patient diary/symptoms"
            ],
            "tips": "ST analysis is most reliable in leads with stable baseline"
        },
        "Pacemaker Analysis": {
            "tabs": ["Detail", "Events", "Settings"],
            "steps": [
                "Enable pacemaker detection in **Settings**",
                "Adjust pacemaker sensitivity (attenuation/augmentation)",
                "Review pacemaker spikes in **Detail** view",
                "Check for capture and sensing failures",
                "Generate pacemaker-specific report sections"
            ],
            "tips": "Adjust sensitivity: attenuate for unipolar, augment for bipolar"
        },
        "Review Recording Quality": {
            "tabs": ["Display", "Review", "SO"],
            "steps": [
                "Open **SO** (Strip Overview) for quick scan",
                "Look for artifact, noise, or dropout sections",
                "Use **Display** to examine questionable areas",
                "Mark poor quality sections",
                "Note quality issues in report comments"
            ],
            "tips": "First 30 minutes provide algorithm adjustment opportunity"
        },
        "Export Data": {
            "tabs": ["File", "Report"],
            "steps": [
                "Complete analysis and report generation",
                "Go to File menu → Export",
                "Choose export format (PDF, HL7, ZPT)",
                "Configure destination (EMR, network folder)",
                "Verify export completion"
            ],
            "tips": "HL7 export requires prior configuration of output settings"
        }
    }
    
    if search_query:
        # Filter tasks based on search
        filtered_tasks = {k: v for k, v in tasks.items() if search_query.lower() in k.lower() or 
                         any(search_query.lower() in step.lower() for step in v["steps"])}
        
        if filtered_tasks:
            st.success(f"Found {len(filtered_tasks)} matching task(s)")
            for task_name, task_info in filtered_tasks.items():
                with st.expander(f"📋 {task_name}", expanded=True):
                    st.markdown(f"**Required Tabs:** {', '.join(task_info['tabs'])}")
                    st.markdown("**Steps:**")
                    for i, step in enumerate(task_info['steps'], 1):
                        st.markdown(f"{i}. {step}")
                    st.info(f"💡 **Tip:** {task_info['tips']}")
        else:
            st.warning("No matching tasks found. Try different keywords.")
    else:
        st.info("👆 Enter a task or arrhythmia type in the search box above")
        
        # Show all tasks
        st.markdown("### 📚 All Available Tasks")
        for task_name, task_info in tasks.items():
            with st.expander(f"📋 {task_name}"):
                st.markdown(f"**Required Tabs:** {', '.join(task_info['tabs'])}")
                st.markdown("**Steps:**")
                for i, step in enumerate(task_info['steps'], 1):
                    st.markdown(f"{i}. {step}")
                st.info(f"💡 **Tip:** {task_info['tips']}")

else:
    st.info(f"Select '{page}' to view detailed guidance on this topic.")
    st.markdown("""
    ### Coming Soon
    
    This section contains comprehensive information about:
    - Step-by-step procedures
    - Best practices
    - Configuration settings
    - Common scenarios
    - Troubleshooting tips
    
    Use the sidebar to navigate between different analysis tasks.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Philips Holter 1810 Series Analysis Guide</strong></p>
    <p>For educational and reference purposes. Always consult official Philips documentation and supervising physicians.</p>
    <p>Version 1.0 | Updated January 2026</p>
</div>
""", unsafe_allow_html=True)
  
