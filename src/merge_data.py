import pandas as pd
import numpy as np
import os
import logging
import sys
from pathlib import Path


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_csv(file_path):
    """Load a CSV file and return a DataFrame."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return pd.read_csv(file_path)


def process_lemma(df_lemma):
    """Group by 'ROOT' and insert new rows with 'ROOT' values in 'PATTERN_ABSTRACT' and 'POS'."""
    if 'ROOT' not in df_lemma.columns:
        raise KeyError("Column 'ROOT' is missing from the LEMMA dataset.")

    new_rows = [pd.DataFrame({
        'ROOT': [root],
        'PATTERN_ABSTRACT': ['ROOT'],
        'POS': ['ROOT'],
        'LEMMA': [root]
    }) for root, group in df_lemma.groupby('ROOT')]

    return pd.concat(new_rows + [df_lemma], ignore_index=True)


def merge_and_clean_data(df_lemma, df_relations):
    """Merge LEMMA and RELATIONS dataframes and clean the merged data."""
    merged_data = pd.merge(df_lemma, df_relations, on=['PATTERN_ABSTRACT', 'POS'], how='inner')
    merged_data.drop_duplicates(inplace=True)
    merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    merged_data.fillna('', inplace=True)
    return merged_data.astype(str)


def save_to_csv(df, file_path):
    """Save DataFrame to CSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    logging.info(f"Successfully written {len(df)} rows to '{file_path}'.")


def run_merge(canonical_data_file, lemma_file, merged_file):
    """Run the data merging process."""
    try:
        df_relations = load_csv(canonical_data_file)
        df_lemma = load_csv(lemma_file)

        df_lemma.drop_duplicates(inplace=True)
        df_lemma = process_lemma(df_lemma)

        merged_data = merge_and_clean_data(df_lemma, df_relations)
        save_to_csv(merged_data, merged_file)

        logging.info("Merge process completed successfully.")

    except Exception as e:
        logging.error(f"Error during merging process: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 4:
        logging.error("Invalid number of arguments.")
        print(sys.argv[0])
        sys.exit(1)

    canonical_data_file = Path(sys.argv[1])
    lemma_file = Path(sys.argv[2])
    merged_file = Path(sys.argv[3])

    run_merge(canonical_data_file, lemma_file, merged_file)


if __name__ == "__main__":
    main()
