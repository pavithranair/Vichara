import pandas as pd
import ast
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

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
df = pd.read_csv("decision_points_json.csv")  # Should include: Case_Context, Present_Court, Labeled_Sentences, and decision_points column filtered for present court

# Prepare lists to store final rulings and statements
final_rulings = []
final_statements = []

for idx, row in df.iterrows():
    context = row["Case_Context"]
    present_court_points = row["present_court_decision_points"]  # already filtered JSON list
    final_statement = extract_final_statement(row.get("Labeled_Sentences", ""))
    print("FINAL STATEMENT")
    print(final_statement)

    # Store the final statement in a separate column
    final_statements.append(final_statement)

    prompt = f"""
Your goal is to identify the **final ruling of the present court** in this appeal — that is, what the present court ultimately decided and ordered.

---

### Case Context:

Below is the context of the case, which clearly identifies:
- Who the **appellant** is (the party who filed the appeal),
- Who the **respondent** is (the party defending against the appeal), and
- What the **main issue** of the appeal is.
- Appellant's Stance (in the current appeal) – What the appellant is arguing for or seeking **in the present appeal**
- Respondent's Stance (in the current appeal) – What the respondent is arguing for or seeking **in the present appeal**
- Present Court – the court currently deciding the present appeal.

Please pay close attention to this information — it overrides any assumptions you might make from the decision points. If the appellants, respondents or the issue of the appeal are not mentioned in the context, ONLY then infer these from the decision points.

{context}
---

### Decision Points:

A **decision point** is any distinct legal issue or question in the case along with the court’s stance or resolution on it.  The below decision points collectively summarize the key determinations the present court made throughout the case.

{present_court_points}
---

### Final Statements from the Present Court:

This section contains the last official statements or conclusions made by the present court in this appeal. These are the most authoritative and conclusive indication of the court’s final position and must be treated as such.

{final_statement}
---

### Your Task:

1. Provide a comprehensive explanation of the final ruling, including:
  - Specific reliefs granted or denied
  - Any orders or directions issued
  - The court’s reasoning and key factors considered
  - Relevant timelines or compliance expectations
2. Focus on the decision points to determine what the present court considered during this appeal.
3. Most importantly, use the **Final Statements from the Present Court** to determine what the court ultimately ruled — these are the court's last and binding position.

---

### Important:

- Do not confuse appellants and respondents. Use the parties as stated in the case context.
- Respond clearly and concisely.
- Do NOT state whether the appeal was granted or dismissed. Your response should only describe the final ruling of the present court.

---

### Output Format:

Final Ruling:
<Provide a detailed and comprehensive explanation of the present court’s final decision in the appeal.>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    final_ruling_text = response.choices[0].message.content.strip()
    print(final_ruling_text)
    final_rulings.append(final_ruling_text)

# Add the final ruling and statement to the dataframe
df["Final_Ruling"] = final_rulings
df["Final_Statement"] = final_statements

# Save results
df.to_csv("cases_with_final_rulings.csv", index=False)
