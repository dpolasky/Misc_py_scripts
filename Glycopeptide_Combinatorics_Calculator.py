"""
Script for calculating the search space (number of modified peptides) of a given fasta file and search settings.
5/1/2023
"""

from pyteomics import fasta, parser
import re
import math

FASTA = r"E:\_Software_Tests\glyco_combinatorics\FourMucins_NoSigPeps_FASTA.fasta"
NUM_GLYCS = 12
ENZYME = 'trypsin'
MISSED_CLEAVAGE = 2
#SEMI_ENZ = False


def main(fasta_file):
    """

    :return:
    :rtype:
    """
    all_peps = set()
    # read proteins
    id_tuple_iterator = fasta.read(fasta_file)

    # digest proteins
    for id_tuple in id_tuple_iterator:
        seq = id_tuple[1]
        unique_peps = parser.cleave(seq, ENZYME, MISSED_CLEAVAGE)
        all_peps.update(unique_peps)

    # compute modified peptides
    glycoform_dict = {}
    for pep_seq in all_peps:
        num_sites = len(re.findall(r'[ST]', pep_seq))
        if num_sites in glycoform_dict.keys():
            glycoform_dict[num_sites].append(pep_seq)
        else:
            glycoform_dict[num_sites] = [pep_seq]

    # count total forms
    total = 0
    for site_count, pep_list in sorted(glycoform_dict.items(), key=lambda x: x[0]):
        num_peps = len(pep_list)
        if site_count == 0:
            forms_per_pep = 1   # only 1 form per peptide if no sites
        else:
            forms_per_pep = combinations_with_replacement(NUM_GLYCS, site_count)
        new_forms = forms_per_pep * num_peps
        total += new_forms
        print('{} sites: {} peps, {} forms/pep, {} forms, {} total'.format(site_count, num_peps, forms_per_pep, new_forms, total))


def combinations_with_replacement(n, r):
    """

    :param n:
    :type n:
    :param r:
    :type r:
    :return:
    :rtype:
    """
    return int(math.factorial(n + r - 1) / (math.factorial(r) * math.factorial(n - 1)))


if __name__ == '__main__':
    main(FASTA)
