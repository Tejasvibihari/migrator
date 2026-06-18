import re

def map_seat(student):

    seat = str(student.get("seatNumber") or "").strip()

    if not seat:
        return None

    seat_upper = seat.upper()

    # Already mapped seat
    if re.match(r"^[BG]\d+$", seat_upper):
        return seat_upper

    # Numeric seat
    if seat.isdigit():

        gender = (student.get("gender") or "").lower()

        if gender == "female":
            return f"G{seat}"

        return f"B{seat}"

    return None