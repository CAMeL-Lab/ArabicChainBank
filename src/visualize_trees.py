import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper
from matplotlib.backends.backend_pdf import PdfPages
import sys
from pathlib import Path

def visualize_trees(input_file: Path, output_file: Path):
    df = pd.read_csv(input_file)
    df[['PARENT_LEMMA_ARA', 'LEMMA_ARA']] = df[['PARENT_LEMMA_ARA', 'LEMMA_ARA']].fillna('')

    with PdfPages(output_file) as pdf:
        for root, group_df in df.groupby('ROOT'):
            G = nx.DiGraph()
            added_edges = set()

            for _, row in group_df.iterrows():
                source_node = f"{row['PARENT_LEMMA']}_{row['PARENT_POS']}"
                target_node = f"{row['LEMMA']}_{row['POS']}"

                parent_lemma_ara = str(row['PARENT_LEMMA_ARA']) if isinstance(row['PARENT_LEMMA_ARA'], str) else ""
                lemma_ara = str(row['LEMMA_ARA']) if isinstance(row['LEMMA_ARA'], str) else ""

                if source_node not in G:
                    G.add_node(source_node, 
                               label=f"{get_display(arabic_reshaper.reshape(parent_lemma_ara))} ({row['PARENT_LEMMA']})\nPOS: {row['PARENT_POS']}",
                               POS=row['PARENT_POS'])

                if target_node not in G:
                    G.add_node(target_node, 
                               label=f"{get_display(arabic_reshaper.reshape(lemma_ara))} ({row['LEMMA']})\nPOS: {row['POS']}",
                               POS=row['POS'])

                edge = (source_node, target_node)
                if edge not in added_edges:
                    G.add_edge(source_node, target_node, DER_CLASS=row['DER_CLASS'])
                    added_edges.add(edge)

            plt.figure(figsize=(14, 10))
            pos = nx.spring_layout(G)
            labels = {node: G.nodes[node]['label'] for node in G.nodes}
            nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=2000,
                    font_size=8, font_color='black', alpha=0.5)
            edge_labels = nx.get_edge_attributes(G, 'DER_CLASS')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
            plt.title(f'Derivational Tree for ROOT: {root}')

            pdf.savefig()
            plt.close()

    print(f"All derivational trees have been saved to: {output_file}")

def main():
    if len(sys.argv) != 3:
       
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    visualize_trees(input_file, output_file)

if __name__ == "__main__":
    main()


