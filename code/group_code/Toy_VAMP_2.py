from numpy import median
import pandas as pd
import seaborn as sns 
import numpy as np

df = pd.read_csv("/Users/alexaorsino/Library/CloudStorage/OneDrive-UniversityofPittsburgh/PhD_Courses/IntroProg/Proj1/toy_vampseq_bin_counts.csv")

# explain what each column means
df.head(2)

bin_cols = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]
weights = np.array([0.25, 0.5, 0.75, 1.0])

# Step 1: frequency, normalized within each replicate separately

# numerator: count of each variant, in each bin, for its specific replicate
variant_counts_per_replicate = df[bin_cols]

# denominator: total count across ALL variants, in each bin, within that same replicate
total_counts_per_replicate = df.groupby("replicate")[bin_cols].transform("sum")

# frequency = variant's count in a bin / total count of all variants in that bin, within the same replicate
freq = variant_counts_per_replicate.div(total_counts_per_replicate)

# Step 2: weighted score per row 
df["W"] = freq.dot(weights) / freq.sum(axis=1)

# normalize within each replicate
def normalize(group):
    nonsense_med = group.loc[group.variant_type == "nonsense", "W"].median()
    wt_med = group.loc[group.variant_type == "wild_type", "W"].median()
    group["abundance_score"] = (group["W"] - nonsense_med) / (wt_med - nonsense_med)
    return group

df = df.groupby("replicate", group_keys=False).apply(normalize)

# then collapse replicates into one score per variant
final_scores = df.groupby("variant")["abundance_score"].mean()
