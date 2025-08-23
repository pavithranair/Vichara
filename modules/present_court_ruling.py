import pandas as pd
import ast
import openai
from dotenv import load_dotenv
import os
from utils.prompts import final_ruling_prompt

# Load environment variables from .env file
load_dotenv()

# Access them using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

def extract_final_statement(labeled_sentences):
    """
    Extract the last <Ruling from present court> sentence from a stringified list.
    """
    if not isinstance(labeled_sentences, str):
        return ""
    try:
        sentences = ast.literal_eval(labeled_sentences)
        rulings = [s.replace("<Ruling by Present Court>", "").strip() 
                   for s in sentences if "<Ruling by Present Court>" in s]
        return rulings[-1] if rulings else ""
    except Exception as e:
        print(f"Error parsing labeled sentences: {e}")
        return ""

# Load your data
df = pd.read_csv("decision_points.csv")  # Should include: Case_Context, Present_Court, Labeled_Sentences, and decision_points column filtered for present court

# Prepare lists to store final rulings and statements
final_rulings = []
final_statements = []

for idx, row in df.iterrows():
    context = row["Case_Context"]
    present_court_points = row["present_court_decision_points"]  # already filtered JSON list
    final_statement = extract_final_statement(row.get("Labeled_Sentences", ""))

    prompt = final_ruling_prompt.format(
        context=context,
        present_court_points=present_court_points,
        final_statement=final_statement
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    final_ruling_text = response.choices[0].message.content.strip()
    final_rulings.append(final_ruling_text)

# Add the final ruling and statement to the dataframe
df["Final_Ruling"] = final_rulings

# Save results
df.to_csv("cases_with_final_rulings.csv", index=False)
