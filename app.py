import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import sys

# Try to import optional visualization libraries with graceful fallbacks
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not available - using basic charts")

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Philips Holter Monitor Analysis Guide",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (simplified version)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00539B;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 10px;
        border-bottom: 3px solid #00539B;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #00539B;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-left: 10px;
        border-left: 4px solid #00539B;
    }
    .task-card {
        background: linear-gradient(135deg, #f5f9ff 0%, #e6f0ff 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00539B;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .tip-box {
        background-color: #fff8e1;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffb300;
        margin: 15px 0;
    }
    .warning-box {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #f44336;
        margin: 15px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4caf50;
        margin: 15px 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2196f3;
        margin: 15px 0;
    }
    .step-number {
        display: inline-block;
        background-color: #00539B;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'role': 'Cardiac Technician',
        'bookmarks': []
    }

# Helper functions for data generation
def generate_sample_ecg_data():
    """Generate synthetic ECG data for demonstration"""
    fs = 200  # Sampling frequency
    t = np.arange(0, 10, 1/fs)
    
    # Generate ECG-like signal using numpy
    ecg = 0.5 * np.sin(2 * np.pi * 1 * t)  # P wave
    ecg += 1.2 * np.sin(2 * np.pi * 5 * t + np.pi/2)  # QRS complex
    ecg += 0.3 * np.sin(2 * np.pi * 0.5 * t + np.pi/4)  # T wave
    ecg += 0.1 * np.random.randn(len(t))  # Noise
    
    return pd.DataFrame({
        'Time (s)': t,
        'Lead II (mV)': ecg
    })

def generate_sample_patient_data():
    """Generate sample patient data"""
    patients = []
    for i in range(5):
        patients.append({
            'ID': f'PAT-{1000 + i}',
            'Name': f'Patient {i+1}',
            'Age': np.random.randint(40, 85),
            'Gender': np.random.choice(['M', 'F']),
            'Recording Duration': f'{np.random.randint(24, 168)} hours',
            'Status': np.random.choice(['Completed', 'In Progress', 'Pending Review'])
        })
    return pd.DataFrame(patients)

def create_simple_plot(data):
    """Create a simple plot using Streamlit's native chart or fallback"""
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Time (s)'], 
                                y=data['Lead II (mV)'],
                                mode='lines',
                                name='Lead II',
                                line=dict(color='#00539B', width=2)))
        fig.update_layout(
            title="ECG Signal",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude (mV)",
            height=400
        )
        return fig
    else:
        # Use Streamlit's native line chart
        chart_data = pd.DataFrame({
            'Time (s)': data['Time (s)'],
            'Lead II (mV)': data['Lead II (mV)']
        })
        return chart_data

# Main application
def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">🫀 Philips Holter 1810/2010 Plus Analysis Guide</div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📋 Navigation")
        
        # User profile
        st.session_state.user_data['role'] = st.selectbox(
            "Select your role:",
            ["Cardiologist", "Cardiac Technician", "Trainee", "Researcher"]
        )
        
        # Main navigation
        st.markdown("---")
        page = st.radio(
            "Select Analysis Task:",
            [
                "🏠 Home Dashboard",
                "🔍 Quick Task Finder",
                "💓 Atrial Fibrillation Detection",
                "⚡ Arrhythmia Analysis",
                "📊 ST Segment Analysis",
                "🔋 Pacemaker Analysis",
                "📈 HRV Analysis",
                "📝 Report Generation",
                "⚙️ Settings & Rules",
                "📚 Reference Guide"
            ]
        )
        
        # Quick metrics
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tasks", "12")
        with col2:
            st.metric("Procedures", "8")
    
    # Page content
    if page == "🏠 Home Dashboard":
        home_dashboard()
    elif page == "🔍 Quick Task Finder":
        quick_task_finder()
    elif page == "💓 Atrial Fibrillation Detection":
        af_detection_page()
    elif page == "📝 Report Generation":
        report_generation_page()
    elif page == "📚 Reference Guide":
        reference_guide_page()
    else:
        st.info(f"**{page}** - This section is under development")
    
    # Footer
    display_footer()

