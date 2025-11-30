"""Main Streamlit application for DecisionGuide."""
import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime

from utils.config import Config
from services.decision_tree_service import DecisionTreeService
from services.pdf_service import PDFService
from services.history_service import HistoryService
from services.analytics_service import AnalyticsService
from models.decision_tree import DecisionResult
from utils.validators import validate_radio_selection, sanitize_input


# ----------------------------
# PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title=Config.APP_TITLE,
    layout="centered",
    initial_sidebar_state="expanded"
)

# ----------------------------
# INITIALIZE SERVICES
# ----------------------------
@st.cache_resource
def get_services():
    """Initialize and cache services."""
    return {
        "tree_service": DecisionTreeService(),
        "pdf_service": PDFService(),
        "history_service": HistoryService(),
        "analytics_service": AnalyticsService()
    }

services = get_services()
tree_service = services["tree_service"]
pdf_service = services["pdf_service"]
history_service = services["history_service"]
analytics_service = services["analytics_service"]

# ----------------------------
# SESSION STATE INITIALIZATION
# ----------------------------
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "current_tree" not in st.session_state:
    st.session_state.current_tree = None
if "decision_result" not in st.session_state:
    st.session_state.decision_result = None
if "show_path" not in st.session_state:
    st.session_state.show_path = False

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def reset_session() -> None:
    """Reset the current session."""
    st.session_state.answers = {}
    st.session_state.current_tree = None
    st.session_state.decision_result = None
    st.session_state.show_path = False
    st.rerun()

def render_question(
    question_id: str,
    question_text: str,
    options: list[str],
    help_text: Optional[str] = None
) -> str:
    """
    Render a question with validation.
    
    Args:
        question_id: Unique identifier for the question
        question_text: Text of the question
        options: List of option strings
        help_text: Optional help text to display
        
    Returns:
        Selected answer or "Select..."
    """
    if help_text:
        st.caption(f"ℹ️ {help_text}")
    
    answer = st.radio(
        question_text,
        options,
        index=0,
        key=question_id,
        horizontal=False
    )
    
    # Sanitize input
    return sanitize_input(answer)

def calculate_progress(answers: Dict[str, Any], tree_name: str) -> float:
    """
    Calculate progress through decision tree.
    
    Args:
        answers: Dictionary of answers
        tree_name: Name of the current tree
        
    Returns:
        Progress percentage (0-100)
    """
    # Estimate based on number of answers
    # This is a simplified calculation
    if tree_name == "Incident Reporting":
        total_questions = 5
    elif tree_name == "Vendor Risk Tiering":
        total_questions = 3
    elif tree_name == "DPIA Requirement":
        total_questions = 3
    else:
        total_questions = 5
    
    answered = sum(1 for v in answers.values() if v and v != "Select...")
    return min(100, (answered / total_questions) * 100) if total_questions > 0 else 0

# ----------------------------
# TREE RENDERING FUNCTIONS
# ----------------------------
def render_incident_reporting_tree() -> Optional[DecisionResult]:
    """Render the incident reporting decision tree."""
    st.subheader("Tree 1 – Vendor Incident Reporting")
    
    # Question 1
    q1 = render_question(
        "ir_q1",
        "1. Does this vendor process personal or sensitive data on your behalf?",
        ["Select...", "Yes", "No"],
        help_text="Personal data includes any information that can identify an individual"
    )
    st.session_state.answers["ir_q1"] = q1
    
    if q1 == "Select...":
        return None
    
    if q1 == "No":
        return tree_service.execute_tree("Incident Reporting", st.session_state.answers)
    
    # Question 2
    q2 = render_question(
        "ir_q2",
        "2. Is there a regulatory or contractual incident/breach reporting requirement "
        "(for example GDPR/UK GDPR, sector rules, or customer contracts)?",
        ["Select...", "Yes", "No"]
    )
    st.session_state.answers["ir_q2"] = q2
    
    if q2 == "Select...":
        return None
    
    if q2 == "No":
        return tree_service.execute_tree("Incident Reporting", st.session_state.answers)
    
    # Question 3
    q3 = render_question(
        "ir_q3",
        "3. What is your required maximum incident notification timeframe?",
        ["Select...", "24 hours", "48 hours", "72 hours"]
    )
    st.session_state.answers["ir_q3"] = q3
    
    if q3 == "Select...":
        return None
    
    # Question 4 - Safe extraction with error handling
    try:
        required_hours = int(q3.split()[0]) if q3 != "Select..." else 24
    except (ValueError, AttributeError, IndexError):
        required_hours = 24
    
    q4 = render_question(
        "ir_q4",
        f"4. Can the vendor contractually commit to notify you within {required_hours} hours?",
        ["Select...", "Yes", "No"]
    )
    st.session_state.answers["ir_q4"] = q4
    
    if q4 == "Select...":
        return None
    
    if q4 == "Yes":
        return tree_service.execute_tree("Incident Reporting", st.session_state.answers)
    
    # Question 5
    q5 = render_question(
        "ir_q5",
        "5. Can you introduce compensating controls (for example enhanced monitoring, "
        "stricter SLAs, high-priority incident routing)?",
        ["Select...", "Yes", "No"]
    )
    st.session_state.answers["ir_q5"] = q5
    
    if q5 == "Select...":
        return None
    
    return tree_service.execute_tree("Incident Reporting", st.session_state.answers)

