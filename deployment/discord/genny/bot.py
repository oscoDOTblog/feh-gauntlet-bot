## python3 genny.py 
import discord
from discord.ext.commands import command
import json
import requests

def get_bot_config(BOT_NAME: str):
    global DISCORD_GUILD 
    global DISCORD_PREFIX 
    global DISCORD_STATUS 
    global DISCORD_TOKEN 
    REST_API_URL = f'http://0.0.0.0:5057/config/bot/discord/{BOT_NAME}'
    RESPONSE = json.loads(requests.get(REST_API_URL).json())
    DISCORD_GUILD = RESPONSE['guild']
    DISCORD_PREFIX = RESPONSE['prefix']
    DISCORD_STATUS = RESPONSE['status']
    DISCORD_TOKEN = RESPONSE['token']

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.PREFIX = DISCORD_PREFIX
        self.ready = False
        self.guild = None 
        super().__init__(command_prefix=DISCORD_PREFIX)

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
        await client.change_presence(activity=discord.Game(DISCORD_STATUS))
        self.guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
        # self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(second="*/5"))
        # self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        # self.scheduler.start()

BOT_NAME = "genny"
get_bot_config(BOT_NAME)
client = MyClient()
client.run(DISCORD_TOKEN)
