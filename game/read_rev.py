from os import listdir       
from os.path import isfile, join
import sys

if len(sys.argv) != 2:
  exit(0)

mypath = '/app/sean/bin/gom/bin/v2_' + sys.argv[1].encode() + '_logs'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for fn in onlyfiles:                 
  fname = mypath + '/' + fn     
  print fname, ':',                                                
  with open(fname, 'rb') as fh:
    fh.seek(-40, 2) # os.SEEK_END)
    last = fh.readlines()[-1].decode()
    strs = last.split(',')
    print strs[0], float(strs[1])
