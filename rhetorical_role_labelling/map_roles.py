import pandas as pd
import ast

# Load the CSV with sentences already split
df = pd.read_csv("predex_sentences_split.csv")

# Read predicted labels from predictions.txt (output from rhetorical role labelling)
with open("predictions.txt", "r", encoding="utf-8") as f:
    line = f.readline().strip()
    raw_labels = [lbl.strip() for lbl in line.split(',') if lbl.strip()]

    # Remove anything before \t if present (removing file name which is output in predictions.txt)
    labels = [lbl.split('\t')[-1] for lbl in raw_labels]

# Annotate each sentence with its label
labeled_sentences_col = []
label_idx = 0

for sentence_list_str in df["Sentences"]:  
    try:
        sentences = ast.literal_eval(sentence_list_str)
        labeled_sentences = []

        for sentence in sentences:
            if label_idx < len(labels):
                label = labels[label_idx]
                annotated = f"<{label}>{sentence.strip()}<{label}>"
                labeled_sentences.append(annotated)
                label_idx += 1
            else:
                print("Ran out of labels!")
                labeled_sentences.append(sentence)  # fallback
        labeled_sentences_col.append(labeled_sentences)

    except Exception as e:
        print(f"Skipping row due to error: {e}")
        labeled_sentences_col.append([])

# Add new column with the labeled sentences
df["Labeled_Sentences"] = labeled_sentences_col

# Save back to CSV
df.to_csv("predex_sentences_annotated.csv", index=False)

print("Annotated CSV written!")
