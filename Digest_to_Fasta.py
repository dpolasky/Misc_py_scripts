"""
Module for pre-digesting a fasta file and saving the output to a new fasta file for Fragger input. If need to
search multiple enzymes with very different numbers of missed cleavages (for example) in Fragger.
"""

import tkinter
from tkinter import filedialog
import os
from pyteomics import fasta, parser


def digest_fasta(fasta_file, min_length, max_length):
    """
    do digestion of file using trypsin rules (can add more as needed). Currently NOT removing duplicate peptides
    :param fasta_file: file to read
    :param min_length: min length of digested seq
    :param max_length: max length of digested seq
    :return: list of (description, sequence) tuples to write to fasta
    """
    output_fasta_tups = []
    index = 0
    for protein_descript, protein_seq in fasta.read(fasta_file):
        if index % 10000 == 0:
            print('parsed seq {}...'.format(index))
        index += 1
        # digest this protein using parser.cleave and filter by min and max length
        new_peptides = parser.cleave(protein_seq, parser.expasy_rules['trypsin'], missed_cleavages=1, min_length=min_length)
        new_peptides = [x for x in new_peptides if len(x) <= max_length]
        # save to output fasta list - all peptides have the same protein description but digested sequence
        for peptide in new_peptides:
            output_fasta_tups.append((protein_descript, peptide))
    print('total num fasta entries = {}'.format(len(output_fasta_tups)))
    return output_fasta_tups


def write_fasta(fasta_tups, output_path):
    """
    manually write output because pyteomics is super slow...
    :param fasta_tups: list of description, seq
    :type fasta_tups: list
    :param output_path: full path
    :type output_path: str
    :return: void
    :rtype:
    """
    index = 0
    with open(output_path, 'w') as outfile:
        for description, seq in fasta_tups:
            if index % 100000 == 0:
                print('printed seq {} of {}'.format(index, len(fasta_tups)))
            index += 1
            outfile.write('>{}\n{}\n'.format(description, seq))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(filetypes=[('Fasta', '.fasta'), ('Fasta', '.fas')])
    maindir = os.path.dirname(files[0])

    for file in files:
        fasta_info = digest_fasta(file, min_length=7, max_length=60)
        new_filename = os.path.splitext(file)[0] + '_digest.fasta'
        print('writing output')
        # fasta.write(fasta_info, output=new_filename)
        write_fasta(fasta_info, new_filename)
    print('done')
