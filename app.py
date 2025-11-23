# app.py
import streamlit as st
from agent import CompanyAgent
import os
from pathlib import Path
import json

st.set_page_config(page_title="Company Research Assistant", layout="wide")
st.title("Company Research Assistant — Account Plan Generator")

# initialize agent (loads keys from env)
agent = CompanyAgent()

# left panel: input
with st.sidebar:
    st.image("/mnt/data/B77BC0A1-9F46-4749-9235-2DED012A3769.jpeg", width=220)
    st.header("Search Company")
    company = st.text_input("Company name (e.g., 'Zoom Video Communications')", "")
    additional_context = st.text_area("Context / Goal (optional)", "Create an account plan for outreach to their sales team.")
    submit = st.button("Generate Plan")

    st.markdown("---")
    st.write("Export")
    if st.button("Export current plan (JSON)"):
        if "plan" in st.session_state:
            Path("saved_plans").mkdir(exist_ok=True)
            fname = f"saved_plans/{company.replace(' ','_')}_plan.json"
            with open(fname, "w") as f:
                json.dump(st.session_state["plan"], f, indent=2)
            st.success(f"Saved to {fname}")
        else:
            st.warning("No plan to export.")

# main area
if submit:
    if not company.strip():
        st.error("Please enter a company name.")
    else:
        with st.spinner("Gathering info & generating plan..."):
            plan, followups = agent.generate_account_plan(company, additional_context)
            st.session_state["plan"] = plan
            st.session_state["followups"] = followups

if "plan" in st.session_state:
    plan = st.session_state["plan"]
    st.subheader(f"Account Plan — {plan.get('company','')}")
    cols = st.columns([2,3])
    with cols[0]:
        st.markdown("### Key Sections")
        for k, v in plan.items():
            if k == "company": continue
            if isinstance(v, str):
                # allow inline edit
                new = st.text_area(k, v, key=f"edit_{k}")
                plan[k] = new
            else:
                st.write(k)
    with cols[1]:
        st.markdown("### Full Plan (Markdown)")
        md = agent.plan_to_markdown(plan)
        st.markdown(md)

    # show follow-ups
    if st.session_state.get("followups"):
        st.markdown("---")
        st.header("Suggested Follow-up Questions")
        for i, q in enumerate(st.session_state["followups"], start=1):
            txt = st.text_input(f"Q{i}", value=q, key=f"follow_{i}")
        if st.button("Ask follow-ups & update plan"):
            answers = []
            idx = 1
            while f"follow_{idx}" in st.session_state:
                answers.append(st.session_state[f"follow_{idx}"])
                idx += 1
            with st.spinner("Updating plan with follow-up answers..."):
                plan = agent.update_plan_with_followups(plan, answers)
                st.session_state["plan"] = plan
                st.success("Plan updated.")
