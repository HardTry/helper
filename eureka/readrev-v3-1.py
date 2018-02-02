import sys, os

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

start = 'Thu Feb  1 15:00:22 2018 : Info: Open,'
inss = 'a9888,'

def get_result(path):
    fp = open(path)
    line = fp.readline()
    fp.close()
    ic = line[len(start) : len(start) + 2]
    tmp = line[len(start) + len(inss) : ]
    ret = tmp.split(',')
    return (ic, ret[0], ret[1])
    
if __name__ == '__main__':
    # read_one_instrument(sys.argv)

    if len(sys.argv) != 2:
        print 'Usage readrev-v3-1 <logpath>'
        exit(0)

    logpath = sys.argv[1].encode('ascii')
    insts = get_all_instrment_in_path(logpath)

    results = []
    for inst in insts:
        filepath = logpath + '/' + inst + '.log'
        results.append(get_result(filepath))

    for ret in results:
        # print '', ret[0], '&', ret[1], '&  &', ret[2], '\\\\'
        # print ' \hline'
        print 'cm', ret[0], ret[2]
