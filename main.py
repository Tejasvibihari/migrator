from pymongo import MongoClient
from config import *

print("=" * 50)
print("LIBRARY SATHI MIGRATION")
print("=" * 50)

client = MongoClient(MONGO_URI)

old_db = client[OLD_DB]
new_db = client[NEW_DB]

print(f"Old DB : {OLD_DB}")
print(f"New DB : {NEW_DB}")

old_student_count = old_db.students.count_documents({})
new_student_count = new_db.students.count_documents({
    "adminId": ADMIN_ID
})

print(f"\nOld Students : {old_student_count}")
print(f"New Students : {new_student_count}")

print("\nConnection Successful")