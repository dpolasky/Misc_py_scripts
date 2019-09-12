"""
Module for testing density of peaks in MS2 spectra from debug
"""

from dataclasses import dataclass
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
import math


@dataclass
class Spectrum(object):
    """
    spec container
    """
    peak_dict: dict
    peaks_before: int
    peaks_after: int


def parsefile(csvfile):
    """

    :param csvfile:
    :return:
    """
    all_range_dict = {'{} - {}'.format(x, x + 100): {} for x in range(0, 2000, 100)}

    # assume file is trimmed from headers and only needs to avoid progress updates
    with open(csvfile, 'r') as readfile:
        for line in list(readfile):
            if line.startswith('total') or line.startswith('final') or line.startswith('\t'):
                continue
            splits = line.rstrip('\n').split(',')
            if splits[1] == '0':
                continue
            try:
                if splits[1] in all_range_dict[splits[0]].keys():
                    all_range_dict[splits[0]][splits[1]] += 1
                else:
                    all_range_dict[splits[0]][splits[1]] = 1
                # all_range_dict[splits[0]].append(splits[1])
            except KeyError:
                print('no key for input: {}'.format(splits[0]))
    return all_range_dict


def plot_outputs(all_range_dict, outputdir, log_mode=False):
    """

    :param all_range_dict:
    :param outputdir
    :return:
    """

    for range_str, dict_pk_nums in all_range_dict.items():
        plt.clf()

        # create frequency histogram
        # xval = int(range_str.split('-')[0].strip())
        for peaknum, freq in sorted(dict_pk_nums.items(), key=lambda x: x[0]):
            if log_mode:
                plt.bar(int(peaknum), math.log(freq, 10))
            else:
                plt.bar(int(peaknum), freq)

            # print('starting peaknum {}'.format(peaknum))
            # for i in range(freq):
            #     plt.scatter(xval + i/10.0, peaknum)
        outpath = os.path.join(outputdir, '{}.png'.format(range_str))
        plt.xlabel('Number of Peaks')
        if log_mode:
            plt.ylabel('Log Frequency')
        else:
            plt.ylabel('Frequency')
        plt.title('m/z: {}'.format(range_str))
        plt.savefig(outpath)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    inputfile = filedialog.askopenfilename(filetypes=[('csv', '.csv')])
    mydict = parsefile(inputfile)
    outputfolder = os.path.join(os.path.dirname(inputfile), 'outputs')
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    plot_outputs(mydict, outputfolder)

    outputfolder_log = os.path.join(os.path.dirname(inputfile), 'outputs_log')
    if not os.path.exists(outputfolder_log):
        os.makedirs(outputfolder_log)
    plot_outputs(mydict, outputfolder_log, log_mode=True)
