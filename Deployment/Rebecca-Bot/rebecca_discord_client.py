# Import FEH-Gauntlet Bot Libraries
import sys
sys.path.append("..") 
from gauntlet_template import * 
from current_vg import * 

# Import Discord.py Bot Libraries
import discord
from discord.ext import commands,tasks
from secrets_discord import *
from itertools import cycle
import logging

# Set up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Set up Client
client = commands.Bot(command_prefix = "!")
status = ["Fire Emblem: The Blazing Blade", "Tempest Crossing (https://atemosta.com/tempest-crossing/)"]
@client.event
async def on_ready():
    logging.info('Bot is on_ready()')
    guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
    channel_name = "bot-test"
    await client.change_presence(activity=discord.Game(status[0]))
    send_vg_ugdate.start(guild,channel_name)

# Set Up Background Task
@tasks.loop(seconds=5)
async def send_vg_ugdate(guild, channel_name):
    logging.info('starting change_status()')
    channel = discord.utils.get(guild.channels, name=channel_name)
    await channel.send("Heya!")

client.run(DISCORD_TOKEN)
# @bot.command(name='create-channel')
# @commands.has_role('admin')
# async def create_channel(ctx, channel_name='real-python'):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)
