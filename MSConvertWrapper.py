"""
Command line runner for MSConvert
"""

import tkinter
from tkinter import filedialog
import os
import subprocess

tool_path = r"C:\Program Files\ProteoWizard\ProteoWizard 3.0.19194.9338c77b2\msconvert.exe"
out_dir = ''


def format_commands(filename):
    """
    Generate a formatted string for running MSConvert
    :param filename:
    :return: string
    """
    cmd_str = '{} {} --mzML -z --64 -o {}'.format(tool_path, filename, out_dir)
    cmd_str += ' --filter "peakPicking true 1-"'
    cmd_str += ' --filter "MS2Deisotope Poisson minCharge=1 maxCharge=4"'

    print(cmd_str)
    return cmd_str


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(filetypes=[('Raw', '.raw')])
    files = [os.path.join(os.path.dirname(x), x) for x in files]
    out_dir = os.path.join(os.path.dirname(files[0]), 'DeIso_output')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for file in files:
        cmd = format_commands(file)
        subprocess.run(cmd)