def render_vendor_classification_tree() -> Optional[DecisionResult]:
    """Render the vendor classification decision tree."""
    st.subheader("Tree 2 – Vendor Data Risk Classification")
    
    q1 = render_question(
        "vc_q1",
        "1. Does the vendor handle personal data?",
        ["Select...", "No data", "Personal data", "Special category / highly sensitive data"]
    )
    st.session_state.answers["vc_q1"] = q1
    
    if q1 == "Select...":
        return None
    
    q2 = render_question(
        "vc_q2",
        "2. What is the scale of processing?",
        ["Select...", "Small (few records, low volume)", "Medium", "Large (high volume / continuous)"]
    )
    st.session_state.answers["vc_q2"] = q2
    
    if q2 == "Select...":
        return None
    
    q3 = render_question(
        "vc_q3",
        "3. Does the vendor connect to your core systems or internal network?",
        ["Select...", "Yes", "No"]
    )
    st.session_state.answers["vc_q3"] = q3
    
    if q3 == "Select...":
        return None
    
    return tree_service.execute_tree("Vendor Risk Tiering", st.session_state.answers)

def render_dpia_tree() -> Optional[DecisionResult]:
    """Render the DPIA requirement decision tree."""
    st.subheader("Tree 3 – DPIA Requirement Check")
    
    q1 = render_question(
        "dp_q1",
        "1. Does the processing involve systematic and extensive profiling or automated decisions about individuals?",
        ["Select...", "Yes", "No"]
    )
    st.session_state.answers["dp_q1"] = q1
    
    if q1 == "Select...":
        return None
    
    q2 = render_question(
        "dp_q2",
        "2. Will the processing involve large-scale use of special category data "
        "(for example health, biometrics, ethnicity)?",
        ["Select...", "Yes", "No"]
    )
    st.session_state.answers["dp_q2"] = q2
    
    if q2 == "Select...":
        return None
    
    q3 = render_question(
        "dp_q3",
        "3. Will the processing involve systematic monitoring of publicly accessible areas "
        "or behaviour (for example CCTV, online tracking)?",
        ["Select...", "Yes", "No"]
    )
    st.session_state.answers["dp_q3"] = q3
    
    if q3 == "Select...":
        return None
    
    return tree_service.execute_tree("DPIA Requirement", st.session_state.answers)

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.title("⚙️ Settings")
    
    if st.button("🔄 Reset Session", use_container_width=True):
        reset_session()
    
    st.markdown("---")
    
    if Config.ENABLE_HISTORY:
        st.subheader("📜 History")
        history = history_service.get_history(limit=5)
        if history:
            for entry in history:
                with st.expander(f"{entry['tree_name']} - {entry['decision']}"):
                    st.write(f"**Date:** {entry['timestamp'][:10]}")
                    st.write(f"**Decision:** {entry['decision']}")
        else:
            st.caption("No history yet")
    
    if Config.ENABLE_ANALYTICS:
        st.markdown("---")
        st.subheader("📊 Statistics")
        stats = analytics_service.get_statistics()
        if stats:
            st.metric("Total Decisions", stats.get("total_decisions", 0))
            if stats.get("tree_usage"):
                st.write("**Tree Usage:**")
                for tree, count in stats["tree_usage"].items():
                    st.caption(f"{tree}: {count}")

