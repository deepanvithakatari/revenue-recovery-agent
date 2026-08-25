import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(7)  # different seed just so this data looks different from payments

behaviors = ["always_on_time", "sometimes_late", "chronic_late"]

overdue_invoices = []
for i in range(50):
    days_overdue = random.randint(1, 60)
    behavior = random.choice(behaviors)
    due_date = datetime.now() - timedelta(days=days_overdue)

    overdue_invoices.append({
        "invoice_id": f"inv_{2000+i}",
        "customer_id": f"cust_{random.randint(1,40)}",
        "amount": round(random.uniform(5000, 200000), 2),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "days_overdue": days_overdue,
        "past_payment_behavior": behavior,
        "contact_email": f"business{i}@example.com"
    })

df_invoices = pd.DataFrame(overdue_invoices)
df_invoices.to_csv("overdue_invoices.csv", index=False)
print("Overdue invoices file created!")
print(df_invoices.head())