"""
Module for pre-digesting a fasta file and saving the output to a new fasta file for Fragger input. If need to
search multiple enzymes with very different numbers of missed cleavages (for example) in Fragger.
"""

import tkinter
from tkinter import filedialog
import os
from pyteomics import fasta, parser
import time


def do_digest(seq, res_to_cut_list, max_missed_cleavages, cut_cterm=True):
    """
    Helper to do the actual digestion.
    :param seq: sequence to digest
    :type seq: str
    :param res_to_cut_list: list of residues at which to cut
    :type res_to_cut_list: list
    :param max_missed_cleavages:
    :type max_missed_cleavages: int
    :param cut_cterm: if true, cut c-term to residues, otherwise cut n-term
    :type cut_cterm: bool
    :return: list of digested peptides
    :rtype: list
    """
    peptides = []
    cleavage_indices = [0]
    cleavage_indices.extend([index for index, char in enumerate(seq) if char in res_to_cut_list])
    for index, cleavage_site in enumerate(cleavage_indices):
        for num_missed in range(1, max_missed_cleavages + 1):
            if cut_cterm:
                if index + num_missed < len(cleavage_indices):
                    peptides.append(seq[index + 1: cleavage_indices[index + num_missed] + 1])
                else:
                    # going to end of sequence (past the final cleavage site)
                    peptides.append(seq[index + 1:])
            else:
                # cut n-term, or at 1 less than the index of the cleavage site
                if index + num_missed < len(cleavage_indices):
                    peptides.append(seq[cleavage_indices[index]: cleavage_indices[index + num_missed]])
                else:
                    # going to end of sequence (past the final cleavage site)
                    peptides.append(seq[cleavage_indices[index]:])
    return set(peptides)


def digest_custom_manual(fasta_file, res_to_cut, max_missed_cleavages, min_length, max_length, c_term=True):
    """
    Digesting by hand because Pyteomics can't handle enzymes that cut N-terminal to a given residue :(. For each
    protein sequence, does the digestion and generates all possible peptides matching the provided rules. Combines
    all outputs into a dict of peptide: all possible proteins that can contain it
    :param fasta_file: full path to fasta
    :type fasta_file: str
    :param max_missed_cleavages: max allowed, will gen up to this
    :type max_missed_cleavages: int
    :param res_to_cut: list of residues at which to cleave
    :type res_to_cut: list
    :param min_length: min peptide length output
    :type min_length: int
    :param max_length: max output length
    :type max_length: int
    :param c_term: whether to cut C-terminal to specified residues or Nterminal
    :type c_term: bool
    :return: dict of peptide: protein descriptions containing it
    :rtype: dict
    """
    output_fasta_dict = {}
    index = 0
    for protein_descript, protein_seq in fasta.read(fasta_file):
        if index % 10000 == 0:
            print('digested seq {}...'.format(index))
        index += 1
        peptides = do_digest(protein_seq, res_to_cut, max_missed_cleavages, c_term)
        peptides = [x for x in peptides if min_length <= len(x) <= max_length]
        for peptide in peptides:
            if peptide in output_fasta_dict.keys():
                output_fasta_dict[peptide].append(protein_descript)
            else:
                output_fasta_dict[peptide] = [protein_descript]
    print_counts(output_fasta_dict)
    return output_fasta_dict


def digest_fasta_trypsin(fasta_file, min_length, max_length):
    """
    do digestion of file using trypsin rules (can add more as needed). Currently NOT removing duplicate peptides
    :param fasta_file: file to read
    :param min_length: min length of digested seq
    :param max_length: max length of digested seq
    :return: list of (description, sequence) tuples to write to fasta
    """
    output_fasta_dict = {}
    index = 0
    for protein_descript, protein_seq in fasta.read(fasta_file):
        if index % 10000 == 0:
            print('digested seq {}...'.format(index))
        index += 1
        # digest this protein using parser.cleave and filter by min and max length
        new_peptides = parser.cleave(protein_seq, parser.expasy_rules['trypsin'], missed_cleavages=2, min_length=min_length)
        new_peptides = [x for x in new_peptides if len(x) <= max_length]
        # save to output fasta list - all peptides have the same protein description but digested sequence
        for peptide in new_peptides:
            if peptide in output_fasta_dict.keys():
                output_fasta_dict[peptide].append(protein_descript)
            else:
                output_fasta_dict[peptide] = [protein_descript]
            # output_fasta_tups.append((protein_descript, peptide))
    # print counts for diagnostics
    print_counts(output_fasta_dict)
    return output_fasta_dict


def print_counts(output_fasta_dict):
    """
    Print counts of multi-protein peptides for diagnostics
    :param output_fasta_dict:
    :type output_fasta_dict:
    :return:
    :rtype:
    """
    print('total peptides = {}'.format(len(output_fasta_dict.keys())))
    # print('total unique peptides = {}'.format(len(set(output_fasta_dict.keys()))))
    counts = {x: 0 for x in range(5)}
    counts[5] = 0
    for peptide, prot_list in output_fasta_dict.items():
        if len(prot_list) < 5:
            counts[len(prot_list)] += 1
        else:
            counts[5] += 1
    print(counts)


def write_fasta(fasta_dict, output_path):
    """
    manually write output because pyteomics is super slow. Chunked to try to improve speed
    :param fasta_dict: dict of seq: description
    :type fasta_dict: dict
    :param output_path: full path
    :type output_path: str
    :return: void
    :rtype:
    """
    index = 0
    with open(output_path, 'w') as outfile:
        current_chunk = []
        current_time = time.time()
        for seq, description in fasta_dict.items():
            if index % 1000000 == 0:
                print('printed seq {} of {} in {:.1f} s'.format(index, len(fasta_dict.keys()), time.time() - current_time))
                current_time = time.time()
            if index % 10000 == 0:
                outfile.write(''.join(current_chunk))
                current_chunk = []
            current_chunk.append('>{}\n{}\n'.format(description[0], seq))
            index += 1
            # outfile.write('>{}\n{}\n'.format(description[0], seq))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(filetypes=[('Fasta', '.fasta'), ('Fasta', '.fas')])
    maindir = os.path.dirname(files[0])

    for file in files:
        # fasta_info = digest_fasta_trypsin(file, min_length=7, max_length=60)
        fasta_info = digest_custom_manual(file, res_to_cut=['S', 'T'], max_missed_cleavages=20, min_length=7, max_length=1000, c_term=False)
        new_filename = os.path.splitext(file)[0] + '_digest.fasta'
        print('writing output')
        # fasta.write(fasta_info, output=new_filename)
        write_fasta(fasta_info, new_filename)
    print('done')
