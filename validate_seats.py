from pymongo import MongoClient
from config import *
from helpers.seat_mapper import map_seat

client = MongoClient(MONGO_URI)

old_db = client[OLD_DB]
new_db = client[NEW_DB]

students = list(old_db.students.find({}))

seat_set = set()

for seat in new_db.seats.find({
    "adminId": ADMIN_ID
}):
    seat_set.add(seat["seatNumber"])

missing = []

for student in students:

    seat_number = map_seat(student)

    if seat_number is None:
        continue

    if seat_number not in seat_set:
        missing.append({
            "sid": student["sid"],
            "name": student["name"],
            "seat": seat_number
        })

print("Missing Seats:", len(missing))

for row in missing[:50]:
    print(row)