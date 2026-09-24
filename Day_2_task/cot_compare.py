"""Day 2: Direct Prompting vs Chain-of-Thought Prompting."""

from config import client, MODEL, banner


# --------------------------------------------------
# DIRECT PROMPTING
# --------------------------------------------------

def direct_prompt(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# --------------------------------------------------
# CHAIN-OF-THOUGHT STYLE PROMPTING
# --------------------------------------------------

def chain_of_thought_prompt(question):

    prompt = f"""
You are a student travel assistant.

Solve the following question carefully.

Use a step-by-step reasoning approach before giving
the final answer.

Give only a concise explanation of the important
calculation steps and then the final answer.

Do not invent information that is not provided.

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# --------------------------------------------------
# QUESTIONS
# --------------------------------------------------

questions = [

    "A student has ₹1000. "
    "The train ticket costs ₹650 and food costs ₹200. "
    "How much money remains?",

    "A train ticket costs ₹650. "
    "The student gets a 20% discount. "
    "What is the final ticket price?",

    "The ticket costs ₹650 and food costs ₹200. "
    "A student has ₹800. "
    "Can the student afford both expenses?",

    "What is the fare of Cheran Express according to "
    "the train information?"
]


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    banner("DAY 2 - DIRECT PROMPTING vs CHAIN-OF-THOUGHT")

    for question in questions:

        print("\n" + "-" * 70)
        print("QUESTION:")
        print(question)

        print("\n[ DIRECT PROMPTING ]")
        print(direct_prompt(question))

        print("\n[ CHAIN-OF-THOUGHT STYLE PROMPTING ]")
        print(chain_of_thought_prompt(question))