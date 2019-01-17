from SaveDataModifier import iOS

a = iOS()

#food
a.modify("L", 7, 4978)
#exp
a.modify("L", 75, 97867564)
#fruit
fb = 233189
for i in xrange(11):
    a.modify("L", fb + 4 * i, 9)
#storage
d = [349, 351] + [6] * 5 + [7] * 8 + [8] * 6 + [9] * 6 + [149] * 56 + [50] * 15
print("adding {} units...".format(len(d)))
rb = 17569 + 8 # leave two metal cat at first
for i in xrange(len(d)):
    a.modify("L", rb + 4 * i, d[i] - 1)
    a.modify("L", rb + 400 + 4 * i, 1)
#eyes
eb = 236089
for i in xrange(4):
    a.modify("L", eb + 4 * i, 142)
#items
ib = 10936
for i in xrange(6):
    a.modify("L", ib + 4 * i, 142)

a.save_to_file("NEW_DATA")
