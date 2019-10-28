"""
module for removing scans from an mzML file without using MSConvert. Why? Because that way:
1) scan indices will be correct (with reference to the original file)
2) we can handle things like separating HCD from EThcD, where both "ETD" and "HCD" strings appear in the dissoc info
"""

import tkinter
from tkinter import filedialog
import os
from enum import Enum
import pyopenms


class ActivationType(Enum):
    """
    Holder for filetypes
    """
    HCD = 8
    ETD = 11
    CID = 0
    ECD = 5
    BIRD = 4
    IRMPD = 6


def filter_scans(mzml_file, exact_activation_list, output_dir):
    """
    Remove scans matching the provided activation rule
    :param mzml_file: mzML file path
    :param exact_activation_list: list of ActivationType. Exact match required to ALL activation types specified
    :param output_dir: where to save
    :return: void
    """
    print('loading file {}'.format(mzml_file))
    exp = pyopenms.MSExperiment()
    pyopenms.MzMLFile().load(mzml_file, exp)
    activation_ints = [x.value for x in exact_activation_list]

    filtered_spectra = []
    for index, spectrum in enumerate(exp.getSpectra()):
        if index % 5000 == 0:
            print('filtered {} spectra'.format(index))
        precs = spectrum.getPrecursors()
        lvl = spectrum.getMSLevel()
        if lvl == 1:
            filtered_spectra.append(spectrum)
        elif lvl == 2:
            for precursor in precs:
                act = precursor.getActivationMethods()
                if len(act) == len(exact_activation_list):
                    # correct number of activation types
                    all_found = True
                    for method in act:
                        if method not in activation_ints:
                            all_found = False
                    if all_found:
                        filtered_spectra.append(spectrum)

    exp.setSpectra(filtered_spectra)

    output_file = os.path.join(output_dir, os.path.basename(mzml_file))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pyopenms.MzMLFile().store(output_file, exp)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    mzmls = filedialog.askopenfilenames(filetypes=[('mzML', '.mzml')])
    main_dir = os.path.dirname(mzmls[0])
    for mzml in mzmls:
        hcd_dir = os.path.join(main_dir, 'HCD')
        filter_scans(mzml, [ActivationType.HCD], hcd_dir)    # HCD only
        # ethcd_dir = os.path.join(main_dir, 'EThcD')
        # filter_scans(mzml, [ActivationType.HCD, ActivationType.ETD], ethcd_dir)    # EThcD only