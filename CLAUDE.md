# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Coursework for a Python class (Project 1: PTEN variant abundance). The analysis is done in Jupyter notebooks with pandas/numpy/seaborn; there is no build system, test suite, linter, or package manifest. Python 3.11 on Windows (PowerShell). The assignment spec is `slides/project-1.md`; it describes a six-class arc: toy VAMP-seq scoring, data audit of real PTEN data, position/region summaries, testing a claim, robustness, then an extension and presentation.

The data come from a VAMP-seq MAVE (Matreyek et al. 2018), MaveDB score set `urn:mavedb:00000013-a-1`. The assay measures protein abundance only, not catalytic activity or pathogenicity, so keep interpretations within that.

## Layout

- `data/raw_data/` is course-provided, read-only input.
  - `raw/` holds unchanged MaveDB downloads (scores CSV with per-replicate `score1..score8` and `exp*_w_ave` columns, plus metadata JSON). Never modify these.
  - `derived/` holds course-prepared tables: `pten-variant-abundance.csv` (main table; `hgvs_pro`, `score`, `se`, `expts`, `record_type`, `abundance_class_label`), the PTEN FASTA (403 aa), region annotations, and a small preview.
  - `examples/toy_vampseq_bin_counts.csv` is invented teaching data (4 sort bins per variant per replicate), not real measurements.
  - `manifest.json` records SHA-256 hashes, provenance, and validation counts (4409 rows: 4112 missense, 140 nonsense, 156 synonymous, 1 wild_type).
- `code/my_code/`: the user's own notebooks, one per session (warmup, data audit, scores).
- `code/group_code/`: teammates' notebooks and scripts. Treat as reference; don't edit without being asked.
- `slides/`: course notebooks, slide PDFs, and the project spec.

Save generated tables and figures separately from `data/raw_data/`, for example in a new `outputs/` folder, so the original data stay unchanged.

## Domain conventions

- Toy scoring pipeline (see `code/group_code/Toy_VAMP_2.py`): per-replicate bin frequencies (variant count / column total within that replicate), then a weighted-average score `W` with bin weights `[0.25, 0.5, 0.75, 1.0]` divided by the frequency sum. Next, normalize each replicate as `(W - median_nonsense) / (median_wt - median_nonsense)`, so nonsense is 0 and wild type is 1. Finally, average across replicates per variant.
- Variant labels are HGVS protein notation (`p.Met1Val`). Synonymous variants appear as `p.Gly12Gly`, and wild type is the literal `WT`. `record_type` and `variant_type` distinguish missense, nonsense, synonymous, and wild_type.
- Missing replicate values are `NA` in the raw CSV. Handle them explicitly in the data audit, not silently.
- Region coordinates (UniProt P60484): phosphatase domain 14-185, C2 domain 190-350, disordered tail 352-403.

## Known quirks

- `Toy_VAMP_2.py` (a teammate's script) hardcodes a macOS absolute path to the CSV; it won't run here without changing the path.
- `slides/project-1.md` links data under `./data/project-1/...`, but the files here live under `data/raw_data/`.
- `manifest.json` cites `scripts/prepare_data.py`, which is not in this directory.
- The directory is inside OneDrive, so avoid large generated files, and it is not a git repository.

## Working preferences

The user is learning to work with Claude Code and has strong background in the analysis itself. Explain design choices, and leave key analytical decisions to them where practical instead of making them silently.
