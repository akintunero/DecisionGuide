import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


st.set_page_config(
    page_title="DecisionGuide",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the NEW "Digital Blueprint" styling
# Color Palette:
# Background: #f0f2f6 (Light Gray) with subtle grid/blueprint pattern
# Primary Text: #212529 (Dark/Black)
# Accent Color (Electric Blue): #007bff
# Highlight Color (Lighter Blue): #00bfff 
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Light background with subtle pattern for "Blueprint" feel */
    .stApp {
        background: #f0f2f6;
        /* Subtle grid pattern for technical feel */
        background-image: linear-gradient(0deg, #e9ecef 1px, transparent 1px), linear-gradient(90deg, #e9ecef 1px, transparent 1px);
        background-size: 20px 20px;
        background-position: 0 0;
    }
    
    /* Ensure all text is dark and readable */
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6 {
        color: #212529 !important;
    }
    
    /* Input elements and labels */
    .stRadio label, .stRadio span, .stTextInput label, .stSelectbox label {
        color: #212529 !important;
        font-weight: 600 !important;
    }
    
    /* Notification/Info boxes */
    .stAlert {
        border-left: 5px solid #007bff !important;
        background-color: #eaf3ff !important;
        color: #007bff !important;
    }
    
    /* Hero section styling - Sleek and structured */
    .hero-section {
        background: white;
        padding: 5rem 3rem;
        border-radius: 15px;
        text-align: center;
        color: #212529;
        margin-bottom: 3rem;
        box-shadow: 0 8px 30px rgba(0, 123, 255, 0.2);
        border: 2px solid #007bff;
        min-height: auto; /* Allow content to dictate height */
        display: block;
    }
    
    .hero-content {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .hero-logo {
        font-size: 6rem;
        margin-bottom: 1rem;
        color: #007bff;
        filter: drop-shadow(0 0 5px rgba(0, 123, 255, 0.3));
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        color: #212529;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        color: #007bff; /* Bright accent for main sub-header */
        font-weight: 500;
    }
    
    .hero-description {
        font-size: 1.1rem;
        max-width: 700px;
        margin: 0.5rem auto 0 auto;
        color: #555;
        line-height: 1.7;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-top: 5px solid #007bff; /* Accent line on top */
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 123, 255, 0.25);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #007bff;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #212529;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #6c757d;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Assessment cards */
    .assessment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        color: #212529;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.1);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
        border-left: 5px solid #007bff;
    }
    
    .assessment-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 123, 255, 0.2);
    }
    
    .assessment-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #007bff; 
    }
    
    .assessment-description {
        font-size: 0.95rem;
        opacity: 0.9;
        flex-grow: 1;
        color: #495057;
    }
    
    /* Section styling */
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin: 3rem 0 0.5rem 0;
        color: #212529;
    }
    
    .section-subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    /* Use case boxes */
    .use-case-box {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #00bfff; /* Lighter blue accent */
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .use-case-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #007bff;
        margin-bottom: 0.5rem;
    }
    
    .use-case-box ul, .use-case-box li {
        color: #495057;
        list-style-type: '✔️ '; /* Custom bullet */
    }
    
    .use-case-box li {
        margin-bottom: 0.5rem;
    }
    
    /* CTA section */
    .cta-section {
        background: #007bff; /* Solid accent color */
        padding: 3rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 3rem 0;
        box-shadow: 0 8px 30px rgba(0, 123, 255, 0.4);
    }
    
    .cta-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: white; 
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        margin-top: 3rem;
        background: white;
        border-top: 3px solid #007bff;
        border-radius: 15px;
    }
    
    .custom-footer strong {
        color: #212529;
    }
    
    .custom-footer a {
        color: #007bff;
        text-decoration: none;
        font-weight: 600;
    }
    
    .custom-footer a:hover {
        color: #0056b3;
        text-decoration: underline;
    }
    
    /* Buttons - Primary Action */
    .stButton>button {
        background: #007bff;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        background: #0056b3;
        box-shadow: 0 6px 15px rgba(0, 123, 255, 0.4);
    }
    
    /* Download Buttons - Secondary Action (Contrast from primary) */
    .stDownloadButton>button {
        background: #eaf3ff;
        color: #007bff;
        border: 1px solid #007bff;
        padding: 0.75rem 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        background: #d4e8ff;
        color: #0056b3;
    }
    
    /* Reroute the Radio Buttons to look better on light theme */
    div[data-testid="stRadio"] label {
        background: white;
        padding: 10px 15px;
        border-radius: 5px;
        border: 1px solid #dee2e6;
        margin-bottom: 5px;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    div[data-testid="stRadio"] label:has(input:checked) {
        background: #007bff1a; /* Very light blue shade */
        border-color: #007bff;
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.2);
    }
    
    /* Assessment page styling for readability */
    .assessment-path {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #00bfff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-top: 15px;
    }
    
