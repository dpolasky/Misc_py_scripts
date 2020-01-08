"""
quickly calculate glycan mass from a list
"""

import tkinter
from tkinter import filedialog
import os
import itertools

MASS_DICT = {'HexNAc': 203.07937,
             'Hex': 162.05282,
             'Fuc': 146.057909,
             'NeuAc': 291.0954,
             'Phospho': 79.96633,
             'NeuGc': 307.0903,
             'Pent': 132.0423,
             'Sulfo': 79.9568,
             'KDN': 250.0689,
             'HexA': 176.03209
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


def gen_glyco_masses(hexnacs, hexes, fucs, neuacs, phosphos):
    """
    Generate all combinations of provided components
    :param hexnacs: [min, max]
    :param hexes: [min, max]
    :param fucs: [min, max]
    :param neuacs: [min, max]
    :param phosphos: [min, max]
    :return: list of (name, mass)
    """
    all_outputs = []
    for hexnac_count in range(hexnacs[0], hexnacs[1]):
        for hex_count in range(hexes[0], hexes[1]):
            for fuc_count in range(fucs[0], fucs[1]):
                for neuac_count in range(neuacs[0], neuacs[1]):
                    for phosph_count in range(phosphos[0], phosphos[1]):
                        mass = MASS_DICT['HexNAc'] * hexnac_count + MASS_DICT['Hex'] * hex_count + MASS_DICT['Fuc'] * fuc_count + MASS_DICT['NeuAc'] * neuac_count + MASS_DICT['Phospho'] * phosph_count
                        name = 'HexNAc,{},Hex,{},Fuc,{},NeuAc,{},Phosph,{}'.format(hexnac_count, hex_count, fuc_count, neuac_count, phosph_count)
                        all_outputs.append((name, mass))
    return all_outputs
    # combo_inputs = []
    # for key, range_list in dict_glyc_ranges.items():
    #     for num in range(range_list[0], range_list[1]):
    #         new_key_parts = []
    #         for _ in range(num):
    #             new_key_parts.append(key)
    #         combo_inputs.append('_'.join(new_key_parts))
    #
    # # iterate over all combinations of all possible numbers of the input
    # for combo in itertools.combinations(combo_inputs, len(dict_glyc_ranges.keys())):
    #     both_parts = combo[0] + combo[1]


def gen_glyco_masses_dict(mass_range_dict):
    """
    Generate all combiations of provided masses
    :param mass_range_dict: dict of component name: [min, max]
    :type mass_range_dict: dict
    :return: list of (name, mass) of all combinations
    :rtype: list
    """
    inputs = []
    for name, minmax in mass_range_dict.items():
        # generate all input strings of 'name_number' for all numbers in range
        this_input = []
        if minmax[1] == 0:
            continue
        current_num = minmax[0]
        while current_num < minmax[1]:
            this_input.append('{}_{}'.format(name, current_num))
            current_num += 1
        if len(this_input) > 0:
            inputs.append(this_input)

    # now make all products and compute mass
    all_outputs = []
    for combination in itertools.product(*inputs):
        # decode mass
        mass = 0
        name_items = []
        for glycan_string in combination:
            name_items.append(glycan_string)
            splits = glycan_string.split('_')
            mass += int(splits[1]) * MASS_DICT[splits[0]]
        all_outputs.append((','.join(name_items), mass))
    return all_outputs


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    # in_file = filedialog.askopenfilename(filetypes=[('.csv', '.csv')])
    # read_masses, read_glycans = glycan_text_to_mass(in_file)
    # outfilepath = os.path.join(os.path.dirname(in_file), 'output.csv')
    # write_output(read_masses, read_glycans, outfilepath)

    # NOTE: b/c range, it goes to 1 less than specified (so use [0, 1] to ignore)
    # masses = gen_glyco_masses(hexnacs=[1, 7], hexes=[0, 9], fucs=[0, 5], neuacs=[0, 2], phosphos=[0, 1])
    # masses = gen_glyco_masses(hexnacs=[1, 9], hexes=[0, 12], fucs=[0, 3], neuacs=[0, 3], phosphos=[0, 2])
    # masses = gen_glyco_masses(hexnacs=[1, 9], hexes=[0, 12], fucs=[0, 3], neuacs=[0, 3], phosphos=[0, 2])
    massdict = {'HexNAc': [0, 12],
                'Hex': [0, 14],
                'Fuc': [0, 4],
                'NeuAc': [0, 4],
                'Phospho': [0, 4],
                'NeuGc': [0, 4],
                'Pent': [0, 4],
                'Sulfo': [0, 0],
                'KDN': [0, 0],
                'HexA': [0, 0]
                }
    masses = gen_glyco_masses_dict(massdict)
    root.clipboard_clear()
    outputs = []
    outputs.append('Name,Mass\n')
    for mass_tup in masses:
        outputs.append('{},{}\n'.format(mass_tup[0], mass_tup[1]))
        print('{},{}'.format(mass_tup[0], mass_tup[1]))
    root.clipboard_append(''.join(outputs))
    root.mainloop()
    # root.destroy()
