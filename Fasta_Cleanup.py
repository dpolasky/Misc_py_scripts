"""
clean up fasta files
"""

fasta_path = r"E:\_Software_Tests\crystalC\2022-01-18-decoys-FiveMucins_FASTA.fasta.fas"

# fix lower case letters in proteins
output = []
with open(fasta_path, 'r') as readfile:
    for line in readfile:
        if line.startswith('>'):
            output.append(line)
        else:
            output.append(line.upper())

with open(fasta_path, 'w') as outfile:
    for line in output:
        outfile.write(line)
