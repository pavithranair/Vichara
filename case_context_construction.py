import pandas as pd
import re
import openai
import ast

# Load CSV with labeled sentences
df = pd.read_csv("rhetorical_role_labelling/predex_sentences_annotated.csv")

def extract_facts(labeled_sentences):
    """
    Extracts sentences tagged with <Facts> from a stringified list.
    """
    if not isinstance(labeled_sentences, str):
        return []
    try:
        # Parse the stringified list into a real list
        sentences = ast.literal_eval(labeled_sentences)
        facts = []
        for s in sentences:
            if "<Facts>" in s:
                # Remove all <Facts> markers and strip
                cleaned = s.replace("<Facts>", "").strip()
                if cleaned:
                    facts.append(cleaned)
        return facts
    except Exception as e:
        print(f"Parse error: {e}")
        return []

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

# Prompt template
prompt_template = """You are a legal assistant helping summarize appeal case details.

Given the following facts from an appeal case document, extract the following information about the current appeal only:

1. Appellants – the persons or entities filing the current appeal. If their name is not mentioned, write what they are referred to as in the text (e.g., "the petitioner", "the appellant").
2. Respondents – the persons or entities against whom the current appeal is filed. If their name is not mentioned, write what they are referred to as in the text (e.g., "respondent 1", "the respondent-Management").
3. Issue – the main legal or factual issue being disputed in the current appeal.
4. Appellant's Stance (in the current appeal) – clearly state what the appellant is arguing for or seeking in the present appeal.
5. Respondent's Stance (in the current appeal) – clearly state what the respondent is arguing for or seeking in the present appeal.
6. Present Court – the court currently deciding the present appeal (e.g., Supreme Court of India, High Court of Bombay). 

Important instructions:
- Do NOT assume the appellant is the party introduced first. Carefully check who has filed the current appeal.
- Do NOT summarize or include opinions or findings of lower courts unless those are being specifically challenged in this appeal.
- Do NOT list courts or tribunals unless they are explicitly a party.
- Focus on the actual parties to the legal dispute.
- Use only the format below for your output:

Appellants: <name or description>
Respondents: <name or description>
Issue: <brief summary>
Appellant's Stance: <stance>
Respondent's Stance: <stance>
Present Court: <court name>

### Facts:
\"\"\"{facts}\"\"\""""

# Process each row
contexts = []
for i, row in df.iterrows():
    facts = extract_facts(row.get("Labeled_Sentences", ""))
    if not facts:
        contexts.append("")
        continue

    facts_text = " ".join(facts)

    # Format prompt
    prompt = prompt_template.format(facts=facts_text)

    # Call GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    contexts.append(response.choices[0].message.content.strip())

# Save back into dataframe
df["Case_Context"] = contexts
df.to_csv("cases_with_context.csv", index=False)
