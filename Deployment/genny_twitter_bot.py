## python3 genny_twitter_bot.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config.secrets_tweepy import *
from gauntlet_template import * 
import sys
import tweepy

def send_twitter_update(logger):
    # Check scores
    logger.debug(f'~~~~~starting {__file__}.send_twitter_update()~~~~~')
    vg_scores = check_vg(logger)
    if (vg_scores == -1):
        logger.debug("In Beween Rounds, Do Nothing")
    else:
        logger.debug("During Voting Gauntlet")
        # Twitter authentication
        auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        api = tweepy.API(auth)

        # Tweet if multiplier is active for losing team (other team has 3% more flags)
        for score in vg_scores:
            # try:
            message = score["Message"]
            # Send only text tweet
            if "Tie" in score["Losing"]:
                api.update_status(message)
                logger.debug("Tweet Sent Successfully")
            # Send image and text
            else:
                losing_unit = score["Losing"]
                updated_message = "#Team" + losing_unit + message
                current_details = unit_assets(logger, losing_unit)
                response = api.media_upload(current_details[1])
                media_list = list()
                media_list.append(response.media_id_string)
                api.update_status(status=updated_message, media_ids=media_list)
                logger.debug("Tweet Sent Successfully")
            # except:
                # Print out timestamp in the event of failure
                # logger.debug(f"Ping failed for #Team{losing_unit}") 

if __name__ == "__main__":
    logger = set_up_logger(__file__)
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(send_twitter_update(logger), CronTrigger(second="*/5"))
    scheduler.add_job(send_vg_ugdate, CronTrigger(minute="5")) # cron expression: (5 * * * *)
    scheduler.start()