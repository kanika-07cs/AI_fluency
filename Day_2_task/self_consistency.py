"""Day 2: Self-Consistency demonstration."""

from collections import Counter

from config import client, MODEL, banner


# ==================================================
# SOLVE QUESTION
# ==================================================

def solve_question(question):

    prompt = f"""
You are a student travel assistant.

Solve this problem carefully.

Question:
{question}

Give a short explanation and then provide
the final numerical answer.

Use this format:

ANSWER: <answer>
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# ==================================================
# EXTRACT ANSWER
# ==================================================

def extract_answer(response):

    for line in response.splitlines():

        if line.strip().upper().startswith("ANSWER:"):

            return line.split(
                ":",
                1
            )[1].strip()

    return response.strip()


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    banner("DAY 2 - SELF CONSISTENCY")

    question = (
        "A student has ₹1000. "
        "The train ticket costs ₹650 and food costs ₹200. "
        "How much money remains?"
    )

    print("\nQUESTION:")
    print(question)

    answers = []

    # Run the same problem multiple times
    for i in range(5):

        print("\n" + "-" * 60)

        print(f"RUN {i + 1}")

        result = solve_question(question)

        print(result)

        answer = extract_answer(result)

        answers.append(answer)

    # ------------------------------------------------
    # Count repeated answers
    # ------------------------------------------------

    print("\n" + "=" * 60)
    print("SELF-CONSISTENCY SUMMARY")
    print("=" * 60)

    counts = Counter(answers)

    for answer, count in counts.items():

        print(
            f"{answer} -> {count} time(s)"
        )

    # Most common answer
    most_common = counts.most_common(1)

    if most_common:

        print(
            "\nMost frequently produced answer:",
            most_common[0][0]
        )