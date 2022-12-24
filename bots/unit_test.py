## py.test
from config.current_vg import * # current VG particpants and round dates
from gauntlet_template import *
import pytest

@pytest.fixture
def supply_unit_names():
	units = [round_1_unit_1, round_1_unit_2, round_1_unit_3, round_1_unit_4, round_1_unit_5, round_1_unit_6, round_1_unit_7, round_1_unit_8]
	return units

def test_list_of_unit_names(supply_unit_names):
	unit_list = get_list_of_unit_names()
	for unit_name in unit_list:
		assert unit_name in supply_unit_names, "assert unit exists"

def test_check_unit_validity(supply_unit_names):
	unit_list = get_list_of_unit_names()
	for unit_name in unit_list:
		assert check_unit_validity(unit_name), "assert unit can be validated from config file"
	assert check_unit_validity("Pizza Guy") is not True, "assert invalid units cannot be validated from config file"

def test_get_unit_quote_random(supply_unit_names):
	for unit_name in supply_unit_names:
		unit_quote_random = get_unit_quote_random(unit_name)
		assert (isinstance(unit_quote_random, str)), "assert random quote is a string"
		quotes_url = get_unit_quotes_url(unit_name)
		quotes = open(quotes_url, 'r+', encoding="utf-8").read().splitlines()
		for quote in quotes:
			assert(isinstance(quote, str)), "assert quote has no ascii issues"

def test_assets(supply_unit_names):
	# units = [round_1_unit_1, round_1_unit_2, round_1_unit_3, round_1_unit_4, round_1_unit_5, round_1_unit_6, round_1_unit_7, round_1_unit_8]
	for unit_name in supply_unit_names:
		quotes_url = get_unit_quotes_url(unit_name)
		quotes = open(quotes_url).read().splitlines()
		assert quotes, "assert quote exists"
		img_url = get_unit_image_url(unit_name)
		fd = open(img_url, 'r')
		assert fd, "assert image exists"
		fd.close()

def test_unit_scores(supply_unit_names):
	unit_scores = get_unit_scores()
	for unit in unit_scores:
		unit_name 	= 	unit[0]
		unit_score = 	int(unit[1].replace(',', ''))
		assert unit_name in supply_unit_names, "assert unit exists"
		assert (isinstance(unit_score, int)), "assert score in an integer"

## check_vg returns a LIST of DICTIONARYS; 
## this tests validates the list content if 
def test_check_vg_distinct_scores(supply_unit_names):
	current_unit_scores = [(round_3_unit_1, '6,599'), (round_3_unit_1, '8,726')] 
	vg_scores = check_vg(current_unit_scores)
	for score in vg_scores:
		assert (isinstance(score['Round'],     str)), "assert round_name is a string"
		assert (isinstance(int(score['Hour']), int)), "assert hours_remain is an integer"
		assert (isinstance(score['Losing'],    str)), "assert losing_unit is a string"
		assert (isinstance(score['Message'],   str)), "assert message is a string"

## check_vg returns a LIST of DICTIONARYS; 
## this tests validates the list content if 
def test_check_vg_same_scores(supply_unit_names):
	current_unit_scores = [(round_3_unit_1, '4,545'), (round_3_unit_1, '4,545')] 
	vg_scores = check_vg(current_unit_scores)
	for score in vg_scores:
		assert (isinstance(score['Round'],     str)), "assert round_name is a string"
		assert (isinstance(int(score['Hour']), int)), "assert hours_remain is an integer"
		assert (isinstance(score['Losing'],    str)), "assert losing_unit is a string"
		assert ("Tie" in score["Losing"]), 			  "assert Tie is in score['Losing']"
		assert (isinstance(score['Message'],   str)), "assert message is a string"		
