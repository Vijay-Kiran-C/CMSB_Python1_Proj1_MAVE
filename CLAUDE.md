# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Coursework for a Python class (Project 1: PTEN variant abundance). The analysis is done in Jupyter notebooks with pandas/numpy/seaborn; there is no build system, test suite, or linter. Python 3.11 on Windows (PowerShell). The venv lives outside OneDrive at `C:\Users\james\venvs\pten-project` (run `Scripts\python.exe` from there, or select it as the notebook kernel); `requirements.txt` pins its packages (pandas 3.x, numpy 2.x). The system `python` has no packages. The assignment spec is `slides/project-1.md`; it describes a six-class arc: toy VAMP-seq scoring, data audit of real PTEN data, position/region summaries, testing a claim, robustness, then an extension and presentation.

The data come from a VAMP-seq MAVE (Matreyek et al. 2018), MaveDB score set `urn:mavedb:00000013-a-1`. The assay measures protein abundance only, not catalytic activity or pathogenicity, so keep interpretations within that.

## Layout

- `data/raw_data/` is course-provided, read-only input.
  - `raw/` holds unchanged MaveDB downloads (scores CSV with per-replicate `score1..score8` and `exp*_w_ave` columns, plus metadata JSON). Never modify these.
  - `derived/` holds course-prepared tables: `pten-variant-abundance.csv` (main table; `hgvs_pro`, `score`, `se`, `expts`, `record_type`, `abundance_class_label`), the PTEN FASTA (403 aa), region annotations, and a small preview.
  - `examples/toy_vampseq_bin_counts.csv` is invented teaching data (4 sort bins per variant per replicate), not real measurements.
  - `manifest.json` records SHA-256 hashes, provenance, and validation counts (4409 rows: 4112 missense, 140 nonsense, 156 synonymous, 1 wild_type).
- `code/my_code/`: the user's own notebooks, one per session assignment. They are scaffolds (imports, data loading, markdown prompts, empty code cells) that the user fills in by hand to learn, so do not write the analysis code in them. When asked, proofread only. `session-1-warmup` is the toy scoring, `session-2-dataAudit` is the real-data audit, `session-3-scores` is position coverage and statistics, and `session-4-dataViz` covers regions, figures, and sensitivity. Run the notebooks with `code/my_code` as the working directory.
- `code/final_code/`: the team's integrated notebooks, started as an exact copy of `my_code`. The repo owner (`@Vijay-Kiran-C`) owns it via `.github/CODEOWNERS`, which only auto-requests review unless branch protection requires code-owner approval. Teammates propose changes through pull requests. Do not edit it unless asked, and keep it consistent with `my_code` only when the user says to sync them.
- `code/group_code/`: teammates' notebooks and scripts. Treat as reference; don't edit without being asked.
- `slides/`: course notebooks, slide PDFs, and the project spec.

Save generated tables and figures separately from `data/raw_data/`, for example in a new `outputs/` folder, so the original data stay unchanged.

## Domain conventions

- Toy scoring pipeline (see `code/group_code/Toy_VAMP_2.py`): per-replicate bin frequencies (variant count / column total within that replicate), then a weighted-average score `W` with bin weights `[0.25, 0.5, 0.75, 1.0]` divided by the frequency sum. Next, normalize each replicate as `(W - median_nonsense) / (median_wt - median_nonsense)`, so nonsense is 0 and wild type is 1. Finally, average across replicates per variant.
- Variant labels are HGVS protein notation (`p.Met1Val`). Synonymous variants appear as `p.Gly12Gly`, and wild type is the literal `WT`. `record_type` and `variant_type` distinguish missense, nonsense, synonymous, and wild_type.
- Missing replicate values are `NA` in the raw CSV. Handle them explicitly in the data audit, not silently.
- Region coordinates (UniProt P60484): phosphatase domain 14-185, C2 domain 190-350, disordered tail 352-403.

## Course conventions (from `slides/notebook-01..06.ipynb`)

The six course notebooks are a Python-fundamentals sequence on toy DNA strings, not the PTEN analysis: strings and indexing, slicing/`.count`/`.replace`, `if`/`elif`, `for` loops, accumulators, then functions with contracts and `assert` tests. They share a house style that student code and reviews should follow:

