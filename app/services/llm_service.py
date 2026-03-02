from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Groq client using API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# System prompt with strict rules
SYSTEM_PROMPT = """
You are an AI assistant for BeanOrbit International Public School.

STRICT RULES:
1. Answer ONLY using the provided context.
2. If the answer is not found in the context, say:
   "I can only answer questions related to BeanOrbit International Public School."
3. Do NOT make up information.
4. Keep answers clear and professional.
"""

def generate_response(context, question):
    question_lower = question.lower().strip()

    # ✅ Handle greetings manually
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]

    if question_lower in greetings:
        return "Hello! 👋 How can I assist you regarding BeanOrbit International Public School?"

    if "how are you" in question_lower:
        return "I'm doing great! 😊 How can I help you with BeanOrbit International Public School?"

    # 🚫 If no context, restrict answer
    if not context or not context.strip():
        return "I can only answer questions related to BeanOrbit International Public School."

    # 🤖 LLM Response
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""
            }
        ]
    )

    return response.choices[0].message.content
