# uvicorn api:app --host 0.0.0.0 --port 5057
import json
from config import * # current VG particpants and round dates
from fastapi import FastAPI
from pydantic import BaseModel
from secrets import *

app = FastAPI()

# Request body classes
class Bot(BaseModel):
    name: str
    # description: str = None

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

@app.get('/config/bot/discord/{bot_name}')
def get_config_for_discord_bot(bot_name: str):
    name = bot_name
    guild = DISCORD_GUILD
    token = DISCORD_TOKEN [name]
    return json.dumps({"bot":[{"name":name}, {"guild": guild}, {"token": token}]})
