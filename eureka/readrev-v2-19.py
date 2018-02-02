import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os

def get_one_line_result(line, result):
    s = line.split(',')
    # print s
    for i in range(1, 22, 2):
        # print i, s[i], s[i + 1]
        a = (s[i], s[i + 1])
        result.append(a)
    # print result

def make_revenue_frame(inst):
    delta = 10
    start = 10
    all_test = 18
    cols = []
    for i in range (0, 11 * all_test):
        cols.append(str(start + delta + delta * i))
    # print cols
    df = pd.DataFrame(columns=(cols), index = inst)
    # print df
    return df

def get_result(logpath, inst):
    filepath = logpath + '/' + inst + '.log'
    result = []
    with open(filepath) as fp:
        for line in fp:
            get_one_line_result(line, result)
    return result

def draw_line(inst, df, logpath, x):
    fig = plt.figure(0, figsize=(8, 4.5))
    fig.canvas.set_window_title(inst)
    fig.suptitle(inst)

    # print type(df.loc[inst])
    # print df.loc[inst]
    plt.plot(x, pd.to_numeric(df.loc[inst]))
    # imgpath = './level-images/' + inst + '.png'
    # plt.savefig(imgpath)
    # plt.close()
    plt.show()


def read_one_instrument(argv):
    if len(argv) != 3:
        print 'Usage readrev-v2-19 <logpath> <instrument code>'
        exit(0)

    logpath = argv[1].encode('ascii')
    inst = argv[2].encode('ascii')
    if (len(inst) == 1):
        inst += '9888'
    else:
        inst += '888'

    revdf = make_revenue_frame([inst])
    result = get_result(logpath, inst)

    for rev in result:
        revdf.at[inst, rev[0]] = rev[1]

    # print revdf

    draw_line(inst, revdf)


def get_all_instrment_in_path(logpath):
    insts = []
    for dirname, dirnames, filenames in os.walk(logpath):
        # print path to all subdirectories first.
        # print path to all filenames.
        # for subdirname in dirnames:
        #     print(os.path.join(dirname, subdirname))

        for filename in filenames:
            # print os.path.join(dirname, filename), filename
            insts.append(filename.split('.')[0])

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        # if '.git' in dirnames:
        #     # don't go into any .git directories.
        #     dirnames.remove('.git')
    return insts

if __name__ == '__main__':
    # read_one_instrument(sys.argv)

    if len(sys.argv) != 2:
        print 'Usage readrev-v2-19 <logpath>'
        exit(0)

    logpath = sys.argv[1].encode('ascii')
    insts = get_all_instrment_in_path(logpath)
    # print insts

    revdf = make_revenue_frame(insts)

    for inst in insts:
        result = get_result(logpath, inst)
        for rev in result:
            revdf.at[inst, rev[0]] = rev[1]

    revdf.reindex(sorted(revdf.columns), axis=1)
    cols = list(revdf.columns.values)

    x = [int(c) for c in cols]

    # print revdf
   
    for inst in insts:
        draw_line(inst, revdf, logpath, x)
