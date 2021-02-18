from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config.secrets_discord import *
from datetime import datetime
import discord
from discord.ext.commands import command
from gauntlet_template import *

PREFIX = "++"
STATUS = ["Fire Emblem: The Blazing Blade", "Tempest Crossing (https://atemosta.com/tempest-crossing/)"]

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None 
        self.logger = set_up_logger('discord')
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX)

    #Check scores and send update to discord if required
    async def send_vg_ugdate(self):
        await self.wait_until_ready()
        self.logger.debug(f'~~~~~starting rebecca_discord_client.send_vg_ugdate()~~~~~')
        current_unit_scores = get_unit_scores()
        if (current_unit_scores == -1):
            logger.debug("In Beween Rounds, Do Nothing")
        else:
            self.logger.debug("During Voting Gauntlet")
            vg_scores = check_vg(current_unit_scores)

            # Ping if multiplier is active for losing team (other team has 3% more flags)
            for score in vg_scores:
            # try:
                self.logger.debug(score)
                losing_unit = score["Losing"]
                if "Tie" in losing_unit:
                    self.logger.debug("Do nothing, Twitter Bot sends tie tweet.")
                else:
                    img_url = get_unit_image_url(losing_unit)
                    updated_message = discord_role_ids[losing_unit] + score["Message"]
                    channel_name = "team-" + losing_unit.lower()
                    channel = discord.utils.get(self.guild.channels, name=channel_name)
                    await channel.send(content=updated_message,file=discord.File(img_url))
                    self.logger.debug("Ping sent successfully for #Team" + losing_unit)
            # except:
                # Print out timestamp in the event of failure
                # self.logger.debug(f"Ping failed for #Team{losing_unit}") 

    ## Ohaiyo!!!
    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    # Bot Commands
    async def on_message(self, message):
        # Ignore all messages from bot
        if message.author == client.user:
            return

        # Parse string from message
        msg = message.content
        member = message.author 

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        ## Help Command
        if message.content.startswith((f'{PREFIX}help')):
            await message.channel.send('`Here is a list of Rebecca bot\'s commands!`')

        # Join (Attach Role) Command
        if message.content.startswith(f'{PREFIX}join'):
            params = msg.split()
            # Check if unit exits with supplied params
            if len(params) > 1:
                unit_name = params[1]
                # Check if unit exists
                if check_unit_validity(unit_name):
                    # Check if role exists, and add if approriate
                    unit_name_index = unit_name.capitalize()
                    role = discord.utils.get(member.guild.roles, name=f"Team {unit_name_index}")
                    if (role):
                        # Add role if member does not already have
                        if not (role in member.roles):
                            await discord.Member.add_roles(member, role)
                            await message.channel.send(f'`Successfully joined Team {unit_name_index}!`')
                        else:
                            await message.channel.send(f'`You are already on Team {unit_name_index}!`')
                    else:
                        await message.channel.send(f'There is no role for **{unit_name_index}**! Ping {discord_role_id_admin} to create this role!')
                else: 
                    await message.channel.send(f'`There is no role for {unit_name}! Try again with a valid unit name!`')
            # Reject command if no params supplied
            else: 
                await message.channel.send("`Add a unit name after ++join to join their team!`")



    async def on_ready(self):
        await client.change_presence(activity=discord.Game(STATUS[0]))
        self.guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
        # self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(second="*/5"))
        self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        self.scheduler.start()

client = MyClient()
client.run(DISCORD_TOKEN)
