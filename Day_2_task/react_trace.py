"""Day 2: ReAct Agent using a Python tool."""

from config import client, MODEL, banner


# -----------------------------
# External information tool
# -----------------------------
def get_train_fare(train_name):
    train_fares = {
        "Cheran Express": 650,
        "Brindavan Express": 550
    }

    fare = train_fares.get(train_name)

    if fare is None:
        return f"Train '{train_name}' was not found."

    return f"{train_name} fare is ₹{fare}"


# -----------------------------
# ReAct instructions
# -----------------------------
SYSTEM_PROMPT = """
You are a student travel assistant.

You have access to this external tool:

get_train_fare(train_name)

Use the tool whenever the question asks for
the fare of a train.

Follow this format:

PLAN: briefly state what information is needed.
ACTION: get_train_fare("Train Name")

After receiving the tool result, use it to answer
the original question.

If no external information is required,
answer the question directly.

Do not invent train fares.

At the end provide:

FINAL ANSWER: ...
"""


# -----------------------------
# ReAct Agent
# -----------------------------
def react_agent(question):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for step in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print("\nMODEL RESPONSE:")
        print(answer)

        # Check whether the model wants to use the tool
        if "ACTION:" not in answer:
            return answer

        # Find ACTION line
        action_line = None

        for line in answer.splitlines():
            if line.strip().startswith("ACTION:"):
                action_line = line.strip()
                break

        if action_line is None:
            return answer

        print("\nACTION:")
        print(action_line)

        # Extract train name
        start = action_line.find("(")
        end = action_line.rfind(")")

        if start == -1 or end == -1:
            return "Invalid ACTION format."

        argument = action_line[start + 1:end].strip()
        train_name = argument.strip("\"'")

        # Call the tool
        observation = get_train_fare(train_name)

        print("\nOBSERVATION:")
        print(observation)

        # Give tool result back to model
        messages.append({
            "role": "assistant",
            "content": answer
        })

        messages.append({
            "role": "user",
            "content": f"""
The external tool returned:

OBSERVATION:
{observation}

Now continue solving the original question.

Use the observation when necessary.

If the problem is solved, provide:

FINAL ANSWER: ...
"""
        })

    return "Stopped: maximum steps reached."


# -----------------------------
# Questions
# -----------------------------
questions = [
    "What is the fare of Cheran Express?",

    "If the Cheran Express ticket costs ₹650 "
    "and food costs ₹200, how much money remains from ₹1000?",

    "If the Cheran Express fare is ₹650 "
    "and the student gets a 20% discount, "
    "what is the final ticket price?",

    "Can a student with ₹800 afford the "
    "Cheran Express ticket and ₹200 food expense?"
]


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    banner("DAY 2 - ReAct AGENT")

    for question in questions:

        print("\n" + "=" * 70)

        print("QUESTION:")
        print(question)

        react_agent(question)