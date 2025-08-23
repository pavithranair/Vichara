import pandas as pd
from rouge_score import rouge_scorer
import sacrebleu
from nltk.translate.meteor_score import single_meteor_score
import nltk

# Ensure required NLTK resources are available
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')

# Load your CSV
df = pd.read_csv("explanations.csv")

# Drop rows with missing values
df = df.dropna(subset=["Structured_Explanation", "ground_truth_explanation"])

# Extract as lists
predictions = df["Structured_Explanation"].astype(str).tolist()
references = df["ground_truth_explanation"].astype(str).tolist()

# Initialize ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Accumulate ROUGE scores
rouge1, rouge2, rougeL = [], [], []
for pred, ref in zip(predictions, references):
    scores = scorer.score(ref, pred)
    rouge1.append(scores["rouge1"].fmeasure)
    rouge2.append(scores["rouge2"].fmeasure)
    rougeL.append(scores["rougeL"].fmeasure)

print(f"ROUGE-1: {sum(rouge1)/len(rouge1):.4f}")
print(f"ROUGE-2: {sum(rouge2)/len(rouge2):.4f}")
print(f"ROUGE-L: {sum(rougeL)/len(rougeL):.4f}")

# BLEU (SacreBLEU expects one reference per prediction)
bleu = sacrebleu.corpus_bleu(predictions, [references])
print(f"BLEU Score: {bleu.score/100:.4f}")

from nltk.tokenize import word_tokenize

meteor_scores = [
    single_meteor_score(word_tokenize(ref), word_tokenize(pred))
    for ref, pred in zip(references, predictions)
]
print(f"METEOR Score: {sum(meteor_scores)/len(meteor_scores):.4f}")