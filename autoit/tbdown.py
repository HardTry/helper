import pyautogui as ag
import time
import filecmp
import datetime

img_100 = 'c:\\tmp\\100.png'
my_img_100 = 'c:\\tmp\\is_100.png'

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
    
    ag.moveTo(345,135)
    ag.click()
    
    #select period to 1d
    ag.moveTo(632, 169)
    ag.click()
    ag.moveTo(632, 255)
    ag.click()
    
    #click download button
    ag.moveTo(794, 162)
    ag.click()
    
    time.sleep(2)

#st and et are date type
def input_download_param(st, et, period):
	#enter start year
	ag.moveTo(575, 295)
	ag.click()
	enter_string(str(st.year))
	#enter start month
	ag.moveTo(605, 295)
	ag.click()
	enter_string(str(st.month))
	#enter start day
	ag.moveTo(629, 295)
	ag.click()
	enter_string(str(st.day))

	#enter end year
	ag.moveTo(770, 295)
	ag.click()
	enter_string(str(et.year))
	#enter end month
	ag.moveTo(803, 295)
	ag.click()
	enter_string(str(et.month))
	#enter end day
	ag.moveTo(825, 295)
	ag.click()
	enter_string(str(et.day))

	#SELECT period
	ag.moveTo(647, 325)
	ag.click()
	ag.moveTo(751, 328)
	ag.click()
	#1d period
	if period == '1d':
		ag.moveTo(776, 406)
		ag.click()


def download_instrument(inst):
	#enter instrument
	ag.moveTo(570, 416)
	ag.click()
	ag.moveTo(765, 416)
	ag.click()

	enter_string(inst)

	#start download
	ag.moveTo(618, 490)
	ag.click()

	#wait for finish
	while(True):
		ag.screenshot(img_100, region=(842,444, 35, 20))
		if filecmp.cmp(my_img_100, img_100):
			break
		else:
			time.sleep(1)

st = datetime.date(2000, 1, 1)
et = datetime.date(2017, 9, 7)
period = '1d'
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
instruments = ['ru1801', 'ru888', 'v1709', 'v1801', 'v9888',
       'y1709', 'y1801', 'y9888', 'zn1709', 'zn1710', 'zn1711', 'zn888']

open_download_dialog()
input_download_param(st, et, period)
for inst in instruments:
	download_instrument(inst)
