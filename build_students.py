import json
import os

from pymongo import MongoClient
from bson import ObjectId

from config import *
from helpers.shift_mapper import map_shift
from helpers.seat_mapper import map_seat

client = MongoClient(MONGO_URI)

old_db = client[OLD_DB]
new_db = client[NEW_DB]

students = list(old_db.students.find({}))

# Load shifts for this admin
shift_map = {}

for shift in new_db.shifts.find({
    "adminId": ADMIN_ID
}):
    shift_map[shift["name"]] = shift

output = []

for student in students:

    sid = student.get("sid")

    # Student ID
    student_id = f"STD101-{sid:04d}"

    # Shift Mapping
    shift_name = map_shift(
        student.get("shift"),
        student.get("time")
    )

    shift_doc = shift_map.get(shift_name)

    if not shift_doc:
        print(
            f"Shift not found for SID {sid}: {shift_name}"
        )
        continue

    # Seat Mapping
    seat_number = map_seat(student)

    # Subscription Status
    old_status = (student.get("status") or "").strip()

    if old_status == "Active":
        subscription_status = "active"

    elif old_status == "Trash":
        subscription_status = "trash"

    else:
        subscription_status = "inactive"

    # Image
    image_name = student.get("image")

    profile_image = ""

    if image_name:
        profile_image = (
            f"uploads/student/{LIBRARY_ID}/profilepic/{image_name}"
        )

    document = {

        "libraryId": LIBRARY_ID,

        "adminId": str(ADMIN_ID),

        "studentId": student_id,

        "name": student.get("name"),

        "email": student.get("email", ""),

        "phone": student.get("mobile", ""),

        "gender": (
            student.get("gender", "")
            .lower()
            .strip()
        ),

        "address": student.get("address", ""),

        "admissionDate": student.get("admissionDate"),

        "profileImage": profile_image,

        "password": student.get("password"),

        "subscription": {
            "startDate": student.get("admissionDate"),
            "endDate": student.get("nextPayment"),
            "status": subscription_status
        },

        "paymentStatus": "due",

        "totalPaid": 0,
        "dueAmount": 0,
        "advanceAmount": 0,

        "lastPaymentDate": student.get("lastPayment"),

        "overallDiscount": 0,

        "seat": {
            "seatNumber": seat_number or "",
            "fixed": bool(seat_number)
        },

        "shift": {
            "shiftName": shift_doc["name"]
        },

        "locker": {
            "hasLocker": False,
            "lockerId": None,
            "lockerNumber": "",
            "startDate": None,
            "endDate": None,
            "paid": False
        },

        "registrationFee": {
            "registrationAmount": 0,
            "status": "paid"
        },

        "registrationFeeApplicable": False,
        "registrationFeePaid": False,
        "registrationFeeWaived": False,

        "shiftAmount": shift_doc["price"],

        "lockerAmount": 0,

        "amount": shift_doc["price"]
    }

    output.append(document)

os.makedirs("exports", exist_ok=True)

with open(
    "exports/students_ready.json",
    "w"
) as f:
    json.dump(
        output,
        f,
        indent=2,
        default=str
    )

print(
    f"Students Generated: {len(output)}"
)