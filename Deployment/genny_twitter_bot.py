## python3 genny_twitter_bot.py
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
# from config.secrets_poets import *
from config.secrets_tweepy import *
from gauntlet_template import * 
import sys
import tweepy

def send_twitter_update():
    # Check scores
    logger.debug(f'~~~~~starting genny_twitter_bot.send_twitter_update()~~~~~')
    current_unit_scores = get_unit_scores()
    if (current_unit_scores == -1):
        logger.debug("In Beween Rounds, Do Nothing")
    else:
        logger.debug("During Voting Gauntlet")
        vg_scores = check_vg(current_unit_scores)
        
        # Twitter authentication
        auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        api = tweepy.API(auth)

        # Tweet if multiplier is active for losing team (other team has 3% more flags)
        for score in vg_scores:
            message = score["Message"]
            # Send only text tweet
            if "Tie" in score["Losing"]:
                api.update_status(message)
                logger.debug("Tweet Sent Successfully")
            # Send image and text
            else:
                losing_unit = score["Losing"]
                updated_message = "#Team" + losing_unit + message
                response = api.media_upload(get_unit_image_url(losing_unit))
                media_list = list()
                media_list.append(response.media_id_string)
                api.update_status(status=updated_message, media_ids=media_list)
                logger.debug("Tweet Sent Successfully")

if __name__ == "__main__":
    logger = set_up_logger("genny_twitter_bot")
    # scheduler = AsyncIOScheduler()
    # scheduler = BackgroundScheduler()
    scheduler = BlockingScheduler()
    # scheduler.add_job(send_twitter_update, CronTrigger(second="*/5"))
    scheduler.add_job(send_twitter_update, CronTrigger(minute="5")) # cron expression: (5 * * * *)
    scheduler.start()
