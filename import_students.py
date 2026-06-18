import json

from pymongo import MongoClient
from bson import ObjectId

from config import *

client = MongoClient(MONGO_URI)

db = client[NEW_DB]

with open(
    "exports/students_ready.json"
) as f:

    students = json.load(f)

student_id_map = {}

inserted = 0

for student in students:

    student["adminId"] = ObjectId(
        student["adminId"]
    )

    seat_number = (
        student["seat"]
        .get("seatNumber")
    )

    if seat_number:

        seat_doc = db.seats.find_one({
            "adminId": ADMIN_ID,
            "seatNumber": seat_number
        })

        if seat_doc:

            student["seat"]["seatId"] = (
                seat_doc["_id"]
            )

    shift_name = (
        student["shift"]
        .get("shiftName")
    )

    shift_doc = db.shifts.find_one({
        "adminId": ADMIN_ID,
        "name": shift_name
    })

    if shift_doc:

        student["shift"]["shiftId"] = (
            shift_doc["_id"]
        )

    result = db.students.insert_one(
        student
    )

    student_id_map[
        student["studentId"]
    ] = str(result.inserted_id)

    inserted += 1

with open(
    "exports/student_id_map.json",
    "w"
) as f:

    json.dump(
        student_id_map,
        f,
        indent=2
    )

print(
    f"Students Imported: {inserted}"
)