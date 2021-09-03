import asyncio, os
import discord
import json
from config import * # current VG particpants and round dates
from discord.ext.commands import command
from easyjobs.manager import EasyJobsManager
from fastapi import FastAPI
from secrets_poets import *

PREFIX = "++"
STATUS = ["Fire Emblem: The Blazing Blade", "Tempest Crossing (https://atemosta.com/tempest-crossing/)"]
server = FastAPI()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None 
        super().__init__(command_prefix=PREFIX)

    # Bot Commands
    async def on_message(self, message):
        # Ignore all messages from bot
        if message.author == client.user:
            return

        # Parse string from message
        msg = message.content
        member = message.author 
        message_channel = message.channel


        if message.content.startswith('++hello'):
            await message.channel.send('Hello!')


    async def on_ready(self):
        await client.change_presence(activity=discord.Game(STATUS[0]))
        self.guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
        # self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(second="*/5"))
        # self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        # self.scheduler.start()

def send_twitter_update():
    print("Pizza Time")


@server.on_event('startup')
async def startup():
    server.job_manager = await EasyJobsManager.create(
        server,
        server_secret='abcd1234'
    )

    # Discord Bot
    client = MyClient()
    client.run(DISCORD_TOKEN)

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

# Discord Bot
# client = MyClient()
# client.run(DISCORD_TOKEN)