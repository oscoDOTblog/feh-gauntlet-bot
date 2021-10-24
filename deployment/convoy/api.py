# uvicorn api:app --host 0.0.0.0 --port 5057
import json
from config import * # current VG particpants and round dates
from fastapi import FastAPI
from gauntlet_template import *
from pydantic import BaseModel
from secrets import *

app = FastAPI()

# Request body classes
class Bot(BaseModel):
    name: str
    # description: str = None

@app.get('/health')
def hello():
    """Test endpoint"""
    return {'status': '200'}
    

@app.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}
    
@app.get('/unit/check/{unit_name}')
def check_if_unit_is_valid(unit_name: str):
    return json.dumps({"is_valid": check_unit_validity(unit_name)})

@app.get('/unit/discord/channel/{unit_name}')
def get_unit_discord_channel(unit_name: str):
    return json.dumps({"channel": discord_channel_ids[unit_name]})

@app.get('/unit/discord/colour/{unit_name}')
def get_unit_discord_colour(unit_name: str):
    return json.dumps({"colour": discord_hex_colours[unit_name]})


@app.get('/units')
def get_list_of_unit_names_rest():
    data = get_list_of_unit_names()
    return json.dumps({"units":[{"name":value} for value in data]})

@app.get('/config/bot/discord/{bot_name}')
def get_config_for_bot_discord(bot_name: str):
    return json.dumps(
        { 
            "name": bot_name, 
            "guild": discord_guild, 
            "prefix": discord_prefix, 
            "status": discord_status[bot_name], 
            "token": DISCORD_TOKEN [bot_name]
        }
        
    )
    
@app.get('/config/bot/discord/guild/')
def get_guild_for_bot_discord():
    return json.dumps({"guild": discord_guild})

@app.get('/config/bot/discord/prefix')
def get_prefix_for_bot_discord():
    return json.dumps({"prefix": discord_prefix})
    
@app.get('/config/bot/discord/role/admin')
def get_prefix_for_bot_discord():
    return json.dumps({"role": discord_role_id_admin})
    
@app.get('/config/bot/discord/status/{bot_name}')
def get_status_for_bot_discord(bot_name: str):
    return json.dumps({"status": discord_status[bot_name]})

@app.get('/config/bot/discord/token/{bot_name}')
def get_token_for_bot_discord(bot_name: str):
    return json.dumps({"token": DISCORD_TOKEN [bot_name]})

@app.get('/config/bot/twitter/auth/{bot_env}')
def get_auth_for_bot_twitter(bot_env: str):
  if (bot_env == 'prod'):
    return json.dumps({ 
        "C_KEY": C_KEY_PROD, 
        "C_SECRET": C_SECRET_PROD, 
        "A_TOKEN": A_TOKEN_PROD, 
        "A_TOKEN_SECRET": A_TOKEN_SECRET_PROD
    }) 
  elif (bot_env == 'dev'): 
    return json.dumps({ 
        "C_KEY": C_KEY_DEV, 
        "C_SECRET": C_SECRET_DEV, 
        "A_TOKEN": A_TOKEN_DEV, 
        "A_TOKEN_SECRET": A_TOKEN_SECRET_DEV
    })

@app.get('/feh-vg-bot/check-vg')
def check_vg_restful():
    return json.dumps(check_vg(get_unit_scores()))

@app.get('/feh-vg-bot/get-unit-scores')
def gen_unit_scores_restful():
    return json.dumps(get_unit_scores())