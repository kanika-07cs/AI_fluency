student_data = {
    "student_id": "STU1024",
    "name": "Kanika",
    "room": "A-204",
    "complaint_id": "C102",
    "complaint": "Fan not working",
    "status": "In Progress"
}


def get_complaint_status():

    if student_data["status"] == "Resolved":
        return "Your complaint has been resolved."

    elif student_data["status"] == "In Progress":
        return "Your complaint is currently being processed."

    elif student_data["status"] == "Pending":
        return "Your complaint is pending."

    else:
        return "Unknown complaint status."


def hostel_workflow():

    print("Student ID:", student_data["student_id"])
    print("Room:", student_data["room"])
    print("Complaint:", student_data["complaint"])

    result = get_complaint_status()

    print("Status:", result)


if __name__ == "__main__":

    hostel_workflow()