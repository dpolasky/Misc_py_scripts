"""
read through a bunch of Byonic files to get a list of all Y ions they found
"""
import tkinter
from tkinter import filedialog
import os


def parse_byonic_csv(csvfile):
    """
    Return all the Y-ion relevant strings for parsing
    :param csvfile: full path
    :return: list of strings
    """
    strings = []
    with open(csvfile, 'r') as readfile:
        for line in list(readfile):
            if not line.startswith('Pep'):
                continue
            else:
                strings.append(line.rstrip('\n'))
    return strings


def getAllYionsByonic(file_list):
    """
    Read through a list of byonic output csv files and generate list of unique Y ions and their masses
    :param file_list: list of csv files to parse (full paths)
    :return:
    """

    dict_y_ions = {}
    for current_file in file_list:
        y_strings = parse_byonic_csv(current_file)
        for y_string in y_strings:
            y_id, y_mass = parse_y_string(y_string)
            if y_id in dict_y_ions.keys():
                dict_y_ions[y_id] += 1
            else:
                # save the mass and count of times this fragment has been found
                dict_y_ions[y_id] = 1
    return dict_y_ions


def parse_y_string(y_string):
    """
    The Byonic CSV output saves Y ions as "Pep_[sugar]_[charge]+", followed by the mass after a comma. Get the
    sugar ID (exclude charge) and the mass to save to dictionary
    :param y_string: string input from byonic
    :return: string (ID), float (mass)
    """
    column_splits = y_string.split(',')
    id_splits = column_splits[0].split('_')
    sugar_id = id_splits[0][4:]     # remove the 'PEP+' from the beginning
    mz_splits = column_splits[1].split('=')
    mz = float(mz_splits[1])
    return sugar_id, mz


def save_output_to_file(dict_y_ions, output_path):
    """
    Save the dictionary of unique sugars to text file
    :param dict_y_ions: dict of key=sugar ID, value=mass, count
    :param output_path: full path
    :return: void
    """
    with open(output_path, 'w') as outfile:
        outfile.write('Y Glycan,count\n')
        for key, value in dict_y_ions.items():
            outfile.write('{},{}\n'.format(key, value))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    folder = filedialog.askdirectory()
    files = [os.path.join(folder, x) for x in os.listdir(folder) if x.endswith('.csv')]
    output_dict = getAllYionsByonic(files)
    save_output_to_file(output_dict, os.path.join(folder, 'output.csv'))