# ----------------------------
# MAIN CONTENT
# ----------------------------
st.title(Config.APP_TITLE)
st.write(Config.APP_DESCRIPTION)

# Tree selection
available_trees = ["Select..."] + tree_service.get_available_trees()
if not available_trees or available_trees == ["Select..."]:
    # Fallback to hardcoded trees if JSON loading fails
    available_trees = [
        "Select...",
        "Incident Reporting",
        "Vendor Risk Tiering",
        "DPIA Requirement"
    ]

tree_choice = st.selectbox(
    "Select a decision guide to run:",
    available_trees,
    key="tree_select"
)

# Reset if tree changes
if st.session_state.current_tree != tree_choice:
    st.session_state.answers = {}
    st.session_state.current_tree = tree_choice
    st.session_state.decision_result = None

if tree_choice == "Select...":
    st.info("👆 Please select a decision guide from the dropdown above to begin.")
    st.markdown("""
    ### Available Decision Trees:
    - **Incident Reporting**: Determine vendor incident notification requirements
    - **Vendor Risk Tiering**: Classify vendor data risk levels
    - **DPIA Requirement**: Check if a Data Protection Impact Assessment is required
    """)
else:
    # Progress bar
    progress = calculate_progress(st.session_state.answers, tree_choice)
    st.progress(progress / 100, text=f"Progress: {int(progress)}%")
    
    # Render questions based on tree
    decision_result: Optional[DecisionResult] = None
    
    if tree_choice == "Incident Reporting":
        decision_result = render_incident_reporting_tree()
    elif tree_choice == "Vendor Risk Tiering":
        decision_result = render_vendor_classification_tree()
    elif tree_choice == "DPIA Requirement":
        decision_result = render_dpia_tree()
    
    # Store result
    if decision_result and decision_result.decision:
        st.session_state.decision_result = decision_result
        
        # Save to history
        if Config.ENABLE_HISTORY:
            history_service.save_decision(
                tree_choice,
                decision_result,
                st.session_state.answers.copy()
            )
        
        # Track analytics
        if Config.ENABLE_ANALYTICS:
            analytics_service.track_decision(
                tree_choice,
                decision_result.decision
            )
    
    # Display results
    st.markdown("---")
    
    if decision_result and decision_result.decision:
        # Decision
        st.subheader("✅ Decision")
        
        # Color code based on decision type
        if "ACCEPT" in decision_result.decision:
            st.success(decision_result.decision)
        elif "REJECT" in decision_result.decision or "REQUIRED" in decision_result.decision:
            st.error(decision_result.decision)
        elif "MITIGATION" in decision_result.decision or "RECOMMENDED" in decision_result.decision:
            st.warning(decision_result.decision)
        else:
            st.info(decision_result.decision)
        
        # Explanation
        if decision_result.explanation:
            st.subheader("📝 Explanation")
            st.write(decision_result.explanation)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Start Over"):
                reset_session()
        
        with col2:
            if Config.ENABLE_PDF_EXPORT and pdf_service.available:
                if st.button("📄 Export PDF"):
                    pdf_path = pdf_service.generate_pdf(
                        decision_result,
                        tree_choice
                    )
                    if pdf_path:
                        with open(pdf_path, 'rb') as f:
                            st.download_button(
                                "⬇️ Download PDF",
                                f.read(),
                                file_name=pdf_path.name,
                                mime="application/pdf"
                            )
        
        with col3:
            st.session_state.show_path = st.checkbox(
                "Show decision path",
                value=st.session_state.show_path
            )
        
        # Decision path
        if st.session_state.show_path and decision_result.path:
            st.subheader("🛤️ Decision Path")
            for i, step in enumerate(decision_result.path, 1):
                st.write(f"{i}. {step}")
