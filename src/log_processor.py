import requests

def summarize_logs(log_text):
    prompt = f"""You are a site reliability expert. Read the following logs and summarize the issue:
    
    Logs:
    {log_text}

    Summarize the key problem in 2-3 sentences:
    """

    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    return res.json()['response']

def classify_incident(log_text):
    prompt = f"""Classify the following log content into one of the categories: cpu, memory, disk, security, network, hardware, database, application, unknown.
    
    Logs:
    {log_text}

    Respond with one word only: the category."""

    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    return res.json()['response'].strip().lower()

# Example usage

with open("..\logs\sample_application_log.log") as f:
    logs = f.read()

summary = summarize_logs(logs)
category = classify_incident(logs)

print("📝 Summary:", summary)
print("🏷️ Category:", category)
