import pandas as pd
import tiktoken
import openai
import json
from dotenv import load_dotenv
import os
from utils.prompts import decision_point_prompt

# Load environment variables from .env file
load_dotenv()

# Access them using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# Tokenizer for the model
enc = tiktoken.encoding_for_model("gpt-4o-mini")

def extract_decision_points(text, present_court, chunk_size=1000):
    """
    Splits the text into chunks of 'chunk_size' tokens, 
    sends each to GPT, and returns concatenated JSON decision points.
    """
    tokens = enc.encode(text)
    outputs = []

    for i in range(0, len(tokens), chunk_size):
        chunk = enc.decode(tokens[i:i+chunk_size])
        
        prompt = decision_point_prompt.format(group_text=chunk, present_court=present_court)
        
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
df.to_csv("decision_points.csv", index=False)
