from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

def break_goal_into_tasks(goal):
    prompt = f"""
    You are an AI productivity assistant.
    Break the following goal into 7-10 small daily actionable tasks.
    Return output as a numbered list only.

    Goal: {goal}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful productivity assistant."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content
