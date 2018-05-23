import pyautogui as ag
import time
import filecmp
import datetime

st = datetime.date(2018, 1, 26)
et = datetime.date(2018, 5, 22)
period = '10s'
st_str = ['2018', '1', '26']
et_str = ['2018', '5', '22']
save_path = 'c:\\tmp\\csv'

instruments = [
'a9888',  'bb888',  'cu888', 'i9888', 'jd888', 'm9888', 'pb888',  'RM888',  'sn888',  'ZC888',
'ag888',  'bu888',  'fb888', 'IC888', 'jm888', 'MA888', 'PM888',  'RS888',  'SR888',  'v9888',
'al888',  'c9888',  'FG888', 'IF888', 'JR888', 'ni888', 'pp888',  'ru888',  'T9888',  'WH888',
'au888',  'CF888',  'fu888', 'IH888', 'l9888', 'OI888', 'rb888',  'SF888',  'TA888',  'wr888',
'b9888',  'cs888',  'hc888', 'j9888', 'LR888', 'p9888', 'RI888',  'SM888',  'TF888',  'y9888',
'zn888'
]

shfe_inst = ['al', 'au', 'ag', 'cu', 'fu', 'pb', 'rb', 'ru', 'wr', 'zn', 'bu', 'hc', 'sn', 'ni']
dce_inst = ['a9', 'b9', 'c9', 'j9', 'jm', 'l9', 'm9', 'p9', 'pp', 'v9', 'y9', 'i9', 'jd', 'fb',
            'bb', 'cs']
zce_inst = ['CF', 'ER', 'FG', 'ME', 'OI', 'PM', 'RI', 'RM', 'RO', 'RS', 'SR', 'TA', 'WH', 'WS',
            'WT', 'TC', 'JR', 'MA', 'SF', 'SM', 'LR', 'ZC', 'CY', 'AP']


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

    ag.moveTo(345, 135)
    ag.click()

	# period
    ag.moveTo(629, 164)
    ag.click()

    if period == '10s':
	    ag.moveTo(600, 200)
	    ag.click()


def move_to_top(count):
    ag.moveTo(507, 190)
    for i in range(0, count):
        ag.click()


def select_something(y0, insts):
    # open
    ag.moveTo(275, y0)
    ag.click()

    y = y0 + 14
    for i in range(0, len(insts)):
        if insts[i] + '888' in instruments:
            print(insts[i] + '888')
            ag.moveTo(294, y + i * 14)
            ag.click()

            move_to_top(20)

            if 'cs' == insts[i]:
                ag.moveTo(332, y + (i + 1) * 14)
            else:
                ag.moveTo(332, y + (i + 2) * 14)
            ag.click()

            ag.moveTo(294, y + i * 14)
            ag.click()

    # close
    ag.moveTo(275, y0)
    ag.click()



def select_instruments():
    #shanghai
    select_something(190, shfe_inst)
    #dalian
    select_something(204, dce_inst)
    #zhengzhou
    select_something(218, zce_inst)


def export():
    ag.moveTo(758, 168)
    ag.click()
    #start date
    ag.moveTo(680, 280)
    ag.click()
    enter_string(st_str[0])
    ag.moveTo(716, 280)
    ag.click()
    enter_string(st_str[1])
    ag.moveTo(738, 280)
    ag.click()
    enter_string(st_str[2])
    #end date
    ag.moveTo(680, 366)
    ag.click()
    enter_string(et_str[0])
    ag.moveTo(716, 366)
    ag.click()
    enter_string(et_str[1])
    ag.moveTo(738, 366)
    ag.click()
    enter_string(et_str[2])
    # save to path
    ag.moveTo(688, 450)
    ag.click()
    enter_string(save_path)
    # start export
    ag.moveTo(758, 535)
    ag.click()



open_download_dialog()
select_instruments()
export()
