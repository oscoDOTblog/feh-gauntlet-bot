""" By Oscar K. Sandoval (https://github.com/mtfalls/) """
#!/usr/bin/env python
import sys
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
    unit_dict = round_2()
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
    keyorder = ['Gaius', 'Leo', 'Robin', 'Corrin']
    unit_scores = sorted(unit_dict.items(), key=lambda i:keyorder.index(i[0]))

    # tweet if unit in battle is at (severe?) disadvantage
    for (a, b) in pairwise_compare(unit_scores):
        a_name = a[0]
        b_name = b[0]

        # obtain integer from string literal
        a_score = int(a[1].replace(',', ''))
        b_score = int(b[1].replace(',', ''))

        # TODO: add disadvantage multiplier to tweet
        current_hour = "???"
        multiplier = "???"
        disadvantage = b_score - a_score
        disadvantage_abs = abs(disadvantage)

        # compare unit scores, then tweet if multiplier is active for losing team
        if (disadvantage > 0): # team a is losing
            tweet = "#Team%s is losing by %d with a %s multiplier up! Come show some support!" % (a_name, disadvantage_abs, multiplier)
            print(tweet)
        elif (disadvantage < 0): # team_b is losing
            tweet = "#Team%s is losing by %d with a %s multiplier up! Come show some support!" % (b_name, disadvantage_abs, multiplier)
            print(tweet)

    # close mechanize browser
    br.close()

def round_1():
    print("pizza")

def round_2():
    unit_dict = {'Gaius': False, 'Leo': False, 'Robin': False, 'Corrin': False, }
    return unit_dict

def final_round():
    unit_dict = {'Gaius': False, 'Corrin': False}
    return unit_dict

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
