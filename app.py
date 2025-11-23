import streamlit as st
from session_state import Session
from research_manager import ResearchManager
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Company Insights",
    layout="wide",
)

# ------------------------------------------------------------
# 🔥 FULL LIGHT MODE — Forces text & background to white everywhere
# ------------------------------------------------------------
st.markdown("""
<style>

/* Force light mode on everything */
html, body, div, section, header, main, footer,
span, p, h1, h2, h3, h4, h5, h6,
label, textarea, input, select, button,
[class*="css"], * {
    color-scheme: light !important;
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f4f4f4 !important;
    border-right: 1px solid #e5e5e5 !important;
    padding: 25px 20px !important;
    color: #000000 !important;
}

/* Remove Streamlit dark overlays */
[data-testid="stAppViewContainer"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stHeader"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Inputs */
input, textarea, select {
    border-radius: 8px !important;
    border: 1px solid #d0d0d0 !important;
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Blue buttons */
.stButton>button {
    background-color: #5e8df7 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
    border: none !important;
}
.stButton>button:hover {
    background-color: #4c7ee0 !important;
}

/* Card */
.clean-card {
    background-color: #ffffff !important;
    padding: 20px !important;
    border-radius: 12px !important;
    border: 1px solid #e6e6e6 !important;
    margin-bottom: 22px !important;
}

/* Expander full width */
.streamlit-expander, .streamlit-expanderContent {
    background-color: #ffffff !important;
    color: #000000 !important;
    width: 100% !important;
}

/* Textarea full width */
textarea {
    width: 100% !important;
}

/* Logs */
.log-box, .log-box * {
    background-color: #fafafa !important;
    color: #000000 !important;
    border: 1px solid #e0e0e0 !important;
}

.block-container {
    max-width: 92% !important;
}

.title-text {
    font-size: 28px !important;
    font-weight: 600 !important;
    margin-top: 40px !important;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Initialize session + manager
# ------------------------------------------------------------
session = Session()
manager = ResearchManager()


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("### Company Insights")

    company = st.text_input("Company Name", value=session.get("company", ""))

    if st.button("Start Research"):
        if company.strip():
            session.set("company", company.strip())
            with st.spinner("Running research…"):
                manager.start_research(company.strip(), session)
            st.rerun()
        else:
            st.error("Please enter a company name.")

    st.markdown("### Model")
    selected_model = st.selectbox(
        "",
        ["Gemini 2.5 Flash", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    )

    if selected_model != "Gemini 2.5 Flash":
        os.environ["GROQ_MODEL"] = selected_model

    st.markdown("---")

    if st.button("Reset Session"):
        session.clear()
        st.rerun()


# ------------------------------------------------------------
# Show welcome screen if no research yet
# ------------------------------------------------------------
plan = session.get("account_plan", {})

if not plan:
    st.markdown("<div class='title-text'>Company Research Assistant</div>", unsafe_allow_html=True)
    st.write("Enter a company name in the sidebar to generate a full account plan.")
    st.stop()


# ------------------------------------------------------------
# Main Layout: Left = Q/A, Right = Account Plan
# ------------------------------------------------------------
col_left, col_right = st.columns([0.9, 2.1])


# ------------------------------------------------------------
# LEFT SIDE — Q/A
# ------------------------------------------------------------
with col_left:

    # Ask a Question
    st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
    st.markdown("#### Ask a Question")

    q = st.text_input("Your question:")

    if st.button("Submit Question"):
        if q.strip():
            answer = manager.ask_question(q.strip(), session)
            session.set("last_answer", answer)
            session.append_log(f"Q: {q}")
            session.append_log(f"A: {answer}")
            st.success("Answer added.")
            st.rerun()
        else:
            st.error("Please type a question.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Answer panel
    answer = session.get("last_answer")
    if answer:
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.markdown("#### Answer")
        st.write(answer)
        st.markdown("</div>", unsafe_allow_html=True)

    # Logs
    with st.expander("Show Logs"):
        logs = session.get("logs", [])
        if logs:
            st.markdown("<div class='log-box'>", unsafe_allow_html=True)
            for log in logs:
                st.write(log)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No logs available.")


# ------------------------------------------------------------
# RIGHT SIDE — Full-width Account Plan
# ------------------------------------------------------------
with col_right:
    st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
    st.markdown("### Account Plan")

    for section, content in plan.items():
        with st.expander(section, expanded=True):

            updated = st.text_area(f"Edit {section}", content, height=220)

            c1, c2 = st.columns(2)

            if c1.button(f"Save {section}"):
                session.set_account_section(section, updated)
                st.success("Saved.")

            if c2.button(f"Regenerate {section}"):
                new_content = manager.regenerate_section(section, session)
                session.set_account_section(section, new_content)
                st.success("Regenerated.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
