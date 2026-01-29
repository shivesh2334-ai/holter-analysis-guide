import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import signal
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Philips Holter Monitor Analysis Guide",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.philips.com/healthcare',
        'Report a bug': 'https://github.com/yourusername/holter-guide/issues',
        'About': """
        # Philips Holter Analysis Guide v2.0
        
        Clinical decision support tool for Philips Holter 1810/2010 Plus systems.
        
        For educational purposes. Always consult official documentation.
        """
    }
)

# Custom CSS with enhanced styling
st.markdown("""
<style>
    /* Main headers */
    .main-header {
        font-size: 2.5rem;
        color: #00539B;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 15px;
        border-bottom: 3px solid #00539B;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        background: linear-gradient(90deg, #00539B, #0083B0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #00539B;
        font-weight: 700;
        margin-top: 1.8rem;
        margin-bottom: 1.2rem;
        padding-left: 15px;
        border-left: 5px solid #00539B;
        background-color: #f8f9fa;
        padding: 12px 20px;
        border-radius: 8px;
    }
    
    .section-header {
        font-size: 1.4rem;
        color: #2c3e50;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding: 8px 15px;
        background: linear-gradient(90deg, #e3f2fd, #f3e5f5);
        border-radius: 5px;
    }
    
    /* Cards and boxes */
    .task-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #00539B;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .task-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .tip-box {
        background: linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffb300;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(255,179,0,0.2);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(244,67,54,0.2);
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(76,175,80,0.2);
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(33,150,243,0.2);
    }
    
    /* Metrics and statistics */
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #00539B;
        transition: all 0.3s;
    }
    
    .metric-box:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Step indicators */
    .step-number {
        display: inline-block;
        background: linear-gradient(135deg, #00539B, #0083B0);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        text-align: center;
        line-height: 32px;
        font-weight: bold;
        margin-right: 15px;
        box-shadow: 0 2px 4px rgba(0,83,155,0.3);
    }
    
    /* Buttons and interactive elements */
    .stButton > button {
        background: linear-gradient(135deg, #00539B, #0083B0);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,83,155,0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00539B, #0083B0);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00539B, #0083B0);
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'role': 'Cardiac Technician',
        'experience': 'Intermediate',
        'theme': 'light',
        'bookmarks': [],
        'recent_searches': [],
        'settings': {
            'auto_save': True,
            'notifications': True,
            'data_privacy': 'standard'
        }
    }

if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = {
        'current_patient': None,
        'recording_duration': None,
        'analysis_started': False,
        'last_export': None
    }

# Header with dynamic content
def display_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">🫀 Philips Holter 1810/2010 Plus Analysis Guide</div>', unsafe_allow_html=True)
        st.markdown(f"**Welcome, {st.session_state.user_data['role']}!** Today is {datetime.now().strftime('%B %d, %Y')}")
    return col1, col2, col3

# Sidebar navigation
def create_sidebar():
    with st.sidebar:
        st.markdown("## 📋 Navigation")
        
        # User profile
        with st.expander("👤 User Profile", expanded=False):
            st.session_state.user_data['role'] = st.selectbox(
                "Role:",
                ["Cardiologist", "Cardiac Technician", "Trainee", "Researcher", "Administrator"]
            )
            st.session_state.user_data['experience'] = st.select_slider(
                "Experience Level:",
                options=["Beginner", "Intermediate", "Advanced", "Expert"]
            )
        
        # Main navigation
        st.markdown("---")
        page_options = [
            "🏠 Home Dashboard",
            "🔍 Quick Task Finder",
            "💓 Atrial Fibrillation Detection",
            "⚡ Arrhythmia Analysis",
            "📊 ST Segment Analysis",
            "🔋 Pacemaker Analysis",
            "📈 HRV Analysis",
            "📝 Report Generation",
            "⚙️ Settings & Rules",
            "🎓 Scanning Modes",
            "📚 Reference Guide",
            "🚨 Troubleshooting",
            "📁 Patient Management",
            "📤 Export Tools"
        ]
        
        selected_page = st.radio(
            "### 📚 Select Page:",
            page_options,
            index=0
        )
        
        # Quick actions
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.analysis_data['analysis_started'] = True
            st.rerun()
        
        if st.button("📊 Sample Report", use_container_width=True):
            generate_sample_report()
        
        if st.button("⚙️ Configure", use_container_width=True):
            st.session_state.user_data['settings']['config_mode'] = True
        
        # Bookmarks
        if st.session_state.user_data['bookmarks']:
            st.markdown("---")
            st.markdown("### 🔖 Bookmarks")
            for bookmark in st.session_state.user_data['bookmarks'][:5]:
                if st.button(f"📍 {bookmark}", key=f"bm_{bookmark}", use_container_width=True):
                    st.session_state.current_page = bookmark
        
        # System status
        st.markdown("---")
        st.markdown("### 📊 System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tasks", "12", "3 new")
        with col2:
            st.metric("Patients", "24", "+2")
        
        return selected_page

# Sample data generation functions
def generate_sample_ecg_data():
    """Generate synthetic ECG data for demonstration"""
    fs = 200  # Sampling frequency
    t = np.arange(0, 10, 1/fs)
    
    # Generate ECG-like signal
    ecg = 0.5 * np.sin(2 * np.pi * 1 * t)  # P wave
    ecg += 1.2 * signal.sawtooth(2 * np.pi * 5 * t, 0.5)  # QRS complex
    ecg += 0.3 * np.sin(2 * np.pi * 0.5 * t + np.pi/4)  # T wave
    ecg += 0.1 * np.random.randn(len(t))  # Noise
    
    return pd.DataFrame({
        'Time (s)': t,
        'Lead I (mV)': ecg,
        'Lead II (mV)': ecg * 0.8 + 0.1 * np.random.randn(len(t)),
        'Lead V5 (mV)': ecg * 1.1 + 0.15 * np.random.randn(len(t))
    })

def generate_sample_patient_data():
    """Generate sample patient data"""
    patients = []
    for i in range(10):
        patients.append({
            'ID': f'PAT-{1000 + i}',
            'Name': f'Patient {i+1}',
            'Age': np.random.randint(40, 85),
            'Gender': np.random.choice(['M', 'F']),
            'Recording Duration': f'{np.random.randint(24, 168)} hours',
            'AF Burden': f'{np.random.uniform(0, 30):.1f}%',
            'VPB Count': np.random.randint(0, 5000),
            'Status': np.random.choice(['Completed', 'In Progress', 'Pending Review']),
            'Last Updated': f'{np.random.randint(1, 30)} days ago'
        })
    return pd.DataFrame(patients)

def generate_sample_report():
    """Generate a sample report"""
    report_data = {
        'Patient Information': {
            'Name': 'John Doe',
            'ID': 'PAT-2024-001',
            'Age': 65,
            'Gender': 'M',
            'Recording Date': '2024-01-15',
            'Duration': '48 hours'
        },
        'Summary Statistics': {
            'Total Beats': '112,450',
            'Average HR': '78 bpm',
            'Maximum HR': '142 bpm',
            'Minimum HR': '48 bpm',
            'AF Burden': '12.5%',
            'VPB Count': '1,245',
            'APB Count': '567'
        },
        'Diagnostic Findings': {
            'Primary Rhythm': 'Sinus rhythm with intermittent AF',
            'AF Episodes': '8 episodes (longest: 4.5 hours)',
            'Ventricular Arrhythmias': 'Occasional VPBs, no VT',
            'ST Analysis': 'No significant ST deviation',
            'HRV': 'Reduced SDNN (86 ms)',
            'Clinical Impression': 'Paroxysmal atrial fibrillation'
        }
    }
    return report_data

# Main page functions
def home_dashboard():
    """Home dashboard page"""
    display_header()
    
    # Dashboard metrics
    st.markdown('<div class="sub-header">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h3>24</h3>
            <p>Active Patients</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3>8</h3>
            <p>Pending Reviews</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h3>94%</h3>
            <p>Analysis Complete</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-box">
            <h3>12</h3>
            <p>Tasks Today</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start section
    st.markdown('<div class="section-header">🚀 Quick Start</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("### 📁 Import Data\n\nLoad patient Holter data", use_container_width=True):
            st.info("Data import initiated...")
    with col2:
        if st.button("### 🔍 Quick Analysis\n\nRun automated analysis", use_container_width=True):
            st.info("Starting analysis...")
    with col3:
        if st.button("### 📄 Generate Report\n\nCreate clinical report", use_container_width=True):
            st.info("Report generation started...")
    
    # Recent patients
    st.markdown('<div class="section-header">👥 Recent Patients</div>', unsafe_allow_html=True)
    patient_df = generate_sample_patient_data()
    st.dataframe(patient_df.head(5), use_container_width=True, hide_index=True)
    
    # System status
    st.markdown('<div class="section-header">🖥️ System Status</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Software Version:** 2.0.1")
        st.info("**Database:** Connected (24.7 GB used)")
        st.info("**Last Backup:** Today 02:00 AM")
    with col2:
        st.info("**Memory Usage:** 68%")
        st.info("**CPU Load:** 42%")
        st.info("**Network:** Online")
    
    # Quick tips
    st.markdown('<div class="section-header">💡 Quick Tips</div>', unsafe_allow_html=True)
    
    tips = [
        "Use **Retrospective mode** for comprehensive AF detection",
        "Always verify automated detections with manual review",
        "Check patient diary entries when reviewing events",
        "Export reports in both PDF and HL7 formats",
        "Regularly backup your analysis database"
    ]
    
    for tip in tips:
        st.markdown(f"• {tip}")

def quick_task_finder():
    """Quick task finder page"""
    st.markdown('<div class="sub-header">🔍 Quick Task Finder</div>', unsafe_allow_html=True)
    
    # Search and filter
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input("", placeholder="Search for tasks, arrhythmias, or procedures...", 
                                   help="Type keywords like 'AF detection', 'QT interval', or 'export report'")
    with col2:
        category = st.selectbox("Category", ["All", "Detection", "Measurement", "Analysis", "Reporting", "Export"])
    with col3:
        difficulty = st.selectbox("Level", ["All", "Beginner", "Intermediate", "Advanced"])
    
    # Tasks database
    tasks_db = {
        "Detect Atrial Fibrillation": {
            "category": "Detection",
            "difficulty": "Intermediate",
            "time": "10-15 min",
            "priority": "High",
            "tabs": ["Rules", "Events", "Detail"],
            "steps": [
                "Navigate to **Rules** → AF Detection settings",
                "Set R-R variability threshold to 12%",
                "Configure minimum episode duration (30 seconds)",
                "Start scan in Retrospective mode",
                "Review purple-highlighted AF episodes in Events tab",
                "Verify in Detail view with all 12 leads"
            ],
            "tips": [
                "Use R-R interval tachogram for visual confirmation",
                "Check for associated symptoms in patient diary",
                "Consider CHA₂DS₂-VASc score for stroke risk assessment"
            ]
        },
        "Measure QT Interval": {
            "category": "Measurement",
            "difficulty": "Beginner",
            "time": "5 min",
            "priority": "Medium",
            "tabs": ["Caliper", "Display"],
            "steps": [
                "Select Caliper tool (press 'C')",
                "Navigate to clear QRS complex in Display view",
                "Place first caliper at Q wave onset",
                "Place second caliper at T wave end",
                "Record measurement from on-screen display",
                "Calculate QTc using Bazett's formula"
            ],
            "tips": [
                "Measure in lead II or V5 for best accuracy",
                "Average measurements from 3 consecutive beats",
                "Avoid measuring in leads with U waves"
            ]
        }
    }
    
    # Display tasks
    if search_query:
        filtered_tasks = {k: v for k, v in tasks_db.items() 
                         if search_query.lower() in k.lower()}
    else:
        filtered_tasks = tasks_db
    
    for task_name, task_info in filtered_tasks.items():
        with st.expander(f"📋 {task_name}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Category:** {task_info['category']}")
                st.markdown(f"**Difficulty:** {task_info['difficulty']}")
            with col2:
                st.markdown(f"**Time:** {task_info['time']}")
                st.markdown(f"**Priority:** {task_info['priority']}")
            with col3:
                st.markdown(f"**Tabs:** {', '.join(task_info['tabs'])}")
                
                # Bookmark button
                if st.button("🔖 Bookmark", key=f"book_{task_name}"):
                    if task_name not in st.session_state.user_data['bookmarks']:
                        st.session_state.user_data['bookmarks'].append(task_name)
                        st.success("Bookmarked!")
            
            st.markdown("**Steps:**")
            for i, step in enumerate(task_info['steps'], 1):
                st.markdown(f'<div class="step-number">{i}</div> {step}', unsafe_allow_html=True)
            
            st.markdown("**Tips:**")
            for tip in task_info['tips']:
                st.markdown(f"• {tip}")

def af_detection_page():
    """Atrial Fibrillation Detection page"""
    st.markdown('<div class="sub-header">💓 Atrial Fibrillation Detection</div>', unsafe_allow_html=True)
    
    # Configuration section
    st.markdown('<div class="section-header">⚙️ Configuration Settings</div>', unsafe_allow_html=True)
    
    with st.form("af_config"):
        col1, col2, col3 = st.columns(3)
        with col1:
            min_beats = st.slider("Minimum beats", 20, 100, 30, 
                                help="Number of consecutive beats analyzed for AF")
            sensitivity = st.select_slider("Sensitivity", 
                                         options=["Low", "Medium", "High", "Very High"],
                                         value="High")
        with col2:
            rr_var = st.slider("R-R variability (%)", 5, 30, 12,
                             help="Minimum R-R interval variability required")
            min_duration = st.slider("Min duration (seconds)", 10, 120, 30)
        with col3:
            auto_stop = st.checkbox("Auto-stop at AF episodes", True)
            require_symptoms = st.checkbox("Require symptom correlation", False)
        
        if st.form_submit_button("💾 Save Configuration", use_container_width=True):
            st.success("Configuration saved successfully!")
    
    # Live demo section
    st.markdown('<div class="section-header">📊 Live Demo</div>', unsafe_allow_html=True)
    
    # Generate sample ECG data
    ecg_data = generate_sample_ecg_data()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Create ECG plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ecg_data['Time (s)'], 
                                y=ecg_data['Lead II (mV)'],
                                mode='lines',
                                name='Lead II',
                                line=dict(color='#00539B', width=2)))
        
        # Add AF annotation
        fig.add_vrect(x0=3, x1=7, 
                     fillcolor="rgba(255,0,0,0.2)", 
                     line_width=0,
                     annotation_text="Detected AF Episode",
                     annotation_position="top left")
        
        fig.update_layout(
            title="ECG Signal with AF Detection",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude (mV)",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Detection Statistics")
        st.metric("AF Episodes", "3", "+1")
        st.metric("Total AF Duration", "2.5 hours")
        st.metric("AF Burden", "5.2%")
        st.metric("Longest Episode", "1.2 hours")
    
    # AF Classification
    st.markdown('<div class="section-header">📈 AF Classification</div>', unsafe_allow_html=True)
    
    af_types = pd.DataFrame({
        'Type': ['Paroxysmal AF', 'Persistent AF', 'Long-standing Persistent AF', 'Permanent AF'],
        'Duration': ['<7 days', '>7 days', '>1 year', 'Accepted'],
        'Rate Control': ['Beta-blockers', 'Beta-blockers, CCB', 'Digoxin ± BB', 'All options'],
        'Rhythm Control': ['Flecainide, Propafenone', 'Dofetilide, Amiodarone', 'Amiodarone', 'Not attempted'],
        'Ablation': ['Consider early', 'First-line option', 'Consider if symptomatic', 'Not indicated']
    })
    
    st.dataframe(af_types, use_container_width=True, hide_index=True)

def report_generation_page():
    """Report Generation page"""
    st.markdown('<div class="sub-header">📝 Report Generation</div>', unsafe_allow_html=True)
    
    # Report configuration
    st.markdown('<div class="section-header">⚙️ Report Configuration</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        report_type = st.selectbox("Report Type", 
                                 ["Standard", "Comprehensive", "Summary", "Pacemaker", "Research"])
        include_graphs = st.checkbox("Include Graphs", True)
        anonymize = st.checkbox("Anonymize Data", False)
    with col2:
        export_format = st.multiselect("Export Format", 
                                     ["PDF", "HL7", "CSV", "ZPT", "HTML"],
                                     default=["PDF", "HL7"])
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
    with col3:
        physician_name = st.text_input("Physician Name", "Dr. Smith")
        clinic_name = st.text_input("Clinic Name", "Cardiac Care Center")
    
    # Report content
    st.markdown('<div class="section-header">📋 Report Content</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Patient Info", "Findings", "Statistics", "Graphs", "Comments"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Patient ID", "PAT-2024-001")
            patient_name = st.text_input("Patient Name", "John Doe")
            patient_age = st.number_input("Age", 18, 120, 65)
        with col2:
            patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            recording_date = st.date_input("Recording Date")
            duration = st.selectbox("Duration", ["24h", "48h", "72h", "7 days"])
    
    with tabs[1]:
        findings = st.text_area("Clinical Findings", 
                              "Sinus rhythm with intermittent atrial fibrillation. Occasional VPBs. No significant ST segment changes. Normal HRV parameters.", 
                              height=150)
        diagnosis = st.text_input("Diagnosis", "Paroxysmal Atrial Fibrillation")
        recommendations = st.text_area("Recommendations", 
                                     "1. Start anticoagulation based on CHA₂DS₂-VASc score\n2. Consider rate control with beta-blocker\n3. Follow-up in 3 months", 
                                     height=100)
    
    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Total Beats", 0, 1000000, 112450)
            st.number_input("Average HR", 30, 200, 78)
            st.number_input("Maximum HR", 60, 250, 142)
        with col2:
            st.number_input("Minimum HR", 30, 100, 48)
            st.number_input("AF Burden (%)", 0.0, 100.0, 12.5)
            st.number_input("VPB Count", 0, 10000, 1245)
    
    with tabs[3]:
        graph_options = st.multiselect("Include Graphs", 
                                     ["HR Trend", "AF Burden", "ST Segment", "HRV", "Event Distribution"],
                                     default=["HR Trend", "AF Burden"])
        
        # Generate sample plot
        if "HR Trend" in graph_options:
            fig = px.line(x=pd.date_range(start='2024-01-15', periods=48, freq='H'),
                         y=np.random.randn(48).cumsum() + 70,
                         title="Heart Rate Trend (24 hours)")
            fig.update_layout(xaxis_title="Time", yaxis_title="Heart Rate (bpm)")
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[4]:
        additional_comments = st.text_area("Additional Comments", 
                                         "Patient experienced palpitations during AF episodes. No chest pain reported.", 
                                         height=100)
        quality_rating = st.slider("Recording Quality", 1, 5, 4)
    
    # Generate report button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Generate Report", use_container_width=True):
            with st.spinner("Generating report..."):
                # Simulate report generation
                import time
                time.sleep(2)
                
                # Show success message
                st.success("✅ Report generated successfully!")
                
                # Provide download link
                report_data = generate_sample_report()
                st.download_button(
                    label="📥 Download Report (PDF)",
                    data="Sample report content would be here",
                    file_name=f"Holter_Report_{patient_id}.pdf",
                    mime="application/pdf"
                )

# Main application logic
def main():
    """Main application function"""
    
    # Display header
    display_header()
    
    # Create sidebar and get selected page
    selected_page = create_sidebar()
    
    # Page routing
    if selected_page == "🏠 Home Dashboard":
        home_dashboard()
    elif selected_page == "🔍 Quick Task Finder":
        quick_task_finder()
    elif selected_page == "💓 Atrial Fibrillation Detection":
        af_detection_page()
    elif selected_page == "📝 Report Generation":
        report_generation_page()
    elif selected_page == "📚 Reference Guide":
        st.markdown('<div class="sub-header">📚 Reference Guide</div>', unsafe_allow_html=True)
        # Add reference guide content here
    else:
        # Placeholder for other pages
        st.markdown(f'<div class="sub-header">{selected_page}</div>', unsafe_allow_html=True)
        st.info(f"Page '{selected_page}' is under development. Check back soon!")
    
    # Footer
    display_footer()

def display_footer():
    """Display application footer"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p><strong>Philips Holter 1810/2010 Plus Analysis Guide v2.0</strong></p>
            <p>For clinical reference and educational purposes only.</p>
            <p>Always consult official Philips documentation and supervising physicians.</p>
            <p>© 2024 Philips Healthcare • Support: support@philips.com</p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
