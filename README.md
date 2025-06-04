# Arabic ChainBank

## Introduction

This project presents version 1.0 of the Arabic ChainBank, the first derivational resource for Modern Standard Arabic. The ChainBank is designed to link all derivatives that belong to the same derivational family in the form of a chain, beginning with the root and progressing through successive derived forms. Each chain captures the relationships between a base form and its derivatives, offering insights into how words evolve morphologically while maintaining their semantic and grammatical connections. The Arabic ChainBank is composed of two primary data sources: a knowledge graph-based network of abstract patterns [abstract network](https://github.com/RMarzouk/Arabic_ChaiBank/blob/main/Abstract%20Network/CamelMorph_Alignment%20-%20CANONIC_DATA.tsv)  and the database of multidialectal morphological analyzer  [camel_morph](https://github.com/CAMeL-Lab/camel_morph).

![tree_chart.png](https://github.com/RMarzouk/Arabic-chainbank/blob/main/tree_chart.png)


## Data

The data for this version is extracted from CamelMorph v1.0, which provides the essential morphological features required for constructing the ChainBank [lemmas](). If you are only interested in replicating our experiment, you only need the data provided as a sample under the folder [data]()

## The ChainBank

The ChainBank introduces the alignment between the abstract network dataset and the CamelMorph dataset to construct derivational subtree for each root.  It streamlines the creation of structured derivational knowledge graphs, making it a valuable resource for linguistic analysis and computational morphology. 


This process is carried out in three main stages:

**Merging Data:** Integrating root data with the abstract network, src/DataMerging/merge_data.py.  
**Building Trees:** Recursively generating derivational trees starting from each root, src/TreeBuilding/build_tree.py.
**Visualizing Trees:** Creating graphical representations of the derivational structures, src\DataMerging\merge_data.py.

 If you are interested in running a sample of data to test the adopted method to build the Chainbank, you can follow the instrcutions as in the following section. To run them using the full data extracted from Camelmorph you should to add the directory of this data.

## Running Generation Scripts

Below are instructions on how to generate a ChainBank using an input dataset as well as how to generate visualization graphs for the ChainBank. 

**Note:** In the below code snippets, we use a smaller set of lemmas as input, data file `data/lemmas_sample.csv`. To generate the full ChainBank, use file `data/lemmas.csv` instead where appropriate.

### Prerequisites 
Before using the provided scrits, ensure you have the required libraries installed. You can install them using the following command:

```bash
pip install -r requirements.txt
```

### Merge_Data

Run the following command to merge the lemma data with the abstract network from ChainBank:

```
python src/merge_data.py data/abstract_network.csv data/lemmas_sample.csv output/merged.csv
```

This will generate a processed dataset that combines lemmas and the abstract network.

### Build the Derivational Trees

To construct the derivational trees using the merged data, execute:

```
python src/build_trees.py output/merged.csv output/trees.csv
```

This script recursively builds the tree structures for derivational relationships.

### Visualize the Derivational Trees

To generate and visualize the derivational trees, run:

```
python src/visualize_trees.py output/trees.csv output/trees.pdf
```

This will create a PDF file containing a graphical representation of the derivational relationships in the ChainBank dataset in forms of trees.

**IMPORTANT:** It is advised not to run this on the full dataset. This process is resource heavy and will generate a huge PDF file for the full data.

## License

The data files accessed through the below links are licensed under a Creative Commons Attribution 4.0 International License.

The scripts used for generating the data files are released under the [MIT license](./LICENSE).

## Authors

Reham Marzouk
Nizar Habash

## Citation 
The framwork of ChainBank 1.0 is introduced in a paper buplished in COLING 2025. If you find the database of Arabic ChainBank is useful in your research, please cite our [paper](https://aclanthology.org/2025.abjadnlp-1.9/)
