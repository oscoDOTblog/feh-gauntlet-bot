from config import BOT_NAME, REST_API_URL
import discord
from discord.ext.commands import command
import json
import requests

# Get Bot Secret
def get_bot_token(BOT_NAME: str):
    RESPONSE = rest_get(f'config/bot/discord/{BOT_NAME}')
    DISCORD_TOKEN = RESPONSE['token']
    return DISCORD_TOKEN

##  Get Image URL 
def get_unit_image_url(unit_name):
    return f"../../assets/{unit_name}/{unit_name}_Preview.png" # LOCAL PATH
    # return f"assets/{unit_name}/{unit_name}_Preview.png" # CONTAINER PATH

# Skip Message if Author is Discord Client (Bot)
def message_from_bot(client_user, message_user):
    # Ignore all messages from bot
    # return (message.author == client.user)
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

# client = MyDiscordClient()
# client.run(get_bot_token(BOT_NAME))

