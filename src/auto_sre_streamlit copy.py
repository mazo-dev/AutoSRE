import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import datetime

# Initialize the LLM
llm = OllamaLLM(model="llama3")

# Prompts
root_cause_prompt = PromptTemplate(
    input_variables=["summary"],
    template="""
    You are a site reliability assistant. Analyze the following incident summary and determine the most likely root cause.

    Incident: {summary}

    Root Cause (1-2 sentences with additional insights):
    """
)

resolution_prompt = PromptTemplate(
    input_variables=["summary", "root_cause"],
    template="""
    An incident occurred. Please suggest the most effective resolution steps.

    Summary: {summary}
    Root Cause: {root_cause}

    Resolution Steps:
    """
)

# Chains
root_cause_chain = root_cause_prompt | llm
responder_chain = resolution_prompt | llm

# Vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embedding_model)

# Functions
def analyze_root_cause(summary: str):
    return root_cause_chain.invoke({"summary": summary})

def get_similar_incidents(summary: str, k=1):
    return vectorstore.similarity_search(summary, k=k)

def generate_resolution(summary: str, root_cause: str):
    return responder_chain.invoke({"summary": summary, "root_cause": root_cause})

# Streamlit UI
st.set_page_config(page_title="AutoSRE Assistant", page_icon="🛠️")

st.title("🛠️ AutoSRE - Incident Analyzer")

st.write("Analyze incidents, fetch similar past issues, and recommend resolutions automatically!")

incident_summary = st.text_area("📝 Enter Incident Summary:", height=200)

if st.button("Analyze Incident"):
    if incident_summary.strip() == "":
        st.warning("Please enter an incident summary.")
    else:
        with st.spinner("🔍 Analyzing root cause..."):
            root_cause = analyze_root_cause(incident_summary)

        st.success("🧠 Root Cause Identified!")
        st.write(root_cause)

        with st.spinner("📚 Fetching similar incidents..."):
            similar_incidents = get_similar_incidents(incident_summary)

        st.subheader("📄 Similar Past Incidents")
        for i, result in enumerate(similar_incidents):
            st.markdown(f"**Incident {i+1}:** {result.page_content}")

        with st.spinner("🤖 Generating resolution steps..."):
            resolution = generate_resolution(incident_summary, root_cause)

        st.success("✅ Recommended Resolution")
        st.write(resolution)

st.markdown("---")
st.caption("Tools used:LangChain, Ollama, llama3,Chroma, HuggingFace, and Streamlit.")

# After your resolution is generated get the feedback
# 🚀 --- FEEDBACK LOOP Starts Here ---
#if st.button("Give Feedback"):
st.markdown("### 🛠️ Feedback")

feedback = st.radio(
    "Was the Root Cause and Resolution helpful?",
    ("👍 Yes", "👎 No"),
    horizontal=True,
)

if feedback == "👎 No":
    st.warning("Please suggest the correct Root Cause or Resolution:")

    corrected_root_cause = st.text_area("✏️ Correct Root Cause (optional)")
    corrected_resolution = st.text_area("✏️ Correct Resolution Steps (optional)")

    if st.button("Submit Correction"):
        if corrected_root_cause.strip() == "" and corrected_resolution.strip() == "":
            st.error("Please provide at least one correction.")
        else:
            # 🚀 Create a new document from the correction
            corrected_doc = f"""
            [Feedback Correction]
            Incident Summary: {incident_summary}
            Corrected Root Cause: {corrected_root_cause}
            Corrected Resolution: {corrected_resolution}
            Timestamp: {datetime.datetime.now().isoformat()}
            """

            # 🚀 Save this correction into Chroma VectorDB
            vectorstore.add_texts([corrected_doc])

            st.success("✅ Correction submitted successfully! The agent will learn from it.")
else:
    st.success("🎯 Great! Thanks for confirming. The agent will continue learning.")

