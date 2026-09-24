from tools import (
    get_student_details,
    get_complaint_details,
    check_complaint_status
)


def hostel_agent(question):

    print("\n[AGENT] User question received.")

    # Step 1: Understand the request
    print("[AGENT] Understanding the user's request...")

    # Step 2: Get student information
    print("[AGENT] Selecting get_student_details tool.")

    student = get_student_details()

    print("[TOOL] Student information retrieved.")

    # Step 3: Get complaint information
    print("[AGENT] Selecting get_complaint_details tool.")

    complaint = get_complaint_details()

    print("[TOOL] Complaint information retrieved.")

    # Step 4: Check complaint status
    print("[AGENT] Selecting check_complaint_status tool.")

    status = check_complaint_status(
        complaint["status"]
    )

    print("[TOOL] Complaint status checked.")

    # Step 5: Generate final response
    answer = f"""
Student: {student["name"]}
Student ID: {student["student_id"]}
Room: {student["room"]}

Complaint ID: {complaint["complaint_id"]}
Complaint: {complaint["complaint"]}

Status: {status}
"""

    return answer


if __name__ == "__main__":

    question = input("Student: ")

    result = hostel_agent(question)

    print("\nAgent:")
    print(result)