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

# Rest Endpoint
def rest_get(path: str):
    RESPONSE = json.loads(requests.get(f'{REST_API_URL}/{path}').json())
    return RESPONSE

class MyDiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.config = rest_get(f'config/bot/discord/{BOT_NAME}')
        self.PREFIX = self.config['prefix']
        self.ready = False
        self.guild = None 
        super().__init__()

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

        if message.content.startswith('++test'):
            await message.channel.send(rest_get(f'config/bot/discord/{BOT_NAME}'))

    async def on_ready(self):
        print("pizza_time")
        await client.change_presence(activity=discord.Game(self.config['status']))
        self.guild = discord.utils.get(client.guilds, name=self.config['guild'])

# client = MyDiscordClient()
# client.run(get_bot_token(BOT_NAME))

