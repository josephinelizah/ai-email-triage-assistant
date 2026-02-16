import ollama
import json
import time
from app.thread_scaler import compress_thread


def analyze_email(subject, thread):
    """
    Analyzes an email thread using a local LLM.
    Returns structured JSON output.
    """

    start_time = time.time()

    # Compress thread (ScaleDown simulation)
    compressed_thread = compress_thread(thread)

    prompt = f"""
You are an AI Email Triage Assistant.

Analyze the email below and return ONLY valid JSON.

Email Subject:
{subject}

Email Content:
{compressed_thread}

Return JSON in this exact format:

{{
    "category": "Work | Personal | Spam | Urgent",
    "priority": 1-5,
    "meeting_detected": true/false,
    "unsubscribe_suggested": true/false,
    "summary": "short summary",
    "draft_reply": "professional reply"
}}

Do NOT return anything except valid JSON.
"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response["message"]["content"]

        # Try parsing JSON
        parsed_output = json.loads(raw_output)

    except Exception as e:
        parsed_output = {
            "error": "Failed to parse model output",
            "details": str(e)
        }

    end_time = time.time()
    processing_time = round(end_time - start_time, 2)

    return {
        "result": parsed_output,
        "processing_time_seconds": processing_time
    }
