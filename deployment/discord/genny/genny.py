from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import BOT_NAME, REST_API_URL
from discordclient import rest_get, get_bot_token, MyDiscordClient

class Genny(MyDiscordClient):
    def __init__(self, *args, **kwargs):
        # global DISCORD_GUILD 
        # global DISCORD_PREFIX 
        # global DISCORD_STATUS 
        # global DISCORD_TOKEN 
        # RESPONSE = rest_get(f'config/bot/discord/{BOT_NAME}')
        # # path = f'config/bot/discord/{BOT_NAME}'
        # # RESPONSE = json.loads(requests.get(f'{REST_API_URL}/{path}').json())
        # DISCORD_GUILD = RESPONSE['guild']
        # DISCORD_PREFIX = RESPONSE['prefix']
        # DISCORD_STATUS = RESPONSE['status']
        # DISCORD_TOKEN = RESPONSE['token']
        # self.PREFIX = DISCORD_PREFIX
        # self.ready = False
        # self.guild = None 
        self.scheduler = AsyncIOScheduler()
        super().__init__()

    async def on_message(self, message):
        # Ignore all messages from bot
        if message.author == client.user:
            return

        # Parse string from message
        msg = message.content
        member = message.author 
        message_channel = message.channel

        if message.content.startswith('++hello'):
            await message.channel.send('Heya!')

        super().on_message()

    async def on_ready(self):
        print("pizza_time_2")
        super().on_ready()

# It's Showtime
client = Genny()
client.run(get_bot_token(BOT_NAME))

