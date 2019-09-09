"""
Module for file renaming, especially for bad names from PRIDE/etc
"""

import tkinter
from tkinter import filedialog
import os

FILE_EXTENSION = '.mzML'


def parse_info_file(info_file):
    """
    read a csv with one filename on each line
    :param info_file: csv file
    :return: list of sample name strings
    """
    names = []
    with open(info_file, 'r') as infile:
        for line in list(infile):
            if not line == '\n':
                names.append(line.rstrip('\n'))
    return names


def rename_files(file_list, name_list):
    """
    Rename a list of files using exact matches between substrings of the name and the new, better name.
    :param file_list: list of raw file paths
    :param name_list: list of names
    :return: void
    """
    success_count = 0
    for filename in file_list:
        # get short name
        short_name = os.path.basename(filename).rstrip(FILE_EXTENSION)
        dir_name = os.path.dirname(filename)

        # search for match in name list
        matches = [x for x in name_list if short_name in x]
        if len(matches) == 1:
            # rename file
            new_name = os.path.join(dir_name, matches[0])
            new_name = new_name.rstrip('.raw') + FILE_EXTENSION
            os.rename(filename, new_name)
            success_count += 1
        else:
            print('too many or too few matches for filename {}: {}'.format(os.path.basename(filename), matches))

    print('Renamed {} of {} files'.format(success_count, len(file_list)))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    raw_files = filedialog.askopenfilenames(filetypes=[(FILE_EXTENSION, FILE_EXTENSION)])
    infofile = filedialog.askopenfilename(filetypes=[('csv', '.csv')])

    samplenames = parse_info_file(infofile)
    rename_files(raw_files, samplenames)
