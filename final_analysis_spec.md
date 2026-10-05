# Final Analysis Specifications 

I will point Claude at this file and direct it to build the final analysis accordingly

## Claude, here's a summary of what we want to do.

What kinds of amino-acid substitutions have the greatest changes on PTEN abundance? How does the domain in which the substitution takes place affect the typical change in abundance?

Here are the aspects of our analysis that my team discussed:
- We want to start with a heatmap (hm.abund.0) to probe abundances of ALL variants at ALL positions. This heatmap will havel PTEN positions (403?) along the x-axis, similar to the heatmap you made in session-5 Aim 4, and all amino acid substitutions possible. The cells should be colored by the abundance / average abundance of the variant. This will likely be a messy, sparse heatmap, so don't spend too much time on this or making it look pretty.
- Next, we'd want to see more refined heatmaps. Make a heatmap (hm.abund.1) with the same x-axis, but with variants on the y-axis limited to the variants that are actually observed in the dataset. Another heatmap (hm.abund.2) that groups the variants by one of the 24? I think? possible changes in class. i.e. Charged -> Polar, Charged -> Charged, Charged -> Hydrophobic, Charged -> Special Cases for all classes. For  hm.2, I dont want you to aggregate! Just group the variants and add a grouping label on the y-axis. In the neaxt heatmap (hm.abund.3), I want you to aggregate the abundances by the variant class changes using the site median we used in session-4. 
- After those four heatmaps, I want you to remake them with a similar naming scheme (hm.diff.x). However, instead of plotting the abundances in each cell, I want you to plot the log ratio of the variant abundance score vs. the wild type abundance score, similar to what you plotted in part 2 of session 5. You might have problems or questions here - I'll mention it in the Open Decisions section.
- Furthermore, we want to summarize the effects of region type on the change in abundance observed for each variant. I think a similar scheme to what I described earlier will help. Look at raw abundances first, refine, then the normalized comparisons. I'm not sure what plots would work best for summarizing the the relationship between region and abundance change, so pull from what you've already made and ask me if you need feedback. I think that the boxplots with the four domains would be cool to see, but I love seeing landscape figures like heatmaps. 
- In the hypothesis, I predict that a particular class change will have the strongest effect on a particular region. Please consider this and tell me about the kind of statistical test and visualization that would best interrogate these changes across the entire protein. For this one step, just go ahead and make what you think is best. 
- This should be enough for now. I could see myself wanting more once you're done, so "leave the door open" for further iteration, meaning that if you see holes in this analysis, raise them to me at the end as proposed next steps instead of being proactive. 


## Things Claude asked for that I need to fill out:
- Question: What are the relationships between variant class change and region type on PTEN abundance and the change in abundance vs. wild type. 
- Hypothesis: The more different a variant's sidechain is from the wild type, the greater the difference in abundance will be for that PTEN variant. We predict that variants which change the class of amino acid will have larger aggregate effects on the change in protein abundance. We also predict that, again, the phosphatase domain and the c2 domain will see the largest changes in abundance. Additionally, I predict that that electrically charged -> hydrophobic sidechains will have the strongest effects on the phosphatase domain. 
- Data to use:
    "Project_1_MAVE\aminoacids-pic.png" for the classing of amino acids into four groups based on side chains. Electrically charged sidechains, Polar Uncharged side chains, Hydrophobic sidechains, and special cases. Use these classes for the amino acids. Include a column for `wt` and `mut` called `wt_class` and `mut_class` which contains the class of that amino acid according to the chart I point you towards.
- Definitions and Decisions:
    - Use the formatting of `hgvs_pro`, which corresponds to standard protein mutation nomenclature, for the y-axis on the heatmaps.  
    - Include code chunks that save all plots to data/my_data/pdfs as pdfs with descriptive names formatted like 'VKC_CLAUDE_vblhablhablas.pdf'
- Open decisions:
    - The .pdf at "Project_1_MAVE\Amino Acid Chart.pdf" contains an alternative classing of amino acids. Honestly, I like this one better, but I think it's better to stick to the .png because its what we see in class. Just decided to add it in case it helps you.
    - I'm not sure exactly how the difference in abundances will work when making the second set of heatmaps. In my mind, its a straightforward normalization of each abundance score by the wild type. I think the average works better here because of how the histograms look in session-5, but we've been working with medians...when you get to making the second set of heatmaps, feel free to stop and ask me for input on any problems or questions you have. 
    - I think there is a cool way of looking at region type, sidechain class changes, and change in abundance that I'm not thinking about right now. Feel free to think about this and include suggestions in your proposed next steps at the end of the task. 
- Verifications / Checks:
    - I'm really not sure what makes a check "good" when it comes to this kind of data analysis. I'm used to manually checking the shape of a dataframe and the values of objects themselves before running things and that tends to work. Writing checks is hard, but good practice. When you write the checks, use it as a teaching opportunity for me. Stick to the 'assert' syntax and conventions we were taught in the slides AND that you've already developed for the other scripts.
