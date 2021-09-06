## python3 genny.py 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
from discord.ext.commands import command
import json
import requests
import tweepy

## Global Variables
BOT_NAME = "genny"
REST_API_URL = "http://0.0.0.0:5057"

# Set Up Requests Method
def fetch_info_rest(path: str):
    return json.loads(requests.get(f'{REST_API_URL}/{path}').json())

## Get Bot Config from REST Endpoint
def get_bot_config(BOT_NAME: str):
    global DISCORD_GUILD 
    global DISCORD_PREFIX 
    global DISCORD_STATUS 
    global DISCORD_TOKEN 
    RESPONSE = fetch_info_rest(f'config/bot/discord/{BOT_NAME}')
    DISCORD_GUILD = RESPONSE['guild']
    DISCORD_PREFIX = RESPONSE['prefix']
    DISCORD_STATUS = RESPONSE['status']
    DISCORD_TOKEN = RESPONSE['token']

##  Get Image URL 
## TODO: Update to REST Endpoint)
def get_unit_image_url(unit_name):
    return f"../../assets/{unit_name}/{unit_name}_Preview.png"

## Discord Bot Client
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.PREFIX = DISCORD_PREFIX
        self.ready = False
        self.guild = None 
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=DISCORD_PREFIX)

    #Check scores and send update to discord if required
    async def send_twitter_ugdate(self):
        await self.wait_until_ready()
        # self.logger.debug(f'~~~~~starting rebecca_discord_client.send_vg_ugdate()~~~~~')
        # current_unit_scores = get_unit_scores() # TODO UPDATE TO REST ENDPOINT
        current_unit_scores = fetch_info_rest('feh-vg-bot/get-unit-scores')
        if (len(current_unit_scores) <= 1):
            # logger.debug("In Beween Rounds, Do Nothing")
            print("In Beween Rounds, Do Nothing")
        else:
            # self.logger.debug("During Voting Gauntlet")
            # vg_scores = check_vg(current_unit_scores) # TODO UPDATE TO REST ENDPOINT
            vg_scores  = fetch_info_rest('feh-vg-bot/check-vg')

            # Twitter authentication 
            RESPONSE  = fetch_info_rest('config/bot/twitter/auth')
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
        if message.content.startswith(f'{DISCORD_PREFIX}hello'):
            await message.channel.send('Hello!')

        # Debug Bot
        if message.content.startswith(f'{DISCORD_PREFIX}debug-{BOT_NAME}'):
            em = discord.Embed(title = f"{BOT_NAME.capitalize()} Bot: Welcome and Twitter Bot",color = discord.Color.dark_magenta())
            unit_scores = fetch_info_rest('feh-vg-bot/get-unit-scores')
            em.add_field(name = "Unit Scores", value = f'`{unit_scores}`')
            check_vg = fetch_info_rest('feh-vg-bot/check-vg')
            em.add_field(name = "Check VG", value = f'`{check_vg}`')
            await message.channel.send(embed = em)

        # Help Menu
        if message.content.startswith(f'{DISCORD_PREFIX}help-{BOT_NAME}'):
            em = discord.Embed(title = f"{BOT_NAME.capitalize()} Bot: Welcome and Twitter Bot",color = discord.Color.dark_magenta())
            em.add_field(name = "Hello!", value = f'`{DISCORD_PREFIX}hello`')
            em.add_field(name = "Debug", value = f'`{DISCORD_PREFIX}debug`')
            await message.channel.send(embed = em)
            # await message.channel.send('Hello!')


    async def on_ready(self):
        await client.change_presence(activity=discord.Game(DISCORD_STATUS))
        self.guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
        # self.scheduler.add_job(self.send_twitter_ugdate, CronTrigger(second="*/5"))
        # self.scheduler.add_job(self.send_twitter_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        # self.scheduler.start()

## Start Discord Bot Client
get_bot_config(BOT_NAME)
client = MyClient()
client.run(DISCORD_TOKEN)
