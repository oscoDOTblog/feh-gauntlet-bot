from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config.secrets_discord import *
from datetime import datetime
import discord
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
        super().__init__(command_prefix=PREFIX,*args, **kwargs)

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

    async def on_ready(self):
        await client.change_presence(activity=discord.Game(STATUS[0]))
        self.guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
        self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(second="*/5"))
        # self.scheduler.add_job(self.send_vg_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        self.scheduler.start()

client = MyClient()
client.run(DISCORD_TOKEN)
