import re

# Manual corrections for bad data in old database
MANUAL_GENDER_FIXES = {
    557: "female",  # Sweety kumari
}


def map_seat(student):

    sid = student.get("sid")

    seat = str(student.get("seatNumber") or "").strip()

    if not seat:
        return None

    # Ignore students having "Other" seat
    if seat.lower() == "other":
        return None

    # Fix leading zeros
    # Example: 01 -> 1
    if seat.isdigit():
        seat = str(int(seat))

    seat_upper = seat.upper()

    # Already formatted seat
    # Example: B21, G48
    if re.match(r"^[BG]\d+$", seat_upper):
        return seat_upper

    # Gender handling
    gender = (student.get("gender") or "").lower()

    # Apply manual correction if needed
    if sid in MANUAL_GENDER_FIXES:
        gender = MANUAL_GENDER_FIXES[sid]

    # Numeric seat mapping
    if seat.isdigit():

        if gender == "female":
            return f"G{seat}"

        return f"B{seat}"

    return None