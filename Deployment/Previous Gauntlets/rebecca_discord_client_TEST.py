from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from credentials.secrets_discord import *
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

# source: https://www.youtube.com/watch?v=Le_RNN4po30
PREFIX = "++"
class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()
        # self.logger = set_up_logger(__file__)

		super().__init__(command_prefix=PREFIX, owner_ids=DISCORD_OWNER_IDS)

	def run(self):
		# self.VERSION = version
		self.TOKEN = DISCORD_TOKEN

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	async def rules_reminder(self):
		channel = self.get_channel(783177224139702274)
		await channel.send("Remember to adhere to the rules!")

	async def on_connect(self):
		print("bot connected")

	async def on_disconnect(self):
		print("bot disconnected")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong.")

		channel = self.get_channel(783177224139702274)
		await channel.send("An error occured.")
		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass

		else:
			raise exc.original

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(DISCORD_OWNER_IDS[0])
			self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=0, minute=0, second=0))
			self.scheduler.start()
			channel = self.get_channel(783177224139702274)
			await channel.send("Now online!")
			print("bot ready")
		else:
			print("bot reconnected")

	async def on_message(self, message):
		pass

bot = Bot()
Bot.run(DISCORD_TOKEN)