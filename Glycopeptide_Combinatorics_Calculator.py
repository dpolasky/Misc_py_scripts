"""
Script for calculating the search space (number of modified peptides) of a given fasta file and search settings.
5/1/2023
"""

from pyteomics import fasta, parser
import re
import math

# FASTA = r"E:\_Software_Tests\glyco_combinatorics\FourMucins_NoSigPeps_FASTA.fasta"
FASTA = r"E:\_Software_Tests\glyco_combinatorics\2019-08-22-td-rev-NODECOY-UP000005640.fas"
NUM_GLYCS = 2
ENZYME = 'trypsin'
MISSED_CLEAVAGE = 2
# SEMI_ENZ = True
SEMI_ENZ = False
MIN_PEP_LEN = 7
MAX_PEP_LEN = 50


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
        unique_peps = parser.cleave(seq, ENZYME, MISSED_CLEAVAGE, semi=SEMI_ENZ)
        for pep in unique_peps:
            if MIN_PEP_LEN <= len(pep) <= MAX_PEP_LEN:
                all_peps.add(pep)

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
    total_peps = 0
    for site_count, pep_list in sorted(glycoform_dict.items(), key=lambda x: x[0]):
        num_peps = len(pep_list)
        total_peps += num_peps
        if site_count == 0:
            forms_per_pep = 1   # only 1 form per peptide if no sites
        else:
            forms_per_pep = combinations_with_replacement(NUM_GLYCS, site_count)
        new_forms = forms_per_pep * num_peps
        # new_forms_peptfirst = num_peps
        total += new_forms
        # total_pepfirst += new_forms_peptfirst
        print('{} sites: {} peps,\t{} total peps,\t{} forms/pep,\t{:.2E} forms,\t{:.3E}\ttotal'.format(site_count, num_peps, total_peps, forms_per_pep, new_forms, total))


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
