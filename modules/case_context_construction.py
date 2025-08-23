import pandas as pd
import re
import openai
import ast
import json

# Load CSV with labeled sentences
df = pd.read_csv("rhetorical_role_labelling/predex_sentences_annotated.csv")

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

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

# JSON prompt template
prompt_template = """You are a legal assistant helping summarize appeal case details.

Given the following facts from an appeal case document, extract the following information about the current appeal only:

1. Appellants – the persons or entities filing the current appeal. If their name is not mentioned, write what they are referred to as in the text (e.g., "the petitioner", "the appellant").
2. Respondents – the persons or entities against whom the current appeal is filed. If their name is not mentioned, write what they are referred to as in the text (e.g., "respondent 1", "the respondent-Management").
3. Issue – the main legal or factual issue being disputed in the current appeal.
4. Appellant's Stance (in the current appeal) – clearly state what the appellant is arguing for or seeking in the present appeal.
5. Respondent's Stance (in the current appeal) – clearly state what the respondent is arguing for or seeking in the present appeal.
6. Present Court – the court currently deciding the present appeal (e.g., Supreme Court of India, High Court of Bombay).

### Important instructions:

- Do NOT assume the appellant is the party introduced first. Carefully check who has filed the current appeal.
- Do NOT summarize or include opinions or findings of lower courts unless those are being specifically challenged in this appeal.
- Do NOT list courts or tribunals unless they are explicitly a party.
- Focus on the actual parties to the legal dispute.
- Do NOT invent names or facts. If something is not mentioned, leave it as an empty string.
- Use only the output format specified below.

### Output Format:

{{
  "appellants": "<name or description of appellant>",
  "respondents": "<name or description of respondent>",
  "issue": "<brief summary of the legal/factual issue>",
  "appellant_stance": "<stance of the appellant>",
  "respondent_stance": "<stance of the respondent>",
  "present_court": "<name of the court currently deciding the appeal>"
}}

### Facts:
\"\"\"{facts}\"\"\"
"""

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
    prompt = prompt_template.format(facts=facts_text)

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
