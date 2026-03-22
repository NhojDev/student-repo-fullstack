import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('Data/Price_Data/2026-03-14.csv')
nan_mask  = df.isna().any(axis=1)
nan_df    = df[nan_mask]
clean_df  = df[~nan_mask]

print(clean_df.head())