import requests

def query_ollama(prompt: str, model: str = "llama3") -> str:
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

if __name__ == "__main__":
    test_prompt = "Summarize this log for these errors and provide resolution:\n[2025-04-13 12:03:22] ERROR: Service XYZ failed due to OOM \n [2025-04-13 12:04:22] ERROR: Service XYZ is unavailable due to connection refused"
    print(query_ollama(test_prompt))
