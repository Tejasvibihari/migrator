from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

OLD_DB = os.getenv("OLD_DB")
NEW_DB = os.getenv("NEW_DB")

ADMIN_ID = os.getenv("ADMIN_ID")
LIBRARY_ID = os.getenv("LIBRARY_ID")
LIBRARY_SERIAL = os.getenv("LIBRARY_SERIAL")