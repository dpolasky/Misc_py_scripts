"""
Command line runner for MSConvert
"""

import tkinter
from tkinter import filedialog
import os
import subprocess

tool_path = r"C:\Program Files\ProteoWizard\ProteoWizard 3.0.19194.9338c77b2\msconvert.exe"
out_dir = ''
DEISOTOPE = True
RUN_BOTH = True


def format_commands(filename, deisotope):
    """
    Generate a formatted string for running MSConvert
    :param filename:
    :param deisotope: boolean
    :return: string
    """
    # create output directory
    if deisotope:
        output_dir = os.path.join(os.path.dirname(filename), 'DeIso_output')
    else:
        output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd_str = '{} {} --mzML -z --64 -o {}'.format(tool_path, filename, output_dir)
    cmd_str += ' --filter "peakPicking true 1-"'
    if deisotope:
        cmd_str += ' --filter "MS2Deisotope Poisson minCharge=1 maxCharge=6"'
        # cmd_str += ' --filter "MS2Deisotope hi_res"'

    print(cmd_str)
    return cmd_str


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(filetypes=[('Raw', '.raw')])
    files = [os.path.join(os.path.dirname(x), x) for x in files]

    for file in files:
        if RUN_BOTH:
            cmd = format_commands(file, deisotope=True)
            subprocess.run(cmd)
            cmd = format_commands(file, deisotope=False)
            subprocess.run(cmd)
        else:
            cmd = format_commands(file, deisotope=DEISOTOPE)
            subprocess.run(cmd)
