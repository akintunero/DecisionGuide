import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


st.set_page_config(
    page_title="DecisionGuide | Neon Circuit",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the "Neon Circuit" Styling (20-Year Designer's Best)
# Color Palette:
# Background: #0d1117 (Deep Black/Charcoal)
# Primary Text: #f0f6fc (High-Contrast White)
# Accent Color (Neon Green): #00ff99
# Secondary Accent: #00b36b 
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Deep dark background for the entire application */
    .stApp {
        background: #0d1117;
        color: #f0f6fc;
        font-family: 'Consolas', 'Courier New', monospace; /* Monospace font for technical feel */
    }
    
    /* Ensure all text is bright and readable */
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6 {
        color: #f0f6fc !important; 
    }
    
    /* Input elements and labels */
    .stRadio label, .stRadio span, .stTextInput label, .stSelectbox label {
        color: #00ff99 !important; /* Neon Green labels */
        font-weight: 600 !important;
    }
    
    /* Notifications (Success/Info) - Glowing effect */
    div[data-baseweb="notification"] {
        background-color: #00ff9915 !important;
        border-left: 5px solid #00ff99 !important;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.5);
    }
    div[data-baseweb="notification"] * {
        color: #00ff99 !important;
    }
    
    /* Hero section styling - Illuminated box */
    .hero-section {
        background: #161b22; /* Slightly lighter dark background */
        padding: 6rem 3rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 4rem;
        /* The WOW factor: Neon border and shadow */
        box-shadow: 0 0 50px rgba(0, 255, 153, 0.3), 0 0 10px rgba(0, 255, 153, 0.6);
        border: 2px solid #00ff99;
        min-height: auto; 
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .hero-logo {
        font-size: 7rem;
        margin-bottom: 1.5rem;
        color: #00ff99; 
        text-shadow: 0 0 10px #00ff99;
    }
    
    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        color: #f0f6fc;
        letter-spacing: -3px;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    }
    
    .hero-subtitle {
        font-size: 1.8rem;
        margin-bottom: 2rem;
        color: #00ff99; 
        font-weight: 500;
        line-height: 1.6;
        text-shadow: 0 0 3px #00ff9980;
    }
    
    .hero-description {
        font-size: 1.1rem;
        max-width: 800px;
        margin: 0.5rem auto 0 auto;
        color: #a0a8b3;
        line-height: 1.7;
    }
    
    /* Feature cards - Component look */
    .feature-card {
        background: #161b22;
        padding: 2rem;
        border-radius: 8px;
        height: 100%;
        transition: all 0.3s ease;
        border: 1px solid #00ff9944;
        box-shadow: inset 0 0 10px rgba(0, 255, 153, 0.1); /* Subtle inner glow */
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0, 255, 153, 0.2), inset 0 0 15px rgba(0, 255, 153, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #00ff99;
        text-shadow: 0 0 5px #00ff99;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #a0a8b3;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Assessment cards - Decision nodes */
    .assessment-card {
        background: #161b22;
        padding: 1.5rem;
        border-radius: 5px;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
        border-left: 5px solid #00ff99; /* Strong left accent */
    }
    
    .assessment-card:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 255, 153, 0.4);
    }
    
    .assessment-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #00ff99; 
    }
    
    .assessment-description {
        font-size: 0.95rem;
        opacity: 0.8;
        flex-grow: 1;
        color: #a0a8b3;
    }
    
    /* Section styling */
    .section-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin: 4rem 0 1rem 0;
        color: #f0f6fc;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
    }
    
    .section-subtitle {
        text-align: center;
        color: #00ff99;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        text-shadow: 0 0 3px #00ff9980;
    }
    
    /* Use case boxes - Highlighted applications */
    .use-case-box {
        background: #161b22;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #00ff9944;
        margin-bottom: 1rem;
        box-shadow: inset 0 0 10px rgba(0, 255, 153, 0.1);
    }
    
    .use-case-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #00ff99;
        margin-bottom: 0.5rem;
    }
    
    .use-case-box ul, .use-case-box li {
        color: #a0a8b3;
        list-style-type: '⚡ '; /* Custom bullet */
    }
    
    /* CTA section - High energy */
    .cta-section {
        background: #00ff99; 
        padding: 3rem;
        border-radius: 10px;
        text-align: center;
        color: #0d1117; /* Dark text on bright background */
        margin: 4rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 153, 0.8);
        border: 3px solid white;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #0d1117; 
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        color: #a0a8b3;
        margin-top: 4rem;
        background: #161b22;
        border-top: 3px solid #00ff99;
        border-radius: 10px;
    }
    
    .custom-footer strong {
        color: #f0f6fc;
    }
    
    .custom-footer a {
        color: #00ff99;
        text-decoration: none;
        font-weight: 600;
        text-shadow: 0 0 5px #00ff9980;
    }
    
    .custom-footer a:hover {
        color: #00b36b;
    }
    
    /* Buttons - Primary Action (Glow) */
    .stButton>button {
        background: #00ff99;
        color: #0d1117;
        border: none;
        padding: 0.8rem 2.5rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 5px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.5);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        background: #00b36b;
        color: white;
        box-shadow: 0 0 20px rgba(0, 255, 153, 0.8);
    }
    
    /* Download Buttons - Secondary Action (Dark with neon border) */
    .stDownloadButton>button {
        background: #0d1117;
        color: #00ff99;
        border: 1px solid #00ff99;
        padding: 0.75rem 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        border-radius: 5px;
        transition: all 0.3s ease;
        box-shadow: 0 0 5px rgba(0, 255, 153, 0.2);
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        background: #161b22;
        border-color: #00ff99;
        box-shadow: 0 0 15px rgba(0, 255, 153, 0.5);
    }
    
    /* Radio Buttons - The core interaction (Illuminated selection) */
    div[data-testid="stRadio"] label {
        background: #161b22;
        padding: 12px 18px;
        border-radius: 5px;
        border: 1px solid #30363d;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.3s;
        color: #f0f6fc;
        box-shadow: inset 0 0 5px rgba(255, 255, 255, 0.05);
    }

    div[data-testid="stRadio"] label:has(input:checked) {
        background: #00ff991a; /* Neon shade */
        border-color: #00ff99;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.5), inset 0 0 15px rgba(0, 255, 153, 0.2);
        color: #f0f6fc;
    }
    
    /* Assessment page styling for readability */
    .assessment-path {
        background: #161b22;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #00ff99;
        box-shadow: inset 0 0 10px rgba(0, 255, 153, 0.1);
        margin-top: 15px;
    }
    
    /* Decision Result Box */
    .decision-result-box {
        background: #00ff9915;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #00ff99;
        box-shadow: 0 0 15px rgba(0, 255, 153, 0.5);
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
    """Display the authoritative "Neon Circuit" landing page"""
    
    # Hero Section - BIG CENTERED
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-content'>
            <div class='hero-logo'>🤖</div>
            <div class='hero-title'>DecisionGuide</div>
            <div class='hero-subtitle'>Structured Assessment Engine for **Digital Governance**</div>
            <div class='hero-description'>
                Experience GRC as it should be: **Illuminated Logic and Instant Auditability.** Navigate complex standards with the precision of a circuit board.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("<div class='section-title'>CORE LOGIC MODULES</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Precision-engineered features for modern GRC.</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🗂️</div>
            <div class='feature-title'>Circuit Flow Validation</div>
            <div class='feature-text'>
                Each path is a validated circuit. Zero ambiguity, 100% logic integrity. Ensures consistent, repeatable results every time.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📡</div>
            <div class='feature-title'>Local Execution Engine</div>
            <div class='feature-text'>
                Runs entirely locally. Your data stays yours. The logic is the engine; privacy is the default setting.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>💾</div>
            <div class='feature-title'>Immutable Audit Trail</div>
            <div class='feature-text'>
                Export the decision, the path, and the explanation instantly. Ready for any compliance check, audit, or legal review.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Available Assessments
    st.markdown("<div class='section-title'>⚡ ENGAGE ASSESSMENT MODULES</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Select a decision logic to initialize your assessment sequence.</div>", unsafe_allow_html=True)
    
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
            
            if st.button(f"Initialize Module →", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Use Cases Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🎯 TARGETED APPLICATIONS</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>CYBER RISK & INCIDENT RESPONSE</div>
            <ul>
                <li>Objective incident severity scoring (e.g., NIST/CVSS)</li>
                <li>Systematic forensic scope definition</li>
                <li>Automated legal reporting triggers</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>COMPLIANCE & REGULATORY MAPPING</div>
            <ul>
                <li>Accurate global compliance scoping (GDPR, CCPA, etc.)</li>
                <li>Policy deviation justification matrix</li>
                <li>Regulatory control applicability decisioning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>SUPPLY CHAIN & VENDOR RISK</div>
            <ul>
                <li>Automated risk tier classification (Tiers 1-4)</li>
                <li>Required due diligence level calculation</li>
                <li>Contractual security clause necessity determination</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>INTERNAL AUDIT & GOVERNANCE</div>
            <ul>
                <li>Consistent audit sampling methodology</li>
                <li>Risk acceptance criteria validation</li>
                <li>Internal control effectiveness scoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class='cta-section'>
        <div class='cta-title'>INITIATE YOUR STRUCTURED GRC FUTURE.</div>
        <p style='font-size: 1.1rem; margin-bottom: 1.5rem; color: #0d1117; font-weight: 600;'>
            Stop using spreadsheets for critical decisions. Adopt the Neon Circuit.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='custom-footer'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>
            <strong>DecisionGuide: Precision Logic, Zero Guesswork.</strong>
        </p>
        <p style='margin-bottom: 1rem; color: #a0a8b3;'>
            Open-source framework. Designed to empower GRC professionals and students worldwide.
        </p>
        <p>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>
                ⭐ Fork the Repository
            </a>
            &nbsp;|&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>
                💬 Contribute Logic Modules
            </a>
        </p>
        <p style='margin-top: 1.5rem; font-size: 0.9rem; color: #444;'>
            V1.0.0 • MIT License • Built for the Digital Age
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
        # Highlight the current question number with Neon Green
        st.markdown(f"## <span style='color: #00ff99;'>[STEP {current_question}]</span>: {node_label}", unsafe_allow_html=True)
        st.markdown("<hr style='border-top: 1px solid #00ff9980;'>", unsafe_allow_html=True)
        
        options = list(node["options"].keys())
        
        if node_id in answers:
            selected = answers[node_id]
        else:
            # The radio buttons use the custom CSS styling for illuminated selection
            selected = st.radio(
                node_label, 
                options, 
                key=f"{tree['id']}_{node_id}",
                index=None,
                label_visibility="collapsed" # Hide the default label since we used H2 above
            )
            
            if selected is None:
                return None, None, path_so_far
            
            answers[node_id] = selected
        
        path_entry = f"**{node_label}** ➡️ **{selected}**"
        new_path = path_so_far + [path_entry]
        
        selected_branch = node["options"][selected]
        
        if "decision" in selected_branch:
            decision = selected_branch["decision"]
            explanation = selected_branch.get("explanation", "")
            return decision, explanation, new_path
        
        next_node = selected_branch["next"]
        return traverse_tree_interactive(tree, next_node, answers, new_path)
    
    elif node_type == "text":
        st.markdown(f"### {node_label}")
        return None, None, path_so_far + [node_label]
    
    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, path_so_far


def show_assessment_page():
    """Display the assessment page"""
    trees = load_trees()
    
    # Back button
    if st.button("← EXIT MODULE"):
        st.session_state.show_landing = True
        st.session_state.pop('selected_tree', None)
        st.rerun()
    
    st.markdown("<hr style='border-top: 1px solid #00ff9980;'>", unsafe_allow_html=True)
    
    selected_tree_id = st.session_state.get('selected_tree')
    
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("Assessment not found. Circuit Broken.")
        return
    
    tree = trees[selected_tree_id]
    
    st.title(f"// EXECUTE: {tree.get('title', 'Assessment').upper()}")
    if tree.get("description"):
        st.info(f"STATUS: Initializing Module. {tree['description']}")
    
    st.markdown("<hr style='border-top: 1px solid #00ff9980;'>", unsafe_allow_html=True)

    answers_key = f"answers_{selected_tree_id}"
    result_key = f"result_{selected_tree_id}"
    
    if answers_key not in st.session_state:
        st.session_state[answers_key] = {}
    
    if result_key not in st.session_state:
        st.session_state[result_key] = None

    answers = st.session_state[answers_key]
    
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
        st.success("✅ Assessment Complete! Final Decision Reached.")
        
        st.markdown("<hr style='border-top: 3px solid #00ff99;'>", unsafe_allow_html=True)
        
        result = st.session_state[result_key]
        
        # Result section
        st.markdown("## <span style='color: #00ff99;'>[FINAL DETERMINATION]</span>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='decision-result-box'>
            <h4 style='color: #00ff99; margin-bottom: 5px;'>DECISION CODE: <code style='background: #0d1117; padding: 5px; border-radius: 3px; border: 1px solid #00ff99;'>{result['decision']}</code></h4>
            <p style='color: #f0f6fc;'>{result.get('explanation', 'No detailed explanation provided for this decision.')}</p>
        </div>
        """, unsafe_allow_html=True)


        # Path section
        st.markdown("## <span style='color: #00ff99;'>[AUDIT TRAIL LOG]</span>", unsafe_allow_html=True)
        
        st.markdown("<div class='assessment-path'>", unsafe_allow_html=True)
        for i, step in enumerate(result['path']):
            # Use a monospace, code-like output for the audit trail
            st.markdown(f"<p style='margin-bottom: 5px; color: #a0a8b3; font-family: monospace;'>{i+1}: {step}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-top: 1px solid #00ff9980;'>", unsafe_allow_html=True)
        st.markdown("## <span style='color: #00ff99;'>[EXPORT & RESET]</span>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📄 EXPORT PDF (Report)",
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
                label="📋 EXPORT JSON (Data)",
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
                label="📝 EXPORT TXT (Log)",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain"
            )
        
        with col4:
            if st.button("🔄 RE-INITIALIZE MODULE"):
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
