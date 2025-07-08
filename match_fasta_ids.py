"""
match proteins in one file to another based on sequences
"""
import pathlib
import subprocess
import sys
from io import StringIO

from Bio.Blast import NCBIXML, NCBIWWW
from Bio.Blast.Applications import NcbimakeblastdbCommandline, NcbiblastnCommandline, NcbiblastpCommandline
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
from misc_fasta_manipulations import parse_fasta, replace_ids_with_matched

file1 = r"C:\_Local\_raw-conversion\HGI_2025\HGI_FASTA_ModuleAndB.fasta"
file2 = r"C:\_Local\_raw-conversion\HGI_2025\HGI_FASTA_ModuleC.fasta"
DB_NAME = "HGI_FASTA_ModuleC.fasta"


def match_fasta_sequences(file_1, file_2):
    """
    Match sequences from two FASTA files and return a list of matching IDs.
    """
    seqs1 = parse_fasta(file_1)
    seqs2 = parse_fasta(file_2)

    matches = {}
    blast_seqs = {}
    for id1, seq1 in seqs1.items():
        found_match = False
        for id2, seq2 in seqs2.items():
            if seq1 == seq2:
                matches[id1] = id2
                found_match = True
        if not found_match:
            blast_seqs[id1] = seq1

    results = perform_online_blast_batch(blast_seqs, database="nr", program="blastp", hitlist_size=20)
    matches.update(results)

    return matches


def perform_online_blast_batch(query_sequences, database="nr", program="blastp", hitlist_size=10):
    """
    Perform an online BLAST search against the NCBI database for a batch of sequences.

    :param query_sequences: A list of sequences to search for.
    :param database: The NCBI database to use (default: "nr").
    :param program: The BLAST program to use (default: "blastp").
    :param hitlist_size: The maximum number of hits to return (default: 10).
    :return: A dictionary of query sequences and their top hit IDs.
    """
    results = {}
    ids = list(query_sequences.keys())
    try:
        # Combine sequences into a single FASTA string
        fasta_query = "\n".join([f">Query_{i}\n{seq}" for i, seq in enumerate(query_sequences.values())])

        # Perform the BLAST search
        result_handle = NCBIWWW.qblast(program, database, fasta_query, hitlist_size=hitlist_size)
        blast_records = NCBIXML.parse(result_handle)

        # Parse results
        for i, record in enumerate(blast_records):
            if record.alignments:
                found_sp = False
                for alignment in record.alignments:
                    if alignment.hit_id.startswith("sp"):
                        # Use the first hit ID that starts with "sp" (SwissProt)
                        results[ids[i]] = alignment.title
                        found_sp = True
                        break
                if not found_sp:
                    results[ids[i]] = record.alignments[0].title
            else:
                results[ids[i]] = None
    except Exception as e:
        print(f"Online BLAST search failed: {e}")
    return results


def perform_online_blast(query_sequence, database="nr", program="blastp", evalue=0.04):
    """
    Perform an online BLAST search against the NCBI database.

    :param query_sequence: The sequence to search for.
    :param database: The NCBI database to use (default: "nr").
    :param program: The BLAST program to use (default: "blastp").
    :param evalue: The E-value threshold (default: 0.04).
    :return: The top hit ID, or None if no hit is found.
    """
    try:
        result_handle = NCBIWWW.qblast(program, database, query_sequence)
        blast_results = NCBIXML.read(result_handle)

        if blast_results.alignments:
            top_alignment = blast_results.alignments[0]
            top_id = top_alignment.title
            return top_id
        else:
            return None
    except Exception as e:
        print(f"Online BLAST search failed: {e}")
        return None


def perform_local_blast(query_sequence, db_name="custom_blast_db", evalue=0.04):
    """
    Perform a local BLAST search against the custom database.

    :param query_sequence: The sequence to search for.
    :param db_name: The name of the BLAST database.
    :param evalue: The E-value threshold.
    :return: BLAST results.
    """
    # blastn_cline = NcbiblastnCommandline(query="-", db=db_name, evalue=evalue, outfmt=5)
    # stdout, stderr = blastn_cline(stdin=query_sequence)
    # blast_results = NCBIXML.read(StringIO(stdout))
    # return blast_results

    blastp_cline = NcbiblastpCommandline(query="-", db=db_name, evalue=evalue, outfmt=5)
    try:
        stdout, stderr = blastp_cline(stdin=query_sequence)
        blast_results = NCBIXML.read(StringIO(stdout))
        return blast_results
    except Exception as e:
        print(f"BLAST search failed: {e}")
        return None


def create_local_blast_db(fasta_file, db_name="custom_blast_db", db_type="prot"):
    """
    Create a local BLAST database from a list of sequences.

    :param db_name: The name of the BLAST database.
    :param db_type: Type of database (nucl or prot).
    """
    # Create the BLAST database
    # makeblastdb_cline = NcbimakeblastdbCommandline(dbtype=db_type, input_file=fasta_file)
    # stdout, stderr = makeblastdb_cline()
    # print(f"BLAST database '{db_name}' created successfully.")

    # Check if makeblastdb is in PATH
    try:
        subprocess.run(['makeblastdb', '-help'], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: 'makeblastdb' not found in PATH.")
        print("Please ensure that the BLAST+ executables are in your system's PATH.")
        sys.exit(1)

    fasta_path = pathlib.Path(fasta_file)
    if not fasta_path.exists():
        print(f"Error: The file {fasta_file} does not exist.")
        sys.exit(1)

    cmd = ['makeblastdb', '-dbtype', db_type, '-in', str(fasta_path)]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"BLAST database '{db_name}' created successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error creating BLAST database: {e}")
        print(e.stderr)


def main():
    """
    Main function to execute the matching and ID replacement.
    """
    # set up the BLAST database for matching
    # create_local_blast_db(file2, db_name=DB_NAME, db_type="prot")

    matches = match_fasta_sequences(file1, file2)
    print(f"Found {len(matches)} matching sequences.")

    # Replace IDs in the first file
    replace_ids_with_matched(file1, matches, 'unmasked')


if __name__ == "__main__":
    main()

