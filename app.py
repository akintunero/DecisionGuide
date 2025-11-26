import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


st.set_page_config(
    page_title="DecisionGuide",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimalist Luxury CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Elegant background */
    .stApp {
        background: #fafafa;
    }
    
    /* Minimalist hero */
    .hero-section {
        text-align: center;
        padding: 6rem 2rem 4rem 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .logo-mark {
        font-size: 4rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 300;
        letter-spacing: -1px;
        color: #1a1a1a;
        margin-bottom: 1.5rem;
    }
    
    .hero-title strong {
        font-weight: 700;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        color: #666;
        line-height: 1.8;
        max-width: 700px;
        margin: 0 auto 3rem auto;
    }
    
    .divider {
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #1a1a1a, transparent);
        margin: 3rem auto;
        opacity: 0.3;
    }
    
    /* Feature cards - minimal */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        max-width: 1200px;
        margin: 3rem auto;
        padding: 0 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 2.5rem 2rem;
        border: 1px solid #e8e8e8;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .feature-card:hover {
        border-color: #1a1a1a;
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.75rem;
        letter-spacing: -0.3px;
    }
    
    .feature-text {
        font-size: 0.95rem;
        color: #666;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Section headers */
    .section-header {
        text-align: center;
        max-width: 800px;
        margin: 5rem auto 3rem auto;
        padding: 0 2rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: #1a1a1a;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: #666;
        font-weight: 400;
    }
    
    /* Assessment cards - minimal luxury */
    .assessment-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .assessment-card {
        background: white;
        border: 1px solid #e8e8e8;
        padding: 3rem 2rem;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .assessment-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #1a1a1a, #666);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .assessment-card:hover::before {
        transform: scaleX(1);
    }
    
    .assessment-card:hover {
        border-color: #1a1a1a;
        transform: translateY(-6px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.1);
    }
    
    .assessment-number {
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
    }
    
    .assessment-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .assessment-description {
        font-size: 0.95rem;
        color: #666;
        line-height: 1.7;
        flex-grow: 1;
    }
    
    /* Use cases - refined */
    .use-case-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
        max-width: 1200px;
        margin: 3rem auto;
        padding: 0 2rem;
    }
    
    .use-case-card {
        background: white;
        border: 1px solid #e8e8e8;
        padding: 2.5rem;
    }
    
    .use-case-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .use-case-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .use-case-list li {
        padding: 0.75rem 0;
        color: #666;
        font-size: 0.95rem;
        border-bottom: 1px solid #f5f5f5;
        line-height: 1.6;
    }
    
    .use-case-list li:last-child {
        border-bottom: none;
    }
    
    .use-case-list li::before {
        content: '—';
        margin-right: 0.75rem;
        color: #1a1a1a;
        font-weight: 600;
    }
    
    /* CTA section */
    .cta-section {
        background: #1a1a1a;
        color: white;
        text-align: center;
        padding: 5rem 2rem;
        margin: 6rem 0 4rem 0;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    .cta-text {
        font-size: 1.1rem;
        color: #999;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.8;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 4rem 2rem;
        color: #999;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .footer-links {
        margin-bottom: 2rem;
    }
    
    .footer-links a {
        color: #1a1a1a;
        text-decoration: none;
        margin: 0 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        transition: opacity 0.2s ease;
    }
    
    .footer-links a:hover {
        opacity: 0.6;
    }
    
    .footer-note {
        font-size: 0.9rem;
        color: #666;
        line-height: 1.8;
        margin-top: 2rem;
    }
    
    /* Buttons - minimalist */
    .stButton>button {
        background: #1a1a1a;
        color: white;
        border: 1px solid #1a1a1a;
        padding: 1rem 2.5rem;
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background: white;
        color: #1a1a1a;
        border: 1px solid #1a1a1a;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .feature-grid,
        .assessment-grid,
        .use-case-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .section-title {
            font-size: 2rem;
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
    """Minimalist luxury landing page"""
    
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='logo-mark'>◈</div>
        <h1 class='hero-title'><strong>Decision</strong>Guide</h1>
        <p class='hero-subtitle'>
            Open-source assessment framework for GRC professionals.
            Make consistent, defensible decisions through structured logic flows.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div class='feature-grid'>
        <div class='feature-card'>
            <div class='feature-icon'>○</div>
            <div class='feature-title'>Transparent</div>
            <div class='feature-text'>Clear decision paths with complete reasoning trails</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>◇</div>
            <div class='feature-title'>Private</div>
            <div class='feature-text'>Zero-document approach, all processing local</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>◈</div>
            <div class='feature-title'>Professional</div>
            <div class='feature-text'>Audit-ready exports in multiple formats</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section Header
    st.markdown("""
    <div class='section-header'>
        <div class='divider'></div>
        <h2 class='section-title'>Assessments</h2>
        <p class='section-subtitle'>Choose a framework to begin your evaluation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Assessment Cards
    trees = load_trees()
    
    assessment_numbers = ["01", "02", "03"]
    
    cards_html = "<div class='assessment-grid'>"
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        cards_html += f"""
        <div class='assessment-card'>
            <div>
                <div class='assessment-number'>{assessment_numbers[idx] if idx < len(assessment_numbers) else f"0{idx+1}"}</div>
                <div class='assessment-title'>{tree_data.get('title', 'Assessment')}</div>
                <div class='assessment-description'>{tree_data.get('description', '')}</div>
            </div>
        </div>
        """
    cards_html += "</div>"
    
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # Buttons for assessments
    cols = st.columns(len(trees))
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx]:
            if st.button(f"Begin", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
    
    # Use Cases Section
    st.markdown("""
    <div class='section-header'>
        <div class='divider'></div>
        <h2 class='section-title'>Built For Professionals</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='use-case-grid'>
        <div class='use-case-card'>
            <div class='use-case-title'>Auditors & Compliance</div>
            <ul class='use-case-list'>
                <li>Standardize assessment approaches</li>
                <li>Generate defensible documentation</li>
                <li>Ensure regulatory compliance</li>
            </ul>
        </div>
        <div class='use-case-card'>
            <div class='use-case-title'>Risk & Security Teams</div>
            <ul class='use-case-list'>
                <li>Classify risks systematically</li>
                <li>Document decision rationale</li>
                <li>Maintain audit trails</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div class='cta-section'>
        <h2 class='cta-title'>Ready to begin?</h2>
        <p class='cta-text'>
            Join GRC professionals using DecisionGuide for consistent, 
            transparent assessments backed by structured logic.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <div class='footer-links'>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>GitHub</a>
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>Contribute</a>
            <a href='#'>Documentation</a>
        </div>
        <div class='divider'></div>
        <p class='footer-note'>
            <strong>DecisionGuide</strong> — Making structured, smart decisions, one at a time.<br>
            Built with empathy for professionals who need clarity in complex assessments.
        </p>
        <p style='margin-top: 2rem; font-size: 0.85rem; color: #999;'>
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
        st.info(f"Question {current_question}")
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
    
    # Back button
    if st.button("← Home"):
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
        st.success("✓ Assessment Complete")
        
        st.markdown("---")
        
        result = st.session_state[result_key]
        
        st.markdown("### Result")
        st.write(f"**Decision:** {result['decision']}")
        if result['explanation']:
            st.write(result['explanation'])

        st.markdown("### Decision Path")
        for step in result['path']:
            st.write(f"— {step}")
        
        st.markdown("---")
        st.markdown("### Export")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="PDF",
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
                label="JSON",
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
                label="TXT",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain"
            )
        
        with col4:
            if st.button("Reset"):
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