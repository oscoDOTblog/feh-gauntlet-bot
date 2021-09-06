## python3 genny.py 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
from discord.ext.commands import command
import json
import requests
import tweepy

## Global Variables
BOT_NAME = "genny"

## Get Bot Config from REST Endpoint
def get_bot_config(BOT_NAME: str):
    global DISCORD_GUILD 
    global DISCORD_PREFIX 
    global DISCORD_STATUS 
    global DISCORD_TOKEN 
    REST_API_URL = f'http://0.0.0.0:5057/config/bot/discord/{BOT_NAME}'
    RESPONSE = json.loads(requests.get(REST_API_URL).json())
    DISCORD_GUILD = RESPONSE['guild']
    DISCORD_PREFIX = RESPONSE['prefix']
    DISCORD_STATUS = RESPONSE['status']
    DISCORD_TOKEN = RESPONSE['token']

## Discord Bot Client
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.PREFIX = DISCORD_PREFIX
        self.ready = False
        self.guild = None 
        super().__init__(command_prefix=DISCORD_PREFIX)

    #Check scores and send update to discord if required
    async def send_vg_ugdate(self):
        await self.wait_until_ready()
        # self.logger.debug(f'~~~~~starting rebecca_discord_client.send_vg_ugdate()~~~~~')
        current_unit_scores = get_unit_scores() # TODO UPDATE TO REST ENDPOINT
        if (current_unit_scores == -1):
            # logger.debug("In Beween Rounds, Do Nothing")
            print("In Beween Rounds, Do Nothing")
        else:
            # self.logger.debug("During Voting Gauntlet")
            vg_scores = check_vg(current_unit_scores) # TODO UPDATE TO REST ENDPOINT

            # Twitter authentication 
            REST_API_URL = f'http://0.0.0.0:5057/config/bot/twitter/auth'
            RESPONSE = json.loads(requests.get(REST_API_URL).json())
            auth = tweepy.OAuthHandler(RESPONSE['C_KEY'], RESPONSE['C_SECRET'])
            auth.set_access_token(RESPONSE['A_TOKEN'], RESPONSE['A_TOKEN_SECRET'])
            api = tweepy.API(auth)

            # Ping if multiplier is active for losing team (other team has 3% more flags)
            for score in vg_scores:
                message = score["Message"]
                # Send only text tweet
                if "Tie" in score["Losing"]:
                    api.update_status(message)
                    # logger.debug("Tweet Sent Successfully")
                # Send image and text
                else:
                    losing_unit = score["Losing"]
                    updated_message = "#Team" + losing_unit + message
                    response = api.media_upload(get_unit_image_url(losing_unit))
                    media_list = list()
                    media_list.append(response.media_id_string)
                    api.update_status(status=updated_message, media_ids=media_list)
                    # logger.debug("Tweet Sent Successfully")
            # except:
                # Print out timestamp in the event of failure
                # self.logger.debug(f"Ping failed for #Team{losing_unit}") 


    # Bot Commands
    async def on_message(self, message):
        # Ignore all messages from bot
        if message.author == client.user:
            return

        # Parse string from message
        msg = message.content
        member = message.author 
        message_channel = message.channel

        # Test Message
        if message.content.startswith('++hello'):
            await message.channel.send('Hello!')


    async def on_ready(self):
        await client.change_presence(activity=discord.Game(DISCORD_STATUS))
        self.guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
        self.scheduler.add_job(self.send_twitter_ugdate, CronTrigger(second="*/5"))
        # self.scheduler.add_job(self.send_twitter_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        self.scheduler.start()

## Start Discord Bot Client
get_bot_config(BOT_NAME)
client = MyClient()
client.run(DISCORD_TOKEN)