- Every notebook ends with an "Audit" section: code that runs but overclaims (for example, an `N` check labeled "valid sequence", a complement that is not reversed, a GC calculation that counts only G). Prefer stating exactly what a check verifies and no more.
- Functions start from a written contract (accepted input, returned value, no mutation), then get known-answer `assert` tests chosen to expose plausible errors (e.g. a C-only input for a G-only bug). Out-of-contract input (lowercase, `N`, empty string) is flagged, not silently accepted.
- Loop and accumulator bugs are localized by printing intermediate state, not by inspecting only the final result.
- Plain loops, `if`/`elif`, and built-in string operations are the expected level. Avoid introducing libraries or idioms the course has not yet covered when writing example code, unless the task involves pandas (the project spec does).

## Project sessions (from the `Project 1, Session 1-4` slide PDFs)

Each session ends with an assignment that feeds the next. Later sessions rely on earlier definitions, so keep them consistent:

1. **Toy VAMP-seq:** explain columns, compute weighted scores, normalize (subtract median nonsense, divide by WT minus median nonsense), and critique the results.
2. **Data audit:** explain what each row and column means; parse `hgvs_pro` into site, WT residue, and mutant; verify the WT residue against the FASTA (mind 1-based sites vs 0-based Python indexes; decide what happens to stop labels and out-of-range positions); compare score distributions for WT, missense, nonsense, and synonymous variants. The real table differs from the toy one: scores per variant (not counts per variant-replicate), and the nonsense reference is an average, not a median. The real scores are published, not recomputed.
3. **Position-level summaries:** coverage across all 403 positions (including positions with no measured substitutions), per-position statistics for positions with at least `minimum_variants=5` included substitutions, missing kept distinct from zero, and test functions that flag or reject unexpected input.
4. **Regions and sensitivity:** assign each variant a region; per region report included variants, included sites, and total sites; report both the median of all variant scores and the median of per-site medians and interpret the difference; visualize by region; test sensitivity to `minimum_variants` and to a minimum `expts` per variant. Roles rotate at the start of Session 4.

Every session's discussion asks for the same three things: what was done conceptually, how the code achieves it, and how assumptions were checked. Structure results and explanations that way.

### pandas and reproducibility conventions

- Use `pathlib.Path` for paths, relative to a stated project root, not hardcoded absolute paths.
- Compare or combine tables by merging on an identifier (`on="position"`, `how="outer"`, `indicator=True`, `validate="one_to_one"`), never by row order. A missing comparison is not zero change.
- Use tidy layout: one variable per column, one observation per row, one value per cell. State what one row represents and what missing values mean.
- Record inputs and their source, filtering rules and parameters, and versions. End notebooks with `session_info.show(dependencies=True)`, and export the environment (`conda env export > environment.yml`). Restart and run all cells before saving a notebook.

### Figure style (Session 4)

- Labels are descriptive and legible, with units where relevant. State the WT reference, since "high" and "low" abundance are anchored to WT (score 1).
- Set `figsize` to the final display size (paper, slide, poster) so text is readable.
- Color and shape keep one meaning across figures and panels. Use colorblind-safe categorical palettes. Use perceptually uniform sequential palettes for ordered quantities, and diverging palettes only with a meaningful center (1 for abundance vs WT, 0 for a difference), with a colorbar that has a label and scale marks.
- Do not let a color scheme create sharp boundaries that the data do not support. Keep gridlines subtle.

## Known quirks

- `Toy_VAMP_2.py` (a teammate's script) hardcodes a macOS absolute path to the CSV; it won't run here without changing the path.
- `slides/project-1.md` links data under `./data/project-1/...`, but the files here live under `data/raw_data/`.
- `manifest.json` cites `scripts/prepare_data.py`, which is not in this directory.
- Reading PDFs needs poppler, which was installed with winget. If the Read tool still reports `pdftoppm` missing after an app restart, render pages to PNG with the full path to `pdftoppm.exe` (under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\oschwartz10612.Poppler_*`) and read the images.
- The directory is inside OneDrive, so avoid large generated files. It is a git repository (branch `main`) with the remote `origin` at `github.com/Vijay-Kiran-C/CMSB_Python1_Proj1`. Commit before large edits so they can be undone, and only push when the user asks.

## Working preferences

The user is learning to work with Claude Code and has strong background in the analysis itself. Explain design choices, and leave key analytical decisions to them where practical instead of making them silently.
