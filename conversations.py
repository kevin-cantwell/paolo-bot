import os
import redis
import json
from dotenv import load_dotenv
load_dotenv()
if "REDISCLOUD_URL" not in os.environ:
    print("REDISCLOUD_URL not found in environment.")
    exit(1)
else:
    redis_url = os.environ['REDISCLOUD_URL']
    db = redis.from_url(redis_url)

def add_system_message(phone_number, message):
    return db.rpush(phone_number, json.dumps({"role":"system", "content": message}))

def add_user_message(phone_number, message):
    return db.rpush(phone_number, json.dumps({"role":"user", "content": message}))

def get_convo(phone_number):
    list_items = db.lrange(phone_number, 0, -1)
    return [json.loads(item.decode('utf-8')) for item in list_items]

def convo_length(phone_number):
    return db.llen(phone_number)

def forget_oldest_user_messages(phone_number, count):
    return db.lpop(phone_number, count)