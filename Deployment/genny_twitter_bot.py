## python3 genny_twitter_bot.py
import sys
from gauntlet_template import * 
from credentials.secrets_tweepy import *
import tweepy

def send_tweet(vg_scores):
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Tweet if multiplier is active for losing team (other team has 3% more flags)
    for score in vg_scores:
        try:
            message = score["Message"]
            # Send only text tweet
            if "Tie" in score["Losing"]:
                api.update_status(message)
                print("Tweet Sent Successfully")
            # Send image and text
            else:
                losing_unit = score["Losing"]
                updated_message = "#Team" + losing_unit + message
                current_details = unit_assets(losing_unit)
                response = api.media_upload(current_details[1])
                media_list = list()
                media_list.append(response.media_id_string)
                api.update_status(status=updated_message, media_ids=media_list)
                print("Tweet Sent Successfully")
        except:
            # Print out timestamp in the event of failure
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Tweet failed at %s for %s" % (timestamp, score["Losing"]))

if __name__ == "__main__":
    #Check scores
    vg_scores = check_vg()
    if (vg_scores == -1):
        print("In Beween Rounds")
    else:
        print("During Voting Gauntlet")
        send_tweet(vg_scores)
    # Repeat Every Hour
    time.sleep(60*60)