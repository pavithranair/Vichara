import pandas as pd
import evaluate
from blanc import BlancHelp

# Load your CSV
df = pd.read_csv("explanations.csv")
# Extract reference (ground truth) and predicted summaries
references = df["ground_truth_explanation"].tolist()
predictions = df["Structured_Explanation"].tolist()

bertscore = evaluate.load("bertscore")

bertscore_results = bertscore.compute(
    predictions=predictions,
    references=references,
    lang="en"  # English
)

# Print average scores
print(f"BERTScore Precision: {sum(bertscore_results['precision']) / len(bertscore_results['precision']):.4f}")
print(f"BERTScore Recall:    {sum(bertscore_results['recall']) / len(bertscore_results['recall']):.4f}")
print(f"BERTScore F1:        {sum(bertscore_results['f1']) / len(bertscore_results['f1']):.4f}")

# Initialize model (after downgrading required packages)
blanc = BlancHelp()

# Compute BLANC-help score
blanc_score = blanc.eval_pairs(references, predictions)
print(blanc_score)
avg_blanc = sum(blanc_score) / len(blanc_score)
print(f"Average BLANC-help Score: {avg_blanc:.4f}")