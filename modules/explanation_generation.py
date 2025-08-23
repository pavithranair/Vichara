import pandas as pd
import openai
from dotenv import load_dotenv
import os
from utils.prompts import explanation_prompt

# Load environment variables from .env file
load_dotenv()

# Access them using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

def generate_structured_explanation(context, court_ruling, decision_points_text, predicted_outcome, model="gpt-4o-mini"):
    """
    Generates a structured legal explanation from case context, final ruling, decision points, and predicted outcome.
    """
    # Format the predicted outcome text
    outcome_text = "GRANTED" if predicted_outcome == 1 else "DISMISSED" if predicted_outcome == 0 else "UNKNOWN"
    
    prompt = explanation_prompt.format(
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
