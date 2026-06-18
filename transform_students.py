from pymongo import MongoClient
from config import *
from helpers.shift_mapper import map_shift
from helpers.seat_mapper import map_seat
import pandas as pd

client = MongoClient(MONGO_URI)

old_db = client[OLD_DB]
new_db = client[NEW_DB]

students = list(old_db.students.find({}))

shifts = list(
    new_db.shifts.find({
        "adminId": ADMIN_ID
    })
)

seats = list(
    new_db.seats.find({
        "adminId": ADMIN_ID
    })
)

print(f"Students : {len(students)}")
print(f"Shifts   : {len(shifts)}")
print(f"Seats    : {len(seats)}")

preview = []

for student in students:

    sid = student.get("sid")

    new_student_id = f"STD101-{sid:04d}"

    shift_name = map_shift(
        student.get("shift"),
        student.get("time")
    )

    seat_name = map_seat(student)

    preview.append({
        "sid": sid,
        "studentId": new_student_id,
        "name": student.get("name"),
        "oldShift": student.get("shift"),
        "oldTime": student.get("time"),
        "newShift": shift_name,
        "oldSeat": student.get("seatNumber"),
        "newSeat": seat_name,
        "status": student.get("status")
    })

df = pd.DataFrame(preview)

df.to_excel(
    "reports/migration_preview.xlsx",
    index=False
)

print("Preview Created")