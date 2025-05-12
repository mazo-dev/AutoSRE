import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import io
import re

st.set_page_config(page_title="Incident Viewer", page_icon="📚")

st.title("Incident Database Viewer")

# --- DB Connection ---
with st.spinner("Connecting to database..."):
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embedding_model)
        collection = vectorstore._collection
        results = collection.get(include=["documents"])
        st.success("Connected to Chroma DB!")
    except Exception as e:
        st.error(f"Failed to connect: {e}")
        st.stop()

docs = list(zip(results["ids"], results["documents"]))

# --- Sidebar Settings ---
with st.sidebar:
    st.header("Settings")
    per_page = st.selectbox("Incidents per page", [5, 10, 20], index=1)

# --- Search Feature with "debounce" ---
search_query = st.text_input("🔎 Search incidents...", "")

if search_query:
    docs = [(doc_id, doc_text) for doc_id, doc_text in docs if search_query.lower() in doc_text.lower()]

# --- Pagination State ---
total_docs = len(docs)
total_pages = (total_docs + per_page - 1) // per_page

if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# --- Navigation Buttons ---
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ Previous") and st.session_state.page_num > 1:
        st.session_state.page_num -= 1

with col3:
    if st.button("Next ➡️") and st.session_state.page_num < total_pages:
        st.session_state.page_num += 1

st.write(f"Page {st.session_state.page_num} of {total_pages}")

# --- Pagination ---
start_idx = (st.session_state.page_num - 1) * per_page
end_idx = start_idx + per_page
current_docs = docs[start_idx:end_idx]

# --- Highlight Text Function ---
def highlight_text(text, keyword):
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

# --- Severity Tagging ---
def get_severity_tag(text):
    text_upper = text.upper()
    if "CRITICAL" in text_upper:
        return "CRITICAL"
    elif "WARNING" in text_upper:
        return "WARNING"
    elif "INFO" in text_upper:
        return "INFO"
    else:
        return "UNKNOWN"

# --- Display Current Page Incidents ---
if current_docs:
    for doc_id, doc_text in current_docs:
        severity = get_severity_tag(doc_text)
        with st.expander(f"ID: {doc_id} [{severity}]"):
            if search_query:
                highlighted_text = highlight_text(doc_text, search_query)
                st.markdown(highlighted_text, unsafe_allow_html=True)
            else:
                st.write(doc_text)
else:
    st.warning("No incidents to display.")

# --- Download Feature ---
def generate_download_file(docs):
    output = io.StringIO()
    for doc_id, doc_text in docs:
        output.write(f"ID: {doc_id}\n{doc_text}\n\n{'-'*50}\n\n")
    return output.getvalue()

if docs:
    download_content = generate_download_file(docs)
    st.download_button(
        label="⬇️ Download Incidents as TXT",
        data=download_content,
        file_name="incident_records.txt",
        mime="text/plain",
    )

st.markdown("---")
#st.caption("Built with using LangChain, Chroma, HuggingFace, and Streamlit.")
