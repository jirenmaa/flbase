import os
import string
import random
import pyrebase
from pathlib import Path
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Celery("tasks", broker=os.getenv("BROKER"))

FIREBASE_CONFIG = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": os.getenv("DATABASE_URL"),
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID"),
    "measurementId": os.getenv("MEASURMENT_ID"),
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)

@app.task
def create_firebase_data(length):
    global firebase

    db = firebase.database()
    size = 12
    length = int(length)
    char_name = string.ascii_letters
    char_pswd = string.ascii_letters + string.punctuation

    print(length, type(length),"\n")
    for _ in range(length):
        print(f"Task-{_} running")
        data = {
            "name": ''.join(random.choice(char_name) for _ in range(size)),
            "age": random.randint(16, 24),
            "password": ''.join((char_pswd) for _ in range(size)),
        }

        db.push(data)
        print(f"Task-{_} completed")

