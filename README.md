# E. coli Oxygen response: An Automated RNA-seq Analysis Pipeline  
Comprehensive analysis of *Escherichia coli* gene expression dynamics during anaerobic to aerobic transition using RNA-seq.

---

## Table of Contents
- Description of the Project  
- Dataset  
- Installation  
- Prerequisites  
- Expected Outputs  
- Usage  
- Run Specific Analyses  
- Configuration  
- Troubleshooting  
- Authors and Acknowledgments  
- License  
- Citation  

---

## Description of the Project

This project is an assignment for the **Laboratório de Bioinformática** course (3rd year, *Licenciatura em Bioinformática*).

*Escherichia coli* is able to shift between anaerobic and aerobic metabolism by rapidly adapting its gene expression. This study re-analyzes publicly available RNA-seq data examining gene expression dynamics after an anaerobic to aerobic shift on a very short time scale (0.5, 1, 2, 5, and 10 minutes).

The main goal of this project is to create an automated and reproducible RNA-seq analysis pipeline that performs:

- Differential gene expression analysis  
- Functional enrichment  
- Co-expression network analysis  
- Metabolic pathway visualization  

The pipeline automatically processes raw sequencing data using Snakemake rules for:

- Quality control  
- Read trimming  
- Alignment  
- Read counting  

These steps generate a unified gene expression matrix, which serves as the main input for all downstream analyses.

After preprocessing, the pipeline:

- Identifies differentially expressed genes using DESeq2  
- Determines early responding metabolic pathways through KEGG enrichment  
- Discovers co-expressed gene modules using WGCNA
- Visualizes pathway-level changes using Pathview  

All raw FASTQ files are automatically downloaded from NCBI SRA using accession numbers provided in:

```
config/SraRunTable.csv
```

---

## Dataset

The dataset comes from NCBI GEO under the accession GSE71562 (published July 1, 2016).

#Organism: Escherichia coli K-12 strain W3110  
#Experimental design:
- Anaerobic growth at pH 7 and 37°C  
- Aeration at 1 L/min when OD₆₀₀ reached 3  
- Sampling at: 0, 0.5, 1, 2, 5, and 10 minutes  
- 3 biological replicates per timepoint  
- Total: 18 RNA-seq samples  

#Source:  
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE71562  

---

## Installation

Clone the repository:

```bash
git clone https://gitlab.com/lbinf2025-2026/sem-paciencia/ecoli_oxygen_survival.git
cd ecoli_oxygen_survival
```

Create the Snakemake environment:

```bash
conda create -n snakemake -c conda-forge -c bioconda snakemake
conda activate snakemake
```

Verify installation:

```bash
snakemake --version
```

---

## Prerequisites

- **conda 25.7.0** – Environment management  
- **git 2.34.1** – Repository cloning  

---

## Expected Outputs

### Differential Expression
- `TOP_GENES_UP.csv`  
- `TOP_GENES_DOWN.csv`  
- `heatmap_global.pdf`  
- `plot_top_gene.png`  

### Pathway Analysis
- `kegg_dotplot.pdf`  
- `eco00190.pathview.png`  
- `eco00910.pathview.png`  

### Co-expression Networks
- Gene modules  
- Module–trait correlations  
- Hub genes  

### Quality Metrics
- FastQC reports  
- Alignment statistics  
- Gene count distributions  

---

## Usage

Activate the environment:

```bash
conda activate snakemake
```

Navigate to the worflow directory:

```bash
cd RNAseq_Project/worflow
```

Dry run:

```bash
snakemake --dry-run --cores all --use-conda
```

Run the full pipeline:

```bash
snakemake --cores all --use-conda
```

---

## Run Specific Analyses

```bash
snakemake <desired_output_path> --cores all --use-conda
```

Examples:

```bash
snakemake results/TOP_GENES_UP.csv --cores all --use-conda
snakemake results/kegg_dotplot.pdf --cores all --use-conda
```

---

## Configuration

Edit:

```
config/config.yaml
```

Example:

```yaml
samples_csv: "data/SraRunTable.csv"
reference_fasta: "https://..."
reference_gtf: "https://..."
threads: 4
```

---

## Troubleshooting

**Problem:** snakemake not found  
**Solution:**
```bash
conda activate snakemake
```

**Problem:** Out of memory  
**Solution:**
```bash
--resources mem_mb=8000
```

**Problem:** File not found  
**Solution:**
```bash
snakemake --cores all --use-conda
```

**Problem:** KEGG returns no results  
**Solution:**  
Check:
```
objetos_temp/gene_list_entrez.rds
```

---

## Authors and Acknowledgments

**Authors:**
- Maria Oliveira  
- Sara Sampaio  
- Afonso Manso  
- Acacia Santos  

---

## License

MIT License  
Copyright (c) 2026  

---

## Citation

```text
Santos, A., Sampaio, S., Manso, A., & Eduarda, M. (2026).
E. coli Oxygen Survival: Gene Expression Analysis Pipeline.
Laboratório de Bioinformática, Licenciatura em Bioinformática.
https://gitlab.com/lbinf2025-2026/sem-paciencia/ecoli_oxygen_survival
```
