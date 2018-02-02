import os

insts = ['CF709', 'CF801', 'CF888', 'FG709', 'FG801', 'FG888', 'MA709',
       'MA801', 'MA888', 'OI709', 'OI801', 'OI888', 'RM709', 'RM801',
       'RM888', 'SR801', 'SR888', 'TA709', 'TA801', 'TA888', 'ZC709',
       'ZC801', 'ZC888', 'a1709', 'a1801', 'a9888', 'ag1712', 'ag888',
       'al1709', 'al1710', 'al1711', 'al888', 'au1712', 'au888', 'bu1709',
       'bu1712', 'bu888', 'c1801', 'c9888', 'cu1709', 'cu1710', 'cu1711',
       'cu888', 'i1709', 'i1801', 'i9888', 'j1709', 'j1801', 'j9888',
       'jd1709', 'jd1801', 'jd888', 'jm1709', 'jm1801', 'jm888', 'l1709',
       'l1801', 'l9888', 'm1709', 'm1801', 'm9888', 'ni1709', 'ni1801',
       'ni888', 'p1709', 'p1801', 'p9888', 'pb1708', 'pb1709', 'pb1710',
       'pb1711', 'pb888', 'pp1709', 'pp1801', 'pp888', 'rb1710', 'rb1801',
       'rb888', 'ru1709', 'ru1801', 'ru888', 'v1709', 'v1801', 'v9888',
       'y1709', 'y1801', 'y9888', 'zn1709', 'zn1710', 'zn1711', 'zn888']

filepath = '/data/sean/futures_csv/1m'
postfix = '_1m_20000101_20170912.csv'
mongo_uri = '10.10.10.13:29875'
period = '1m'

for inst in insts:
    command = 'python ./tbk2mongo.py ' + filepath + ' ' + inst + postfix + ' ' + mongo_uri + ' ' + inst + ' ' + period
    print command
    # os.system(command)
