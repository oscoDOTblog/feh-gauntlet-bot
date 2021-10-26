from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import BOT_ENV, BOT_NAME, REST_API_URL
import discord
from discordclient import ( 
  MyDiscordClient,
  get_bot_token, 
  get_unit_image_url, 
  message_from_bot, 
  message_parse, 
  rest_get
)
import tweepy

class Genny(MyDiscordClient):
    def __init__(self, *args, **kwargs):
        self.scheduler = AsyncIOScheduler()
        super().__init__()

    async def on_message(self, message):
        if (not message_from_bot(client.user, message.author)):
            msg, member, message_channel = message_parse(message)
            await super().on_message(client, message)

            if message.content.startswith('++hello'):
                await message.channel.send('Heya!')

            DISCORD_PREFIX = self.prefix
            ## ----- Debug Bot ----- ##
            if message.content.startswith(f'{DISCORD_PREFIX}debug-{BOT_NAME}'):
                em = discord.Embed(title = f"{BOT_NAME.capitalize()} Bot: Welcome and Twitter Bot",color = discord.Color.dark_magenta())
                unit_scores = rest_get('feh-vg-bot/get-unit-scores')
                em.add_field(name = "Unit Scores", value = f'`{unit_scores}`')
                check_vg = rest_get('feh-vg-bot/check-vg')
                em.add_field(name = "Check VG", value = f'`{check_vg}`')
                await message.channel.send(embed = em)

            ## ----- Help Menu ----- ## 
            if message.content.startswith(f'{DISCORD_PREFIX}help-{BOT_NAME}'):
                em = discord.Embed(title = f"{BOT_NAME.capitalize()} Bot: Welcome and Twitter Bot",color = discord.Color.dark_magenta())
                em.add_field(name = "Hello!", value = f'`{DISCORD_PREFIX}hello`')
                em.add_field(name = "Debug", value = f'`{DISCORD_PREFIX}debug-genny`')
                await message.channel.send(embed = em)
                # await message.channel.send('Hello!')

    ## ----- Check scores and send update to discord if required ----- ##
    async def send_twitter_update(self):
        await self.wait_until_ready()
        # self.logger.debug(f'~~~~~starting rebecca_discord_client.send_vg_ugdate()~~~~~')
        current_unit_scores = rest_get('feh-vg-bot/get-unit-scores')
        if (len(current_unit_scores) <= 1):
            # logger.debug("In Beween Rounds, Do Nothing")
            print("In Beween Rounds, Do Nothing")
        else:
            # self.logger.debug("During Voting Gauntlet")
            vg_scores  = rest_get('feh-vg-bot/check-vg')

            ## ----- Twitter authentication ----- ##
            RESPONSE  = rest_get(f'config/bot/twitter/auth/{BOT_ENV}')
            auth = tweepy.OAuthHandler(RESPONSE['C_KEY'], RESPONSE['C_SECRET'])
            auth.set_access_token(RESPONSE['A_TOKEN'], RESPONSE['A_TOKEN_SECRET'])
            api = tweepy.API(auth)

            ## ----- Ping if multiplier is active for losing team (other team has 3% more flags) ----- ##
            for score in vg_scores:
                message = score["Message"]
                # Send only text tweet
                if "Tie" in score["Losing"]:
                    api.update_status(message)
                    # logger.debug("Tweet Sent Successfully")
                ## ----- Send image and text ----- ##
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

    async def on_ready(self):
        await super().on_ready(client)
        if (BOT_ENV == 'dev'):
          self.scheduler.add_job(self.send_twitter_update, CronTrigger(second="*/5")) 
        elif (BOT_ENV == 'prod'):
          self.scheduler.add_job(self.send_twitter_update, CronTrigger(minute="5")) # cron expression: (5 * * * *)
        self.scheduler.start()

## ----- It's Showtime ----- ##
# if (BOT_ENV == 'dev'):
# elif (BOT_ENV == 'prod'):
client = Genny()
client.run(get_bot_token(BOT_NAME))

