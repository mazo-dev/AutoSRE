from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = Ollama(model="llama3")

prompt = PromptTemplate(
    input_variables=["incident_summary"],
    template="""
    You are a site reliability assistant. Analyze the following incident summary and determine the most likely root cause.

    Incident: {incident_summary}

    Root Cause (1-2 sentences):
    """
)

root_cause_chain = LLMChain(llm=llm, prompt=prompt)

def analyze_root_cause(summary: str):
    return root_cause_chain.run(summary)


