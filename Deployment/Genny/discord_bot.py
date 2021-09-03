import discord
from discord.ext.commands import command
from secrets_poets import *

PREFIX = "++"
STATUS = ["Fire Emblem: The Blazing Blade", "Tempest Crossing (https://atemosta.com/tempest-crossing/)"]


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

client = MyClient()
client.run(DISCORD_TOKEN)
