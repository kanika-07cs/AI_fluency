from config import client, MODEL


private_data = """
Student ID: STU1024
Student Name: Kanika
Room Number: A-204
Complaint ID: C102
Complaint: Fan not working
Complaint Status: In Progress
"""


def chatbot(question):

    prompt = f"""
You are a hostel complaint assistant.

Here is the student's private hostel information:

{private_data}

Answer the student's question using this information.

Student question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    question = input("Student: ")

    answer = chatbot(question)

    print("\nChatbot:")
    print(answer)