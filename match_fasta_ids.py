"""
match proteins in one file to another based on sequences
"""


file1 = r"C:\_Local\_raw-conversion\HGI_2025\HGI_FASTA_ModuleAndB.fasta"
file2 = r"C:\_Local\_raw-conversion\HGI_2025\HGI_FASTA_ModuleC.fasta"


def parse_fasta(file_path):
    """
    Parse a FASTA file and return a dictionary of sequences indexed by their IDs.
    """
    sequences = {}
    with open(file_path, 'r') as f:
        current_id = None
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                current_id = line[1:]  # Remove the '>' character
                sequences[current_id] = ''
            elif current_id is not None:
                sequences[current_id] += line
    return sequences


def match_fasta_sequences(file_1, file_2):
    """
    Match sequences from two FASTA files and return a list of matching IDs.
    """
    seqs1 = parse_fasta(file_1)
    seqs2 = parse_fasta(file_2)

    matches = {}
    for id1, seq1 in seqs1.items():
        for id2, seq2 in seqs2.items():
            if seq1 == seq2:
                matches[id1] = id2

    return matches


def replace_ids_with_matched(file, matches):
    """
    Replace IDs in the sequences dictionary with matched IDs.
    """
    with open(file, 'r') as f:
        output = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                current_id = line[1:]  # Remove the '>' character
                if current_id in matches:
                    line = '>' + matches[current_id]
            output.append(line)

    output_file = file.replace('.fasta', '_unmasked.fasta')
    with open(output_file, 'w') as f:
        for line in output:
            f.write(line + '\n')


def main():
    """
    Main function to execute the matching and ID replacement.
    """
    matches = match_fasta_sequences(file1, file2)
    print(f"Found {len(matches)} matching sequences.")

    # Replace IDs in the first file
    replace_ids_with_matched(file1, matches)


if __name__ == "__main__":
    main()

