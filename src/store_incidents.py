import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document

filename = "data/it_incident_dataset_2000.json"
# Load incidents
print(f"Reading the file {filename}")
with open(filename, "r") as f:
    incidents = json.load(f)

print(f"Preparing document for loading..........")
docs = []
for incident in incidents:
    text = f"""
    Date: {incident['date']}
    Incident_Number: {incident['incident_number']}
    Incident_Category: {incident['incident_category']}
    Incident_Summary: {incident['incident_summary']}
    Incident_Details: {incident['incident_details']}
    Incident_RCA: {incident['root_cause']}
    Incident_Impact: {incident['incident_impact']}
    Incident_Resolution: {incident['incident_resolution']}
    Incident_Errors: {incident['errors']}
    Incident_Exception: {incident['exception']}
    Incident_Full_Exception: {incident['qualified_exception']}
    Incident_Stacktrace: {incident['exception_stack_trace']}
    """
    docs.append(Document(page_content=text))

# Create embeddings and store in ChromaDB
print(f"Loading the incident data in data/chroma_db..........")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(docs, embedding_model, persist_directory="data/chroma_db")

print("Incident data successfully embedded and stored in ChromaDB.")
