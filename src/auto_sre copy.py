from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
#from langchain.chains import LLMChain

# Create the LLM
llm = OllamaLLM(model="llama3")

############################### Analyse the Root Cause ####################
# Create the prompt
prompt = PromptTemplate(
    input_variables=["incident_summary"],
    template="""
    You are a site reliability assistant. Analyze the following incident summary and determine the most likely root cause.

    Incident: {incident_summary}

    Root Cause (1-2 sentences):
    """
)

# Create the chain
#root_cause_chain = LLMChain(llm=llm, prompt=prompt)
root_cause_chain = prompt | llm

def analyze_root_cause(summary: str):
    #return root_cause_chain.run(summary)
    return root_cause_chain.invoke(summary)

################### Get similiar incidents from vecorDB ###################
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embedding_model)

def get_similar_incidents(summary: str, k=3):
    return vectorstore.similarity_search(summary, k=k)
##################### Generate the incident resolution #######################
resolution_prompt = PromptTemplate(
    input_variables=["summary", "root_cause"],
    template="""
    An incident occurred. Please suggest the most effective resolution steps.

    Summary: {summary}
    Root Cause: {root_cause}

    Resolution Steps:
    """
)

#responder_chain = LLMChain(llm=llm, prompt=resolution_prompt)
responder_chain = resolution_prompt | llm

def generate_resolution(summary: str, root_cause: str):
    return responder_chain.invoke({"summary": summary, "root_cause": root_cause})
################################################################################
def run_auto_sre():
    print("--------------------------------------------")
    summary = input("📝 Enter incident summary(or type 'exit' to quit):\n")
    print("--------------------------------------------")

    if summary.strip().lower() == "exit":
        return False  # Return False to signal exit
    
    print("\n🔍 Analyzing root cause...")
    root_cause = analyze_root_cause(summary)
    print("--------------------------------------------")
    print(f"\n🧠 Root Cause: {root_cause}")
    print("--------------------------------------------")

    print("\n📚 Fetching similar past incidents...Showing latest top 3 incidents")
    list = get_similar_incidents(summary)
    for i, result in enumerate(list):
        print(f"\n📄 Past Incident {i+1}:\n{result.page_content}")

    print("--------------------------------------------")
    print("🤖 Generating resolution steps...")
    resolution = generate_resolution(summary, root_cause)
    print(f"\n✅ Recommended Resolution:\n{resolution}")
    print("--------------------------------------------")

if __name__ == "__main__":
    while True:
        continue_running = run_auto_sre()
        if not continue_running:
            print("\n👋 Exiting AutoSRE Program. Bye!")
            break
    
