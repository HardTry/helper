from pyautogui import *
import time

# im = screenshot('my_screenshot.png')

cmdwnd_x = 1256
cmdwnd_y = 256
wait_time = 15

png_x = 75
png_y = 40

amount = 4

def get_one_time():
    # active command line window
    click(x = cmdwnd_x, y = cmdwnd_y)
    # run script 
    typewrite('python rand_with_stop.py\n')
    time.sleep(10)

    click(x = png_x, y = png_y)
    # run
    press('r')
    time.sleep(5)

    # save 1st picture
    click(x = png_x, y = png_y)
    press('a')
    time.sleep(1)
    press('r')

    # continue
    click(x = cmdwnd_x, y = cmdwnd_y)
    press('enter')
    time.sleep(1)

    # run
    click(x = png_x, y = png_y)
    time.sleep(5)

    # save 2nd picture
    click(x = png_x, y = png_y)
    press('a')
    time.sleep(1)
    press('r')

    # continue
    click(x = cmdwnd_x, y = cmdwnd_y)
    press('enter')
    time.sleep(1)

    # run
    click(x = png_x, y = png_y)
    time.sleep(5)

    # save 3rd picture
    click(x = png_x, y = png_y)
    press('a')
    time.sleep(1)

    # close figure window
    click(x = png_x, y = png_y)
    press('x')
    time.sleep(0.5)
    click(x = png_x, y = png_y)
    hotkey('alt', 'f4')

    # exit python script
    click(x = cmdwnd_x, y = cmdwnd_y)
    press('enter')
    time.sleep(0.5)


for i in range(0, amount):
    get_one_time()

print 'ok'
