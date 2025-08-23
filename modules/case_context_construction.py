import pandas as pd
import re
import openai
import ast
import json
from dotenv import load_dotenv
import os
from utils.prompts import case_context_prompt

# Load environment variables from .env file
load_dotenv()

# Access them using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# Load CSV with labeled sentences
df = pd.read_csv("sentences_annotated.csv")

def extract_facts(labeled_sentences):
    """
    Extracts sentences tagged with <Facts> from a stringified list.
    """
    if not isinstance(labeled_sentences, str):
        return []
    try:
        sentences = ast.literal_eval(labeled_sentences)
        facts = []
        for s in sentences:
            if "<Facts>" in s:
                cleaned = s.replace("<Facts>", "").strip()
                if cleaned:
                    facts.append(cleaned)
        return facts
    except Exception as e:
        print(f"Parse error: {e}")
        return []

# Process each row
contexts = []
present_courts = []

for i, row in df.iterrows():
    facts = extract_facts(row.get("Labeled_Sentences", ""))
    if not facts:
        contexts.append("")
        present_courts.append("")
        continue

    facts_text = " ".join(facts)
    prompt = case_context_prompt.format(facts=facts_text)

    # Call GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        print(f"⚠️ JSON parse error at row {i}, raw output: {raw_output}")
        parsed = {
            "appellants": "",
            "respondents": "",
            "issue": "",
            "appellant_stance": "",
            "respondent_stance": "",
            "present_court": ""
        }

    contexts.append(parsed)
    present_courts.append(parsed.get("present_court", ""))

# Save into dataframe
df["Case_Context"] = contexts
df["Present_Court"] = present_courts

df.to_csv("cases_with_context.csv", index=False)
