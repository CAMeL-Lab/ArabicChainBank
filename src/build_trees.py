import pandas as pd
import os
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"TreeNode({self.value})"

def build_tree_from_df(df, parent_row):
    """Recursively build a tree structure from a DataFrame."""
    parent = TreeNode({
        "ROOT": parent_row["ROOT"],
        "LEMMA": parent_row["LEMMA"],
        "POS": parent_row["POS"],
        "LEMMA_ARA": parent_row["LEMMA_ARA"],
        "DER_CLASS": parent_row["CHILD_DER_CAT"],
        "GLOSS": parent_row["GLOSS"],
        "FUNCTION": parent_row["FUNCTION"],
        "PATTERN_ABSTRACT": parent_row["PATTERN_ABSTRACT"]
    })

    children_df = df[
        (df["PARENT_POS"] == parent_row["POS"]) & 
        (df["PARENT_PATTERN_ABSTRACT"] == parent_row["PATTERN_ABSTRACT"])
    ].drop_duplicates(subset=["LEMMA", "PATTERN_ABSTRACT"])

    for _, child_row in children_df.iterrows():
        child_node = build_tree_from_df(df, child_row)
        parent.add_child(child_node)

    return parent

def extract_tree_to_df(node, parent=None, rows=None):
    if rows is None:
        rows = []

    if parent:
        rows.append({
            "ROOT": node.value["ROOT"],
            "LEMMA": node.value["LEMMA"],
            "POS": node.value["POS"],
            "LEMMA_ARA": node.value["LEMMA_ARA"],
            "DER_CLASS": node.value["DER_CLASS"],
            "GLOSS": node.value["GLOSS"],
            "FUNCTION": node.value["FUNCTION"],
            "PATTERN_ABSTRACT": node.value["PATTERN_ABSTRACT"],
            "PARENT_LEMMA": parent.value["LEMMA"],
            "PARENT_POS": parent.value["POS"],
            "PARENT_LEMMA_ARA": parent.value["LEMMA_ARA"],
            "PARENT_DER_CLASS": parent.value["DER_CLASS"],
            "PARENT_GLOSS": parent.value["GLOSS"],
            "PARENT_FUNCTION": parent.value["FUNCTION"],
            "PARENT_PATTERN_ABSTRACT": parent.value["PATTERN_ABSTRACT"]
        })

    for child in node.children:
        extract_tree_to_df(child, node, rows)

    return rows

def run_tree_builder(input_file: Path, output_file: Path):
    try:
        df = pd.read_csv(input_file)
        required_columns = {
            "ROOT", "LEMMA", "POS", "CHILD_DER_CAT", "GLOSS", "FUNCTION",
            "PARENT_POS", "PARENT_PATTERN_ABSTRACT", "PATTERN_ABSTRACT", "LEMMA_ARA"
        }

        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Missing required columns: {missing}")

        all_tree_data = []
        for root, dataset_df in df.groupby("ROOT"):
            root_rows = dataset_df[dataset_df["POS"] == "ROOT"]
            if root_rows.empty:
                logging.warning(f"No 'ROOT' found for root '{root}'. Skipping this tree.")
                continue

            root_row = root_rows.iloc[0]
            tree = build_tree_from_df(dataset_df, root_row)
            tree_rows = extract_tree_to_df(tree)
            all_tree_data.extend(tree_rows)

        tree_df = pd.DataFrame(all_tree_data)
        tree_df.to_csv(output_file, index=False)
        logging.info(f"Build process completed successfully. Output saved to: {output_file}")

    except Exception as e:
        logging.error(f"Error during build process: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.csv> <output_file.csv>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    run_tree_builder(input_file, output_file)

if __name__ == "__main__":
    main()
