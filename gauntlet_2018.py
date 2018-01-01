""" By Oscar K. Sandoval (https://github.com/mtfalls/) """
#!/usr/bin/env python
import sys
import math
import random
import decimal
import time
from timeit import default_timer as timer
from datetime import datetime
import mechanize
from bs4 import BeautifulSoup
import tweepy
from secrets_poets import * #TODO: Change before VG to secrets

# main method (called every 30 minutes)
def check_gauntlet():
    # start timer
    start_time = timer()

    # set encoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Use mechanize to set the locale's select value to 'en-US'
    br = mechanize.Browser()
    br.open('https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/10') # TODO: Change every voting gauntlet

    # select locale form
    br.select_form(action="/voting_gauntlet/locale")
    control = br.form.find_control("locale")

    # iterate through locale select options until "en-US" appears, then set to true
    for item in control.items:
        if item.name == "en-US":
                item.selected = True

    # submit form
    br.submit()

    # Use BeautifulSoup to parse the response
    r = br.response().read()
    soup = BeautifulSoup(r, 'html.parser')
    #print(p.prettify());

    # find all p elements (which contain the current scores)
    p = soup.find_all("p")

    # TODO: change every round
    # round 1 variables
    round_start = datetime.strptime('Jan 1 2017 2:00AM', '%b %d %Y %I:%M%p')
    unit_dict = {'Robin': False, 'Lissa': False, 'Chrom': False, 'Tharja': False, 'Azura': False, 'Camilla': False, 'Takumi': False, 'Ryoma': False}
    round_name = 'Round 1'

    # round 2 variables
    #round_start = datetime.strptime('Jan 3 2017 2:00AM', '%b %d %Y %I:%M%p')
    #unit_dict = {'Faye': False, 'Tharja': False, 'Dorcas': False, 'Sigurd': False}
    #round_name = 'Round 2'

    # final round variables
    #round_start = datetime.strptime('Jan 5 2017 2:00AM', '%b %d %Y %I:%M%p')
    #unit_dict = {'Tharja': False, 'Sigurd': False}
    #round_name = 'Final Round'

    # all round variables
    vg_hashtag = '#WFvNY'
    count = len(unit_dict)

    # get units' current score by interating through all p elements
    # TODO: Change before VG
    vg_now = False
    # Live VG!
    if (vg_now):
        for (x, y) in pairwise_list(p):
            # 1) iterate through keys (unit names)
            # 2) if x contains the unit name and the dict's value is False,
            #    then y contains the unit's current round score
            # 3) save value in dictionary
            # 4) reduce value of count by 1
            x_text = x.get_text()
            y_text = y.get_text()
            # Check for Male Corrin, then Female Corrin
            for key in unit_dict:
                if (x_text == key) and (not unit_dict[key]):
                    unit_dict[key] = y_text
                    count -= 1

            # stop searching for scores if all units are accounted for (when count is 0)
            if not count:
                break
    # Testing before VG
    else:
        for key in unit_dict:
            unit_dict[key] = format (random.randint(0, 10000), ',d')

    # custom sort dictionary values into a list
    # TODO: change every VG
    keyorder = ['Robin', 'Lissa', 'Chrom' ,'Tharja', 'Azura', 'Camilla', 'Takumi', 'Ryoma']
    unit_scores = sorted(unit_dict.items(), key=lambda i:keyorder.index(i[0]))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(unit_scores)

    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # pairwise compare units in battle to detect disadvantages
    for (a, b) in pairwise_compare(unit_scores):

        # obtain name of units battling
        a_name = a[0]
        b_name = b[0]

        # obtain integer from string literal
        a_score = int(a[1].replace(',', ''))
        b_score = int(b[1].replace(',', ''))

        # calculate disadvantage multiplier based on hour of round
        # divmod is a little complex so,
        # 1) divide the total seconds from time_elapsed into hours (60*60)
        # 2) divmod return a list with the quotient as [0] and remainder as [1]
        time_now = datetime.now()
        time_elapsed =  time_now - round_start
        current_hour = divmod(time_elapsed.total_seconds(), 60*60)[0]
        multiplier = (current_hour * 0.1) + 3.1

        # variables for checking if multiplier is up for either team
        disadvantage_a = float(a_score) / float(b_score)
        disadvantage_b = float(b_score) / float(a_score)

        # Tweet if multiplier is active for losing team (other team has 3% more flags)
        try:
            if (disadvantage_a > 1.01): # Team B is losing
                tweet_multiplier(b_name, multiplier, vg_hashtag, round_name, current_hour, api)
            elif (disadvantage_b > 1.01): # Team A is losing
                tweet_multiplier(a_name, multiplier, vg_hashtag, round_name, current_hour, api)
            else:
                print("#Team%s #Team%s are tied" % (a_name, b_name))
        except:
            # Print out timestamp in the event of failure
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Tweet failed at %s for #Team%s #Team%s" % (timestamp, a_name, b_name))

    # End of Log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("End of successful check: %s" % timestamp)

    # close mechanize browser
    br.close()

    # return time elapsed
    end_time = timer()
    time_elapsed = int(math.floor(end_time - start_time))
    print(time_elapsed)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return (time_elapsed)

def unit_details(name):
    # Get unit quote
    ## Get unit quote url
    quote_url = "Assets/%s/%s_Quotes.txt" % (name)
    ## Parse text file line by line into list, then select random quote
    quotes = [line.rstrip('\n') for line in open(quote_url)]
    secure_random = random.SystemRandom()
    quote = secure_random.choice(quotes)

    # Get unit img_url
    img_url = "Assets/%s/%s_Preview.png" % (name)
    unit_details = [quote, img_url]
    print("QuoteURL: " + quote_url + "| ImageURL: " + img_url)
    return unit_details

def tweet_multiplier(name, multiplier, vg_hashtag, round_name, current_hour, api):
    # Tweet with image
    try:
        # Get unit details
        current_details = unit_details(name)
        quote = current_details[0]
        img_url = current_details[1]
        message = '#Team%s is losing with a %.1fx multiplier up!\n"%s"\n(%s %s Hour %d)' % (name, multiplier, quote, vg_hashtag, round_name, current_hour)
        print(message)
        # Attach image to tweet
        media_list = list()
        response = api.media_upload(img_url)
        media_list.append(response.media_id_string)
        api.update_status(status=message, media_ids=media_list)

    # Plaintext tweet
    except:
        message = '#Team%s is losing with a %.1fx multiplier up!\n(%s %s Hour %d)' % (name, multiplier, vg_hashtag, round_name, current_hour)
        api.update_status(message)

def pairwise_list(iterable):
    it = iter(iterable)
    a = next(it, None)
    for b in it:
        yield (a, b)
        a = b

def pairwise_compare(iterable):
    it = iter(iterable)
    for x in it:
        yield (x, next(it))

# copy-pasted from https://stackoverflow.com/a/783927
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

# It's showtime
if __name__ == "__main__":
    #Check scores every hour
    while True:
        time_elapsed = check_gauntlet()
        time.sleep(60*60 - time_elapsed)
