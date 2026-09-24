"""System 2: LLM with one external tool."""

import json

from config import client, MODEL
from my_tools import read_attendance_notice, TOOLS


SYSTEM_PROMPT = """
You are a college attendance assistant.

You can answer general questions directly.

If the user asks about the actual attendance of a student,
you MUST use the read_attendance_notice tool.

Never guess or invent attendance information.
"""


def agent(question):

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

    # 1. Ask the LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        temperature=0
    )

    message = response.choices[0].message

    # 2. No tool required
    if not message.tool_calls:
        return message.content

    # 3. Add the assistant's tool request
    messages.append({
        "role": "assistant",
        "content": message.content or "",
        "tool_calls": [
            {
                "id": call.id,
                "type": "function",
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments
                }
            }
            for call in message.tool_calls
        ]
    })

    # 4. Execute the requested tool
    for call in message.tool_calls:

        name = call.function.name

        arguments = json.loads(
            call.function.arguments or "{}"
        )

        print("\nTOOL CALL")
        print("Tool:", name)
        print("Arguments:", arguments)

        if name == "read_attendance_notice":

            result = read_attendance_notice()

        else:

            result = f"Unknown tool: {name}"

        print("\nTOOL RESULT:")
        print(result)

        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": str(result)
        })

    # 5. Give the tool result back to the LLM
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        temperature=0
    )

    return final_response.choices[0].message.content


if __name__ == "__main__":

    print("\n=== SYSTEM 2: LLM + ONE EXTERNAL TOOL ===\n")

    questions = [
        "What is student attendance?",
        "Why is regular attendance important?",
        "What is the current attendance of student 23CS101?",
        "What is the attendance of Priya?"
    ]

    for question in questions:

        print("\nQ:", question)

        answer = agent(question)

        print("A:", answer)

        print("-" * 70)