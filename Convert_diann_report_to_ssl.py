"""
script to convert a DIA-NN report.tsv to ssl for reading in Skyline
"""

from pyteomics import mass
import re
import os

PATH = r"E:\_Software_Tests\DIA\glyco\2023-10-31_test01_updatedFragPipe\test_report.tsv"

HEADER_DICT = {'file': ["File.Name"],
               'scan': ["MS2.Scan"],
               'charge': ["Precursor.Charge"],
               'sequence': ["Modified.Sequence"],
               'score': ["Q.Value"],
               'retention-time': ["RT"]
               }


def convert_file(filepath):
    """

    :param filepath:
    :type filepath:
    :return:
    :rtype:
    """
    output = []
    with open(filepath, 'r') as readfile:
        header = readfile.readline()
        header_dict = match_header_to_dict(header, HEADER_DICT, '\t')
        for line in readfile:
            splits = line.split('\t')
            file = splits[header_dict['file']].replace('\\', '/')
            scan = splits[header_dict['scan']]
            charge = splits[header_dict['charge']]
            sequence = splits[header_dict['sequence']]
            rt = splits[header_dict['retention-time']]
            score = splits[header_dict['score']]

            # convert mods
            mod_splits = sequence.split('(')
            revised_sequence = ""
            prev_aa = ""
            for mod_split in mod_splits:
                if ")" in mod_split:
                    mass_splits = mod_split.split(")")
                    mod_mass = float(mass_splits[0])
                    revised_mass = mod_mass - mass.std_aa_mass[prev_aa]
                    revised_sequence += '[+{:.4f}]{}'.format(revised_mass, mass_splits[1])
                    if len(mass_splits[1]) > 0:
                        prev_aa = mass_splits[1][-1]
                else:
                    # first bit, just append
                    revised_sequence += mod_split
                    prev_aa = mod_split[-1]
            output.append('{}\n'.format('\t'.join([file, scan, charge, revised_sequence, 'PERCOLATOR QVALUE', score, rt])))

    output_path = os.path.splitext(filepath)[0] + '.ssl'
    with open(output_path, 'w') as outfile:
        outfile.write('file\tscan\tcharge\tsequence\tscore-type\tscore\tretention-time\n')
        for line in output:
            outfile.write(line)


def match_header_to_dict(header_str: str, psm_attributes_dict: dict, delimiter: str, quiet=False):
    """
    Match parsed header to attributes to determine the indices of columns in the file
    :param header_str: string header from file
    :param psm_attributes_dict: dict of attribute name: list of acceptable parsed names
    :param delimiter: file delimiter
    :param quiet: suppress printing output
    :return: dict of attribute name: column index
    """
    output_dict = {key: '' for key in psm_attributes_dict.keys()}
    header_str = header_str.replace('"', '')
    header_splits = header_str.rstrip('\n').split(delimiter)
    for attribute_name, allowed_names_list in psm_attributes_dict.items():
        for index, split in enumerate(header_splits):
            if split in allowed_names_list:
                output_dict[attribute_name] = index
                break

    # make sure all keys got parsed and warn if not
    for key, val in output_dict.items():
        if val == -1:
            if not quiet:
                print('Warning: nothing parsed for key {}'.format(key))
    return output_dict


if __name__ == '__main__':
    convert_file(PATH)
