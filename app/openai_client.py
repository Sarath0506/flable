import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_openai_summary(query: str, sources: list) -> str:
    """
    Generate marketing-specific summary using OpenAI GPT, including source content.
    """
    content = "\n\n".join(
        [f"Source: {item['url']}\nContent: {item.get('text', '')[:1500]}" for item in sources]
    )

    messages = [
        {"role": "system", "content": "You are a marketing research expert."},
        {
            "role": "user",
            "content": (
                f"Based on these recent web sources, summarize actionable marketing insights for the query: '{query}'. "
                f"Focus on trends, strategies, and practical takeaways. Keep it professional and concise.\n\n{content}"
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content

def generate_followup_questions(query: str, summary: str) -> List[str]:
    """Generate relevant follow-up questions based on the research summary"""
    messages = [
        {"role": "system", "content": "You are a marketing research expert. Generate 3 relevant follow-up questions that would help deepen the understanding of the topic."},
        {"role": "user", "content": f"Based on this research summary about '{query}', generate 3 follow-up questions:\n\n{summary}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    questions = response.choices[0].message.content.split('\n')
    return [q.strip() for q in questions if q.strip()][:3] 
