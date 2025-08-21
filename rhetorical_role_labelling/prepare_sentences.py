import pandas as pd
import json
from wtpsplit import SaT

# Initialize sentence tokenizer
sat_lora_distinct = SaT("sat-12l", style_or_domain="legal-judgement", language="en")

# Load input CSV
df = pd.read_csv("~/Projects/Legal/Datasets/ILDC_expert.csv")

def process_text(text, row_idx=None):
    """
    Splits a block of text into individual sentences using the SaT model.

    Args:
        text (str): The input text string to split into sentences.
        row_idx (int, optional): Row index.

    Returns:
        list: A list of sentences (strings).
    """
    if not isinstance(text, str) or not text.strip():
        return []

    sentences = sat_lora_distinct.split(text.strip())

    if row_idx is not None:
        print(f"Row {row_idx}: {len(sentences)} sentences split")
    return sentences

# Apply sentence splitting row-by-row on the "text" column
df["Sentences"] = df.apply(
    lambda row: json.dumps(process_text(row["text"], row.name), ensure_ascii=False),
    axis=1
)

# Save CSV with sentences as JSON lists
df.to_csv("ILDC_sentences_split.csv", index=False)

# Flatten all sentences into one .txt file to feed as input to Hier-BiLSTM-CRF model for rhetorical role labelling
output_file = "sentences.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for sentence_list in df["Sentences"]:
        try:
            parsed = json.loads(sentence_list)  # convert back from JSON string to list
            for sentence in parsed:
                f.write(sentence.strip() + "\n")
        except Exception as e:
            print(f"Skipping row due to error: {e}")

print(f"Flattened sentences written to {output_file}")
