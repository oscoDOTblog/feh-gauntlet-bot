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
                    role_team = discord.utils.get(client.guild.roles, name=f"Team {losing_unit}")
                    role_webhook = f'<@&{role_team.id}>'
                    updated_message =  role_webhook + score["Message"]
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
        message_channel = message.channel


        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        ## Help Command
        if message.content.startswith((f'{PREFIX}help')):
            await message.channel.send('`Here is a list of Rebecca bot\'s commands!\nTODO`')

        # Join (Attach Role) Command
        # Checks if role exists and adds/removes role as appropriate
        if message.content.startswith((f'{PREFIX}vg-join', f'{PREFIX}vg-leave')):
            # Check if command is being performed in test channel or members command channel 
            test_channel        = client.get_channel(id=discord_channel_id_test_commands)
            commands_channel_id = client.get_channel(id=discord_channel_id_member_commands)
            if message_channel is test_channel or message_channel is commands_channel_id:
                params = msg.split(" ", 1) # split on first white space only
                command = params[0].split(PREFIX,1)[1] ## get command name after prefix
                # Check if unit exits with supplied params
                if len(params) > 1:
                    unit_name = params[1]
                    # Check if unit exists
                    if check_unit_validity(unit_name):
                        # Check if role exists, and add/remove if approriate
                        unit_name_index = unit_name.capitalize()
                        role = discord.utils.get(member.guild.roles, name=f"Team {unit_name_index}")
                        if (role):
                            ## Add role to user if they did not have role
                            if (command == "vg-join" ):
                                if not (role in member.roles):
                                    await discord.Member.add_roles(member, role)
                                    await message.channel.send(f'`Successfully joined Team {unit_name_index}!`')
                                else:
                                    await message.channel.send(f'`You are already on Team {unit_name_index}!`')
                            # Remove role from user if they have role
                            elif (command == "vg-leave" ):
                                if (role in member.roles):
                                    await discord.Member.remove_roles(member, role)
                                    await message.channel.send(f'`Successfully left Team {unit_name_index}!`')
                                else:                                
                                    await message.channel.send(f'`You cannot leave a team you never joined!`')
                        else:
                            await message.channel.send(f'There is no role for **Team {unit_name_index}**! Ping **{discord_role_id_admin}** to create this role!')
                    else: 
                        await message.channel.send(f'`There is no role for {unit_name}! Try again with a valid unit name!`')
                # Reject command if no params supplied
                else: 
                    await message.channel.send(f"`Add a unit name after ++{command} to {command[3:]} their team!`")
            else:
                await message.channel.send(f"*You cannot perform `{msg}` here! Perform this command in <#{discord_channel_id_member_commands}>*")

        # Setup/Teardown Command
        if message.content.startswith((f'{PREFIX}vg-setup', f'{PREFIX}vg-teardown')):
            # TODO
            # check if user has admin credentials
            admin_role = discord.utils.get(member.guild.roles, name=discord_role_id_admin)
            if admin_role in member.roles:
                params = msg.split(" ", 1) # split on first white space only
                command = params[0].split(PREFIX,1)[1] ## get command name after prefix
                unit_list = get_list_of_unit_names()
                for unit_name in unit_list:
                    role_name = f"Team {unit_name}"
                    role = discord.utils.get(member.guild.roles, name=role_name)
                    ## If command is teardown and role exists, delete it
                    if command == "vg-teardown" and role:
                        await discord.Role.delete(role)
                        await message.channel.send(f'`{role_name} has been successfully deleted!`')
                    elif command == "vg-teardown" and not role: 
                        await message.channel.send(f'`{role_name} does not exist and thus cannot be deleted!`')
                    # If command is setup and role does not exist, create it
                    if command == "vg-setup" and not role:
                        unit_hex_colour = discord_hex_colours[unit_name] #0xffffff
                        role = await message.guild.create_role(name=role_name,mentionable=True,hoist=True,colour=discord.Colour(unit_hex_colour))
                        await message.channel.send(f'`{role_name} has been successfully created!`')
                    elif command == "vg-setup" and role: 
                        await message.channel.send(f'`{role_name} already exists and thus cannot be created!`')
                    ## Setup channels
                    if command == "vg-setup":
                        unit_name_lowercase = unit_name.lower()
                        unit_channel_id = discord_channel_ids[unit_name]
                        await client.get_channel(id=unit_channel_id).edit(name=f"team-{unit_name_lowercase}")
                        await message.channel.send(f'Succesfully updated channel id **{unit_channel_id}** to <#{unit_channel_id}>')

            else:
                await message.channel.send(f'You do not have the **{discord_role_id_admin}** role needed to perform this action!')

        # Returns Current Score
        if message.content.startswith((f'{PREFIX}vg-scores')):
            bot_msg = "***Current Scores:***\n"
            unit_scores = get_unit_scores()
            for (a, b) in pairwise_compare(unit_scores):

                # obtain name of units battling
                a_name = a[0]
                b_name = b[0]

                # obtain integer from string literal
                a_score = a[1]
                b_score = b[1]

                # Create + Append String
                bot_msg += f"*{a_name}* *(**{a_score}**)* *vs* *{b_name}* *(**{b_score}**)*\n"

            await message.channel.send(bot_msg)

        # Announce Command
        if message.content.startswith((f'{PREFIX}vg-declare')):
            admin_role = discord.utils.get(member.guild.roles, name=discord_role_id_admin)
            if admin_role in member.roles:
                unit_list = get_list_of_unit_names()
                await message.channel.send(f'***A new Voting Gauntlet is coming!***\
                \n*Join your team in <#{discord_channel_id_member_commands}> by typing `{PREFIX}vg-join [unit name]`!*\
                \n\n**Commands to Join Team (Subscribe to Alerts):**\
                \n`{PREFIX}vg-join {unit_list[0]}`\
                \n`{PREFIX}vg-join {unit_list[1]}`\
                \n`{PREFIX}vg-join {unit_list[2]}`\
                \n`{PREFIX}vg-join {unit_list[3]}`\
                \n`{PREFIX}vg-join {unit_list[4]}`\
                \n`{PREFIX}vg-join {unit_list[5]}`\
                \n`{PREFIX}vg-join {unit_list[6]}`\
                \n`{PREFIX}vg-join {unit_list[7]}`\
                \n\n**Commands to Leave Team (Unsubscribe from Alerts):**\
                \n`{PREFIX}vg-leave {unit_list[0]}`\
                \n`{PREFIX}vg-leave {unit_list[1]}`\
                \n`{PREFIX}vg-leave {unit_list[2]}`\
                \n`{PREFIX}vg-leave {unit_list[3]}`\
                \n`{PREFIX}vg-leave {unit_list[4]}`\
                \n`{PREFIX}vg-leave {unit_list[5]}`\
                \n`{PREFIX}vg-leave {unit_list[6]}`\
                \n`{PREFIX}vg-leave {unit_list[7]}`\
                \n\n**Other Commands:**\
                \n`{PREFIX}vg-scores` Return scores of all teams in current round \
                ')
            else:
                await message.channel.send(f'You do not have the **{discord_role_id_admin}** role needed to perform this action!')


    async def on_ready(self):
        await client.change_presence(activity=discord.Game(STATUS[0]))
        self.guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
        # self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(second="*/5"))
        self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        self.scheduler.start()

client = MyClient()
client.run(DISCORD_TOKEN)
