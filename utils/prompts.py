# Prompt for extracting case context
case_context_prompt = """You are a legal assistant helping summarize appeal case details.

Given the following facts from an appeal case document, extract the following information about the current appeal only:

1. Appellants – the persons or entities filing the current appeal. If their name is not mentioned, write what they are referred to as in the text (e.g., "the petitioner", "the appellant").
2. Respondents – the persons or entities against whom the current appeal is filed. If their name is not mentioned, write what they are referred to as in the text (e.g., "respondent 1", "the respondent-Management").
3. Issue – the main legal or factual issue being disputed in the current appeal.
4. Appellant's Stance (in the current appeal) – clearly state what the appellant is arguing for or seeking in the present appeal.
5. Respondent's Stance (in the current appeal) – clearly state what the respondent is arguing for or seeking in the present appeal.
6. Present Court – the court deciding the present appeal (e.g., Supreme Court of India, High Court of Bombay).

### Important instructions:

- Do NOT assume the appellant is the party introduced first. Carefully check who has filed the current appeal.
- Do NOT summarize or include opinions or findings of lower courts unless those are being specifically challenged in this appeal.
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

# Prompt for extracting decision points
decision_point_prompt = """You are a legal assistant tasked with extracting **all decision points** from an excerpt of a court case proceeding. 
Decision points are discrete legal determinations made at different stages throughout the case.

Given the following text and the present court, extract **all identifiable decision points** and output them in strict JSON format as a list of objects.

Each decision point object should include:

- "issue": the legal issue or question being addressed
- "decision_maker": the court or authority that made the decision (e.g., Supreme Court, Trial Court, High Court)
- "outcome": the result or resolution of the issue
- "time": (optional) the date or timeframe of the decision if mentioned
- "reasoning": (optional) summary of the Court's reasoning, including references to statutes, arguments, facts, or precedents
- "present_court_decision": true if the "decision_maker" is the same as the present court provided, otherwise false

### Important instructions:
- Do not include any extra text or explanation.
- Do not assume or hallucinate decision makers.
- Do NOT include triple backticks (```) anywhere.

### Output Format:

[
  {{
    "issue": "<string>",
    "decision_maker": "<string>",
    "outcome": "<string>",
    "time": "<string or null>",
    "reasoning": "<string or null>",
    "present_court_decision": <true or false>
  }}
]

### Input:
Present Court: "{present_court}"
Text: \"\"\"{group_text}\"\"\"
"""

# Prompt for generating the present court's final ruling
final_ruling_prompt = """
Your goal is to identify the **final ruling of the present court** in this appeal — that is, what the present court ultimately decided and ordered.

### Case Context:

Below is the context of the case, which clearly identifies:
- Who the **appellant** is (the party who filed the appeal)
- Who the **respondent** is (the party defending against the appeal)
- What the **main issue** of the appeal is.
- Appellant's Stance (in the current appeal) – What the appellant is arguing for or seeking **in the present appeal**
- Respondent's Stance (in the current appeal) – What the respondent is arguing for or seeking **in the present appeal**
- Present Court – the court deciding the present appeal.

Please pay close attention to this information, it overrides any assumptions you might make from the decision points. If the appellants, respondents or the issue of the appeal are not mentioned in the context, ONLY then infer these from the decision points.

{context}
---

### Decision Points:

Decision points are discrete legal determinations made at different stages throughout the case. The below decision points collectively summarize the key determinations the present court made throughout the case.

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
3. Use the **Final Statements from the Present Court** to determine what the court ultimately ruled. These are the court's last and binding position.
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

# Prompt template for judgment prediction
judgment_prompt = """You are a legal assistant helping to analyze the outcome of an appeal. Your task is to determine whether the **present court’s final ruling** aligns with what the **appellant** was seeking in this appeal.

### Case Context:
The context below includes:
- Appellants: The **appellant** (party who filed the appeal)
- Respondents: The **respondent** (party defending the appeal)
- Issue: The **main issue**
- Appellant's Stance: What the **appellant is seeking** in the current appeal
- Respondent's Stance: What the **respondent is seeking** in the current appeal
- Present Court: The court deciding the present appeal.

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

# Prompt template for structured legal explanation
explanation_prompt = """You are a legal assistant. Your task is to generate a structured legal explanation for the court's predicted decision in this appeal case.

You are given:
- The **case context** including appellant, respondent, issue, stances and the court deciding the appeal
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