def home_dashboard():
    """Home dashboard page"""
    st.markdown(f"### 👋 Welcome, {st.session_state.user_data['role']}!")
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Patients", "24", "+3")
    with col2:
        st.metric("Pending Reviews", "8", "-2")
    with col3:
        st.metric("Analysis Complete", "94%", "+4%")
    with col4:
        st.metric("Tasks Today", "12", "3 new")
    
    # Quick start section
    st.markdown('<div class="sub-header">🚀 Quick Start</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📁 Import Data", use_container_width=True):
            st.info("Data import initiated...")
    with col2:
        if st.button("🔍 Quick Analysis", use_container_width=True):
            st.info("Starting analysis...")
    with col3:
        if st.button("📄 Generate Report", use_container_width=True):
            st.info("Report generation started...")
    
    # Recent patients
    st.markdown('<div class="sub-header">👥 Recent Patients</div>', unsafe_allow_html=True)
    patient_df = generate_sample_patient_data()
    st.dataframe(patient_df, use_container_width=True, hide_index=True)
    
    # System status
    st.markdown('<div class="sub-header">🖥️ System Status</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Software Version:** 2.0.0")
        st.info("**Last Backup:** Today 02:00 AM")
    with col2:
        st.info("**Memory Usage:** 68%")
        st.info("**Network:** Online")
    
    # Quick tips
    st.markdown("""
    <div class="tip-box">
    <strong>💡 Quick Tips:</strong>
    <ul>
    <li>Use <strong>Retrospective mode</strong> for comprehensive AF detection</li>
    <li>Always verify automated detections with manual review</li>
    <li>Check patient diary entries when reviewing events</li>
    <li>Export reports in both PDF and HL7 formats</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

def quick_task_finder():
    """Quick task finder page"""
    st.markdown('<div class="sub-header">🔍 Quick Task Finder</div>', unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("🔎 Search for a task or arrhythmia type:", 
                                placeholder="e.g., detect AF, measure QT interval, generate report")
    
    # Tasks database
    tasks = {
        "Detect Atrial Fibrillation": {
            "tabs": ["Rules", "Events", "Detail"],
            "difficulty": "Intermediate",
            "steps": [
                "Open the **Rules** menu from the toolbar",
                "Adjust AF detection settings: Number of beats analyzed and R-R interval variability",
                "Set Auto Stops to stop at AF episodes",
                "Start the scan in **Retrospective** or **Page** mode",
                "Review detected AF episodes in **Events** tab",
                "Verify episodes in **Detail** view with all 12 leads"
            ],
            "tips": ["Use R-R interval variability to increase sensitivity for paroxysmal AF",
                    "Minimum episode duration should be set to 30 seconds"]
        },
        "Measure QT Interval": {
            "tabs": ["Caliper", "Display"],
            "difficulty": "Beginner",
            "steps": [
                "Select **Caliper** tool from toolbar (or press 'C')",
                "Navigate to a clear QRS complex in **Display** view",
                "Place first caliper at Q wave onset",
                "Place second caliper at T wave end",
                "Read measurement displayed on screen",
                "Calculate QTc using Bazett's formula: QTc = QT/√RR"
            ],
            "tips": ["Use lead II or V5 for best QT measurements",
                    "Measure in multiple beats and average"]
        },
        "Generate Report": {
            "tabs": ["Report", "Review"],
            "difficulty": "Beginner",
            "steps": [
                "Complete the scan and event review",
                "Click **Report** tab",
                "Select report template",
                "Review automatically generated content",
                "Add physician comments if needed",
                "Export as PDF, HL7, or ZPT format"
            ],
            "tips": ["Reports can be edited after generation using ZPT Report Viewer"]
        }
    }
    
    # Display tasks
    if search_query:
        filtered_tasks = {k: v for k, v in tasks.items() 
                         if search_query.lower() in k.lower()}
    else:
        filtered_tasks = tasks
    
    for task_name, task_info in filtered_tasks.items():
        with st.expander(f"📋 {task_name} ({task_info['difficulty']})", expanded=False):
            st.markdown(f"**Required Tabs:** {', '.join(task_info['tabs'])}")
            
            st.markdown("**Steps:**")
            for i, step in enumerate(task_info['steps'], 1):
                st.markdown(f'<div class="step-number">{i}</div> {step}', unsafe_allow_html=True)
            
            st.markdown("**Tips:**")
            for tip in task_info['tips']:
                st.markdown(f"• {tip}")
            
            # Bookmark button
            if st.button(f"🔖 Bookmark", key=f"book_{task_name}"):
                if task_name not in st.session_state.user_data['bookmarks']:
                    st.session_state.user_data['bookmarks'].append(task_name)
                    st.success("Bookmarked!")

def af_detection_page():
    """Atrial Fibrillation Detection page"""
    st.markdown('<div class="sub-header">💓 Atrial Fibrillation Detection</div>', unsafe_allow_html=True)
    
    # Configuration section
    st.markdown("### ⚙️ Configuration Settings")
    
    with st.form("af_config"):
        col1, col2, col3 = st.columns(3)
        with col1:
            min_beats = st.slider("Minimum beats", 20, 100, 30)
            sensitivity = st.select_slider("Sensitivity", 
                                         options=["Low", "Medium", "High", "Very High"],
                                         value="High")
        with col2:
            rr_var = st.slider("R-R variability (%)", 5, 30, 12)
            min_duration = st.slider("Min duration (seconds)", 10, 120, 30)
        with col3:
            auto_stop = st.checkbox("Auto-stop at AF episodes", True)
            require_symptoms = st.checkbox("Require symptom correlation", False)
        
        if st.form_submit_button("💾 Save Configuration"):
            st.success("Configuration saved successfully!")
    
    # Live demo section
    st.markdown("### 📊 Live Demo")
    
    # Generate sample ECG data
    ecg_data = generate_sample_ecg_data()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if PLOTLY_AVAILABLE:
            fig = create_simple_plot(ecg_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart_data = create_simple_plot(ecg_data)
            st.line_chart(chart_data.set_index('Time (s)'))
    
    with col2:
        st.markdown("### Detection Statistics")
        st.metric("AF Episodes", "3", "+1")
        st.metric("Total AF Duration", "2.5 hours")
        st.metric("AF Burden", "5.2%")
        st.metric("Longest Episode", "1.2 hours")
    
    # Step-by-step procedure
    st.markdown("### 📋 Step-by-Step Procedure")
    
    steps = [
        ("Setup Rules", "Navigate to Rules → AF Detection → Set parameters as configured above"),
        ("Select Leads", "Choose optimal leads (typically II and V1 for best P-wave visibility)"),
        ("Start Scan", "Begin in Retrospective mode for comprehensive analysis"),
        ("Review Events", "Check Events tab for detected AF episodes (marked in purple)"),
        ("Verify Diagnosis", "Use Detail view to confirm irregular R-R intervals and absent P waves"),
        ("Measure Duration", "Use Caliper tool to measure exact episode duration"),
        ("Document Burden", "Calculate AF burden = (Total AF time / Recording time) × 100%")
    ]
    
    for i, (step, description) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="task-card">
            <div class="step-number">{i}</div>
            <strong>{step}</strong><br>
            {description}
        </div>
        """, unsafe_allow_html=True)
    
    # Tips and warnings
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="tip-box">
        <strong>💡 Pro Tips:</strong>
        <ul>
        <li>Use "AF Evidence" view to see R-R interval tachogram</li>
        <li>Check for Ashman phenomenon (wide QRS after long cycle)</li>
        <li>Look for associated symptoms in patient diary</li>
        <li>Consider CHA₂DS₂-VASc score for stroke risk</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <strong>⚠️ Common Pitfalls:</strong>
        <ul>
        <li>Don't confuse AF with atrial flutter (regular atrial activity)</li>
        <li>Artifact can mimic AF - verify in multiple leads</li>
        <li>Medications (digoxin) may regularize AF</li>
        <li>Consider sick sinus syndrome if long pauses after AF</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def report_generation_page():
    """Report Generation page"""
    st.markdown('<div class="sub-header">📝 Report Generation</div>', unsafe_allow_html=True)
    
    # Report configuration
    st.markdown("### ⚙️ Report Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Report Type", 
                                 ["Standard", "Comprehensive", "Summary", "Pacemaker"])
        include_graphs = st.checkbox("Include Graphs", True)
        anonymize = st.checkbox("Anonymize Data", False)
    with col2:
        export_format = st.multiselect("Export Format", 
                                     ["PDF", "HL7", "CSV"],
                                     default=["PDF"])
        physician_name = st.text_input("Physician Name", "Dr. Smith")
    
    # Report content
    st.markdown("### 📋 Report Content")
    
    tabs = st.tabs(["Patient Info", "Findings", "Statistics"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Patient ID", "PAT-2024-001")
            patient_name = st.text_input("Patient Name", "John Doe")
        with col2:
            patient_age = st.number_input("Age", 18, 120, 65)
            patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    with tabs[1]:
        findings = st.text_area("Clinical Findings", 
                              "Sinus rhythm with intermittent atrial fibrillation. Occasional VPBs. No significant ST segment changes.", 
                              height=100)
        diagnosis = st.text_input("Diagnosis", "Paroxysmal Atrial Fibrillation")
    
    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            total_beats = st.number_input("Total Beats", 0, 1000000, 112450)
            avg_hr = st.number_input("Average HR", 30, 200, 78)
            max_hr = st.number_input("Maximum HR", 60, 250, 142)
        with col2:
            min_hr = st.number_input("Minimum HR", 30, 100, 48)
            af_burden = st.number_input("AF Burden (%)", 0.0, 100.0, 12.5)
            vpb_count = st.number_input("VPB Count", 0, 10000, 1245)
    
    # Generate report button
    st.markdown("---")
    if st.button("🔄 Generate Report", use_container_width=True):
        with st.spinner("Generating report..."):
            # Simulate report generation
            import time
            time.sleep(2)
            
            # Show success message
            st.success("✅ Report generated successfully!")
            
            # Create sample report data
            report_data = f"""
            Philips Holter Analysis Report
            ==============================
            
            Patient Information:
            --------------------
            ID: {patient_id}
            Name: {patient_name}
            Age: {patient_age}
            Gender: {patient_gender}
            
            Findings:
            ---------
            {findings}
            
            Diagnosis: {diagnosis}
            
            Statistics:
            -----------
            Total Beats: {total_beats:,}
            Average HR: {avg_hr} bpm
            Maximum HR: {max_hr} bpm
            Minimum HR: {min_hr} bpm
            AF Burden: {af_burden}%
            VPB Count: {vpb_count:,}
            
            Physician: {physician_name}
            Date: {datetime.now().strftime('%Y-%m-%d')}
            """
            
            # Provide download button
            st.download_button(
                label="📥 Download Report (TXT)",
                data=report_data,
                file_name=f"Holter_Report_{patient_id}.txt",
                mime="text/plain"
            )

def reference_guide_page():
    """Reference Guide page"""
    st.markdown('<div class="sub-header">📚 Reference Guide</div>', unsafe_allow_html=True)
    
    # Quick Reference Tables
    st.markdown("### 📊 Normal Values & Thresholds")
    
    hr_params = pd.DataFrame({
        'Parameter': ['Normal Sinus Rhythm', 'Bradycardia', 'Tachycardia', 
                     'Maximum HR (Age-predicted)', 'Nighttime HR Drop'],
        'Range': ['60-100 bpm', '<60 bpm', '>100 bpm', 
                 '220 - Age', '10-20% decrease'],
        'Clinical Note': ['Regular rhythm, normal P waves', 
                         'Check for sinus vs. junctional',
                         'Assess for sinus vs. pathological',
                         'Use for exercise assessment',
                         'Abnormal if <10% (loss of circadian)']
    })
    
    st.dataframe(hr_params, use_container_width=True, hide_index=True)
    
    # Interval Reference
    st.markdown("### ⏱️ ECG Interval Reference")
    
    intervals = pd.DataFrame({
        'Interval': ['PR Interval', 'QRS Duration', 'QT Interval', 'QTc (Bazett)', 'RR Interval'],
        'Normal': ['120-200 ms', '<120 ms', '<440 ms (M), <460 ms (F)', '<450 ms (M), <470 ms (F)', '600-1000 ms'],
        'Measurement Lead': ['II', 'Any clear lead', 'II or V5', 'II or V5', 'Any lead']
    })
    
    st.dataframe(intervals, use_container_width=True, hide_index=True)
    
    # Arrhythmia Classification
    st.markdown("### 💓 Arrhythmia Classification")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Supraventricular:**
        - Atrial Fibrillation: Irregularly irregular, no P waves
        - Atrial Flutter: Sawtooth pattern, atrial rate 250-350 bpm
        - SVT: Regular, rate 150-250 bpm, narrow QRS
        """)
    with col2:
        st.markdown("""
        **Ventricular:**
        - PVC: Wide QRS, bizarre morphology
        - VT: Wide QRS, rate >100 bpm
        - VF: Chaotic, no organized QRS
        """)
    
    # Downloadable resources
    st.markdown("### 📥 Resources")
    
    if st.button("📋 Download Quick Reference Card", use_container_width=True):
        st.success("Quick reference guide would be downloaded here!")

def display_footer():
    """Display application footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>Philips Holter 1810/2010 Plus Analysis Guide v2.0</strong></p>
        <p>For clinical reference and educational purposes only.</p>
        <p>Always consult official Philips documentation and supervising physicians.</p>
    </div>
    """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
