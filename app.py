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

# Custom CSS for modern professional styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Typography */
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6 {
        color: #1a202c !important;
    }
    
    .stRadio label, .stRadio span {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    div[data-baseweb="notification"] * {
        color: #1565c0 !important;
    }
    
    /* Hero Section - Modern Centered Design */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin: 2rem auto 3rem auto;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        max-width: 1200px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-logo {
        font-size: 6rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 1rem;
        color: white;
        letter-spacing: -2px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        color: rgba(255,255,255,0.95);
        line-height: 1.6;
        font-weight: 400;
    }
    
    .hero-description {
        font-size: 1.1rem;
        max-width: 700px;
        margin: 0 auto;
        color: rgba(255,255,255,0.9);
        line-height: 1.8;
        font-weight: 300;
    }
    
    /* Feature Cards - Card Design */
    .features-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .feature-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        height: 100%;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.2) rotate(5deg);
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .feature-text {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    /* Assessment Cards - Modern Card Design */
    .assessments-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .assessment-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }
    
    .assessment-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: var(--gradient);
    }
    
    .assessment-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        border-color: #667eea;
    }
    
    .assessment-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .assessment-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #1a202c;
    }
    
    .assessment-description {
        font-size: 1rem;
        color: #4a5568;
        flex-grow: 1;
        line-height: 1.6;
    }
    
    /* Section Styling */
    .section-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin: 4rem 0 1rem 0;
        color: #1a202c;
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .section-subtitle {
        text-align: center;
        color: #4a5568;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Use Case Boxes - Modern Design */
    .use-cases-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .use-case-box {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .use-case-box:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    .use-case-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .use-case-box ul {
        color: #4a5568;
        padding-left: 1.5rem;
    }
    
    .use-case-box li {
        color: #4a5568;
        margin-bottom: 0.75rem;
        line-height: 1.6;
    }
    
    /* CTA Section - Enhanced */
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin: 4rem auto;
        max-width: 1200px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .cta-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: white;
        position: relative;
        z-index: 1;
    }
    
    .cta-text {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: rgba(255,255,255,0.95);
        position: relative;
        z-index: 1;
    }
    
    /* Footer - Clean Design */
    .custom-footer {
        text-align: center;
        padding: 3rem 2rem;
        color: #4a5568;
        margin: 4rem auto 2rem auto;
        max-width: 1200px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    
    .custom-footer strong {
        color: #1a202c;
    }
    
    .custom-footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .custom-footer a:hover {
        color: #764ba2;
    }
    
    /* Buttons - Modern Design */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 0.875rem 2.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Download Buttons */
    .stDownloadButton>button {
        background: white;
        color: #667eea !important;
        border: 2px solid #667eea;
        padding: 0.75rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: #667eea;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-logo {
            font-size: 4rem;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .hero-description {
            font-size: 1rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .feature-card,
        .assessment-card,
        .use-case-box {
            margin-bottom: 1.5rem;
        }
        
        .hero-section,
        .cta-section {
            padding: 3rem 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero-logo {
            font-size: 3rem;
        }
        
        .hero-title {
            font-size: 2rem;
            letter-spacing: -1px;
        }
        
        .hero-subtitle {
            font-size: 1rem;
        }
        
        .hero-description {
            font-size: 0.95rem;
        }
        
        .section-title {
            font-size: 1.75rem;
        }
        
        .cta-title {
            font-size: 1.75rem;
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Container max-widths */
    .block-container {
        max-width: 1400px;
        padding-left: 2rem;
        padding-right: 2rem;
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
    """Display the redesigned landing page"""
    
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-content'>
            <div class='hero-logo'>🎯</div>
            <div class='hero-title'>DecisionGuide</div>
            <div class='hero-subtitle'>Open-source assessment framework for GRC professionals</div>
            <div class='hero-description'>
                Make consistent, defensible decisions through structured logic flows. 
                Built with empathy for professionals who need clarity in complex assessments.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("<div class='section-title'>Why DecisionGuide?</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Everything you need for professional GRC assessments</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='features-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔍</div>
            <div class='feature-title'>Transparent Logic</div>
            <div class='feature-text'>
                See exactly how decisions are reached with clear, step-by-step reasoning. 
                Every path is documented and traceable for complete transparency.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔒</div>
            <div class='feature-title'>Privacy First</div>
            <div class='feature-text'>
                Zero-document approach means no file uploads, no data collection. 
                All processing happens locally in your browser for maximum security.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📄</div>
            <div class='feature-title'>Audit Ready</div>
            <div class='feature-text'>
                Export professional reports in PDF, JSON, or TXT formats. 
                Complete audit trails for compliance documentation and reviews.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Available Assessments
    st.markdown("<div class='section-title'>📋 Available Assessments</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Choose an assessment to get started</div>", unsafe_allow_html=True)
    
    trees = load_trees()
    
    # Assessment icons and gradients
    assessment_styles = [
        {"icon": "🔐", "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
        {"icon": "⚖️", "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"},
        {"icon": "🛡️", "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"},
    ]
    
    st.markdown("<div class='assessments-container'>", unsafe_allow_html=True)
    cols = st.columns(min(len(trees), 3))
    
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx % 3]:
            style = assessment_styles[idx % len(assessment_styles)]
            
            st.markdown(f"""
            <div class='assessment-card' style='--gradient: {style["gradient"]}'>
                <div>
                    <div class='assessment-icon'>{style["icon"]}</div>
                    <div class='assessment-title'>{tree_data.get('title', 'Assessment')}</div>
                    <div class='assessment-description'>{tree_data.get('description', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Assessment →", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Use Cases Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🎯 Who Is This For?</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Built for professionals who need consistent, defensible decisions</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='use-cases-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>👨‍💼 For Auditors</div>
            <ul>
                <li>Standardize assessment approaches across teams</li>
                <li>Generate consistent, defensible decisions</li>
                <li>Produce audit-ready documentation instantly</li>
                <li>Maintain complete transparency in methodology</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>📊 For Risk Managers</div>
            <ul>
                <li>Classify vendors systematically</li>
                <li>Tier risks consistently across organization</li>
                <li>Document decision rationale clearly</li>
                <li>Create repeatable risk assessment frameworks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>✅ For Compliance Teams</div>
            <ul>
                <li>Determine regulatory requirements quickly</li>
                <li>Apply jurisdiction-specific rules accurately</li>
                <li>Maintain complete audit trails</li>
                <li>Ensure consistent compliance assessments</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>🛡️ For Security Teams</div>
            <ul>
                <li>Assess incident severity objectively</li>
                <li>Make reporting decisions confidently</li>
                <li>Document incident response choices</li>
                <li>Standardize security evaluation processes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class='cta-section'>
        <div class='cta-title'>Ready to Make Better Decisions?</div>
        <p class='cta-text'>
            Join GRC professionals using DecisionGuide for consistent, defensible assessments
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='custom-footer'>
        <p style='font-size: 1.2rem; margin-bottom: 0.75rem;'>
            <strong>DecisionGuide: Making structured, smart decisions—one at a time.</strong>
        </p>
        <p style='margin-bottom: 1.5rem; color: #4a5568; font-size: 1.05rem;'>
            Built with empathy for students and professionals who need clarity in complex assessments.
        </p>
        <p style='font-size: 1.05rem;'>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>
                ⭐ Star on GitHub
            </a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>
                💬 Contribute
            </a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide#readme' target='_blank'>
                📖 Documentation
            </a>
        </p>
        <p style='margin-top: 2rem; font-size: 0.95rem; color: #718096;'>
            Open source • MIT License • Made with 💙 by Adeshola
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_assessment_page():
    """Display the assessment page with improved styling"""
    trees = load_trees()
    
    # Back button with improved styling
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.show_landing = True
            st.session_state.pop('selected_tree', None)
            st.rerun()
    
    st.markdown("---")
    
    selected_tree_id = st.session_state.get('selected_tree')
    
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("❌ Assessment not found")
        return
    
    tree = trees[selected_tree_id]
    
    # Assessment header
    st.markdown(f"<h1 style='text-align: center; color: #1a202c;'>{tree.get('title', 'Assessment')}</h1>", unsafe_allow_html=True)
    if tree.get("description"):
        st.info(f"ℹ️ {tree['description']}")
    
    st.markdown("---")

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
        st.success("✅ Assessment Complete!")
        
        st.markdown("---")
        
        result = st.session_state[result_key]
        
        # Results in a nice container
        st.markdown("### 📊 Assessment Result")
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 10px rgba(0,0,0,0.05);'>
            <p style='margin: 0; color: #1a202c;'><strong>Decision Code:</strong> {result['decision']}</p>
            {f"<p style='margin-top: 0.5rem; color: #4a5568;'>{result['explanation']}</p>" if result['explanation'] else ""}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🗺️ Decision Path")
        st.markdown("<div style='background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        for i, step in enumerate(result['path'], 1):
            st.markdown(f"**{i}.** {step}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📥 Export Your Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📄 PDF Report",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📋 JSON Data",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📝 Text File",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain",
                use_container_width=True
            )
        
        with col4:
            if st.button("🔄 New Assessment", use_container_width=True):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.rerun()


def traverse_tree_interactive(tree, node_id, answers, path_so_far):
    """Interactively traverse the tree"""
    nodes = tree["nodes"]
    node = nodes[node_id]
    
    node_label = node.get("text", "")
    node_type = node.get("type", "choice")
    
    if node_type == "choice":
        current_question = len(answers) + 1
        st.markdown(f"### Question {current_question}")
        
        options = list(node["options"].keys())
        
        if node_id in answers:
            selected = answers[node_id]
        else:
            selected = st.radio(
                node_label, 
                options, 
                key=f"{tree['id']}_{node_id}",
                index=None
            )
            
            if selected is None:
                return None, None, path_so_far
            
            answers[node_id] = selected
        
        path_entry = f"{node_label} → {selected}"
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
        st.warning(f"⚠️ Unknown node type: {node_type}")
        return None, None, path_so_far


def main():
    if 'show_landing' not in st.session_state:
        st.session_state.show_landing = True
    
    if st.session_state.show_landing:
        show_landing_page()
    else:
        show_assessment_page()


if __name__ == "__main__":
    main()