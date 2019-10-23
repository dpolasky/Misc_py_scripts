"""
module for removing scans from an mzML file without using MSConvert. Why? Because that way:
1) scan indices will be correct (with reference to the original file)
2) we can handle things like separating HCD from EThcD, where both "ETD" and "HCD" strings appear in the dissoc info
"""

import tkinter
from tkinter import filedialog
import os
import xml.etree.ElementTree as Et
from enum import Enum
from pyteomics import mzml


class ActivationType(Enum):
    """
    Holder for filetypes
    """
    HCD = 'hcd'
    ETD = 'etd'


def filter_scans(mzml_file, activations_allowed, activations_not_allowed):
    """
    Remove scans matching the provided activation rule
    :param mzml_file: mzML file path
    :param activations_allowed: list of ActivationType
    :param activations_not_allowed: list of ActivationType
    :return: void
    """
    # with mzml.read(mzml_file) as reader:
    #     reader.

    tree = Et.parse(mzml_file)
    treeroot = tree.getroot()

    # iterate over matches
    for thing in treeroot:
        for thing2 in thing:
            for thing3 in thing2:
                for spectrum in thing3:
                    for scan_list in spectrum:
                        for scan_info in scan_list:
                            for scan in scan_info:
                                try:
                                    if scan.attrib['name'] == 'filter string':
                                        scan_header = scan.attrib['value']
                                        if 'hcd' in scan_header or 'etd' in scan_header:
                                            # MS2 scan - do filtering
                                            for activation in activations_not_allowed:
                                                if activation.value in scan_header:
                                                    thing3.remove(spectrum)

                                        print(scan.attrib['value'])
                                except KeyError:
                                    continue
        # charge = int(child_spectrum_query.attrib['assumed_charge'])
        # for search_result in child_spectrum_query:
        #     for search_hit in search_result:
        #         combined_score_container.add_psm(search_hit, charge)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    mzmls = filedialog.askopenfilenames(filetypes=[('mzML', '.mzml')])
    for mzml in mzmls:
        filter_scans(mzml, [ActivationType.ETD], [ActivationType.HCD])
