from dataclasses import dataclass
from datetime import datetime
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from os import environ
import pymongo


app = FastAPI()

# database connection
connection = pymongo.MongoClient(environ.get("MONGO_HOSTNAME"), 27017)
collection = connection['workout']
db = collection['workout']

@dataclass
class Workout:
    burpees: int
    mins: int
    date: datetime = datetime.today()
    id: str = uuid4().hex

# CRUD
@app.get("/")
def route():
    return {"status": "this is the burpeeAPI"}

# Create
@app.post("/workout/")
async def create_workout(workout: Workout):
    db.insert_one(workout.__dict__)    

    return workout

# Read
@app.get("/workout/")
async def all_workouts():
    lst: list = []

    for i in db.find({}):
        lst.append(Workout(**i))

    return lst

@app.get("/workout/{workout_id}")
async def get_by_id(workout_id: str):
    result = db.find_one({"id": workout_id})

    if not result:
        return HTTPException(404, "Entry Not Found")

    return Workout(**result) 

@app.get("/total_reps/")
async def total_burpees():
    total = 0

    for i in db.find({}):
        total += Workout(**i).burpees

    return {"total": total}

# Update
@app.put("/workout/{workout_id}")
async def update(workout_id: str, workout: Workout):
    db.update_one({"id": workout_id}, {"$set": workout.__dict__})

    return workout

# Delete
@app.delete("/workout/{workout_id}")
async def delete(workout_id: str):
    db.find_one_and_delete({"id": workout_id})

    return {} 
