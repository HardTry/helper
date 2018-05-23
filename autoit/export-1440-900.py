import pyautogui as ag
import time
import filecmp
import datetime

st = datetime.date(2018, 5, 21)
et = datetime.date(2018, 5, 23)
period = '10s'
st_str = ['2018', '5', '21']
et_str = ['2018', '5', '23']
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
    ag.click(32, 5)
    ag.click(32, 32)
    ag.click(68, 312)
    ag.click(388, 188)

	# period
    ag.click(663, 215)

    if period == '10s':
	    ag.click(663, 243)



def move_to_top(count):
    ag.moveTo(544, 240)
    for i in range(0, count):
        ag.click()


def select_something(y0, insts):
    # open
    ag.click(312, y0)

    y = y0 + 14
    for i in range(0, len(insts)):
        if insts[i] + '888' in instruments:
            print(insts[i] + '888')
            ag.click(332, y + i * 14)

            move_to_top(20)

            if 'cs' == insts[i]:
                ag.click(368, y + (i + 1) * 14)
            else:
                ag.click(368, y + (i + 2) * 14)

            ag.click(332, y + i * 14)

    # close
    ag.click(312, y0)



def select_instruments():
    #shanghai
    select_something(240, shfe_inst)
    #dalian
    select_something(254, dce_inst)
    #zhengzhou
    select_something(268, zce_inst)


def export():
    ag.click(777, 215)
    #start date
    ag.click(777, 332)
    enter_string(str(st.day))
    ag.click(752, 332)
    enter_string(str(st.month))
    ag.click(720, 332)
    enter_string(str(st.year))
    #end date
    ag.click(777, 416)
    enter_string(str(et.day))
    ag.click(752, 416)
    enter_string(str(et.month))
    ag.click(720, 416)
    enter_string(str(et.year))
    # save to path
    ag.click(719, 502)
    enter_string(save_path)
    # start export
    ag.click(798, 585)



open_download_dialog()
select_instruments()
export()
    