from tools import (
    get_student_details,
    get_complaint_details,
    check_complaint_status
)


def solve_challenge():

    print("=== Hostel Complaint Challenge ===\n")

    question = input("Student: ")

    print("\n[AGENT] Understanding request...")

    # Step 1: Get student details
    print("[AGENT] Getting student details...")

    student = get_student_details()

    print("[TOOL] Student details retrieved.")

    # Step 2: Get complaint details
    print("[AGENT] Getting complaint details...")

    complaint = get_complaint_details()

    print("[TOOL] Complaint details retrieved.")

    # Step 3: Check status
    print("[AGENT] Checking complaint status...")

    status = check_complaint_status(
        complaint["status"]
    )

    print("[TOOL] Status checked.")

    # Step 4: Prepare final response
    print("\n=== Final Answer ===")

    print(f"Student: {student['name']}")
    print(f"Room: {student['room']}")
    print(f"Complaint: {complaint['complaint']}")
    print(f"Complaint ID: {complaint['complaint_id']}")
    print(f"Status: {status}")


if __name__ == "__main__":
    solve_challenge()