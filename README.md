# Vichara: Legal Judgment Prediction and Explanation for the Indian Judicial System

<img width="2559" height="790" alt="image" src="https://github.com/user-attachments/assets/f006c087-18bf-45e8-a58f-9b5f28b17af5" />

We present **Vichara**, a novel framework tailored to the Indian judicial system that predicts and explains legal judgments. Vichara decomposes case proceeding documents into _decision points_. Decision points are discrete legal determinations that encapsulate the legal issue, deciding authority, outcome, reasoning, and temporal context. The structured representation isolates the core determinations and their context, enabling accurate predictions and interpretable explanations. Vichara's explanations follow a structured format, inspired by the IRAC (Issue-Rule-Application-Conclusion) framework and adapted for Indian legal reasoning. This enhances interpretability, allowing legal professionals to assess the soundness of predictions efficiently. 

## Repository structure

### `evaluation/`
Contains modules for evaluating the performance of predictions and explanations.

- **`explanations/`**
  - `lexical_evaluation.py` – Evaluates explanations based on lexical similarity metrics(ROUGE-1, ROUGE-2, ROUGE-L, BLEU, METEOR).
  - `semantic_evaluation.py` – Evaluates explanations based on semantic similarity metrics(BERTScore and BLANC).
- `evaluate_prediction.py` – Combines different evaluation metrics to assess judgment predictions(accuracy, precision, recall, F1-score).

### `modules/`
Contains the core modules of the framework.

- **`rhetorical_role_labelling/`**
  - `prepare_sentences.py` – Prepares and processes sentences for role labelling.
  - `map_roles.py` – Maps sentences or clauses to their rhetorical roles.
  - `README.md` – Documentation specific to the rhetorical role labelling module.
- `case_context_construction.py` – Generates the contexts for the cases.
- `decision_point_extraction.py` – Extracts key decision points from legal cases.
- `present_court_ruling.py` – Generates the ruling of the present court in the current appeal.
- `judgment_prediction.py` – Predicts case outcomes by comparing the present court ruling and the appellant's stance from the case context.
- `explanation_generation.py` – Generates structured explanations for predictions.

### `utils/`
Contains utility scripts.

- `prompts.py` – Contains prompt templates used for LLM-based tasks.



