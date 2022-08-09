"""
Script to fix titles on Byonic generated MGF files to work with MSFragger convention
"""

import re
import os

FILEPATH = r"E:\_debug-tests\DMorgenstern_tims-debug\Byonic_Brain-DDA_04-Jul-22-search_MGF.mgf"


def fix_mgf(mgf_file):
    """

    :param mgf_file:
    :type mgf_file:
    :return:
    :rtype:
    """
    output = []
    with open(mgf_file, 'r') as readfile:
        for line in list(readfile):
            if line.startswith('TITLE='):
                # fix title - remove extra stuff and change the scan number to the index number + 1
                line = re.sub('ScanId;v=1;d1=', '', line)
                splits = line.split('.')
                index_splits = splits[-1].split('_')
                charge = int(''.join(re.findall('[0-9]', index_splits[0])))
                scan_index_str = ''.join(re.findall('[0-9]', index_splits[-1]))
                scan_index = int(scan_index_str) + 1
                newline = '{}.{}.{}.{}\n'.format(splits[0], scan_index, scan_index, charge)
                output.append(newline)
            else:
                output.append(line)

    outpath = os.path.splitext(mgf_file)[0] + '-fixed.mgf'
    with open(outpath, 'w') as outfile:
        for line in output:
            outfile.write(line)


if __name__ == '__main__':
    fix_mgf(FILEPATH)
