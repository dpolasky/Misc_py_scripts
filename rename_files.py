"""
Script to quickly edit param file titles
"""

import tkinter
from tkinter import filedialog
import os
import shutil

# new_date = '2019_10_25'
# append = ''


def rename_add_activation(file_list, activation, skip=None):
    """
    Add activation string to end of files
    :param file_list:
    :param skip
    :param activation:
    :return:
    """
    for file in file_list:
        filename = os.path.splitext(os.path.basename(file))[0]
        extension = os.path.splitext(file)[1]
        splits = filename.split('_')
        if skip is not None:
            if skip in splits:
                continue
        if activation is not '':
            splits.insert(len(splits), activation)
        new_filename = os.path.join(os.path.dirname(file), '_'.join(splits)) + extension
        os.rename(file, new_filename)


def copy_rename_date(file_list, new_date, filename_append):
    """
    Rename date based on naming convention of y_m_d_filename. Creates a copy of the files
    :param file_list: list of paths
    :param new_date: new date string
    :param filename_append: str
    :return: void
    """
    for file in file_list:
        filename = os.path.basename(file)
        splits = filename.split('_')
        if filename_append is not '':
            splits.insert(len(splits) - 1, filename_append)
        new_filename = '{}_{}'.format(new_date, '_'.join(splits[3:]))
        # new_filename = '{}_{}'.format(new_date, '_'.join(splits))

        shutil.copy(file, os.path.join(os.path.dirname(file), new_filename))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames()
    # copy_rename_date(files, new_date='2019_09_25', filename_append='')
    # mydir = filedialog.askdirectory()
    # files = [x for x in os.listdir(mydir)]

    # rename_add_activation(files, 'HCD', skip='AIETD')
    rename_add_activation(files, 'AIETD', skip='HCD')
