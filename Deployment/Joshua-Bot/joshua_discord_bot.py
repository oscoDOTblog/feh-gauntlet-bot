# Import FEH-Gauntlet Bot Libraries
import sys
sys.path.append("..") 
from gauntlet_template import * 
from current_vg import * 

# Import Discord.py Bot Libraries
import discord
from discord.ext import commands,tasks
from secrets_discord import *
import logging

# Set up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# @tasks.loop(seconds=5)
# async def my_loop():
#     print('Hello World')
# my_loop.start()

# class MyClient(discord.Client):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # create the background task and run it in the background
#         self.bg_task = self.loop.create_task(self.my_background_task())
#     async def on_ready(self):
#         print('Logged in as')
#         print(self.user.name)
#         print(self.user.id)
#         print('------')

#     async def my_background_task(self):
#         await self.wait_until_ready()
#         counter = 0
#         channel = self.get_channel(793542106928644116) # channel ID goes here
#         while not self.is_closed():
#             counter += 1
#             await channel.send(counter)
#             await asyncio.sleep(1) # task runs every 60 seconds
# client = MyClient()
# client.run(DISCORD_TOKEN)

# Set up Bot Commands
bot = commands.Bot(command_prefix='!')
@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    print("ctx: " + str(ctx))
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='thorn-in-you', help='The fateful choice')
async def thorn_in_you(ctx):
    print("ctx: " + str(ctx))
    response = "https://www.youtube.com/watch?v=cPgqpdd85_w"
    await ctx.send(response)

bot.run(DISCORD_TOKEN)

# Set Up Background Task
bot.tasks = {}
@bot.group(invoke_without_command=True)
async def foo(ctx):
  task = bot.loop.create_task(my_coro())
  bot.tasks[(ctx.channel.id, ctx.author.id)] = task
  try:
    await task
  except asyncio.CancelledError:
    return
  finally:
    self.tasks.pop((ctx.channel.id, ctx.author.id), None)
@foo.command(name="cancel")
async def foo_cancel(ctx):
  task = bot.tasks.get((ctx.channel.id, ctx.author.id))
  if task:
    task.cancel()

# @bot.command(name='create-channel')
# @commands.has_role('admin')
# async def create_channel(ctx, channel_name='real-python'):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)
