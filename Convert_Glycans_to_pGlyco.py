"""
module to final all structures matching a given composition in the pglyco database provided
"""
import re
import os

# COMPS_FILE = r"Z:\dpolasky\projects\Glyco\OPair_comparison\_OPair-Paper-Data\_Glycan_Databases_and_conversions\GlycanComps_12.txt"
COMPS_FILE = r"Z:\dpolasky\projects\Glyco\OPair_comparison\_OPair-Paper-Data\_Glycan_Databases_and_conversions\GlycanComps_32.txt"
PGLYCO_DB = r"Z:\dpolasky\projects\Glyco\OPair_comparison\_OPair-Paper-Data\_Glycan_Databases_and_conversions\pGlyco_all_OGlyc_structs-no-HexOnly.txt"
COMP_PATTERN = '[a-zA-z]*\\([0-9]*\\)'
CONVERSION_DICT = {'HexNAc': 'N',
                   'Hex': 'H',
                   'Fuc': 'F',
                   'NeuAc': 'A',
                   }


def convert(input_comps_file, input_pglyco_db):
    """

    :param input_comps_file:
    :type input_comps_file:
    :param input_pglyco_db:
    :type input_pglyco_db:
    :return:
    :rtype:
    """
    comps = []
    with open(input_comps_file, 'r') as infile:
        for line in list(infile):
            if line.startswith('Glycan'):
                continue
            matches = re.findall(COMP_PATTERN, line)
            comp_components = {}
            for match in matches:
                splits = match.split('(')
                name = splits[0]
                num = int(splits[1].replace(')', ''))
                comp_components[CONVERSION_DICT[name]] = num
            comps.append(get_comp_str(comp_components))

    pglyco_struct_dict = parse_pglyco_struct_dict(input_pglyco_db)
    output = {comp: pglyco_struct_dict[comp] for comp in comps}
    output_path = os.path.splitext(input_comps_file)[0] + '_pglyco-structs.gdb'
    with open(output_path, 'w') as outfile:
        outfile.write('H,N,A,F\n')
        for comp, struct_list in output.items():
            for struct in struct_list:
                outfile.write(struct + '\n')
            print('{} struct(s) for comp {}'.format(len(struct_list), comp))


def parse_pglyco_struct_dict(input_pglyco_db):
    """
    parse all structures and make a dict of comp: structure list
    :param input_pglyco_db:
    :type input_pglyco_db:
    :return:
    :rtype:
    """
    pglyco_allcomp_dict = {}
    with open(input_pglyco_db, 'r') as searchfile:
        for line in list(searchfile):
            if ',' in line:
                continue    # skip header
            struct_string = line.rstrip('\n')
            comp_str = parse_structure(struct_string)
            if comp_str in pglyco_allcomp_dict.keys():
                if struct_string not in pglyco_allcomp_dict[comp_str]:
                    pglyco_allcomp_dict[comp_str].append(struct_string)
            else:
                pglyco_allcomp_dict[comp_str] = [struct_string]
    return pglyco_allcomp_dict


def parse_structure(struct_string):
    """
    parse structure to a composition by counting elements
    :param struct_string:
    :type struct_string: str
    :return:
    :rtype:
    """
    comp_dict = {glyc_code: struct_string.count(glyc_code) for glyc_code in CONVERSION_DICT.values()}
    return get_comp_str(comp_dict)


def get_comp_str(comp_dict):
    """
    convert dict to a sorted string for hashing
    :param comp_dict: dict of glycan single letter: count
    :type comp_dict: dict
    :return: str
    :rtype:
    """
    output = ''
    for glyc_code, count in sorted(comp_dict.items()):
        if count > 0:
            output += '{}{}'.format(glyc_code, count)
    return output


if __name__ == '__main__':
    convert(COMPS_FILE, PGLYCO_DB)
