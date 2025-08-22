import pandas as pd
import tiktoken
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

# Tokenizer for the model
enc = tiktoken.encoding_for_model("gpt-4o-mini")

# Prompt template
DECISION_POINT_PROMPT = """You are a legal assistant tasked with extracting **all decision points** from an excerpt of a court case proceeding. 
Your task is to extract **all identifiable decision points** based on this text, which will later be used to assess whether the appeal or petition was granted or dismissed. 
A decision point summarizes a legal issue along with the Court’s stance on it.

Please follow this structured format for **each distinct decision point**:

---
**Issue:** What legal issue or question is being addressed?

**Decision Maker:** Who made the decision (e.g., Supreme Court, Trial Court, High Court)?

**Outcome:** What was the result or resolution of the issue?

**Time:** (Optional) When was the decision made, if mentioned?

**Reasoning:** (Optional) Summarize the Court's reasoning behind the decision, including references to statutes, arguments, facts, or precedents where applicable.
---

If there are **no decision points** in the provided text, return the **input text exactly as is**, with no explanation or additional content.

Text to analyze:
\"\"\"{group_text}\"\"\"
"""

def extract_decision_points(text, chunk_size=1000):
    """
    Splits the text into chunks of 'chunk_size' tokens, 
    sends each to GPT, and returns concatenated decision points.
    """
    tokens = enc.encode(text)
    outputs = []

    for i in range(0, len(tokens), chunk_size):
        chunk = enc.decode(tokens[i:i+chunk_size])
        
        prompt = DECISION_POINT_PROMPT.format(group_text=chunk)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        outputs.append(response.choices[0].message.content.strip())

    return "\n\n".join(outputs)

def process_dataframe(df, text_column="text"):
    """
    Processes a DataFrame row by row to extract decision points.
    """
    decision_points = []
    for idx, row in df.iterrows():
        text = row[text_column]
        result = extract_decision_points(text)
        decision_points.append(result)
    
    df["decision_points"] = decision_points
    return df

# Load your data
df = pd.read_csv("ILDC_sentences_annotated.csv")   

# Process row by row
df = process_dataframe(df, text_column="text")

# Save results
df.to_csv("decision_points.csv", index=False)
