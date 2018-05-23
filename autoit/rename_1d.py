import os

path = 'c:\\tmp\\csv'
s = '10秒'
d = '10s_20180521_20180523'

fs = os.listdir(path)
for f in fs:
	os.rename(path + '\\' + f,
              path + '\\' + f.replace(s, d))