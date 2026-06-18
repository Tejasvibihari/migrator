def map_seat(student):

    gender = (student.get("gender") or "").lower()
    seat = str(student.get("seatNumber") or "").strip()

    if not seat:
        return None

    if gender == "male":
        return f"B{seat}"

    if gender == "female":
        return f"G{seat}"

    return f"B{seat}"