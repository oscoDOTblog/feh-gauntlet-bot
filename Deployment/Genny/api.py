from config import * # current VG particpants and round dates
from fastapi import FastAPI
import json

app = FastAPI()

def send_twitter_update():
    print("Pizza Time")

@app.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}
    
@app.get('/units')
def get_list_of_unit_names():
    data = [round_1_unit_1,
            round_1_unit_2,
            round_1_unit_3,
            round_1_unit_4,
            round_1_unit_5,
            round_1_unit_6,
            round_1_unit_7,
            round_1_unit_8]
    return json.dumps({"unit":[{"name":value} for value in data]})
