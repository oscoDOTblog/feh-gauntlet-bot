from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import BOT_NAME, REST_API_URL
from discordclient import get_bot_token, message_from_bot, message_parse, rest_get, MyDiscordClient

class Genny(MyDiscordClient):
    def __init__(self, *args, **kwargs):
        self.scheduler = AsyncIOScheduler()
        super().__init__()

    async def on_message(self, message):
        if (not message_from_bot(client.user, message.author)):
            msg, member, message_channel = message_parse(message)

            if message.content.startswith('++hello'):
                await message.channel.send('Heya!')

            await super().on_message(client, message)

    async def on_ready(self):
        print("pizza_time_genny")
        await super().on_ready(client)
        # super().on_ready()

# It's Showtime
client = Genny()
client.run(get_bot_token(BOT_NAME))