- Constraints - Slide-taught tools only, the comment convention in CLAUDE.md, and no editing final_code or teammates' files
- Deliverables. a notebook session-6-extension.ipynb with the code, figures, and a draft of the what/how/checked notes for the 5 to 7 minute talk

---

# Claude's review of this plan (2026-10-05)

Everything below was checked against `pten-variant-abundance.csv` before writing. Each item has a **recommended default**, so you can answer with "go with the defaults" or override individual ones. Items marked **DECIDE** change what gets built.

## A. Things that would break or mislead as written

1. **DECIDE: `hgvs_pro` on the y-axis cannot make a landscape heatmap.** Each `hgvs_pro` (e.g. `p.His75Asp`) already contains its position, so it occupies exactly one column. A 4112-row by 403-column grid has one filled cell per row (0.25% filled), so you get a thin diagonal stripe and no vertical comparison across sites. What you want is a y-axis that is *shared across positions*. Options:
   - (a) **Mutant residue** (20 rows), like the Session 5 heatmap. Simple and readable. *Recommended for hm.abund.0.*
   - (b) **Substitution type, wt -> mut** (380 possible, 373 observed), written in hgvs_pro vocabulary (`His>Asp`). Only 2.7% of the 380 x 403 grid is filled, because each column can fill at most 19 of 380 rows (the WT residue is fixed at a site). This is the sparse "messy" heatmap you described. *Recommended for hm.abund.1.*
   - (c) Literal `hgvs_pro` rows, sorted by position (the diagonal stripe). I can make it if you want it for the talk, but it will not show the landscape.
   - Note that hm.abund.0 (all 380 possible) and hm.abund.1 (373 observed) would differ by only 7 rows under (b), so hm.1 is nearly a duplicate of hm.0. Under (a)+(b) they are meaningfully different figures.
2. **There are 16 class changes, not 24.** 4 classes x 4 classes = 16 ordered pairs. 12 change class and 4 stay in the same class (e.g. charged -> charged). Keep all 16, because your hypothesis contrasts class-changing with same-class variants. Observed in the data: 3110 class-changing and 1002 same-class missense variants.
3. **"Normalize by wild type" is a no-op on this table.** The `score` column is already scaled so WT = 1.0 (the `_wt` row is exactly 1.0) and nonsense is about 0 (median 0.064). So variant / WT = score / 1 = score, and the log ratio is just `log2(score)`. The ratio only changes the *scale*, not the information. Consequences:
   - **16 missense scores are <= 0**, so their log ratio does not exist. They stay as NaN (shown grey), never dropped silently and never set to 0.
   - **Scores near 0 blow up on the log scale.** The 1st percentile is 0.087, and log2(0.087) is about -3.5, so the log stretches the noisy low end and compresses the high end.
   - **DECIDE:** which "difference from WT" do you want in hm.diff.x? Options: (i) log2 ratio exactly as you described, (ii) linear difference `score - 1`, centered on 0, (iii) both for one figure to compare. *Recommended: (i) for the heatmaps as requested, with one side-by-side against (ii) so the group can see what the log does.*
4. **Mean versus median has a clean answer.** Log is a monotone transform, so the same variant is in the middle on both scales and `median(log2(score)) == log2(median(score))` holds exactly for an **odd** number of values. *(Correction found while building the notebook: for an even number the median averages the two middle values, and the two routes differ slightly, up to 0.14 log2 units in this data.)* The mean never matches (`mean(log2(x)) != log2(mean(x))`). So the log ratio is taken per variant first and summarized second. That is a good reason to keep medians as in Session 4. I'd compute the log ratio per variant first and summarize second, and show the mean as a sensitivity check (this connects to your histogram observation in Session 5). *Recommended default: median, mean as a check.*
5. **DECIDE: hm.abund.3 / hm.diff.3 ("aggregate by class change using the site median").** A "site median" is one median per *site*, and a given site has a fixed WT class, so at each site only 4 of the 16 class-change rows can be filled (25% maximum). Most (site, class change) cells then contain 1 to 3 variants, and the `minimum_variants = 5` rule from Session 4 would remove nearly all of them. Options:
   - (a) Aggregate per (class change x **position window**, e.g. 25 sites per bin), with median and n.
   - (b) Aggregate per (class change x **region**) (16 x 3 or 4 cells), which is also the cleanest bridge to your region hypothesis.
   - (c) Keep the per-site layout but with a small minimum (e.g. 2) and show n.
   - *Recommended: (a) for the position-wise landscape (same x-axis idea) and (b) in the region section.* Rows in all class-change heatmaps should be sorted by `wt_class` then `mut_class` so the 4x4 block structure is visible.
6. **Which variants go in? DECIDE.** Sessions 4 and 5 used the 4005 variants at sites with at least 5 variants. *Recommended: variant-level figures (hm.0/.1/.2) use all 4112 missense variants; every site-median figure applies `minimum_variants = 5`. State this on each figure.*

## B. The hypothesis

