---
layout: default
---

# Project 1: PTEN variant abundance

How do changes in a protein's sequence affect its abundance in cells? In this project, we will analyze measurements for thousands of variants of PTEN, a human protein involved in regulating cell growth. We will ask where substitutions are associated with lower measured abundance, look for patterns across the protein, and examine how our conclusions depend on the choices we make during analysis.

The data come from a **multiplexed assay of variant effect (MAVE)**. The experiment uses VAMP-seq, which combines a fluorescent reporter, cell sorting, and sequencing to estimate the abundance of many protein variants in parallel. This assay measures protein abundance; abundance alone does not tell us a variant's catalytic activity or whether it causes disease.

### Original paper

Matreyek, K. A. *et al.* (2018). **Multiplex assessment of protein variant abundance by massively parallel sequencing.** *Nature Genetics* **50**, 874–882. [[Paper](https://doi.org/10.1038/s41588-018-0122-z)] [[Free full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5980760/)]

# How the project works

The project spans six classes. The first is a warmup lecture, ending with a coding overview. After each of the first five classes, you will work with your team on an assignment that provides the starting point for the next class.

In Classes 2–5, most of our time will be devoted to discussing your work, asking questions, and planning the next analysis. Sometimes two teams will meet to present results and compare approaches; at other times, you will work within your own team. Bring your code, results, and questions, including things that did not work as expected.

1. **Warmup: from an experiment to a table.** Introduction to PTEN and VAMP-seq, principles of storing and analyzing data, and demonstrations of tabular analysis with pandas. **After class:** work with synthetic sequencing counts from sorted abundance bins to calculate and check simple abundance scores.
<!-- 2. **Discuss the toy analysis; begin the real data.** Compare scoring choices and results, then introduce files, folders, and project organization. **After class:** organize and inspect the PTEN datasets, checking variant labels, controls, missing values, and replicate measurements.
3. **Discuss the data audit; look for patterns.** Compare checks and decide what can be summarized meaningfully. **After class:** summarize abundance by position and protein region, make coverage and abundance displays, and develop a provisional biological claim.
4. **Discuss the patterns; test the claim.** Examine the evidence and the analysis choices behind it. **After class:** change one inclusion rule, compare its effect on the same outcome, and independently reproduce another team's result.
5. **Discuss robustness; plan an extension.** Resolve remaining issues in the core analysis and choose a focused new question. **After class:** carry out a small extension in a direction of your team's choice and prepare a brief presentation.
6. **Present your extension.** Explain your question, approach, evidence, and limitations, and discuss what you learned with the class. -->

# Team roles

Each team uses four roles. Rotate roles at the start of Session 4 so that you practice different parts of the work.

- **Biological lead:** keeps the biological question clear and checks that interpretations fit what the assay measures.
- **Computational designer:** helps turn the question into understandable analysis steps, data representations, and code.
- **Verifier:** checks assumptions and results using independent calculations or tests.
- **Integrator:** keeps the team's files and records consistent, combines contributions, and helps everyone prepare to explain the analysis.

These roles assign responsibility without dividing the project into isolated pieces. Everyone should contribute to coding and review, understand the full analysis, and be able to explain the team's decisions and results.

# Data

### Warmup and first assignment

- [Toy VAMP-seq bin counts](./data/project-1/examples/toy_vampseq_bin_counts.csv) — an artificial dataset for the first team assignment. These counts are invented for teaching and are not experimental PTEN measurements.

### Real PTEN data

- [PTEN abundance table](./data/project-1/derived/pten-variant-abundance.csv) — the main teaching table, containing selected published measurements and annotations.
- [Complete published score table](./data/project-1/raw/mavedb-00000013-a-1-scores.csv) — the unchanged source download, including individual replicate score columns for the data audit.
- [PTEN reference protein sequence](./data/project-1/derived/pten-reference-protein.fasta) — a FASTA file for checking variant positions and reference residues.
- [PTEN region annotations](./data/project-1/derived/pten-region-annotations.csv) — coordinates for summarizing measurements across protein regions.
- [Small preview table](./data/project-1/derived/pten-teaching-examples.csv) — a few example records for inspecting the real-data format.

The real abundance scores are already normalized. Here, the `raw/` folder holds unchanged published score files, not sequencing reads. Keep original downloads unchanged and save your generated tables and figures separately.

We use a fixed course snapshot from [MaveDB](https://www.mavedb.org/score-sets/urn%3Amavedb%3A00000013-a-1). [Source metadata](./data/project-1/raw/mavedb-00000013-a-1-metadata.json) and a [data manifest](./data/project-1/manifest.json) record its origin and the preparation of the files. 

**[Return to index](./)**
