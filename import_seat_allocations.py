import json

from pymongo import MongoClient
from bson import ObjectId

from config import *

client = MongoClient(MONGO_URI)

db = client[NEW_DB]

with open(
    "exports/student_id_map.json"
) as f:

    student_map = json.load(f)

with open(
    "exports/seat_allocations_ready.json"
) as f:

    allocations = json.load(f)

inserted = 0

for allocation in allocations:

    student_object_id = (
        student_map.get(
            allocation["studentId"]
        )
    )

    if not student_object_id:

        print(
            f"Student Missing: "
            f"{allocation['studentId']}"
        )
        continue

    document = {

        "adminId": ObjectId(
            allocation["adminId"]
        ),

        "studentId": ObjectId(
            student_object_id
        ),

        "seatId": ObjectId(
            allocation["seatId"]
        ),

        "shiftId": ObjectId(
            allocation["shiftId"]
        ),

        "startDate": allocation["startDate"],

        "endDate": allocation["endDate"],

        "status": allocation["status"]
    }

    db.seatallocations.insert_one(
        document
    )

    inserted += 1

print(
    f"Seat Allocations Imported: "
    f"{inserted}"
)