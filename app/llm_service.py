import logging, time
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(context, email_text):
    prompt = f"""
    Context:
    {context}

    Email:
    {email_text}

    Generate a professional reply.
    """

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"LLM attempt {attempt+1} failed: {str(e)}")
            time.sleep(2)

    return "Temporary issue. Support will respond shortly."
