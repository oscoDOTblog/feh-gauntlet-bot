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
    await client.change_presence(activity=discord.Game(status[0]))
    send_vg_ugdate.start(guild,discord_channel_name)

# Set Up Background Task
@tasks.loop(seconds=60*60)
async def send_vg_ugdate(guild, channel_name):

    #Check scores
    logging.info('starting change_status()')
    channel = discord.utils.get(guild.channels, name=channel_name)
    vg_scores = check_vg()
    if (vg_scores == -1):
        print("In Beween Rounds")
    else:
        print("During Voting Gauntlet")

    # Ping if multiplier is active for losing team (other team has 3% more flags)
    for score in vg_scores:
        try:
            message = score["Message"]
            # Send only text tweet
            if "Tie" in score["Losing"]:
                await channel.send(message)
                logging.info("Ping Sent Successfully")
            # Send image and text
            else:
                losing_unit = score["Losing"]
                # updated_message = "@Team" + losing_unit + message
                losing_unit_role_id = discord_role_ids[losing_unit]
                current_details = unit_assets(losing_unit)
                img_url = current_details[1]
                updated_message =losing_unit_role_id + message
                # api.update_status(status=updated_message, media_ids=media_list)
                await channel.send(content=updated_message,file=discord.File(img_url))
                logging.info("Ping Sent Successfully")
        except:
            # Print out timestamp in the event of failure
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Ping failed at %s for %s" % (timestamp, score["Losing"]))

client.run(DISCORD_TOKEN)
# @bot.command(name='create-channel')
# @commands.has_role('admin')
# async def create_channel(ctx, channel_name='real-python'):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)

# import discord
# import asyncio
# import datetime

# time_for_thing_to_happen = datetime.time(hour=12)  # 12 o'clock in the afternoon, UTC

# async def sometask():
#     while True:
#         now = datetime.datetime.utcnow()
#         date = now.date()
#         if now.time() > time_for_thing_to_happen:
#             date = now.date() + datetime.timedelta(days=1)
#         then = datetime.datetime.combine(date, time_for_thing_to_happen)
#         await discord.utils.sleep_until(then)
#         print("it's 12 o'clock")

# #errors in tasks raise silently normally so lets make them speak up
# def exception_catching_callback(task):
#     if task.exception():
#         task.print_stack()

# task = asyncio.create_task(sometask())
# task.add_done_callback(exception_catching_callback)
