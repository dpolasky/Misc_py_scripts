"""
quickly calculate glycan mass from a list
"""

import tkinter
from tkinter import filedialog
import os

MASS_DICT = {'HexNAc': 203.07937,
             'Hex': 162.05282,
             'Fuc': 146.057909,
             'NeuAc': 291.0954,
             'Phospho': 0
             }


def glycan_text_to_mass(input_file):
    """
    Convert Byonic text output to a list of masses
    :param input_file: text file with masses on individual lines
    :return: list of masses
    """
    input_strings = parse_glycan_file(input_file)

    masses = []
    glycans = []
    for input_string in input_strings:
        # split on parentheses to check number
        splits = input_string.split('(')
        prev_glycan_mass = 0
        prev_glycan = ''
        glycan_id = ''
        for split in splits:
            split = split.strip()
            if ')' in split:
                # this is the number of the previous glycan
                num_str = split.replace('(', '')
                splits2 = num_str.split(')')
                num_str = splits2[0]
                num_glycans = int(num_str)
                glyc_mass = MASS_DICT[prev_glycan] * num_glycans

                prev_glycan_mass += glyc_mass
                if glycan_id is '':
                    glycan_id += '{}({})'.format(prev_glycan, num_glycans)
                else:
                    glycan_id += ',{}({})'.format(prev_glycan, num_glycans)

                # next glycan is in the split too
                try:
                    if splits2[1] is not '':
                        prev_glycan = splits2[1]
                except KeyError:
                    print('no key for string: {}'.format(splits2[1]))

            else:
                # this is a new glycan
                prev_glycan = split

        if prev_glycan_mass not in masses:
            masses.append(prev_glycan_mass)
            glycans.append(glycan_id)
    return masses, glycans


def parse_glycan_file(input_file):
    """

    :param input_file:
    :return:
    """
    count_glyco = 0
    count_multi = 0
    strings = []
    with open(input_file, 'r') as glyc_file:
        for line in list(glyc_file):
            if line is '\n':
                continue
            # treat multiple glycans in one peptide as single entries
            if ';' in line:
                splits = line.rstrip('\n').split(';')
                for split in splits:
                    strings.append(split)
                count_multi += 1
            else:
                glyco_string = line.rstrip('\n')
                strings.append(glyco_string)
                count_glyco += 1
    print('{} single glycans and {} multi-glycans'.format(count_glyco, count_multi))
    return strings


def write_output(masses, glycans, filename):
    """

    :param masses:
    :param glycans:
    :param filename
    :return:
    """
    with open(filename, 'w') as outfile:
        outfile.write('Mass,Glycan\n')
        for index, mass in enumerate(masses):
            outfile.write('{},{}\n'.format(mass, glycans[index]))
        # also write a single string formatted for Java input
        single_string = '0'
        for mass in masses:
            single_string += '/{}'.format(mass)
        outfile.write(single_string)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    in_file = filedialog.askopenfilename(filetypes=[('.csv', '.csv')])
    read_masses, read_glycans = glycan_text_to_mass(in_file)
    outfilepath = os.path.join(os.path.dirname(in_file), 'output.csv')
    write_output(read_masses, read_glycans, outfilepath)

