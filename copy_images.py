import os
import shutil

SOURCE = "/root/Library-Student-Management/server/uploads"

DESTINATION = (
    "/root/Saas-Library-Management/server/uploads/"
    "student/LIB-2402-101/profilepic"
)

os.makedirs(DESTINATION, exist_ok=True)

copied = 0

for file in os.listdir(SOURCE):

    if not (
        file.endswith(".jpg")
        or file.endswith(".jpeg")
    ):
        continue

    src = os.path.join(SOURCE, file)
    dst = os.path.join(DESTINATION, file)

    shutil.copy2(src, dst)

    copied += 1

print(f"Images Copied: {copied}")