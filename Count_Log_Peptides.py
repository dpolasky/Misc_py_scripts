"""
script to count the number of unique peptides from log files when a peptide index is built with MSFragger
"""
import os
import re

DIR_PATH = r"Z:\dpolasky\projects\_BuildTests\_results"


def count_peptides(log_file):
    """
    Find all lines with format 	of length #: ####, extract the count and sum. Print the filepath and count
    """
    total = 0
    pattern = re.compile(r'of length \d+:\s+(\d+)')
    with open(log_file) as f:
        for line in f:
            match = pattern.search(line)
            if match:
                total += int(match.group(1))
    print(f"{log_file}: {total:,} peptides")
    return total


def find_logs_and_count(directory):
    """
    walk the directory, find all logs, and print the filepath and count
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('log_2') and ('2026-03-17' in root):
                log_path = os.path.join(root, file)
                count_peptides(log_path)


if __name__ == '__main__':
    find_logs_and_count(DIR_PATH)
