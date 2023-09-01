"""
quick script for counting glycans by mass from uniques.csv files
"""
import os
import pathlib

PATH = r"Z:\data\HLA\_Results\_uniques"

files = [os.path.join(PATH, x) for x in os.listdir(PATH) if x.endswith("_glycFDR_uniques.csv")]
mass_dict = {}

for file in files:
    nextline = False
    with open(file, 'r') as readfile:
        for line in readfile:
            if nextline:
                # read the counts from this line for the compositions on the previous
                splits = line.split(',')
                counts = [int(x) for x in splits[2:]]
                for i in range(len(counts)):
                    mass_dict[masses[i]] += counts[i]
                nextline = False

            if line.startswith("PTMS Glycan Compositions"):
                splits = line.split(',')
                comps = splits[2:]
                masses = [x.split('~')[0] for x in comps]
                for mass in masses:
                    if mass not in mass_dict.keys():
                        mass_dict[mass] = 0
                nextline = True
            else:
                nextline = False


with open(pathlib.Path(PATH) / "glycan_counts.tsv", 'w') as outfile:
    for mass, count in sorted(mass_dict.items(), key=lambda x: x[1], reverse=True):
        outfile.write('{}\t{}\n'.format(mass, count))
