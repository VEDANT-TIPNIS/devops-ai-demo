import json
import os
import sys
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")


def analyze_failure(log_text):
    prompt = f"""
You are an AI assistant for DevOps CI/CD troubleshooting.

Analyze the Jenkins failure log below.

Provide exactly these sections:

1. Failure Category
2. Evidence
3. Likely Root Cause
4. Recommended Remediation
5. Confidence

Rules:
- Base the analysis only on evidence in the log.
- Do not invent files, versions, errors, or causes.
- Distinguish between an application defect and a test defect when possible.
- If the log shows that the actual application value is correct but the
  test expects a different value, identify the test expectation as the
  likely defect.
- Keep the answer concise and technically specific.
- Use "High" confidence when the log directly proves the cause.
- Use "Medium" or "Low" only when important evidence is missing.

JENKINS FAILURE LOG
-------------------
{log_text}
-------------------
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["message"]["content"]


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ai_analyzer.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]

    with open(log_file, "r", encoding="utf-8") as file:
        log_text = file.read()

    print("=" * 70)
    print("AI DEVOPS FAILURE ANALYSIS")
    print("=" * 70)

    print(analyze_failure(log_text))

    print("=" * 70)


if __name__ == "__main__":
    main()
