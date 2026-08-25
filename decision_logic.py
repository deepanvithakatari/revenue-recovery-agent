import pandas as pd
import random

random.seed(99)

# ---- Load our two "ingredient" files ----
df_payments = pd.read_csv("failed_payments.csv")
df_invoices = pd.read_csv("overdue_invoices.csv")

audit_trail = []  # this will be our "receipt book" — every decision gets logged here

# ============================================================
# PART 1: Decide what to do about each FAILED PAYMENT
# ============================================================
for _, row in df_payments.iterrows():
    reason = row["failure_reason"]
    retries = row["retry_count"]
    amount = row["amount"]
    pid = row["payment_id"]

    # STOPPING RULE: never retry more than 2 times, no matter what
    if retries >= 3:
        action = "give_up_flag_human"
        explanation = f"Already retried {retries} times. Stopping — flagging for a human to check."
    elif reason in ["network_error", "bank_timeout"]:
        action = "auto_retry"
        explanation = f"Failure was '{reason}', which is usually temporary. Safe to auto-retry."
    elif reason == "insufficient_funds":
        action = "send_payment_link_reminder"
        explanation = "Insufficient funds — retrying won't help. Send a reminder instead so the customer can try again later."
    elif reason == "3ds_failed":
        action = "send_auth_reminder"
        explanation = "Authentication step failed. Ask the customer to complete verification again."
    else:  # card_declined or anything else
        action = "request_alternate_payment_method"
        explanation = f"Card was declined. Asking the customer to try a different payment method."

    # ---- Simulate whether the action "worked" ----
    # These success rates are just realistic guesses. In a real product you'd
    # measure these from actual historical data.
    success_chance = {
        "auto_retry": 0.55,
        "send_payment_link_reminder": 0.35,
        "send_auth_reminder": 0.45,
        "request_alternate_payment_method": 0.30,
        "give_up_flag_human": 0.0
    }
    recovered = random.random() < success_chance[action]

    audit_trail.append({
        "record_type": "payment",
        "record_id": pid,
        "amount": amount,
        "diagnosis": reason,
        "action_taken": action,
        "explanation": explanation,
        "recovered": recovered,
        "recovered_amount": amount if recovered else 0,
        "is_exception": action == "give_up_flag_human"
    })

# ============================================================
# PART 2: Decide what to do about each OVERDUE INVOICE
# ============================================================
for _, row in df_invoices.iterrows():
    days = row["days_overdue"]
    behavior = row["past_payment_behavior"]
    amount = row["amount"]
    inv_id = row["invoice_id"]

    # STOPPING RULE: if it's very overdue AND the customer is a repeat offender,
    # don't keep nudging — escalate to a human collections process instead.
    if days > 30 and behavior == "chronic_late":
        action = "escalate_to_collections"
        explanation = f"{days} days overdue and customer has a chronic-late history. Escalating to a human."
    elif days > 30:
        action = "firm_reminder_with_deadline"
        explanation = f"{days} days overdue. Sending a firm reminder with a clear deadline."
    elif behavior == "always_on_time":
        action = "gentle_reminder"
        explanation = "Usually pays on time — probably just an oversight. Gentle nudge should work."
    else:
        action = "reminder_with_deadline"
        explanation = "Somewhat overdue, customer has a mixed payment history. Standard reminder with a deadline."

    success_chance = {
        "gentle_reminder": 0.70,
        "reminder_with_deadline": 0.50,
        "firm_reminder_with_deadline": 0.40,
        "escalate_to_collections": 0.20
    }
    recovered = random.random() < success_chance[action]

    audit_trail.append({
        "record_type": "invoice",
        "record_id": inv_id,
        "amount": amount,
        "diagnosis": f"{days} days overdue, {behavior}",
        "action_taken": action,
        "explanation": explanation,
        "recovered": recovered,
        "recovered_amount": amount if recovered else 0,
        "is_exception": action == "escalate_to_collections"
    })

# ============================================================
# PART 3: Save the audit trail + print a summary
# ============================================================
df_audit = pd.DataFrame(audit_trail)
df_audit.to_csv("audit_trail.csv", index=False)

total_at_risk = df_audit["amount"].sum()
total_recovered = df_audit["recovered_amount"].sum()
recovery_rate = (total_recovered / total_at_risk) * 100
exceptions = df_audit[df_audit["is_exception"]]

print("=" * 50)
print(f"TOTAL AMOUNT AT RISK:      ₹{total_at_risk:,.2f}")
print(f"TOTAL AMOUNT RECOVERED:    ₹{total_recovered:,.2f}")
print(f"RECOVERY RATE:             {recovery_rate:.1f}%")
print(f"EXCEPTIONS (needs human):  {len(exceptions)} records")
print("=" * 50)
print("\nFull audit trail saved to audit_trail.csv")