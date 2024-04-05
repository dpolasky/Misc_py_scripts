"""
combine fasta files
"""
import pathlib
import tkinter
from tkinter import filedialog


def main():
    """

    :return:
    :rtype:
    """
    fastas = filedialog.askopenfilenames(filetypes=[('fasta', '.fasta'), ('fasta', '.fas')])
    output = []
    for fasta in fastas:
        with open(fasta, 'r') as readfile:
            for line in readfile:
                output.append(line)

    output_path = pathlib.Path(fastas[0]).parent / 'combined.fasta'
    with open(output_path, 'w') as outfile:
        for line in output:
            outfile.write(line)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()
    main()
