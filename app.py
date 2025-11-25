import json
from pathlib import Path

import streamlit as st


# ---------- CONFIG ----------

BASE_DIR = Path(__file__).parent
LOGIC_DIR = BASE_DIR / "logic"

TREE_FILES = {
    "Incident Reporting": "incident_reporting.json",
    "Vendor Risk Tiering": "vendor_tiering.json",
    "DPIA Requirement": "dpia_requirement.json",
}


# ---------- HELPERS ----------

def load_tree(file_name: str) -> dict:
    """
    Load a decision tree from a JSON file in the logic/ folder.
    """
    file_path = LOGIC_DIR / file_name
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_tree(tree: dict):
    """
    Generic engine to run any decision tree defined in JSON.

    JSON structure expected:
    {
      "id": "...",
      "title": "...",
      "description": "...",
      "root": "q1",
      "nodes": {
        "q1": {
          "text": "Question?",
          "type": "choice",
          "options": {
            "Yes": {"next": "q2"},
            "No":  {"decision": "ACCEPT", "explanation": "..."}
          }
        },
        ...
      }
    }
    """
    nodes = tree.get("nodes", {})
    current_id = tree.get("root")
    path = []
    decision = None
    explanation = None

    # Defensive checks
    if not current_id or current_id not in nodes:
        st.error("Tree definition is missing a valid root node.")
        return None, None, []

    # Walk through the tree
    while True:
        node = nodes.get(current_id)
        if not node:
            st.error(f"Node '{current_id}' is missing in the tree.")
            break

        node_type = node.get("type", "choice")

        if node_type == "choice":
            question_text = node.get("text", "")
            options_dict = node.get("options", {})

            if not options_dict:
                st.error(f"Node '{current_id}' has no options defined.")
                break

            # Display the question
            st.markdown(f"**{question_text}**")
            options = list(options_dict.keys())

            # NOTE: Streamlit always selects something by default.
            # That is fine for now – users can change the option.
            choice = st.radio(
                "Select an option:",
                options,
                key=f"node_{current_id}",
            )

            path.append(f"{question_text} → {choice}")

            target = options_dict.get(choice, {})

            # Move to next node or finish with a decision
            if "next" in target:
                current_id = target["next"]
                continue
            elif "decision" in target:
                decision = target.get("decision")
                explanation = target.get("explanation", "")
                break
            else:
                st.error(f"Option '{choice}' in node '{current_id}' has no 'next' or 'decision'.")
                break

        else:
            st.error(f"Unsupported node type '{node_type}' in node '{current_id}'.")
            break

    return decision, explanation, path


# ---------- STREAMLIT APP ----------

def main():
    st.set_page_config(page_title="DecisionGuide", page_icon="🧭", layout="centered")

    st.title("DecisionGuide")
    st.write("A simple, logic-based assistant for governance and audit decisions.")

    st.markdown("---")

    # Select which tree to run
    tree_name = st.selectbox(
        "Select a decision guide to run:",
        ["Select..."] + list(TREE_FILES.keys()),
    )

    if tree_name == "Select...":
        st.info("Choose a guide from the dropdown above to begin.")
        return

    # Load the corresponding JSON tree
    file_name = TREE_FILES.get(tree_name)
    try:
        tree = load_tree(file_name)
    except FileNotFoundError:
        st.error(f"Could not find logic file for '{tree_name}'. Expected '{file_name}'.")
        return
    except json.JSONDecodeError:
        st.error(f"Logic file '{file_name}' is not valid JSON.")
        return

    # Show tree metadata
    st.markdown(f"### {tree.get('title', tree_name)}")
    if tree.get("description"):
        st.write(tree["description"])

    st.markdown("---")

    # Run the tree
    decision, explanation, path = run_tree(tree)

    st.markdown("---")

    # Output
    if decision:
        st.subheader("Decision")
        st.write(decision)

    if explanation:
        st.subheader("Explanation")
        st.write(explanation)

    if path:
        if st.checkbox("Show decision path"):
            st.subheader("Path taken")
            for step in path:
                st.write("•", step)


if __name__ == "__main__":
    main()