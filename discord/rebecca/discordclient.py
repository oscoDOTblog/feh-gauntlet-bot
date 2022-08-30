from config import BOT_ENV, BOT_NAME
import discord
from discord.ext.commands import command
import json
import requests
import math

# Get Bot Secret
def get_bot_token(BOT_NAME: str):
    RESPONSE = rest_get(f'config/bot/discord/{BOT_NAME}')
    DISCORD_TOKEN = RESPONSE['token']
    return DISCORD_TOKEN

##  Get Image URL 
def get_unit_image_url(unit_name):
  if (BOT_ENV == 'local'):
    return f"../../assets/{unit_name}/{unit_name}_Preview.png" # LOCAL PATH
  elif (BOT_ENV == 'dev') or (BOT_ENV == 'prod') :
    return f"assets/{unit_name}/{unit_name}_Preview.png" # CONTAINER PATH

# Skip Message if Author is Discord Client (Bot)
def message_from_bot(client_user, message_user):
    return (client_user == message_user)

# Parse Legitimate Message
def message_parse(message):
    # Parse string from message
    msg = message.content
    member = message.author 
    message_channel = message.channel

    return msg, member, message_channel

# Rest Endpoint
def rest_get(path: str):
    print("rest_get path: " + path)
    if (BOT_ENV == 'local'):
      REST_API_URL = "http://0.0.0.0:5057" # LOCAL URL
    elif (BOT_ENV == 'dev') or (BOT_ENV == 'prod') :
      REST_API_URL = "http://convoy:5057" # CONTAINER NETWORK URL
    RESPONSE = json.loads(requests.get(f'{REST_API_URL}/{path}').json())
    return RESPONSE

class MyDiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.config = rest_get(f'config/bot/discord/{BOT_NAME}')
        self.prefix = self.config['prefix']
        self.ready = False
        self.guild = None 
        super().__init__()

    # Bot Commands
    async def on_message(self, client, message):
        if (not message_from_bot(client.user, message.author)):
            msg, member, message_channel = message_parse(message)

            if message.content.startswith('++hello'):
                await message.channel.send('Hello!')

            if message.content.startswith('++test'):
                await message.channel.send(rest_get(f'config/bot/discord/{BOT_NAME}'))

    async def on_ready(self, client):
        await client.change_presence(activity=discord.Game(self.config['status']))
        self.guild = discord.utils.get(client.guilds, name=self.config['guild'])

## Pairwise Compare
def pairwise_compare(iterable):
    it = iter(iterable)
    for x in it:
        yield (x, next(it))

## Truncate Value
def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


