"""
Script to quickly edit param file titles
"""

import tkinter
from tkinter import filedialog
import os
import shutil

new_date = '2019_10_24'
append = ''

if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames()
    for file in files:
        filename = os.path.basename(file)
        splits = filename.split('_')
        if append is not '':
            splits.insert(len(splits) - 1, append)
        new_filename = '{}_{}'.format(new_date, '_'.join(splits[3:]))
        # new_filename = '{}_{}'.format(new_date, '_'.join(splits))

        shutil.copy(file, os.path.join(os.path.dirname(file), new_filename))
