import pandas as pd
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from credentials import API_KEY, PROJECT_ID, URL

credentials = Credentials(url=URL, api_key=API_KEY)

model = ModelInference(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials=credentials,
    project_id=PROJECT_ID,
        params={
        "max_new_tokens": 40,
        "temperature": 0.3,
        "stop_sequences": ["Note:", "```"]
    }
)

def clean_output(text):
    """Keep only the first real sentence, strip stray junk."""
    text = text.strip()
    # Cut off at the first newline if the model still slipped one in
    text = text.split("\n")[0]
    # Cut off anything after "Note" just in case
    text = text.split("Note")[0]
    return text.strip()

df = pd.read_csv("audit_trail.csv")
ai_explanations = []

for _, row in df.iterrows():
    prompt = f"""You are a finance operations assistant. In ONE short sentence,
explain to a human colleague why this decision was made. Be clear and professional.
Respond with ONLY the sentence. Do not add notes, code, or extra commentary.

Record type: {row['record_type']}
Diagnosis: {row['diagnosis']}
Action taken: {row['action_taken']}
Amount: ₹{row['amount']}

One-sentence explanation:"""

    response = model.generate_text(prompt=prompt)
    cleaned = clean_output(response)
    ai_explanations.append(cleaned)
    print(f"{row['record_id']} -> {cleaned}")

df["ai_explanation"] = ai_explanations
df.to_csv("audit_trail_with_ai.csv", index=False)
print("\nDone! Saved as audit_trail_with_ai.csv")