import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


st.set_page_config(
    page_title="DecisionGuide",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Tech Design CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background: #0a0e27;
    }
    
    /* Hero Section - Dark Tech */
    .hero-section {
        background: linear-gradient(135deg, #1a2332 0%, #0a0e27 100%);
        padding: 5rem 2rem;
        text-align: center;
        border-radius: 0;
        position: relative;
        overflow: hidden;
        margin-bottom: 0;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(52, 211, 153, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .logo-compass {
        font-size: 6rem;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
        filter: drop-shadow(0 0 20px rgba(52, 211, 153, 0.5));
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }
    
    .hero-tagline {
        font-size: 1.5rem;
        font-weight: 600;
        color: #34d399;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 700px;
        margin: 0 auto 2.5rem auto;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    .cta-button {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4);
    }
    
    /* Feature Cards Section */
    .features-section {
        background: #0f172a;
        padding: 5rem 2rem;
    }
    
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 4rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(52, 211, 153, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .feature-icon-wrapper {
        width: 80px;
        height: 80px;
        margin: 0 auto 1.5rem auto;
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid rgba(52, 211, 153, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.75rem;
    }
    
    .feature-description {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.7;
    }
    
    /* Assessment Cards */
    .assessments-section {
        background: #0a0e27;
        padding: 5rem 2rem;
    }
    
    .assessment-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .assessment-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .assessment-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #34d399);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .assessment-card:hover::before {
        transform: scaleX(1);
    }
    
    .assessment-card:hover {
        transform: translateY(-5px);
        border-color: rgba(52, 211, 153, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .assessment-number {
        font-size: 0.85rem;
        font-weight: 600;
        color: #34d399;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .assessment-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
    }
    
    .assessment-description {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.7;
        flex-grow: 1;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.9rem 2rem;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
    }
    
    /* Footer */
    .footer-section {
        background: #0f172a;
        padding: 4rem 2rem;
        text-align: center;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .footer-text {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    .footer-links a {
        color: #34d399;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: 500;
    }
    
    .footer-links a:hover {
        color: #3b82f6;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .feature-grid,
        .assessment-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
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
    """Professional tech-inspired landing page"""
    
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='logo-compass'>🧭</div>
        <h1 class='hero-title'>Navigate GRC Complexities with Confidence</h1>
        <p class='hero-tagline'>Standardized, Transparent, and Audit-Ready Decision-Making</p>
        <p class='hero-subtitle'>
            For Governance, Risk, and Compliance professionals who need consistent, 
            defensible decisions through structured logic flows.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class='features-section'>
        <h2 class='section-title'>Why DecisionGuide?</h2>
        <p class='section-subtitle'>Built for GRC professionals who demand excellence</p>
        
        <div class='feature-grid'>
            <div class='feature-card'>
                <div class='feature-icon-wrapper'>🔒</div>
                <div class='feature-title'>Privacy-First</div>
                <div class='feature-description'>
                    Zero-document approach means no file uploads, no data collection. 
                    All processing happens locally.
                </div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper'>📋</div>
                <div class='feature-title'>Audit-Ready Reports</div>
                <div class='feature-description'>
                    Automated documentation with complete decision trails. 
                    Export in PDF, JSON, or TXT formats.
                </div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper'>⚙️</div>
                <div class='feature-title'>Customizable Logic</div>
                <div class='feature-description'>
                    Extend with JSON trees. Add your own frameworks 
                    without writing code.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Assessments Section
    st.markdown("""
    <div class='assessments-section'>
        <h2 class='section-title'>Available Assessments</h2>
        <p class='section-subtitle'>Choose a framework to begin your evaluation</p>
    """, unsafe_allow_html=True)
    
    trees = load_trees()
    assessment_numbers = ["01", "02", "03"]
    
    # Assessment cards HTML
    cards_html = "<div class='assessment-grid'>"
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        cards_html += f"""
        <div class='assessment-card'>
            <div class='assessment-number'>{assessment_numbers[idx] if idx < len(assessment_numbers) else f"0{idx+1}"}</div>
            <div class='assessment-title'>{tree_data.get('title', 'Assessment')}</div>
            <div class='assessment-description'>{tree_data.get('description', '')}</div>
        </div>
        """
    cards_html += "</div>"
    
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # Buttons
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(len(trees))
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx]:
            if st.button(f"Start Assessment →", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='footer-section'>
        <p class='footer-text'>
            <strong>DecisionGuide</strong> — Making structured, smart decisions, one at a time.
        </p>
        <p class='footer-text'>
            Built with empathy for professionals who need clarity in complex assessments.
        </p>
        <div class='footer-links' style='margin-top: 2rem;'>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>GitHub</a>
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>Contribute</a>
        </div>
        <p style='color: #475569; margin-top: 2rem; font-size: 0.85rem;'>
            Open Source • MIT License
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
        st.info(f"📊 Question {current_question}")
        st.markdown("---")
        
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
        st.warning(f"Unknown node type: {node_type}")
        return None, None, path_so_far


def show_assessment_page():
    """Display the assessment page"""
    trees = load_trees()
    
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
    
    st.title(tree.get("title", "Assessment"))
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
        
        st.markdown("### Result")
        st.write(f"**Decision code:** {result['decision']}")
        if result['explanation']:
            st.write(result['explanation'])

        st.markdown("### Path taken")
        for step in result['path']:
            st.write(f"- {step}")
        
        st.markdown("---")
        st.markdown("### Export Options")
        
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
            if st.button("🔄 Start over"):
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
