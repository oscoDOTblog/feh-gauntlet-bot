import asyncio, os
from config import * # current VG particpants and round dates
from easyjobs.manager import EasyJobsManager
from fastapi import FastAPI
import json

server = FastAPI()

def send_twitter_update():
    print("Pizza Time")

@server.on_event('startup')
async def startup():
    server.job_manager = await EasyJobsManager.create(
        server,
        server_secret='abcd1234'
    )

@server.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}
    
@server.get('/units')
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
