""" By Oscar K. Sandoval (https://github.com/mtfalls/) """
#!/usr/bin/env python
import sys
import math
import random
import decimal
import importlib
import time
import logging
from timeit import default_timer as timer
from datetime import datetime
import mechanize
from bs4 import BeautifulSoup
from config.current_vg import * # current VG particpants and round dates

# main method (called every 30 minutes)
def check_vg(logger):
    # start timer
    start_time = timer()

    # Use mechanize to set the locale's select value to 'en-US'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    #br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open(vg_url)

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
    #logger.debug(p.prettify());

    # find all p elements (which contain the current scores)
    p = soup.find_all("p")

    # Get Variables for Current Round
    time_now = datetime.now()
    logger.debug("time_now: " + str(time_now))
    round_1_start = datetime.strptime(round_1_start_raw, '%b %d %Y %I:%M%p')
    round_1_end = datetime.strptime(round_1_end_raw, '%b %d %Y %I:%M%p')
    round_2_start = datetime.strptime(round_2_start_raw, '%b %d %Y %I:%M%p')
    round_2_end = datetime.strptime(round_2_end_raw, '%b %d %Y %I:%M%p')
    round_3_start = datetime.strptime(round_3_start_raw, '%b %d %Y %I:%M%p')
    round_3_end = datetime.strptime(round_3_end_raw, '%b %d %Y %I:%M%p')

    # Check if test VG or real VG

    if not (vg_test):
        # round 1 variables
        if (round_1_start < time_now < round_1_end):
            logger.debug("Currently Round 1")
            round_start = round_1_start
            unit_dict = {round_1_unit_1: False, round_1_unit_2: False, round_1_unit_3: False, round_1_unit_4: False, round_1_unit_5: False, round_1_unit_6: False, round_1_unit_7: False, round_1_unit_8: False}
            round_name = 'Round 1'
        # round 2 variables
        elif (round_2_start < time_now < round_2_end):
            logger.debug("Currently Round 2")
            round_start = round_2_start
            unit_dict = {round_2_unit_1: False, round_2_unit_2: False, round_2_unit_3: False, round_2_unit_4: False}
            round_name = 'Round 2'
        # round 3 variables
        elif (round_3_start < time_now < round_3_end):
            logger.debug("Currently Round 3")
            round_start = round_3_start
            unit_dict = {round_3_unit_1: False, round_3_unit_2: False}
            round_name = 'Final Round'
        # else in between rounds
        else:
            logger.debug("Current time in between rounds. Ending execution.")
            return (-1)
    else: 
        logger.debug("~~~~~Testing VG~~~~~")
        logger.debug("Currently Round 3")
        round_start = round_3_start
        unit_dict = {round_3_unit_1: False, round_3_unit_2: False}
        round_name = 'Final Round'

    # all round variables
    count = len(unit_dict)

    # get units' current score by interating through all p elements
    for (x, y) in pairwise_list(p):
        # 1) iterate through keys (unit names)
        # 2) if x contains the unit name and the dict's value is False,
        #    then y contains the unit's current round score
        # 3) save value in dictionary
        # 4) reduce value of count by 1
        x_text = x.get_text()
        # if "L" in x_text and "f" in x_text:
        #     logger.debug("Changing text to Lif")
        #     x_text = "Lif"
        # if "Black" in x_text and "Knight" in x_text:
        #     logger.debug("Changing text to BlackKnight")
        #     x_text = "BlackKnight"
        if not (vg_test):
            logger.debug("VG is NOW!!!")
            y_text = y.get_text()
        else:
            logger.debug("VG is NOT now!!!")
            y_text = format (random.randint(0, 10000), ',d')
        # Iterate through keys to update their values
        for key in unit_dict:
            # Check for Male Robin, then Female Robin
            # if (x_text == 'Robin') and (not unit_dict['MRobin']):
            #    logger.debug("Key: " + key + "| Value:" + y_text )
            #    unit_dict['MRobin'] = y_text
            #    count -= 1
            # elif (x_text == 'Robin') and (not unit_dict['FRobin']):
            #    logger.debug("Key: " + key + "| Value:" + y_text )
            #    unit_dict['FRobin'] = y_text
            #    count -= 1
            if (x_text == key) and (not unit_dict[key]):
                logger.debug("Key: " + key + "| Value:" + y_text )
                unit_dict[key] = y_text
                count -= 1
        # stop searching for scores if all units are accounted for (when count is 0)
        if not count:
            break

    # custom sort dictionary values into a list
    keyorder = [round_1_unit_1, round_1_unit_2, round_1_unit_3, round_1_unit_4, round_1_unit_5, round_1_unit_6, round_1_unit_7, round_1_unit_8]
    unit_scores = sorted(unit_dict.items(), key=lambda i:keyorder.index(i[0]))
    logger.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    logger.info(unit_scores)

    # calculate disadvantage multiplier based on hour of round
    # divmod is a little complex so,
    # 1) divide the total seconds from time_elapsed into hours (60*60)
    # 2) divmod return'' a list with the quotient as [0] and remainder as [1]
    time_elapsed =  time_now - round_start
    current_hour = divmod(time_elapsed.total_seconds(), 60*60)[0]
    hours_remain = 45 - current_hour
    logger.info("hours_remain: " + str(hours_remain))
    multiplier = (current_hour * 0.2) + 3.2

    # pairwise compare units in battle to detect disadvantages
    vg_scores = []
    for (a, b) in pairwise_compare(unit_scores):

        # obtain name of units battling
        a_name = a[0]
        b_name = b[0]

        # obtain integer from string literal
        a_score = int(a[1].replace(',', ''))
        b_score = int(b[1].replace(',', ''))

        # variables for checking if multiplier is up for either team
        disadvantage_a = float(truncate(float(a_score) / float(b_score),4))
        disadvantage_b = float(truncate(float(b_score) / float(a_score),4))
        logger.debug(disadvantage_a)
        logger.debug(disadvantage_b)
        logger.info(f"disadvantage_a: {disadvantage_a} | disadvantage_b: {disadvantage_b}")
        
        # Create Dictionary Per Pairwise Comparison, then add to list
        losing_unit = ''
        if (disadvantage_a > 1.01): # Team B is losing
            losing_unit = b_name
            message = tweet_multiplier(logger, b_name, multiplier, hours_remain, vg_hashtag, round_name)
        elif (disadvantage_b > 1.01): # Team A is losing
            losing_unit = a_name
            message = tweet_multiplier(logger, a_name, multiplier, hours_remain, vg_hashtag, round_name)
        else:
            losing_unit = "Tie-"+a_name+"-"+b_name
            hour_or_hours = one_hour_string(hours_remain)
            message = "No multiplier for #Team%s vs. #Team%s (%s in %s\'s %s)" % (a_name, b_name, hour_or_hours, vg_hashtag, round_name)

        dic = {}
        dic['Round'] = round_name
        dic['Hour'] = hours_remain
        dic['Losing'] = losing_unit
        dic['Message'] = message
        vg_scores.append(dic)

    # End of Log
    logger.debug("End of successful check")

    # close mechanize browser
    br.close()

    # return time elapsed
    end_time = timer()
    time_elapsed = int(math.floor(end_time - start_time))
    logger.debug(time_elapsed)
    return (vg_scores)

