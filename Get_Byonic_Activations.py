"""
Add activation type to Byonic psm.csv file by reading mzml files
"""
import tkinter
from tkinter import filedialog
import os
import pyopenms

BYONIC_ACTIVATION_COLUMN = 27
BYONIC_RT_COLUMN = 24
BYONIC_SCAN_COLUMN = 25
RAW_DIR = r"\\corexfs.med.umich.edu\proteomics\dpolasky\data\glyco\2017_01_19_MB1-4_Glyco\unsplit"


ACTIVATION_TYPES = {8: 'HCD',
                    11: 'ETD',
                    0: 'CID',
                    5: 'ECD'}
# BIRD = 4
# IRMPD = 6


def find_scan_activations(mzml_file):
    """
    Determine the activation type of each scan and save it to a dict of scan: activation
    :param mzml_file: mzML file path
    :return: dict of scan: activation
    :rtype: dict
    """
    print('loading file {}'.format(mzml_file))
    exp = pyopenms.MSExperiment()
    pyopenms.MzMLFile().load(mzml_file, exp)

    activation_dict = {}
    rt_dict = {}
    for index, spectrum in enumerate(exp.getSpectra()):
        precs = spectrum.getPrecursors()
        lvl = spectrum.getMSLevel()
        if lvl == 2:
            if len(precs) > 1:
                print('WARNING: multiple precursors detected, not supported')
                precursor = None
            else:
                precursor = precs[0]
            act_list = list(precursor.getActivationMethods())
            if len(act_list) > 1:
                activation = '_'.join([ACTIVATION_TYPES[x] for x in act_list])
            else:
                activation = ACTIVATION_TYPES[act_list[0]]
            activation_dict[index + 1] = activation     # add 1 because scans are 1-indexed instead of 0-indexed
            rt = spectrum.getRT() / 60.0     # returns RT in seconds
            rt_dict[index + 1] = rt
    return activation_dict, rt_dict


def edit_psm_table(psm_file, rawfile_scan_dicts, rawfile_rt_dicts):
    """
    Edit the activation in the PSM table to match the provided activation types
    :param psm_file: psm table to read (Byonic.csv)
    :type psm_file: str
    :param rawfile_scan_dicts: dict of rawfile: {scan: activation}
    :type rawfile_scan_dicts: dict
    :param rawfile_rt_dicts: dict of rawfile: {scan: RT}
    :type rawfile_rt_dicts: dict
    :return: void
    :rtype:
    """
    output = []
    with open(psm_file, 'r') as readfile:
        for line in list(readfile):
            if line.startswith('Spectrum'):
                # header
                output.append(line)
                continue
            # parse spectrum
            splits = line.split(',')
            scan_splits = splits[0].split('.')
            scan_num = int(scan_splits[1])
            rawname = scan_splits[0]

            activation = rawfile_scan_dicts[rawname][scan_num]
            splits[BYONIC_ACTIVATION_COLUMN] = activation
            splits[BYONIC_SCAN_COLUMN] = str(scan_num)
            splits[BYONIC_RT_COLUMN] = str(rawfile_rt_dicts[rawname][scan_num])
            newline = ','.join(splits)
            output.append(newline)

    with open(psm_file, 'w') as writefile:
        for line in output:
            writefile.write(line)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    psmfiles = filedialog.askopenfilenames(filetypes=[('PSM file', '_psm.tsv'), ('PSM file', '_byonic.csv'), ('PSM file', '_psm.txt')])

    rawfiles = [os.path.join(RAW_DIR, x) for x in os.listdir(RAW_DIR) if x.endswith('.mzML')]
    rawfile_scandicts = {}
    rawfile_rtdicts = {}
    for rawfile in rawfiles:
        scans, rts = find_scan_activations(rawfile)
        rawfile_scandicts[os.path.basename(os.path.splitext(rawfile)[0])] = scans
        rawfile_rtdicts[os.path.basename(os.path.splitext(rawfile)[0])] = rts

    main_dir = os.path.dirname(psmfiles[0])
    for psmfile in psmfiles:
        edit_psm_table(psmfile, rawfile_scandicts, rawfile_rtdicts)
