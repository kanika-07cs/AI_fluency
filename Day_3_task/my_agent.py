"""System 1: Plain LLM without an external tool."""

from config import client, MODEL


SYSTEM_PROMPT = """
You are a college assistant.

Answer general questions using your existing knowledge.

You do NOT have access to the college attendance notice
or any external files.

Do not guess or invent current student attendance records.
"""


QUESTIONS = [
    "What is student attendance?",
    "Why is regular attendance important?",
    "What is the current attendance of student 23CS101?"
]


def ask_llm(question):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    print("\n=== SYSTEM 1: PLAIN LLM ===\n")

    for question in QUESTIONS:

        print("Q:", question)

        answer = ask_llm(question)

        print("A:", answer)

        print("-" * 70)