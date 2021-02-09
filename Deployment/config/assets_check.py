from current_vg import * # current VG particpants and round dates

print("Hello world!")
units = [round_1_unit_1, round_1_unit_2, round_1_unit_3, round_1_unit_4, round_1_unit_5, round_1_unit_6, round_1_unit_7, round_1_unit_8]
for unit in units:
    print('Testing %s' % unit)
    quote_url = "../assets/%s/%s_Quotes.txt" % (unit, unit)
    quotes = open(quote_url).read().splitlines()
    print("~~~")
    print(quotes[0])
    print(quotes[1])
    print(quotes[2])
    print(quotes[3])
    print("~~~")
    img_url = "../assets/%s/%s_Preview.png" % (unit, unit)
    fd = open(img_url, 'r')
    # pngdata = fd.read()
    fd.close()
    print('Assets of %s successfully opened' % unit)
