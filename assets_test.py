from current_vg import * # current VG particpants and round dates

print("Hello world!")
units = [round_1_unit_1, round_1_unit_2, round_1_unit_3, round_1_unit_4, round_1_unit_5, round_1_unit_6, round_1_unit_7, round_1_unit_8]
for unit in units:
    print('Testing %s' % unit)
    quote_url = "Assets/%s/%s_Quotes.txt" % (unit, unit)
    quotes = open(quote_url).read().splitlines()
    img_url = "Assets/%s/%s_Preview.png" % (unit, unit)
    print('Assets of %s successfully opened' % unit)

Gunnthrа_Quotes.txt
Gunnthra_Quotes.txt
