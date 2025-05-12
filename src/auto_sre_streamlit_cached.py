import os
import sys
import torch
import asyncio
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Disable Streamlit's file watcher
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

# Import torch and manually set torch.classes.__path__
torch.classes.__path__ = []

# --- FIX for PyTorch path error with Streamlit ---
original_import = __import__

def custom_import(name, *args):
    if name.startswith("torch"):
        module = original_import(name, *args)
        module.__path__ = []
        return module
    return original_import(name, *args)

sys.modules["__import__"] = custom_import

# --- FIX for asyncio loop error ---
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# --- Optional: Disable file watching ---
os.environ["STREAMLIT_WATCH_FILE_SYSTEM"] = "false"

# Streamlit UI
st.set_page_config(page_title="AutoSRE Assistant", page_icon="🛠️")

st.title("🛠️ AutoSRE - Incident Analyzer")

st.write("Analyze incidents, fetch similar past issues, and recommend resolutions automatically!")

incident_summary = st.text_area("Enter Incident Summary:", height=200)

# --- Initialize LLM and embeddings ---
@st.cache_resource
def get_llm():
    return OllamaLLM(model="llama3")

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory="data/chroma_db", embedding_function=embedding_model)

# Vectorstore
#embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embedding_model)

# Invoke LLM and vectorstore
llm = get_llm()
vectorstore = get_vectorstore()

# Prompts
root_cause_prompt = PromptTemplate(
    input_variables=["summary"],
    template="""
    You are a site reliability assistant. Analyze the following incident summary/error/exception and determine the most likely root cause.
    
    Incident: {summary}

    Root Cause (1-2 sentences with additional insights):
    """
)

resolution_prompt = PromptTemplate(
    input_variables=["summary", "root_cause"],
    template="""
    An incident occurred. Please suggest the most effective resolution steps with sample code snippet.

    Summary: {summary}
    Root Cause: {root_cause}

    Resolution Steps:
    """
)

# --- LangChain Chains ---
root_cause_chain = root_cause_prompt | llm
resolution_chain = resolution_prompt | llm

# Functions
# --- Cached LLM Functions ---
@st.cache_data(show_spinner="Analyzing root cause...")
def cached_analyze_root_cause(summary: str):
    return root_cause_chain.invoke({"summary": summary})

#def analyze_root_cause(summary: str):
#    return root_cause_chain.invoke({"summary": summary})

@st.cache_data(show_spinner="Fetching similar incidents...")
def cached_get_similar_incidents(summary: str, k=1):
    return vectorstore.similarity_search(summary, k=k)

#def get_similar_incidents(summary: str, k=1):
#    return vectorstore.similarity_search(summary, k=k)

@st.cache_data(show_spinner="Generating resolution steps...")
def cached_generate_resolution(summary: str, root_cause: str):
    return resolution_chain.invoke({"summary": summary, "root_cause": root_cause})

#def generate_resolution(summary: str, root_cause: str):
#    return resolution_chain.invoke({"summary": summary, "root_cause": root_cause})

#####

if st.button("Analyze Incident"):
    if incident_summary.strip() == "":
        st.warning("Please enter an incident summary.")
    else:
        root_cause = cached_analyze_root_cause(incident_summary)
       #with st.spinner("Analyzing root cause..."):
            #root_cause = analyze_root_cause(incident_summary)
            

        st.success("Root Cause Identified!")
        st.write(root_cause)

        similar_incidents = cached_get_similar_incidents(incident_summary)
        #with st.spinner("Fetching similar incidents..."):
            #similar_incidents = get_similar_incidents(incident_summary)
            

        st.subheader("Similar Past Incidents")
        for i, result in enumerate(similar_incidents):
            st.markdown(f"**Incident {i+1}:** {result.page_content}")

        resolution = cached_generate_resolution(incident_summary, root_cause)
        #with st.spinner("Generating resolution steps..."):
            #resolution = generate_resolution(incident_summary, root_cause)
            

        st.success("Recommended Resolution")
        st.write(resolution)

if st.button("Clear Cache"):
    st.cache_data.clear()

st.markdown("---")
#st.caption("Tools used:LangChain, Ollama, llama3,Chroma, HuggingFace, and Streamlit.")
