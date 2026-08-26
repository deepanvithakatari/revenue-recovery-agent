# 💰 AI Revenue Recovery Agent

An AI agent that finds money slipping away — failed payments and overdue invoices — diagnoses the root cause, takes a bounded recovery action, and reports exactly how much it recovered.

Built for the Razorpay AI Buildathon — Track 03: AI Revenue Recovery.

## The Problem

Revenue loss rarely happens in one clean step. A payment fails for a dozen different reasons, or an invoice goes overdue with no automatic follow-up. Most businesses handle this manually, or not at all.

## What This Agent Does

1. **Diagnoses** why a payment failed or why an invoice is overdue (looking at failure reason, retry history, and customer payment behavior)
2. **Decides** the right intervention — auto-retry, send a reminder, or escalate to a human — based on clear rules
3. **Simulates the recovery action** and estimates whether it succeeded
4. **Explains every decision** in plain English using an AI model (IBM watsonx, Llama 3.3 70B)
5. **Reports results** on a live dashboard: total at risk, total recovered, recovery rate, and an honest list of exceptions

## Results on This Batch

- **Total at risk:** ₹61,13,571
- **Total recovered:** ₹29,19,882
- **Recovery rate:** 47.8%
- **Exceptions flagged for human review:** 13 records

## Stopping Rules (Safety Guardrails)

- Payments are never retried more than 2 times
- Payments failed due to insufficient funds are never blindly retried — a reminder is sent instead
- Invoices from chronic-late customers past 30 days are escalated to a human, not endlessly nudged
- Every single decision is logged in a full audit trail (`audit_trail_with_ai.csv`)

## Architecture

Synthetic Data (CSV)  
   → Diagnosis + Decision Logic (decision_logic.py)  
   → AI Explanation Layer (ai_explain.py — IBM watsonx)  
   → Dashboard (dashboard.py — Streamlit)

## How to Run This Yourself

1. Clone this repo
2. Install dependencies: `pip install pandas streamlit ibm-watsonx-ai`
3. Create your own `credentials.py` with your IBM watsonx API key and Project ID (see `credentials_example.py` for the format)
4. Run the pipeline in order:
   - `python generate_data.py`
   - `python generate_invoices.py`
   - `python decision_logic.py`
   - `python ai_explain.py`
   - `streamlit run dashboard.py`

   
**Note:** `audit_trail_with_ai.csv` is already included with real AI-generated explanations, so you can run `streamlit run dashboard.py` immediately without needing your own IBM watsonx credentials. Credentials are only required if you want to regenerate the AI explanations yourself via `ai_explain.py`.

## What I'd Build Next

- Real Razorpay test-mode API integration instead of simulated actions
- A proper train/test split to measure recovery-action success rates from real outcomes, not assumed probabilities
- Retry timing logic (e.g. wait 30 min before auto-retry) instead of instant simulation