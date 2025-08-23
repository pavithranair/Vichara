import pandas as pd
import tiktoken
import openai
import json

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

# Tokenizer for the model
enc = tiktoken.encoding_for_model("gpt-4o-mini")

# JSON prompt template
DECISION_POINT_PROMPT = """You are a legal assistant tasked with extracting **all decision points** from an excerpt of a court case proceeding. 
A decision point summarizes a legal issue along with the Court’s stance on it. 

Given the following text and the present court, extract **all identifiable decision points** and output them in strict JSON format as a list of objects.

Each decision point object should include:

- "issue": the legal issue or question being addressed
- "decision_maker": the court or authority that made the decision (e.g., Supreme Court, Trial Court, High Court)
- "outcome": the result or resolution of the issue
- "time": (optional) the date or timeframe of the decision if mentioned
- "reasoning": (optional) summary of the Court's reasoning, including references to statutes, arguments, facts, or precedents
- "present_court_decision": true if the "decision_maker" is the same as the present court provided, otherwise false

### Important instructions:
- Do not include any extra text or explanation.
- Do not assume or hallucinate decision makers.
- Do NOT include triple backticks (```) anywhere.

### Input
Present Court: "{present_court}"

### Output Format

[
  {{
    "issue": "<string>",
    "decision_maker": "<string>",
    "outcome": "<string>",
    "time": "<string or null>",
    "reasoning": "<string or null>",
    "present_court_decision": <true or false>
  }}
]

Text:
\"\"\"{group_text}\"\"\"
"""

def extract_decision_points(text, present_court, chunk_size=1000):
    """
    Splits the text into chunks of 'chunk_size' tokens, 
    sends each to GPT, and returns concatenated JSON decision points.
    """
    tokens = enc.encode(text)
    outputs = []

    for i in range(0, len(tokens), chunk_size):
        chunk = enc.decode(tokens[i:i+chunk_size])
        
        prompt = DECISION_POINT_PROMPT.format(group_text=chunk, present_court=present_court)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        print(response.choices[0].message.content.strip())
        outputs.append(response.choices[0].message.content.strip())

    # Combine all JSON chunks into one list
    all_points = []
    for o in outputs:
        try:
            points = json.loads(o)
            print("POINTS")
            print(points)
            if isinstance(points, list):
                print("LIST")
                all_points.extend(points)
        except json.JSONDecodeError:
            print(f"⚠️ JSON parse error, raw output:\n{o}\n")
    
    return all_points

def process_dataframe(df, text_column="Input", court_column="Present_Court"):
    """
    Processes a DataFrame row by row to extract decision points.
    """
    all_decision_points = []
    filtered_points = []

    for idx, row in df.iterrows():
        text = row[text_column]
        present_court = row[court_column]
        decision_points = extract_decision_points(text, present_court)
        all_decision_points.append(decision_points)
        
        # Filter only decision points where present court is the decision maker
        filtered = [dp for dp in decision_points if dp.get("present_court_decision")]
        filtered_points.append(filtered)

    df["decision_points"] = all_decision_points
    df["present_court_decision_points"] = filtered_points
    return df

# Load your data
df = pd.read_csv("cases_with_context.csv")   

# Process row by row
df = process_dataframe(df, text_column="Input", court_column="Present_Court")

# Save results
df.to_csv("decision_points_json.csv", index=False)
