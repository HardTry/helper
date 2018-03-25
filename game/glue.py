import os

savepath = '/app/sean/tmp/tpimages'


part_1 = './analysis-p1.txt'


p2 = '\\end{longtabu}\n\n\\clearpage\n\\section{Detail - part 5}\n'
p3 = '\n\n\\end{CJK*}\n\\end{document}\n'


analysis_file = savepath + '/' + 'analysis.txt'
table_file = savepath + '/' + 'table.txt'
detail_file = savepath + '/' + 'detail.txt'

def write_file(filepath, remove_first_line = False):
    fp_write = open(analysis_file, 'a+')

    i = 0
    with open(filepath, 'r') as fp_read:
        for line in fp_read:
            if remove_first_line and i < 2:
                i += 1
                continue
            fp_write.write(line)

    fp_write.close()


def write_string(content):
    fp_write = open(analysis_file, 'a+')
    fp_write.write(content)
    fp_write.close()


write_file(part_1)
write_file(table_file)
write_string(p2)
write_file(detail_file, True)
write_string(p3)


os.remove(table_file)
os.remove(detail_file)
