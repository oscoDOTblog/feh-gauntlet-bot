from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import (
  BOT_ENV, 
  BOT_NAME, 
  DISCORD_CHANNEL_ID_HEROES_FOR_HIRE,
  DISCORD_CHANNEL_ID_MEMBER_COMMANDS, 
  DISCORD_CHANNEL_ID_TEST_COMMANDS 
)
import discord
from discordclient import (
  MyDiscordClient,
  get_bot_token, 
  get_unit_image_url, 
  message_from_bot, 
  message_parse, 
  pairwise_compare,
  rest_get,
  truncate
)
import time

class Rebecca(MyDiscordClient):
    def __init__(self, *args, **kwargs):
        self.scheduler = AsyncIOScheduler()
        super().__init__()

    async def on_message(self, message):
        if (not message_from_bot(client.user, message.author)):
            msg, member, message_channel = message_parse(message)
            await super().on_message(client, message)

            if message.content.startswith('++hello'):
                await message.channel.send('Ha-yee!')

            DISCORD_PREFIX = self.prefix
            # Debug Bot
            if message.content.startswith(f'{DISCORD_PREFIX}debug-{BOT_NAME}'):
                em = discord.Embed(title = f"{BOT_NAME.capitalize()} Bot: Welcome and Twitter Bot",color = discord.Color.green())
                unit_scores = rest_get('feh-vg-bot/get-unit-scores')
                em.add_field(name = "Unit Scores", value = f'`{unit_scores}`')
                check_vg = rest_get('feh-vg-bot/check-vg')
                em.add_field(name = "Check VG", value = f'`{check_vg}`')
                await message.channel.send(embed = em)

            # Help Menu
            if message.content.startswith(f'{DISCORD_PREFIX}help-{BOT_NAME}'):
                em = discord.Embed(title = f"{BOT_NAME.capitalize()} Bot: Welcome and Twitter Bot",color = discord.Color.green())
                em.add_field(name = "Hello!", value = f'`{DISCORD_PREFIX}hello`')
                em.add_field(name = "Debug", value = f'`{DISCORD_PREFIX}debug-rebecca`')
                em.add_field(name = "Declare VG", value = f'`{DISCORD_PREFIX}declare-vg:`')
                em.add_field(name = "Setup VG", value = f'`{DISCORD_PREFIX}setup-vg`')
                em.add_field(name = "Teardown VG", value = f'`{DISCORD_PREFIX}teardown-vg`')
                await message.channel.send(embed = em)

            # Join (Attach Role) Command
            # Checks if role exists and adds/removes role as appropriate
            if message.content.startswith((f'{DISCORD_PREFIX}join', f'{DISCORD_PREFIX}leave')):
                # Check if command is being performed in test channel or members command channel 
                test_channel        = client.get_channel(id=DISCORD_CHANNEL_ID_TEST_COMMANDS)
                commands_channel_id = client.get_channel(id=DISCORD_CHANNEL_ID_MEMBER_COMMANDS)
                if message_channel is test_channel or message_channel is commands_channel_id:
                    params = msg.split(" ", 1) # split on first white space only
                    command = params[0].split(DISCORD_PREFIX,1)[1] ## get command name after prefix
                    # Check if unit exits with supplied params
                    if len(params) > 1:
                        unit_name = params[1]
                        # Check if unit exists
                        # if check_unit_validity(unit_name):
                        if (rest_get(f'unit/check/{unit_name}'))['is_valid']:
                            # Check if role exists, and add/remove if approriate
                            if "BlackKnight".lower() in unit_name:
                                unit_name_index = "BlackKnight"
                            else:
                                unit_name_index = unit_name.title()
                            # unit_name_index = unit_name
                            role = discord.utils.get(member.guild.roles, name=f"Team {unit_name_index}")
                            if (role):
                                ## Add role to user if they did not have role
                                if (command == "join" ):
                                    if not (role in member.roles):
                                        await discord.Member.add_roles(member, role)
                                        await message.channel.send(f'`Successfully joined Team {unit_name_index}!`')
                                    else:
                                        await message.channel.send(f'`You are already on Team {unit_name_index}!`')
                                # Remove role from user if they have role
                                elif (command == "leave" ):
                                    if (role in member.roles):
                                        await discord.Member.remove_roles(member, role)
                                        await message.channel.send(f'`Successfully left Team {unit_name_index}!`')
                                    else:                                
                                        await message.channel.send(f'`You cannot leave a team you never joined!`')
                            else:
                                discord_role_id_admin = rest_get('config/bot/discord/role/admin')['role']
                                await message.channel.send(f'There is no role for **Team {unit_name_index}**! Ping **{discord_role_id_admin}** to create this role!')
                        else: 
                            await message.channel.send(f'`There is no role for {unit_name}! Try again with a valid unit name!`')
                    # Reject command if no params supplied
                    else: 
                        await message.channel.send(f"`Add a unit name after ++{command} to {command} their team!`")
                else:
                    await message.channel.send(f"*You cannot perform `{msg}` here! Perform this command in <#{DISCORD_CHANNEL_ID_MEMBER_COMMANDS}>*")

            # Setup/Teardown Command
            if message.content.startswith((f'{DISCORD_PREFIX}setup-vg', f'{DISCORD_PREFIX}teardown-vg')):
                # TODO
                # check if user has admin credentials
                admin_role = discord.utils.get(member.guild.roles, name=rest_get('config/bot/discord/role/admin')['role'])
                if admin_role in member.roles:
                    params = msg.split(" ", 1) # split on first white space only
                    command = params[0].split(DISCORD_PREFIX,1)[1] ## get command name after prefix
                    unit_list = rest_get('units')
                    for unit in unit_list['units']:
                        unit_name = unit['name']
                        role_name = f"Team {unit_name}"
                        role = discord.utils.get(member.guild.roles, name=role_name)
                        ## If command is teardown and role exists, delete it
                        if command == "teardown-vg" and role:
                            await discord.Role.delete(role)
                            await message.channel.send(f'`{role_name} has been successfully deleted!`')
                        elif command == "teardown-vg" and not role: 
                            await message.channel.send(f'`{role_name} does not exist and thus cannot be deleted!`')
                        # If command is setup and role does not exist, create it
                        if command == "setup-vg" and not role:
                            unit_hex_colour = rest_get(f'unit/discord/colour/{unit_name}')['colour'] #discord_hex_colours[unit_name] #0xffffff
                            role = await message.guild.create_role(name=role_name,mentionable=True,hoist=True,colour=discord.Colour(unit_hex_colour))
                            await message.channel.send(f'`{role_name} has been successfully created!`')
                        elif command == "setup-vg" and role: 
                            await message.channel.send(f'`{role_name} already exists and thus cannot be created!`')
                        ## Setup channels
                        if command == "setup-vg":
                            unit_name_lowercase = unit_name.lower()
                            unit_channel_id = rest_get(f'unit/discord/channel/{unit_name}')['channel'] # discord_channel_ids[unit_name]
                            await client.get_channel(id=unit_channel_id).edit(name=f"team-{unit_name_lowercase}")
                            await message.channel.send(f'Succesfully updated channel id **{unit_channel_id}** to <#{unit_channel_id}>')

                else:
                    await message.channel.send(f'You do not have the **{discord_role_id_admin}** role needed to perform this action!')

            # Returns Current Score
            if message.content.startswith((f'{DISCORD_PREFIX}scores')):
                bot_msg = "***Current Scores:***\n"
                unit_scores =  rest_get('feh-vg-bot/get-unit-scores') #get_unit_scores()
                for (a, b) in pairwise_compare(unit_scores):

                    # obtain name of units battling
                    a_name = a[0]
                    b_name = b[0]

                    # obtain integer from string literal
                    a_score = int(a[1].replace(',', ''))
                    b_score = int(b[1].replace(',', ''))

                    ## Calculate the Percent Difference
                    ## 1.Calculate the absolute difference between the two values
                    abs_dif = abs(a_score - b_score)
                    ## 2. Calculate the average of the values
                    avg_val = (a_score + b_score)/2
                    ## 3. Divide by the average
                    div_avg = abs_dif/avg_val
                    ## 4. Convert to a percentage and truncate
                    per_dif = truncate(div_avg * 100, 2)

                    # Create + Append String
                    bot_msg += f"*{a_name}* *(**{a[1]}**)* *vs* *{b_name}* *(**{b[1]}**)* | **{per_dif}%** *difference*\n"

                await message.channel.send(bot_msg)

            # Announce Command
            if message.content.startswith((f'{DISCORD_PREFIX}declare-vg')):
                discord_role_id_admin = rest_get('config/bot/discord/role/admin')['role']
                admin_role = discord.utils.get(member.guild.roles, name=discord_role_id_admin)
                if admin_role in member.roles:
                    unit_list_rest = rest_get('units') # get_list_of_unit_names()
                    unit_list = []
                    for unit in unit_list_rest['units']:
                      unit_list.append(unit['name'])
                    await message.channel.send(f'***A new Voting Gauntlet is coming!***\
                    \n*Join your team in <#{DISCORD_CHANNEL_ID_MEMBER_COMMANDS}> by typing `{DISCORD_PREFIX}join [unit name]`!*\
                    \n*Share your friend code and lead units in <#{DISCORD_CHANNEL_ID_HEROES_FOR_HIRE}>*\
                    \n\n**Commands to Join Team (Subscribe to Alerts):**\
                    \n`{DISCORD_PREFIX}join {unit_list[0]}`\
                    \n`{DISCORD_PREFIX}join {unit_list[1]}`\
                    \n`{DISCORD_PREFIX}join {unit_list[2]}`\
                    \n`{DISCORD_PREFIX}join {unit_list[3]}`\
                    \n`{DISCORD_PREFIX}join {unit_list[4]}`\
                    \n`{DISCORD_PREFIX}join {unit_list[5]}`\
                    \n`{DISCORD_PREFIX}join {unit_list[6]}`\
                    \n`{DISCORD_PREFIX}join {unit_list[7]}`\
                    \n\n**Commands to Leave Team (Unsubscribe from Alerts):**\
                    \n`{DISCORD_PREFIX}leave {unit_list[0]}`\
                    \n`{DISCORD_PREFIX}leave {unit_list[1]}`\
                    \n`{DISCORD_PREFIX}leave {unit_list[2]}`\
                    \n`{DISCORD_PREFIX}leave {unit_list[3]}`\
                    \n`{DISCORD_PREFIX}leave {unit_list[4]}`\
                    \n`{DISCORD_PREFIX}leave {unit_list[5]}`\
                    \n`{DISCORD_PREFIX}leave {unit_list[6]}`\
                    \n`{DISCORD_PREFIX}leave {unit_list[7]}`\
                    \n\n**Other Commands:**\
                    \n`{DISCORD_PREFIX}scores` Return scores of all teams in current round \
                    ')
                else:
                    await message.channel.send(f'You do not have the **{discord_role_id_admin}** role needed to perform this action!')
           
            # Announce Command
            if message.content.startswith((f'{DISCORD_PREFIX}force-multiplier')):
                await self.wait_until_ready()
                # self.logger.debug(f'~~~~~starting rebecca_discord_client.send_vg_ugdate()~~~~~')
                current_unit_scores = rest_get('feh-vg-bot/get-unit-scores')
                if (len(current_unit_scores) <= 1):
                    # logger.debug("In Beween Rounds, Do Nothing")
                    print("In Beween Rounds, Do Nothing")
                else:
                    # self.logger.debug("During Voting Gauntlet")
                    vg_scores  = rest_get('feh-vg-bot/check-vg')

                    # Ping if multiplier is active for losing team (other team has 3% more flags)
                    for score in vg_scores:
                        message = score["Message"]
                        # Send only text tweet
                        if "Tie" in score["Losing"]:
                            # self.logger.debug("Do nothing, Twitter Bot sends tie tweet.")
                            print("Do nothing, Twitter Bot sends tie tweet.")
                        # Send image and text
                        else:
                            losing_unit = score["Losing"]
                            print(losing_unit)
                            img_url = get_unit_image_url(losing_unit)
                            role_team = discord.utils.get(client.guild.roles, name=f"Team {losing_unit}")
                            role_webhook = f'<@&{role_team.id}>'
                            updated_message =  role_webhook + score["Message"]
                            channel_name = "team-" + losing_unit.lower()
                            channel = discord.utils.get(self.guild.channels, name=channel_name)
                            await channel.send(content=updated_message,file=discord.File(img_url))
                            # self.logger.debug("Ping sent successfully for #Team" + losing_unit)
                    # except:
                        # Print out timestamp in the event of failure
                        # self.logger.debug(f"Ping failed for #Team{losing_unit}") 

    #Check scores and send update to discord if required
    async def send_discord_update(self):
        await self.wait_until_ready()
        # self.logger.debug(f'~~~~~starting rebecca_discord_client.send_vg_ugdate()~~~~~')
        current_unit_scores = rest_get('feh-vg-bot/get-unit-scores')
        if (len(current_unit_scores) <= 1):
            # logger.debug("In Beween Rounds, Do Nothing")
            print("In Beween Rounds, Do Nothing")
        else:
            # self.logger.debug("During Voting Gauntlet")
            vg_scores  = rest_get('feh-vg-bot/check-vg')

            # Ping if multiplier is active for losing team (other team has 3% more flags)
            for score in vg_scores:
                message = score["Message"]
                # Send only text tweet
                if "Tie" in score["Losing"]:
                    # self.logger.debug("Do nothing, Twitter Bot sends tie tweet.")
                    print("Do nothing, Twitter Bot sends tie tweet.")
                # Send image and text
                else:
                    losing_unit = score["Losing"]
                    print(losing_unit)
                    img_url = get_unit_image_url(losing_unit)
                    role_team = discord.utils.get(client.guild.roles, name=f"Team {losing_unit}")
                    role_webhook = f'<@&{role_team.id}>'
                    updated_message =  role_webhook + score["Message"]
                    channel_name = "team-" + losing_unit.lower()
                    channel = discord.utils.get(self.guild.channels, name=channel_name)
                    await channel.send(content=updated_message,file=discord.File(img_url))
                    # self.logger.debug("Ping sent successfully for #Team" + losing_unit)
            # except:
                # Print out timestamp in the event of failure
                # self.logger.debug(f"Ping failed for #Team{losing_unit}") 

    async def on_ready(self):
        await super().on_ready(client)
        if (BOT_ENV == 'dev'):
          self.scheduler.add_job(self.send_discord_update, CronTrigger(second="*/5")) 
        elif (BOT_ENV == 'prod'):
          self.scheduler.add_job(self.send_discord_update, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        self.scheduler.start()

# It's Showtime
time.sleep(1)
client = Rebecca()
client.run(get_bot_token(BOT_NAME))