7. **"Greater difference" has two meanings: the direction and the size of the effect.** Scores above 1 exist (5% of missense scores are above 1.14), so a variant can be *more* abundant than WT. The hypothesis about size is a statement about |effect| (e.g. `abs(score - 1)`), and the direction (loss versus gain) is a separate question. *Recommended: test the magnitude as `abs(score - 1)`, and show signed medians in the heatmaps.*
8. **Class is a crude proxy for "how different the side chain is".** Same-class changes can be large (Ala -> Trp is hydrophobic -> hydrophobic) and class-changing ones small. That is fine for this question, but state it as a limitation. Not now, but side-chain size or hydrophobicity would be natural next steps.
9. **Confounding by WT residue.** The WT class mix differs by region: the tail is 39% polar / 16% hydrophobic WT residues, the phosphatase domain is 14% polar / 41% hydrophobic. Differences between regions in a class-change effect can partly reflect which residues exist there. Worth a sentence in the talk, and a possible check (compare within `wt_class`).

## C. The statistical test (you said "just make what you think is best")

10. Sample sizes are workable: of the 48 class-change x region cells (3 annotated regions), only 1 has n < 10 and 5 have n < 20. Plan:
    - **Figure:** a 16 x 3 (regions) heatmap of the median effect with n printed in each cell, plus the 3-region boxplots of `abs(score - 1)` split by class-changing versus same-class.
    - **Pre-specified test (your hypothesis):** the median `abs(score - 1)` of charged -> hydrophobic in the phosphatase domain versus every other variant in that domain, using a **permutation test** in numpy (shuffle the labels, recompute the statistic 10,000 times). This needs only `for` loops and numpy, so it stays within the course style. It makes no normality assumption and works for any statistic, including the median.
    - **Exploratory screen:** the same permutation statistic for all 48 cells, labelled exploratory and with a multiple-comparison note (48 tests will produce a few "hits" by chance).
    - **Independence caveat:** variants at the same site are correlated (site effects). A stricter version permutes whole sites (blocks) rather than variants. I'd run both and report whether the answer changes.
    - **DECIDE:** the course slides do not cover statistical tests (`scipy.stats` is not in `requirements.txt` as far as I know). OK to use numpy-only permutation tests? *Recommended: yes.*

## D. Checks (teaching moments, plain `assert`, same style as Sessions 3 to 5)

A good check **can fail, and its failure tells you what went wrong.** "I looked at the shape" is a good habit, but an assert makes it permanent and rerun on every change. Planned checks, each aimed at a specific plausible mistake:
- The class dictionary has exactly 20 residues, every `letter` key appears once, and the class sizes are 5 / 4 / 3 / 8 (catches a typo that drops or duplicates an amino acid).
- `wt_class` and `mut_class` have no NaN after mapping, and the row count is still 4112 after adding them (catches a lost row from a bad merge).
- `wt_class` takes exactly one value per position (catches a mismatched WT letter).
- The 16 class-change counts sum to 4112, and the 4x4 table matches the printed one above.
- Heatmap grids: the count of non-NaN cells equals the number of variants (catches two variants colliding in one cell). hm.abund.2 must have no aggregation (cells = variants).
- hm.abund.3 aggregation: the cell counts (n) sum back to the number of variants used.
- Log ratio: known answers `log2(1.0) == 0`, `log2(0.5) == -1`, the `_wt` row maps to 0, and the NaN count equals the 16 non-positive scores.
- Every PDF named in the save step exists after the cell runs.

## E. Smaller notes

- Names like `hm.abund.0` cannot be Python variable names (the dot is attribute access). I'd use `hm_abund_0` in code and `VKC_CLAUDE_hm_abund_0_<description>.pdf` for files, saved to `data/my_data/pdfs/`.
- Class assignment follows `aminoacids-pic.png` as you asked: charged = R, H, K, D, E; polar uncharged = S, T, N, Q; special = C, G, P; hydrophobic = A, V, I, L, M, F, Y, W. His is counted as charged, and Tyr as hydrophobic, per the picture. I did not use the alternative PDF.
- `final_analysis_spec.md` is no longer in `.gitignore`, so it is pushed and visible to your teammates (including this review section). The amino acid PDFs are still ignored.
- Notebook location: `code/my_code/session-6-extension.ipynb`, with the functions defined once in a cell right after the imports, as in the other notebooks.
- Per your instruction, I will list holes and next steps at the end and not act on them.

# VKC Follow Up

## A. 
1. Do (a) + (b), mutant residue and subtitution type
2. Thanks for the clarification.
3. When I said normalize, I just meant log2(score / 1) (log ratio to wild type). My bad. Dp the recommended plan.
4. Sounds good.
5. Sounds good, proceed with recommended.
6. Go ahead with what you recommended. 

## B.
7. Show signed medians in the figures. Ignore testing the magnitudes.
8. Yes, this is a great point and one I had considered. Good job catching this!
9. A check here would be nice. I don't know if we would include it in the talk, so leave it on the table for future steps.

## C.
10. Yes! I'll make sure to explain how exactly I did this, and I'll share the repo with anyone who wants it. 

## E.
- Good to know about `.` being reserved in python. I'll stick with underscores, I like them better anyways.

