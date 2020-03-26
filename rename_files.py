"""
Script to quickly edit param file titles
"""

import tkinter
from tkinter import filedialog
import os
import shutil

NEW_DATE = '2020_03_23_TimsToF'
# append = ''


def copy_rename_original_folder(file_list, output_folder):
    """
    Copy a set of files to a single directory, renaming each with the name of its original containing folder.
    Intended for (e.g.) a group of psm.tsv (or etc) files that want to end up in the same place for combined analysis
    :param file_list: list of files
    :param output_folder: where to save all outputs
    :return: void
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index, file in enumerate(file_list):
        orig_folder = os.path.basename(os.path.dirname(file))
        new_name = '{}_{}'.format(orig_folder, os.path.basename(file))
        new_path = os.path.join(output_folder, new_name)
        print('copying file {} of {}...'.format(index + 1, len(file_list)))
        shutil.copy(file, new_path)


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

    # new_dir = filedialog.askdirectory()
    # copy_rename_original_folder(files, new_dir)

    # copy_rename_date(files, new_date='', filename_append='')
    copy_rename_date(files, new_date=NEW_DATE, filename_append='')

    # mydir = filedialog.askdirectory()
    # files = [x for x in os.listdir(mydir)]

    # rename_add_activation(files, 'HCD', skip='AIETD')
    # rename_add_activation(files, 'AIETD', skip='HCD')
