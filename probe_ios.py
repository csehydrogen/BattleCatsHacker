import base64
import hashlib
import struct

def getData(fn):
    return open(fn, "rb").read()

fn = ["SAVE_DATA"]
n = len(fn)
d = []
for i in xrange(n):
    d.append(getData(fn[i]))
    print "len(d[%d]) = %d" % (i, len(d[i]))

def findExact(x, dtype):
    for i in xrange(len(d[0]) - 32):
        flag = True
        for j in xrange(n):
            if x[j] != struct.unpack_from(dtype, d[j], i)[0]:
                flag = False
                break
        if flag:
            print i

def findSeries(x, dtype):
    for i in xrange(len(d[0]) - 32):
        flag = True
        for j in xrange(len(x)):
            if x[j] != struct.unpack_from(dtype, d[0], i + 4 * j)[0]:
                flag = False
                break
        if flag:
            print i

def findDiff():
    for i in xrange(len(d[0]) - 32):
        flag = True
        for j in xrange(1, n):
            if ord(d[0][i]) != ord(d[j][i]):
                flag = False
                break
        if not flag:
            print i,
            for j in xrange(n):
                print "%3d" % ord(d[j][i]),
            print
def p(i, j, s, e):
    for x in xrange(s, e):
        print x,
        for y in xrange(i, j):
            print ord(d[y][x]),
        print

print "catfood"
findSeries([1086], "<L")
print "exp"
findSeries([4000], "<L")
print "fruit storage"
findSeries([12, 13, 12], "<L")
print "unit storage"
findSeries([200, 200], "<L")
print "eyes"
findSeries([8, 3, 24, 30], "<L")
print "item"
findSeries([17, 104, 43], "<L")


"""
p(7, 11)
p(75, 79)
p(8368, 8372)
p(8364, 8368)
p(104154, 104158)
signature = d0[-32:]
hashed = hashlib.md5("battlecatskr"+d0[:-32]).hexdigest()
print "Signature: ", signature
print "Signature: ", d1[-32:]
print "Computed : ", hashed
"""
