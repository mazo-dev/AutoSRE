from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

print("Setting up connection to data/chroma_db")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embedding_model)
collection = vectorstore._collection

print("Successfully connected to data/chroma_db")
# List all documents
print("Retrieving Incident data from data/chroma_db")
results = collection.get(include=["documents"])

print("Received Incident data from data/chroma_db, now listing it....")
for doc_id, doc_text in zip(results["ids"], results["documents"]):
    print(f"\n📄 ID: {doc_id}\n{doc_text}")

print("Listing Incident data from data/chroma_db is complete")
