student_data = {
    "student_id": "STU1024",
    "name": "Kanika",
    "room": "A-204",
    "complaint_id": "C102",
    "complaint": "Fan not working",
    "status": "In Progress"
}


def get_student_details():

    return {
        "student_id": student_data["student_id"],
        "name": student_data["name"],
        "room": student_data["room"]
    }


def get_complaint_details():

    return {
        "complaint_id": student_data["complaint_id"],
        "complaint": student_data["complaint"],
        "status": student_data["status"]
    }


def check_complaint_status(status):

    if status == "Resolved":
        return "The complaint has been resolved."

    elif status == "In Progress":
        return "The complaint is currently being processed."

    elif status == "Pending":
        return "The complaint is still pending."

    else:
        return "Unknown complaint status."