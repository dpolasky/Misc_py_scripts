"""
check mzML files for FAIMS status.
"""
import tkinter
from tkinter import filedialog
import re
import os


def main(mzml_files):
    """

    :param mzml_files:
    :type mzml_files:
    :return:
    :rtype:
    """
    faims_pattern = re.compile("name=\"FAIMS compensation voltage\"")
    for mzml_file in mzml_files:
        is_faims = False
        name = os.path.basename(mzml_file)
        with open(mzml_file, 'r') as readfile:
            match = faims_pattern.search(readfile.read(10000))      # only read the first bit of the files for speed. Might need to increase if a file has a huge header or lots of MS1s before the first MS2
            if match:
                is_faims = True
            if is_faims:
                print('IS faims: {} '.format(name))
        if not is_faims:
            print('NOT faims: {} '.format(name))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    mzmls = filedialog.askopenfilenames(filetypes=[('mzML', '.mzml')])
    main(mzmls)
