import pandas as pd
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

# Prompt template for judgment prediction
JUDGMENT_PROMPT = """You are a legal assistant helping to analyze the outcome of an appeal. Your task is to determine whether the **present court’s final ruling** aligns with what the **appellant** was seeking in this appeal.

---

### Case Context:
The context below includes:
- Appellants: The **appellant** (party who filed the appeal)
- Respondents: The **respondent** (party defending the appeal)
- Issue: The **main issue**
- Appellant's Stance: What the **appellant is seeking** in the current appeal
- Respondent's Stance: What the **respondent is seeking** in the current appeal
- Present Court: The court currently deciding the present appeal.

{context}

---

### Final Court Ruling:
{court_ruling}

---

### Your Task:
- If the **court fully or partially granted what the appellant was seeking**, output: `Prediction: 1`
- If the **court did not grant what the appellant was seeking**, output: `Prediction: 0`

---

### Output Format:

Prediction: <0 or 1>
"""

def predict_judgment(context, court_ruling, model="gpt-4o-mini"):
    """
    Generates a 0/1 judgment prediction based on case context and final ruling.
    """
    prompt = JUDGMENT_PROMPT.format(context=context, court_ruling=court_ruling)
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    output_text = response.choices[0].message.content.strip()
    print(output_text)
    # Extract prediction number
    if "Prediction: 1" in output_text:
        return 1
    elif "Prediction: 0" in output_text:
        return 0
    else:
        # fallback if the LLM output is unexpected
        return None

# Example: Process a DataFrame of cases
df = pd.read_csv("cases_with_final_rulings.csv")  # contains 'Case_Context' and 'Final_Ruling'

predictions = []
for idx, row in df.iterrows():
    context = row["Case_Context"]
    court_ruling = row["Final_Ruling"]
    pred = predict_judgment(context, court_ruling)
    predictions.append(pred)

df["Judgment_Prediction"] = predictions

# Save results
df.to_csv("cases_with_predictions.csv", index=False)
