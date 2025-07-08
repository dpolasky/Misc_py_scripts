"""
Utility functions for manipulating FASTA files.
"""
import re


DIGESTED_FASTA = r"C:\_Local\misc_testing\2025-07-03_Alessandro-histone-DMO\try_digested-4-mis-histones+human.fasta"
REF_FASTA = r"C:\_Local\fastas\2025-07-08-decoys-reviewed-contam-UP000005640.fas"


def parse_fasta(file_path, header_regex=None):
    """
    Parse a FASTA file and return a dictionary of sequences indexed by their IDs.
    """
    sequences = {}
    with open(file_path, 'r') as f:
        current_id = None
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                current_id = get_id(line, header_regex)
                sequences[current_id] = ''
            elif current_id is not None:
                sequences[current_id] += line
    return sequences


def replace_sequences_with_matched(file, matches, filename='replaced', header_regex=None):
    """
    Replace sequences in the FASTA file with matched sequences from the provided dictionary.
    """
    with open(file, 'r') as f:
        output = []
        found_ids = set()
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                current_id = get_id(line, header_regex)
                if current_id in matches and current_id not in found_ids:
                    output.append(line)
                    output.append(matches[current_id])  # Add the matched sequence
                    found_ids.add(current_id)

    output_file = file.replace('.fasta', f'_{filename}.fasta')
    with open(output_file, 'w') as f:
        for line in output:
            f.write(line + '\n')


def replace_ids_with_matched(file, matches, filename='replaced', header_regex=None):
    """
    Replace IDs in the sequences dictionary with matched IDs.
    """
    with open(file, 'r') as f:
        output = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                current_id = get_id(line, header_regex)
                if current_id in matches:
                    line = '>' + matches[current_id]
            output.append(line)

    output_file = file.replace('.fasta', f'_{filename}.fasta')
    with open(output_file, 'w') as f:
        for line in output:
            f.write(line + '\n')


def get_id(line, header_regex=None):
    """
    Extract the ID from a FASTA header line.
    """
    if header_regex is not None:
        match = re.match(header_regex, line)
        if match:
            current_id = match.group(1)
        else:
            current_id = None
    else:
        current_id = line[1:]  # Remove the '>' character
    return current_id


def undigest_fasta(digested_fasta, reference_fasta):
    """
    take a digested FASTA file and capture all unique IDs, then create an undigested FASTA using the reference FASTA
    to get the full sequence for each ID.
    """
    header_regex = r">(\w+\|\w+)"
    sequence_dict = parse_fasta(digested_fasta, header_regex)       # duplicate IDs will be overwritten, which is fine since the sequences get replaced anyway
    reference_dict = parse_fasta(reference_fasta, header_regex)     # to get IDs matching the sequence dict
    # reference_original_ids = parse_fasta(reference_fasta)           # to get the original IDs for the final output
    for prot_id, sequence in sequence_dict.items():
        if prot_id in reference_dict:
            sequence_dict[prot_id] = reference_dict[prot_id]
        else:
            print(f"Warning: ID {prot_id} not found in reference FASTA. Replace it manually!")

    replace_sequences_with_matched(digested_fasta, sequence_dict, 'undigested', header_regex=header_regex)


if __name__ == "__main__":
    undigest_fasta(DIGESTED_FASTA, REF_FASTA)