</style>
""", unsafe_allow_html=True)


LOGIC_DIR = Path(__file__).parent / "logic"


def load_trees():
    trees = {}
    for path in LOGIC_DIR.glob("*.json"):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            tree_id = data.get("id") or path.stem
            trees[tree_id] = data
        except Exception as e:
            print(f"Failed to load {path}: {e}")
    return trees


def show_landing_page():
    """Display the authoritative "Digital Blueprint" landing page"""
    
    # Hero Section - BIG CENTERED
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-content'>
            <div class='hero-logo'>🎯</div>
            <div class='hero-title'>DecisionGuide</div>
            <div class='hero-subtitle'>Structured Assessment Engine for GRC Professionals</div>
            <div class='hero-description'>
                Stop guessing. Start calculating. DecisionGuide empowers you to make **consistent, auditable, and defensible** decisions based on pre-defined logic flows, providing instant audit trails.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("<div class='section-title'>Why DecisionGuide?</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Clarity, Consistency, and Compliance in one tool.</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>⚙️</div>
            <div class='feature-title'>Structured Logic</div>
            <div class='feature-text'>
                Each assessment follows a defined tree, removing ambiguity and ensuring results are based purely on traceable input criteria.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🚀</div>
            <div class='feature-title'>Local & Fast</div>
            <div class='feature-text'>
                Runs entirely in your browser without sending data to any server. Get instant results and maintain data sovereignty.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📋</div>
            <div class='feature-title'>Certified Auditability</div>
            <div class='feature-text'>
                Instantly export results with a complete path of reasoning in PDF, JSON, or TXT formats for compliance documentation.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Available Assessments
    st.markdown("<div class='section-title'>📊 Available Blueprints</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Select a decision tree to begin your structured assessment.</div>", unsafe_allow_html=True)
    
    trees = load_trees()
    
    cols = st.columns(min(len(trees), 3))
    
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx % 3]:
            # Applying the assessment-card style from the new CSS
            st.markdown(f"""
            <div class='assessment-card'>
                <div>
                    <div class='assessment-title'>{tree_data.get('title', 'Assessment')}</div>
                    <div class='assessment-description'>{tree_data.get('description', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Blueprint →", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Use Cases Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🤝 Trusted By:</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>👩‍💻 Information Security Teams</div>
            <ul>
                <li>Objective incident severity scoring (NIST/CVSS)</li>
                <li>Consistent data classification (P1/P2/P3)</li>
                <li>Clear documentation for vulnerability handling</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>⚖️ Legal and Regulatory Compliance</div>
            <ul>
                <li>Jurisdiction scoping (e.g., GDPR applicability)</li>
                <li>Data breach notification decision paths</li>
                <li>Policy exception justification (risk acceptance)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>📈 Internal Audit & Risk Management</div>
            <ul>
                <li>Standardized risk appetite decisions</li>
                <li>Vendor security tier classification (High/Medium/Low)</li>
                <li>Continuous control monitoring scoping</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>🛠️ Development & Engineering</div>
            <ul>
                <li>"Secure by Design" feature sign-offs</li>
                <li>Open-source license compliance evaluation</li>
                <li>Code change approval process standardization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class='cta-section'>
        <div class='cta-title'>The future of structured GRC is here.</div>
        <p style='font-size: 1.1rem; margin-bottom: 1.5rem; color: white;'>
            Ready to replace intuition with logic? Start building your first Blueprint today.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='custom-footer'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>
            <strong>DecisionGuide: The blueprint for consistent decision-making.</strong>
        </p>
        <p style='margin-bottom: 1rem; color: #6c757d;'>
            Built with empathy for students and professionals who need clarity in complex assessments.
        </p>
        <p>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>
                ⭐ Star on GitHub
            </a>
            &nbsp;|&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>
                💬 Contribute
            </a>
        </p>
        <p style='margin-top: 1.5rem; font-size: 0.9rem; color: #adb5bd;'>
            Open source • MIT License • Made with 💙
        </p>
    </div>
    """, unsafe_allow_html=True)


def traverse_tree_interactive(tree, node_id, answers, path_so_far):
    """Interactively traverse the tree"""
    nodes = tree["nodes"]
    node = nodes[node_id]
    
    node_label = node.get("text", "")
    node_type = node.get("type", "choice")
    
    if node_type == "choice":
        current_question = len(answers) + 1
        # Use a heading with the accent color
        st.markdown(f"### <span style='color: #007bff;'>➡️ Question {current_question}:</span>", unsafe_allow_html=True)
        st.markdown("---")
        
        options = list(node["options"].keys())
        
        if node_id in answers:
            selected = answers[node_id]
        else:
            # The radio buttons use the custom CSS styling
            selected = st.radio(
                node_label, 
                options, 
                key=f"{tree['id']}_{node_id}",
                index=None
            )
            
            if selected is None:
                return None, None, path_so_far
            
            answers[node_id] = selected
        
        path_entry = f"**{node_label}** → **{selected}**"
        new_path = path_so_far + [path_entry]
        
        selected_branch = node["options"][selected]
        
        if "decision" in selected_branch:
            decision = selected_branch["decision"]
            explanation = selected_branch.get("explanation", "")
            return decision, explanation, new_path
        
        next_node = selected_branch["next"]
        return traverse_tree_interactive(tree, next_node, answers, new_path)
    
    elif node_type == "text":
        st.markdown(node_label)
        return None, None, path_so_far + [node_label]
    
    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, path_so_far


def show_assessment_page():
    """Display the assessment page"""
    trees = load_trees()
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.show_landing = True
        st.session_state.pop('selected_tree', None)
        st.rerun()
    
    st.markdown("---")
    
    selected_tree_id = st.session_state.get('selected_tree')
    
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("Assessment not found")
        return
    
    tree = trees[selected_tree_id]
    
    st.title(f"🛠️ {tree.get('title', 'Assessment')}")
    if tree.get("description"):
        st.info(tree["description"])
    
    st.markdown("---")

    answers_key = f"answers_{selected_tree_id}"
    result_key = f"result_{selected_tree_id}"
    
    if answers_key not in st.session_state:
        st.session_state[answers_key] = {}
    
    if result_key not in st.session_state:
        st.session_state[result_key] = None

    answers = st.session_state[answers_key]
    # Pass path_so_far=[] to the initial call
    decision, explanation, path = traverse_tree_interactive(
        tree, 
        tree["root"], 
        answers, 
        []
    )

    if decision is not None:
        st.session_state[result_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path
        }

    if st.session_state[result_key] is not None:
        st.success("✅ Assessment Complete!")
        
        st.markdown("---")
        
        result = st.session_state[result_key]
        
        # Result section
        st.markdown("### <span style='color: #007bff;'>Decision:</span>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: #eaf3ff; padding: 20px; border-radius: 8px; border: 1px solid #007bff;'>
            <h4 style='color: #007bff; margin-bottom: 5px;'>Final Determination Code: **{result['decision']}**</h4>
            <p style='color: #212529;'>{result.get('explanation', 'No detailed explanation provided for this decision.')}</p>
        </div>
        """, unsafe_allow_html=True)


        # Path section
        st.markdown("### <span style='color: #007bff;'>Full Audit Trail (Path Taken):</span>", unsafe_allow_html=True)
        
        st.markdown("<div class='assessment-path'>", unsafe_allow_html=True)
        for i, step in enumerate(result['path']):
            # Use a progress-like visual for the steps
            st.markdown(f"<p style='margin-bottom: 5px; color: #495057;'>**{i+1}.** {step}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### <span style='color: #007bff;'>Export & Control:</span>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📄 Download PDF",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf"
            )
        
        with col2:
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📋 Download JSON",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json"
            )
        
        with col3:
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📝 Download TXT",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain"
            )
        
        with col4:
            if st.button("🔄 Start New Assessment"):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.rerun()


def main():
    if 'show_landing' not in st.session_state:
        st.session_state.show_landing = True
    
    if st.session_state.show_landing:
        show_landing_page()
    else:
        show_assessment_page()


if __name__ == "__main__":
    main()
