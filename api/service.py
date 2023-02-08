import json
import time
import uuid
import redis

from celery import Celery
from firebase_admin import firestore
from flask import Blueprint, request

CELERY_BROKER_URL = 'redis://localhost:6379/0'

r = redis.StrictRedis(
    host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

db = firestore.client()
ref = db.collection("requests")

service = Blueprint('service', __name__)
celery = Celery('task', broker=CELERY_BROKER_URL)


def simple_ask_question(data):
    # create unique id with specific prefix
    uid = "q:" + str(uuid.uuid4().hex)
    timestamp = int(time.time())

    time.sleep(4)  # some huge task
    r.set(uid, f"{data['question']}:{timestamp}", 5)  # 30


@celery.task
def celery_ask_question(data):
    simple_ask_question(data)


@celery.task
def celery_ask_request(data):
    time.sleep(4)  # some huge task

    uid = uuid.uuid4()
    ref.document(uid.hex).set(data)


@service.route('/fast_question', methods=["POST"])
def celery_ask_for_question():
    celery_ask_question.delay(request.json)

    return json.dumps({"success": True})


@service.route('/slow_question', methods=["POST"])
def simple_ask_for_question():
    simple_ask_question(request.json)

    return json.dumps({"success": True})


@service.route('/question', methods=["GET"])
def get_questions():
    # get all keys with prefix
    keys_prefix = r.keys("q:*")

    keyval = []
    for key in keys_prefix:
        value = r.get(key)
        question, cdate = value.split(":")

        keyval.append({"id": key, "question": question, "cdate": int(cdate)})

    questions = sorted(keyval, key=lambda v: v["cdate"])

    return json.dumps({"questions": questions})


@service.route('/request', methods=["POST"])
def ask_for_request():
    # post to firebase
    celery_ask_request.delay(request.json)

    return json.dumps({"success": True})
