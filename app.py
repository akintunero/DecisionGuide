import json
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="DecisionGuide", layout="centered")


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
            # In production you might log this instead
            print(f"Failed to load {path}: {e}")
    return trees


def traverse_tree(tree, node_id, path_prefix=""):
    """
    Recursively walk a decision tree defined in JSON.
    Returns (decision_code, explanation, path_taken)
    """
    nodes = tree["nodes"]
    node = nodes[node_id]

    node_label = node.get("text", "")
    if path_prefix:
        display_label = f"{path_prefix} → {node_label}"
    else:
        display_label = node_label

    node_type = node.get("type", "choice")

    if node_type == "choice":
        options = list(node["options"].keys())
        choice = st.radio(display_label, options, key=f"{tree['id']}_{node_id}")
        st.write("")  # small spacing

        selected_branch = node["options"][choice]
        path_entry = f"{node_label} → {choice}"

        # If this branch leads directly to a decision
        if "decision" in selected_branch:
            decision = selected_branch["decision"]
            explanation = selected_branch.get("explanation", "")
            return decision, explanation, [path_entry]

        # Otherwise, go to next node
        next_node = selected_branch["next"]
        decision, explanation, sub_path = traverse_tree(tree, next_node, path_prefix="")
        return decision, explanation, [path_entry] + sub_path

    elif node_type == "text":
        st.markdown(display_label)
        return None, None, [node_label]

    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, []


def main():
    st.title("DecisionGuide")
    st.caption("One smart decision at a time.")

    trees = load_trees()
    if not trees:
        st.error("No decision trees found in the logic/ folder.")
        return

    # Sidebar: tree selection
    tree_options = {
        data.get("title", tree_id): tree_id for tree_id, data in trees.items()
    }
    selected_label = st.sidebar.selectbox(
        "Select a decision guide", list(tree_options.keys())
    )
    selected_tree_id = tree_options[selected_label]
    tree = trees[selected_tree_id]

    st.header(tree.get("title", "Decision Tree"))
    if tree.get("description"):
        st.markdown(tree["description"])

    st.markdown("---")
    st.markdown("### Answer the questions")

    # Initialize session state for this tree
    state_key = f"result_{selected_tree_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = None

    with st.form(key=f"form_{selected_tree_id}"):
        decision, explanation, path = traverse_tree(tree, tree["root"])
        submitted = st.form_submit_button("Run assessment")

    if submitted:
        if decision is None:
            st.warning("No decision reached. Please ensure all questions are answered.")
            return
        
        # Store result in session state
        st.session_state[state_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path
        }

    # Display result if it exists in session state
    if st.session_state[state_key] is not None:
        result = st.session_state[state_key]
        
        st.markdown("### Result")
        st.write(f"**Decision code:** {result['decision']}")
        if result['explanation']:
            st.write(result['explanation'])

        st.markdown("### Path taken")
        for step in result['path']:
            st.write(f"- {step}")


if __name__ == "__main__":
    main()
