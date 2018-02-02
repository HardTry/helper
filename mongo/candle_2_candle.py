import os
import libnrlib

rootpath = '/data/sean/10s_candle_bindata'
insts = ['a9888',
         'ag888',
         'al888',
         'au888',
         'bu888',
         'c9888',
         'CF888',
         'cu888',
         'FG888',
         'i9888',
         'j9888',
         'jd888',
         'jm888',
         'l9888',
         'm9888',
         'MA888',
         'ni888',
         'OI888',
         'p9888',
         'pb888',
         'pp888',
         'rb888',
         'RM888',
         'ru888',
         'SR888',
         'TA888',
         'trade',
         'v9888',
         'y9888',
         'ZC888',
         'zn888',
         'b9888',
         'bb888',
         'cs888',
         'fb888',
         'fu888',
         'hc888',
         'IC888',
         'IF888',
         'IH888',
         'JR888',
         'LR888',
         'PM888',
         'RI888',
         'RS888',
         'SF888',
         'SM888',
         'sn888',
         'T9888',
         'TF888',
         'WH888',
         'wr888']

for inst in insts:
    allfile = os.listdir(rootpath + '/' + inst + '/')
    for filename in allfile:
        if filename == 'tdays.bin':
            continue
        filepath = rootpath + '/' + inst + '/' + filename
        ret = libnrlib.candle_2_candle(filepath)
        if ret != 0:
            print filepath, ret