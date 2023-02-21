from fastapi import FastAPI
from dataclasses import dataclass, field 
from datetime import datetime
from uuid import uuid4
import requests
import json
import os

app = FastAPI()
SERVER = os.environ.get("DB_API_SERVER")
PORT = int(os.environ.get("DB_API_PORT"))
URL = f"http://{SERVER}:{PORT}"

@dataclass
class Workout:
    burpees: int
    mins: int
    code: str = "2M1P"
    date: datetime = datetime.today()
    id: str = uuid4().hex

@dataclass
class AnalyticsEngine:
    workouts: list = field(default_factory=list)


    def add(self, wo: Workout) -> None:
        self.workouts.append()

    def add_bulk(self, lst_workouts) -> None:
        for i in lst_workouts:
            self.workouts.append(Workout(**i))

    def totals(self) -> dict:
        total_reps: int = 0
        total_mins: int = 0
    
        for workout in self.workouts:
            total_reps += workout.burpees
            total_mins += workout.mins

        return {"burpees": total_reps, "mins": total_mins} 

def pull_json_data(url_str: str) -> AnalyticsEngine:
    analytics = AnalyticsEngine()
    all_workouts = requests.get(url_str).content

    analytics.add_bulk(json.loads(all_workouts))

    return analytics 

@app.get("/")
def home():
    return {"detail": "This is the analytics api"}

@app.get("/totals/")
def get_totals():
    workout_data = pull_json_data(URL + "/workout/")

    return workout_data.totals()
    
@app.get("/code/{code}")
def get_total_by_code(code: str):
    workout_data = pull_json_data(URL + f"/code/{code}")

    return workout_data.totals()



