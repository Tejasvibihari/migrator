import json
import os

from pymongo import MongoClient
from config import *
from helpers.shift_mapper import map_shift
from helpers.seat_mapper import map_seat

client = MongoClient(MONGO_URI)

old_db = client[OLD_DB]
new_db = client[NEW_DB]

students = list(old_db.students.find({}))

# Load shifts
shift_map = {}

for shift in new_db.shifts.find({
    "adminId": ADMIN_ID
}):
    shift_map[shift["name"]] = shift

# Load seats
seat_map = {}

for seat in new_db.seats.find({
    "adminId": ADMIN_ID
}):
    seat_map[seat["seatNumber"]] = seat

output = []

for student in students:

    seat_number = map_seat(student)

    # Skip students having no seat
    if not seat_number:
        continue

    seat_doc = seat_map.get(seat_number)

    if not seat_doc:
        print(
            f"Seat not found for SID {student['sid']} : {seat_number}"
        )
        continue

    shift_name = map_shift(
        student.get("shift"),
        student.get("time")
    )

    shift_doc = shift_map.get(shift_name)

    if not shift_doc:
        print(
            f"Shift not found for SID {student['sid']}"
        )
        continue

    old_status = (student.get("status") or "").strip()

    if old_status == "Active":
        allocation_status = "alloted"

    elif old_status == "Pending":
        allocation_status = "due"

    else:
        allocation_status = "inactive"

    document = {

        "sid": student["sid"],

        "studentId": f"STD101-{student['sid']:04d}",

        "adminId": str(ADMIN_ID),

        "seatId": str(seat_doc["_id"]),

        "seatNumber": seat_number,

        "shiftId": str(shift_doc["_id"]),

        "shiftName": shift_doc["name"],

        "startDate": student.get("admissionDate"),

        "endDate": student.get("nextPayment"),

        "status": allocation_status
    }

    output.append(document)

os.makedirs("exports", exist_ok=True)

with open(
    "exports/seat_allocations_ready.json",
    "w"
) as f:
    json.dump(
        output,
        f,
        indent=2,
        default=str
    )

print(
    f"Seat Allocations Generated: {len(output)}"
)