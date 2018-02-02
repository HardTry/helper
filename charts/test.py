import sys

import gc

from draw.canvas import Canvas
from v2_19.draw_price import draw_price

if __name__ == '__main__':
    gc.disable()
    gc.enable()

    if len(sys.argv) < 3:
        print 'Usage: python dl6.py <instrument> [<level>...]\n'
        exit(0)

    instrument = sys.argv[1].encode('ascii')
    levels = list(set(sys.argv[2::]))
    levels.sort()
    end_date = '20180126'
    # end_date = sys.argv[2].encode('ascii')
    # split = int(sys.argv[3])  # worker
    # tindex = int(sys.argv[4])
    # level = 0
    start = 2099199
    colors = [
        '#FF0000',
        '#B23AEE',
        '#A0522D',
        '#8B8B00',
        '#5B5B5B',
        '#000000',
        '#006400',
        '#EEEE00',
        '#FF1493',
        '#458B00'
    ]

    canvas = Canvas(1, 1, 1)
    ax = canvas.ax[0]
    draw_price(ax, instrument, end_date, levels, start, colors)
    # canvas.save_image(instrument, 'price')
    canvas.show_image()
    print 'Done.'