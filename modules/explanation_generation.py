import pandas as pd
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

# Prompt template for structured legal explanation
STRUCTURED_EXPLANATION_PROMPT = """You are a legal assistant. Your task is to generate a structured legal explanation for the court's predicted decision in this appeal case.

You are given:
- The **case context** including appellant, respondent, issue, and stances
- The **final court ruling** from the present court
- A set of **decision points** extracted from the case. A **decision point** refers to a key moment in the case where a specific issue was considered, a responsible authority or decision-maker evaluated it, and a determination or outcome was reached.
- The **predicted outcome** of the appeal

Generate a structured explanation with the following sections:

---
Facts of the Case:
[A brief summary of the background, parties involved, and what led to the appeal.]

Legal Issue(s) Presented:
[The legal question(s) the court had to decide.]

Applicable Law and Precedents:
[Key statutes, constitutional provisions, or case law relied on.]

Analysis / Reasoning:
[A logical application of law to facts, showing why the court ruled the way it did.]

Predicted Conclusion:
[Restate the predicted outcome using legal terminology (e.g. 'Appeal Allowed' or 'Dismissed').]
---

### Case Context:
{context}

### Final Court Ruling:
{court_ruling}

### Decision Points:
{decision_points_text}

### Predicted Outcome:
{predicted_outcome}
"""

def generate_structured_explanation(context, court_ruling, decision_points_text, predicted_outcome, model="gpt-4o-mini"):
    """
    Generates a structured legal explanation from case context, final ruling, decision points, and predicted outcome.
    """
    # Format the predicted outcome text
    outcome_text = "GRANTED" if predicted_outcome == 1 else "DISMISSED" if predicted_outcome == 0 else "UNKNOWN"
    
    prompt = STRUCTURED_EXPLANATION_PROMPT.format(
        context=context,
        court_ruling=court_ruling,
        decision_points_text=decision_points_text,
        predicted_outcome=outcome_text
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()


# Example usage with a DataFrame
df = pd.read_csv("cases_with_predictions.csv")  # Columns: Case_Context, Final_Ruling, Decision_Points, Judgment_Prediction

structured_explanations = []
for idx, row in df.iterrows():
    context = row["Case_Context"]
    court_ruling = row["Final_Ruling"]
    decision_points_text = row["decision_points"]  # string representation
    predicted_outcome = row["Judgment_Prediction"]
    
    explanation = generate_structured_explanation(context, court_ruling, decision_points_text, predicted_outcome)
    structured_explanations.append(explanation)

df["Structured_Explanation"] = structured_explanations
df.to_csv("cases_with_structured_explanations.csv", index=False)
