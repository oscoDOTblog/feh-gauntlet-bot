""" By Oscar K. Sandoval (https://github.com/mtfalls/) """
#!/usr/bin/env python
import sys
from datetime import datetime
import mechanize
from bs4 import BeautifulSoup
import tweepy
from secrets import *

# main method (called every 30 minutes)
def check_gauntlet():
    # set encoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Use mechanize to set the locale's select value to 'en-US'
    br = mechanize.Browser()
    br.open('https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/5')

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
    round_vars = round_1()
    round_start = round_vars[0]
    unit_dict = round_vars[1]
    count = len(unit_dict)

    # get units' current score by interating through all p elements
    for (x, y) in pairwise_list(p):
        # 1) iterate through keys (unit names)
        # 2) if x contains the unit name and the dict's value is False,
        #    then y contains the unit's current round score
        # 3) save value in dictionary
        # 4) reduce value of count by 1
        for key in unit_dict:
            if (x.get_text() == key) and (not unit_dict[key]):
                unit_dict[key] = y.get_text()
                count -= 1

        # stop searching for scores if all units are accounted for (when count is 0)
        if not count:
            break

    # custom sort dictionary values into a list
    keyorder = ['Gaius', 'Frederick', 'Xander' ,'Leo', 'Robin', 'Tiki', 'Corrin', 'Elise']
    unit_scores = sorted(unit_dict.items(), key=lambda i:keyorder.index(i[0]))

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
        disadvantage_a = float(b_score) / float(a_score)
        disadvantage_b = float(a_score) / float(b_score)
        disadvantage_abs = format (abs(b_score - a_score), ',d') # absolute difference formatted with commas (cuz 'MURICA)

        # tweet if multiplier is active for losing team (other team has 10% more flags)
        if (disadvantage_a > 1.10): # team a is losing
            tweet = "TEST: #Team%s is losing by %s flags with a %.1fx multiplier up! Come show some support! #FEHeroes #VotingGauntlet #CYL " % (a_name, disadvantage_abs, multiplier)
            print(tweet)
        elif (disadvantage_b > 1.10): # team_b is losing
            tweet = "TEST: #Team%s is losing by %s flags with a %.1fx multiplier up! Come show some support! #FEHeroes #VotingGauntlet #CYL" % (b_name, disadvantage_abs, multiplier)
            print(tweet)

    # close mechanize browser
    br.close()

def round_1_vars():
    round_start = datetime.strptime('Aug 29 2017 3:00AM', '%b %d %Y %I:%M%p')
    unit_dict = {'Gaius': False, 'Frederick': False, 'Xander': False, 'Leo': False, 'Robin': False, 'Tiki': False, 'Corrin': False, 'Elise': False}
    round_vars = [round_start, unit_dict]
    return round_vars

def round_2_vars():
    round_start = datetime.strptime('Aug 29 2017 3:00AM', '%b %d %Y %I:%M%p')
    unit_dict = {'Gaius': False, 'Leo': False, 'Robin': False, 'Corrin': False, }
    round_vars = [round_start, unit_dict]
    return round_vars

def final_round_vars():
    round_start = datetime.strptime('Aug 29 2017 3:00AM', '%b %d %Y %I:%M%p')
    unit_dict = {'Gaius': False, 'Corrin': False}
    round_vars = [round_start, unit_dict]
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

# It's showtime
if __name__ == "__main__":
    #Check scores every hour
    #while True:
    check_gauntlet()
    #    time.sleep(1800)
