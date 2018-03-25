
def add_clear_page():
    filepath = '/app/sean/tmp/testcase.txt'
    wfile = '/app/sean/tmp/testtmp.txt'
    wfp = open(wfile, 'w+')

    with open(filepath, 'r') as fp:
        for line in fp:
            if line.startswith('\\subsection'):
                print '\\clearpage\n', line
                wfp.write('\\clearpage\n')
            wfp.write(line)


add_clear_page()
