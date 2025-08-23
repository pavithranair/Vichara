import pandas as pd
import openai
from dotenv import load_dotenv
import os
from utils.prompts import judgment_prompt

# Load environment variables from .env file
load_dotenv()

# Access them using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

def predict_judgment(context, court_ruling, model="gpt-4o-mini"):
    """
    Generates a 0/1 judgment prediction based on case context and final ruling.
    """
    prompt = judgment_prompt.format(context=context, court_ruling=court_ruling)
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    output_text = response.choices[0].message.content.strip()
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
