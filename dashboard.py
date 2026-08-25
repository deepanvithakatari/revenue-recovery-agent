import pandas as pd
import streamlit as st

# ---- Page setup ----
st.set_page_config(page_title="Revenue Recovery Agent", layout="wide")
st.title("💰 AI Revenue Recovery Agent")
st.caption("Recovering money stuck in failed payments and overdue invoices")

# ---- Load our data ----
df = pd.read_csv("audit_trail_with_ai.csv")

# ---- Top summary numbers ----
total_at_risk = df["amount"].sum()
total_recovered = df["recovered_amount"].sum()
recovery_rate = (total_recovered / total_at_risk) * 100
exceptions_count = df["is_exception"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total At Risk", f"₹{total_at_risk:,.0f}")
col2.metric("Total Recovered", f"₹{total_recovered:,.0f}")
col3.metric("Recovery Rate", f"{recovery_rate:.1f}%")
col4.metric("Exceptions (needs human)", int(exceptions_count))

st.divider()

# ---- Split into two tabs: payments and invoices ----
tab1, tab2, tab3 = st.tabs(["📉 Failed Payments", "🧾 Overdue Invoices", "⚠️ Exceptions"])

with tab1:
    payments_df = df[df["record_type"] == "payment"]
    st.subheader(f"{len(payments_df)} Failed Payments Processed")
    st.dataframe(
        payments_df[["record_id", "amount", "diagnosis", "action_taken", "ai_explanation", "recovered"]],
        use_container_width=True
    )

with tab2:
    invoices_df = df[df["record_type"] == "invoice"]
    st.subheader(f"{len(invoices_df)} Overdue Invoices Processed")
    st.dataframe(
        invoices_df[["record_id", "amount", "diagnosis", "action_taken", "ai_explanation", "recovered"]],
        use_container_width=True
    )

with tab3:
    exceptions_df = df[df["is_exception"] == True]
    st.subheader(f"{len(exceptions_df)} Records Needing Human Review")
    st.write("These are cases our agent correctly refused to act on automatically, per our stopping rules.")
    st.dataframe(
        exceptions_df[["record_id", "record_type", "amount", "diagnosis", "action_taken", "ai_explanation"]],
        use_container_width=True
    )

st.divider()

# ---- A simple chart: recovery by action type ----
st.subheader("Recovery Rate by Action Type")
action_summary = df.groupby("action_taken").agg(
    total_amount=("amount", "sum"),
    recovered_amount=("recovered_amount", "sum"),
    count=("record_id", "count")
).reset_index()
action_summary["recovery_rate_%"] = (action_summary["recovered_amount"] / action_summary["total_amount"] * 100).round(1)

st.bar_chart(action_summary.set_index("action_taken")["recovery_rate_%"])
st.dataframe(action_summary, use_container_width=True)