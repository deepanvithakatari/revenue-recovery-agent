import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)  # this makes our "randomness" repeatable every time we run it

# ---- Part A: Fake failed payments ----
failure_reasons = ["insufficient_funds", "card_declined", "bank_timeout", "3ds_failed", "network_error"]
payment_methods = ["card", "upi", "netbanking", "wallet"]

failed_payments = []
for i in range(70):
    failed_payments.append({
        "payment_id": f"pay_{1000+i}",
        "customer_id": f"cust_{random.randint(1,40)}",
        "amount": round(random.uniform(200, 15000), 2),
        "currency": "INR",
        "failure_reason": random.choice(failure_reasons),
        "payment_method": random.choice(payment_methods),
        "retry_count": random.randint(0, 3),
        "timestamp": (datetime.now() - timedelta(days=random.randint(0,10))).strftime("%Y-%m-%d %H:%M"),
        "customer_email": f"customer{i}@example.com"
    })

df_payments = pd.DataFrame(failed_payments)
df_payments.to_csv("failed_payments.csv", index=False)
print("Failed payments file created!")
print(df_payments.head())