## py.test
from config.current_vg import * # current VG particpants and round dates
from gauntlet_template import *
import pytest

@pytest.fixture
def supply_unit_names():
	units = [round_1_unit_1, round_1_unit_2, round_1_unit_3, round_1_unit_4, round_1_unit_5, round_1_unit_6, round_1_unit_7, round_1_unit_8]
	return units

def test_validate_assets(supply_unit_names):
	# units = [round_1_unit_1, round_1_unit_2, round_1_unit_3, round_1_unit_4, round_1_unit_5, round_1_unit_6, round_1_unit_7, round_1_unit_8]
	for unit in supply_unit_names:
		print('Testing %s' % unit)
		quote_url = "assets/%s/%s_Quotes.txt" % (unit, unit)
		quotes = open(quote_url).read().splitlines()
		assert quotes, "assert quote exists"
		img_url = "assets/%s/%s_Preview.png" % (unit, unit)
		fd = open(img_url, 'r')
		assert fd, "assert image exists"
		fd.close()

def test_validate_unit_scores(supply_unit_names):
	unit_scores = get_unit_scores()
	for (a, b) in pairwise_compare(unit_scores):
		a_name 	= 	a[0]
		a_score = 	int(a[1].replace(',', ''))
		b_name 	= 	b[0]
		b_score = 	int(b[1].replace(',', ''))
		assert a_name in supply_unit_names, "assert unit exists"
		assert (isinstance(a_score, int)), "assert score in an integer"
		assert b_name in supply_unit_names, "assert unit exists"
		assert (isinstance(b_score, int)), "assert score in an integer"
