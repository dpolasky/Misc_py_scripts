"""
Need to convert .hk (text) outputs to MGF files to be able to search.
"""

import tkinter
from tkinter import filedialog
import os


def convert_scan(scan_lines):
    """
    Convert the set of strings read in from the Hardklor file to an MGF scan. No processing performed
    on input lines before this

    MGF Format:
    BEGIN IONS
    TITLE=
    SCANS=
    RTINSECONDS=
    CHARGE=
    PEPMASS=
    [peak info]

    :param scan_lines: list of strings corresponding to a single scan header and some number of peak lines
    :type scan_lines: list
    :return: list of strings corresponding to the MGF-formatted version of this scan
    :rtype: list
    """
    output = ['BEGIN IONS\n']

    # header lines
    header_splits = scan_lines[0].rstrip('\n').split('\t')
    filename = os.path.basename(os.path.splitext(header_splits[3])[0])
    scannum = header_splits[1]
    charge = header_splits[5]
    rt_min = float(header_splits[2])
    title = '{}.{}.{}.{}'.format(filename, scannum, scannum, charge)
    output.append('TITLE={}\n'.format(title))
    output.append('SCANS={}\n'.format(scannum))
    output.append('RTINSECONDS={:.5f}\n'.format(rt_min * 60))
    output.append('CHARGE={}+\n'.format(charge))
    output.append('PEPMASS={}\n'.format(header_splits[6]))

    # peak lines
    for peak_line in scan_lines[1:]:
        # convert peak to 1+
        peak_splits = peak_line.rstrip('\n').split('\t')
        neutral_mass = float(peak_splits[1])
        one_plus_mass = neutral_mass + 1.007276
        output.append('{:.6f} {}\n'.format(one_plus_mass, peak_splits[3]))    # mz, intensity
    output.append('END IONS\n\n')
    return output


def convert_file(hk_file):
    """
    Convert the Hardklor file to MGF in same directory
    :param hk_file: full path to file to convert
    :type hk_file: str
    :return: void
    :rtype:
    """
    output_path = os.path.splitext(hk_file)[0] + '.mgf'

    output_lines = []
    with open(hk_file, 'r') as readfile:
        current_scan_lines = []
        for line in list(readfile):
            # no headers
            if line.startswith('\n'):
                continue
            if line.startswith('S'):
                # new scan - save previous scan and start saving lines for the new scan
                if len(current_scan_lines) > 1:     # skip scans with no MS2 ions detected
                    output_lines.extend(convert_scan(current_scan_lines))
                current_scan_lines = [line]
            else:
                current_scan_lines.append(line)
        if len(current_scan_lines) > 1:
            output_lines.extend(convert_scan(current_scan_lines))   # convert final scan

    with open(output_path, 'w') as outfile:
        for line in output_lines:
            outfile.write(line)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(filetypes=[('HK files', '.tsv')])
    for index, file in enumerate(files):
        print('converting file {} of {}'.format(index + 1, len(files)))
        convert_file(file)
