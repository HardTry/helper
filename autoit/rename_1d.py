import os

path = 'c:\\tmp\\tbdatas\\1d'
s = '\xc8\xd5\xcf\xdf'
d = '1d_20000101_20170907'

fs = os.listdir(path)
for f in fs:
	os.rename(f, f.replace(s, d))
