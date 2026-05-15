import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_research(topic: str) -> str:
    api_key = os.getenv("PREPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PREPLEXITY_API_KEY not set in .env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a research assistant. Provide a concise, factual summary "
                    "with key points, interesting facts, and cultural context. "
                    "Structure your response with a brief overview followed by bullet points."
                ),
            },
            {
                "role": "user",
                "content": f"Research this topic thoroughly for a newsletter article: {topic}",
            },
        ],
    }

    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_perplexity.py <topic>")
        sys.exit(1)
    topic = " ".join(sys.argv[1:])
    print(fetch_research(topic))
