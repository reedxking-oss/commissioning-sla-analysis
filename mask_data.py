"""Usage: python mask_data.py <private_export.xlsx> data/tag_log_masked.csv

Turn the private tag log into a masked file safe to analyze and share.
Keeps one random ID per unit, the discipline, tag type, and tag dates. Drops everything else."""
import sys, pandas as pd, numpy as np
src, dst = sys.argv[1], sys.argv[2]
df = pd.read_excel(src)
units = df['Cx Upload Unique No.'].drop_duplicates().sample(frac=1, random_state=42).reset_index(drop=True)
ids = {u: f"EQ-{i+1:05d}" for i, u in enumerate(units)}
out = pd.DataFrame({
    'Unit ID': df['Cx Upload Unique No.'].map(ids),
    'Discipline': df['Discipline'].str.title().replace({'Upw': 'UPW', 'Fire Protection/Ssh': 'Fire Protection/SSH'}),
    'Tag Type': df['Tag Type'],
    'Green Tag': df['Green Tag'],
    'Blue Tag': df['Blue Tag'],
    'Tag Date': df['Tag Date'],
})
out.to_csv(dst, index=False)
print(out.shape, out['Unit ID'].nunique())
