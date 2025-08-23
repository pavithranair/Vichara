import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import re

# Load the DataFrame
df = pd.read_csv("predictions.csv")

# Drop rows where text is empty or only whitespace
df = df[df["text"].astype(str).str.strip() != ""]

# Convert columns to integers
df["label"] = df["label"].astype(int)
df["Judgment_Prediction"] = df["Judgment_Prediction"].astype(int)

# Compute metrics (macro-averaged)
accuracy = accuracy_score(df["label"], df["Judgment_Prediction"])
precision = precision_score(df["label"], df["Judgment_Prediction"], average='macro')
recall = recall_score(df["label"], df["Judgment_Prediction"], average='macro')
f1 = f1_score(df["label"], df["Judgment_Prediction"], average='macro')

# Print results
print(f"Accuracy: {accuracy:.4f}")
print(f"Macro Precision: {precision:.4f}")
print(f"Macro Recall: {recall:.4f}")
print(f"Macro F1 Score: {f1:.4f}")
