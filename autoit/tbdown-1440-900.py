import pyautogui as ag
import time
import filecmp
import datetime

img_100 = 'c:\\tmp\\100.png'
my_img_100 = 'c:\\tmp\\is_100.png'

st = datetime.date(2018, 5, 21)
et = datetime.date(2018, 5, 23)
period = '10s'

instruments = [
'a9888',  'bb888',  'cu888', 'i9888', 'jd888', 'm9888', 'pb888',  'RM888',  'sn888',  'ZC888',
'ag888',  'bu888',  'fb888', 'IC888', 'jm888', 'MA888', 'PM888',  'RS888',  'SR888',  'v9888',
'al888',  'c9888',  'FG888', 'IF888', 'JR888', 'ni888', 'pp888',  'ru888',  'T9888',  'WH888',
'au888',  'CF888',  'fu888', 'IH888', 'l9888', 'OI888', 'rb888',  'SF888',  'TA888',  'wr888',
'b9888',  'cs888',  'hc888', 'j9888', 'LR888', 'p9888', 'RI888',  'SM888',  'TF888',  'y9888',
'zn888'
]

def enter_string(string):
    for c in string:
        ag.press(c)
		


def open_download_dialog():
    ag.moveTo(32, 5)
    ag.click()
    
    ag.moveTo(32, 32)
    ag.click()
    
    ag.moveTo(68, 312)
    ag.click()
        
    ag.click(388, 188)
    
    #select period to 10s
    ag.click(666, 214)
    ag.click(666, 242)
    
    #click download button
    ag.click(820, 214)
    
    time.sleep(2)

#st and et are date type
def input_download_param(st, et, period):
    #enter start year
    ag.click(610, 345)
    enter_string(str(st.year))
    #enter start month
    ag.click(642, 345)
    enter_string(str(st.month))
    #enter start day
    ag.click(666, 345)
    enter_string(str(st.day))

    #enter end year
    ag.click(810, 345)
    enter_string(str(et.year))
    #enter end month
    ag.click(840, 345)
    enter_string(str(et.month))
    #enter end day
    ag.click(860, 345)
    enter_string(str(et.day))

    #SELECT period
    ag.click(683, 375)
    ag.click(872, 376)
    #1d period
    if period == '1d':
        ag.click(800, 455)
    elif period == '10s':
        ag.click(800, 418)


def download_instrument(inst):
	#enter instrument
	ag.click(606, 465)
	ag.click(808, 469)

	enter_string(inst)

	#start download
	ag.click(666, 539)

	#wait for finish
	while(True):
		ag.screenshot(my_img_100,
                     region=(882, 496, 31, 15))
		if filecmp.cmp(my_img_100, img_100):
			break
		else:
			time.sleep(1)


# instruments = ['al888', 'ag888']
# error rb888
# instruments =['CF709', 'CF801', 'CF888', 'FG709', 'FG801', 'FG888', 'MA709',
#        'MA801', 'MA888', 'OI709', 'OI801', 'OI888', 'RM709', 'RM801',
#        'RM888', 'SR801', 'SR888', 'TA709', 'TA801', 'TA888', 'ZC709',
#        'ZC801', 'ZC888', 'a1709', 'a1801', 'a9888', 'ag1712', 'ag888',
#        'al1709', 'al1710', 'al1711', 'al888', 'au1712', 'au888', 'bu1709',
#        'bu1712', 'bu888', 'c1801', 'c9888', 'cu1709', 'cu1710', 'cu1711',
#        'cu888', 'i1709', 'i1801', 'i9888', 'j1709', 'j1801', 'j9888',
#        'jd1709', 'jd1801', 'jd888', 'jm1709', 'jm1801', 'jm888', 'l1709',
#        'l1801', 'l9888', 'm1709', 'm1801', 'm9888', 'ni1709', 'ni1801',
#        'ni888', 'p1709', 'p1801', 'p9888', 'pb1708', 'pb1709', 'pb1710',
#        'pb1711', 'pb888', 'pp1709', 'pp1801', 'pp888', 'rb1710', 'rb1801',
#       'rb888', 'ru1709', ]

open_download_dialog()
input_download_param(st, et, period)
for inst in instruments:
	download_instrument(inst)