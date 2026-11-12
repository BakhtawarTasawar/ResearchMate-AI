import streamlit as st

st.set_page_config(
    page_title="ResearchMate AI",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 ResearchMate AI")
st.subheader("Your AI-powered Scientific Research Assistant")

st.write("Understand scientific research papers through simple summaries and structured insights.")

abstract = st.text_area(
    "Paste your scientific paper abstract:",
    height=250
)

if st.button("Analyze Research Paper"):
    if abstract.strip():
        st.success("Your abstract has been received!")
        st.write(abstract)
    else:
        st.warning("Please enter an abstract.")