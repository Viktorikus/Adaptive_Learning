import pandas as pd

df = pd.read_csv("adaptive_dataset.csv")

print("Kolom dataset:")
print(df.columns)

print("\nContoh 5 data pertama:")
print(df.head())

print("\nDistribusi error_type:")
print(df["error_type"].value_counts())

print("\nStatistik rata-rata:")
print(df.groupby("error_type")[["score", "wrong_count"]].mean())
