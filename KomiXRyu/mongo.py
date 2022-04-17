import asyncio
import sys

from motor import motor_asyncio
from zeldris import MONGO_DB_URI 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from zeldris.conf import get_int_key, get_str_key



MONGO_DB_URI = get_str_key("MONGO_DB_URI")
MONGO_DB = "Violet"


client = MongoClient()
client = MongoClient(MONGO_DB_URI)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
db = motor[MONGO_DB]
db = client["Violet"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(log.critical("Can't connect to mongodb! Exiting..."))
