import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


# Basic page config
st.set_page_config(
    page_title="DecisionGuide",
    page_icon="🎯",
    layout="centered",
)


# Minimal, calm styling
st.markdown(
    """
<style>
    /* Hide Streamlit default bits */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background-color: #f5f5f7;
    }

    .dg-shell {
        max-width: 900px;
        margin: 0 auto;
        padding: 2.5rem 2rem;
        background: #ffffff;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    }

    .dg-header-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #111827;
        margin-bottom: 0.25rem;
    }

    .dg-header-tagline {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 1.2rem;
    }

    .dg-badge {
        display: inline-block;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        background: #eef2ff;
        color: #4f46e5;
        margin-bottom: 0.75rem;
    }

    .dg-section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.4rem;
    }

    .dg-section-text {
        font-size: 0.95rem;
        color: #6b7280;
        line-height: 1.55;
    }

    .dg-assessment-card {
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        background: #f9fafb;
        transition: background 0.2s ease, border-color 0.2s ease;
    }

    .dg-assessment-card:hover {
        background: #eef2ff;
        border-color: #4f46e5;
    }

    .dg-assessment-title {
        font-size: 0.98rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.15rem;
    }

    .dg-assessment-desc {
        font-size: 0.85rem;
        color: #6b7280;
    }

    .dg-footer {
        margin-top: 1.75rem;
        font-size: 0.85rem;
        color: #9ca3af;
        text-align: center;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 999px;
        padding: 0.45rem 1.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid #4f46e5;
        color: #ffffff;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
    }
    .stButton>button:hover {
        filter: brightness(1.03);
    }

    .stDownloadButton>button {
        border-radius: 999px;
        padding: 0.4rem 0.9rem;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #4f46e5;
        color: #ffffff;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
    }

    @media (max-width: 600px) {
        .dg-shell {
            padding: 1.5rem 1.2rem;
            border-radius: 0;
            margin: 0;
            box-shadow: none;
        }
        .dg-header-title {
            font-size: 1.6rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


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


def traverse_tree_interactive(tree, node_id, answers, path_so_far):
    """Interactively walk the tree based on stored answers + current choice."""
    nodes = tree["nodes"]
    node = nodes[node_id]

    node_label = node.get("text", "")
    node_type = node.get("type", "choice")

    if node_type == "choice":
        question_index = len(path_so_far) + 1
        st.markdown(f"**Question {question_index}**")
        st.write(node_label)

        options = list(node["options"].keys())

        # Persist answer in session
        if node_id in answers:
            selected = answers[node_id]
        else:
            selected = st.radio(
                "Select an option:",
                options,
                index=None,
                key=f"{tree['id']}_{node_id}",
            )
            if selected is None:
                st.write("")  # spacing
                return None, None, path_so_far
            answers[node_id] = selected

        path_entry = f"{node_label} → {selected}"
        new_path = path_so_far + [path_entry]

        selected_branch = node["options"][selected]

        # End of branch with decision
        if "decision" in selected_branch:
            decision = selected_branch["decision"]
            explanation = selected_branch.get("explanation", "")
            return decision, explanation, new_path

        # Continue to next question
        next_node = selected_branch["next"]
        st.write("")  # spacing between questions
        return traverse_tree_interactive(tree, next_node, answers, new_path)

    elif node_type == "text":
        st.markdown(node_label)
        return None, None, path_so_far + [node_label]

    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, path_so_far


def render_dpia_jurisdiction_block():
    """Extra guidance shown only after DPIA decision."""
    st.markdown("---")
    st.markdown("#### Jurisdiction-specific pointers")

    region = st.selectbox(
        "Which jurisdiction are you mainly working under?",
        [
            "Select...",
            "UK / ICO (UK GDPR / DPA 2018)",
            "EU / EDPB (EU GDPR)",
            "US (HIPAA / state privacy laws)",
            "Nigeria (NDPR)",
            "Other / mixed",
        ],
        index=0,
        key="dpia_jurisdiction",
    )

    if region == "Select...":
        return

    if region.startswith("UK"):
        st.markdown(
            "- Check UK GDPR Article 35 and ICO guidance on when a DPIA is mandatory.\n"
            "- If CCTV, large-scale monitoring, or profiling is involved, verify against ICO DPIA examples.\n"
            "- Use ICO DPIA templates to structure documentation."
        )
    elif region.startswith("EU"):
        st.markdown(
            "- Refer to EU GDPR Article 35 and EDPB guidelines on DPIA.\n"
            "- Check your activity against your authority’s DPIA 'blacklist' and 'whitelist'.\n"
            "- Ensure you can evidence DPO consultation where required."
        )
    elif region.startswith("US"):
        st.markdown(
            "- Map your DPIA-style assessment to HIPAA Security Rule risk analysis requirements if health data is involved.\n"
            "- Consider state privacy laws (for example CPRA) where high-risk processing or profiling is in scope.\n"
            "- Treat this as a structured impact assessment even if the term 'DPIA' is not used."
        )
    elif region.startswith("Nigeria"):
        st.markdown(
            "- Align to NDPR requirements for high-risk processing.\n"
            "- Check any NITDA guidance for sector expectations.\n"
            "- Pay attention to cross-border transfers and local hosting expectations."
        )
    else:
        st.markdown(
            "- Align your assessment with any applicable local privacy or sector law.\n"
            "- Where no formal DPIA requirement exists, treat this as evidence of responsible risk analysis.\n"
            "- Make sure your reasoning and mitigations are clearly documented."
        )


def show_landing_page():
    trees = load_trees()

    st.markdown("<div class='dg-shell'>", unsafe_allow_html=True)

    st.markdown("<div class='dg-badge'>Open source • GRC-focused</div>", unsafe_allow_html=True)
    st.markdown("<div class='dg-header-title'>DecisionGuide</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='dg-header-tagline'>A lightweight, logic-based assistant for governance, risk, and audit decisions.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='dg-section-text'>"
        "Use clear, predefined assessment logic instead of guesswork. No uploads, no sensitive data, "
        "just structured questions that lead to consistent, defensible outcomes."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("<div class='dg-section-title'>Available guides</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='dg-section-text'>Pick an assessment to start a structured decision flow.</div>",
            unsafe_allow_html=True,
        )
        st.write("")

        for tree_id, tree in trees.items():
            title = tree.get("title", "Assessment")
            desc = tree.get("description", "")

            st.markdown("<div class='dg-assessment-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='dg-assessment-title'>{title}</div>", unsafe_allow_html=True)
            if desc:
                st.markdown(
                    f"<div class='dg-assessment-desc'>{desc}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button(f"Start “{title}”", key=f"start_{tree_id}"):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                # reset state for this tree
                st.session_state.pop(f"answers_{tree_id}", None)
                st.session_state.pop(f"result_{tree_id}", None)
                st.experimental_rerun()

    with col_right:
        st.markdown("<div class='dg-section-title'>What DecisionGuide does</div>", unsafe_allow_html=True)
        st.markdown(
            """
<ul class='dg-section-text'>
    <li>Standardises vendor and incident decisions using shared logic.</li>
    <li>Supports GRC teams with clean, repeatable assessments.</li>
    <li>Exports decision paths for audit and documentation.</li>
    <li>Stays privacy-friendly by keeping everything in the browser.</li>
</ul>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='dg-footer'>Open source • MIT Licence • Built for students, analysts, and GRC teams.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def show_assessment_page():
    trees = load_trees()

    if st.button("← Back to home"):
        st.session_state.show_landing = True
        st.session_state.pop("selected_tree", None)
        st.experimental_rerun()

    st.markdown("<div class='dg-shell'>", unsafe_allow_html=True)

    selected_tree_id = st.session_state.get("selected_tree")
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("Assessment not found.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    tree = trees[selected_tree_id]

    st.markdown("<div class='dg-badge'>Assessment</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='dg-header-title'>{tree.get('title', 'Assessment')}</div>",
        unsafe_allow_html=True,
    )
    if tree.get("description"):
        st.markdown(
            f"<div class='dg-header-tagline'>{tree['description']}</div>",
            unsafe_allow_html=True,
        )

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
        [],
    )

    if decision is not None:
        st.session_state[result_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path,
        }

    result = st.session_state[result_key]

    if result is not None:
        st.markdown("---")
        st.success("Assessment complete.")

        st.markdown("#### Result")
        st.write(f"**Decision code:** {result['decision']}")
        if result["explanation"]:
            st.write(result["explanation"])

        st.markdown("#### Path taken")
        for step in result["path"]:
            st.write(f"- {step}")

        # DPIA extra guidance
        if selected_tree_id.startswith("dpia"):
            render_dpia_jurisdiction_block()

        st.markdown("---")
        st.markdown("#### Export")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result["decision"],
                result["explanation"],
                result["path"],
            )
            st.download_button(
                label="📄 PDF",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf",
            )

        with col2:
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result["decision"],
                result["explanation"],
                result["path"],
            )
            st.download_button(
                label="📋 JSON",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json",
            )

        with col3:
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result["decision"],
                result["explanation"],
                result["path"],
            )
            st.download_button(
                label="📝 TXT",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain",
            )

        with col4:
            if st.button("🔄 Start over"):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    if "show_landing" not in st.session_state:
        st.session_state.show_landing = True

    if st.session_state.show_landing:
        show_landing_page()
    else:
        show_assessment_page()


if __name__ == "__main__":
    main()