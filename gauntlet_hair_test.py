""" By Oscar K. Sandoval (https://github.com/mtfalls/) """
#!/usr/bin/env python
import sys
import time
from datetime import datetime
import decimal
import mechanize
from bs4 import BeautifulSoup
import tweepy
from secrets_test import *
import random

# main method (called every 30 minutes)
def check_gauntlet():
    # set encoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Use mechanize to set the locale's select value to 'en-US'
    br = mechanize.Browser()
    br.open('https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/8') # TODO: Change every voting gauntlet

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

    # TODO: check the date for the current round of the voting gauntlet
    round_vars = round_1_vars() # TODO: change every round
    round_start = round_vars[0]
    unit_dict = round_vars[1]
    round_name = round_vars[2]
    vg_hashtag = round_vars[3]
    count = len(unit_dict)

    # get units' current score by interating through all p elements
    for (x, y) in pairwise_list(p):
        # 1) iterate through keys (unit names)
        # 2) if x contains the unit name and the dict's value is False,
        #    then y contains the unit's current round score
        # 3) save value in dictionary
        # 4) reduce value of count by 1
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        x_text = x.get_text()
        y_text = format (random.randint(0, 10000), ',d')
        # Check for Male Corrin, then Female Corrin
        for key in unit_dict:
            if (x_text == key) and (not unit_dict[key]):
                unit_dict[key] = y_text
                count -= 1

        # stop searching for scores if all units are accounted for (when count is 0)
        if not count:
            break

    # custom sort dictionary values into a list
    keyorder = ['Amelia', 'Katarina', 'Shanna' ,'Hinoka', 'Takumi', 'Karel', 'Soren', 'Ryoma']
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
            print("Check complete! #Team%s #Team%s" % (a_name, b_name))
        except:
            # TODO: Implement logging on the event of failture
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Tweet failed at %s for #Team%s #Team%s" % (timestamp, a_name, b_name))

    # End of Log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("End of successful check: %s" % timestamp)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # close mechanize browser
    br.close()

def unit_details(name):
    # Get unit quote
    img_urls = {"Amelia" : "Assets/Amelia/amelia_quotes.txt",
                "Katarina" : "Assets/Katarina/katarina_quotes.txt",
                "Shanna" : "Assets/Shanna/shanna_quotes.txt",
                "Hinoka" : "Assets/Hinoka/hinoka_quotes.txt",
                "Takumi" : "Assets/Takumi/takumi_quotes.txt",
                "Karel" : "Assets/Karel/karel_quotes.txt",
                "Soren" : "Assets/Soren/soren_quotes.txt",
                "Ryoma" : "Assets/Ryoma/ryoma_quotes.txt"
                }
    # Get unit img_url
    img_urls = {"Amelia" : "Assets/Amelia/amelia_feh.png",
                "Katarina" : "Assets/Katarina/katarina_feh.png",
                "Shanna" : "Assets/Shanna/shanna_feh.png",
                "Hinoka" : "Assets/Hinoka/hinoka_feh.png",
                "Takumi" : "Assets/Takumi/takumi_feh.png",
                "Karel" : "Assets/Karel/karel_feh.png",
                "Soren" : "Assets/Soren/soren_feh.png",
                "Ryoma" : "Assets/Ryoma/ryoma_feh.png"
                }
    img_url = img_urls[name]
    unit_details = [quote, img_url]
    return unit_details

def tweet_multiplier(name, multiplier, vg_hashtag, round_name, current_hour, api):
    #try:

    #except:
    #    tweet = '#Team%s is losing with a %.1fx multiplier up!\n(%s %s Hour %d)' % (name, multiplier, vg_hashtag, round_name, current_hour)
    #    #print(tweet)
    #    api.update_status(tweet)

def round_1_vars():
    round_start = datetime.strptime('Nov 1 2017 3:00AM', '%b %d %Y %I:%M%p')
    unit_dict = {'Amelia': False, 'Katarina': False, 'Shanna': False, 'Hinoka': False, 'Takumi': False, 'Karel': False, 'Soren': False, 'Ryoma': False}
    round_name = 'Round 1'
    vg_hashtag = '#SHLvLHG'
    round_vars = [round_start, unit_dict, round_name, vg_hashtag]
    return round_vars

def round_2_vars():
    round_start = datetime.strptime('Nov 2 2017 3:00AM', '%b %d %Y %I:%M%p')
    unit_dict = {'Amelia': False, 'Amelia': False, 'Amelia': False, 'Amelia': False}
    round_name = 'Round 2'
    vg_hashtag = '#SHLvLHG'
    round_vars = [round_start, unit_dict, round_name, vg_hashtag]
    return round_vars

def final_round_vars():
    round_start = datetime.strptime('Nov 3 2017 3:00AM', '%b %d %Y %I:%M%p')
    unit_dict = {'Amelia': False, 'Amelia': False}
    round_name = 'Final Round'
    vg_hashtag = '#SHLvsLHG'
    round_vars = [round_start, unit_dict, round_name, vg_hashtag]
    return round_vars

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
        check_gauntlet()
        time.sleep(60*60)