def one_hour_string(hours_remain):
    if (hours_remain > 1):
        return "**%d+** hours remain" % hours_remain
    elif (hours_remain <= 1):
        return "Less than **one** hour remains"

def unit_assets(logger, name):
    logger.debug("Starting unit_assets()")
    # Get unit quote
    ## Get unit quote url
    quote_url = "../Assets/%s/%s_Quotes.txt" % (name, name)
    ## Parse text file line by line into list, then select random quote
    quotes = open(quote_url).read().splitlines()
    secure_random = random.SystemRandom()
    quote = secure_random.choice(quotes)

    # Get unit img_url
    img_url = "../Assets/%s/%s_Preview.png" % (name, name)
    unit_assets = [quote, img_url]
    logger.info("QuoteURL: " + quote_url + "| ImageURL: " + img_url + " | pizza")
    return unit_assets

def tweet_multiplier(logger, name, multiplier, hours_remain, vg_hashtag, round_name):
    # Tweet with image
    #try:
    # Get unit details
    logger.debug("Starting tweet_multiplier()")
    current_details = unit_assets(logger, name)
    quote = current_details[0]
    # img_url = current_details[1]
    hour_or_hours = one_hour_string(hours_remain)
    message = ' is losing with a **%.1fx** multiplier up!\n"%s"\n(%s in %s\'s %s)' % (multiplier, quote, hour_or_hours, vg_hashtag, round_name)
    logger.info(message)
    return message

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

# Set up logger
def set_up_logger(module_name):
    # Gets or creates a logger
    logger = logging.getLogger(module_name)  

    # set log level
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

    # define file handler and set formatter
    file_name = 'logs/' + module_name + '.log'
    file_handler = logging.FileHandler(filename=file_name, encoding='utf-8', mode='w')
    formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)

    return logger
