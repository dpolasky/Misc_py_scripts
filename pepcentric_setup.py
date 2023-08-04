"""
setup files for pepcentric
"""

import os
import re
import pathlib

# COPY_FOLDER = r"Z:\data\HLA\Racle_2019_PXD012308"
# DESTINATION = r"Z:\yufe\pepcentric\production\dataset"
COPY_FOLDER = "/storage/data/HLA/Purcell_2021_PXD025877"
DESTINATION = "/storage/yufe/pepcentric/production/dataset"
# FOLDERS = ["/storage/data/HLA/Racle_2019_PXD012308"]
FOLDERS = ["/storage/data/HLA/Bassani_2021_PXD020079",
           "/storage/data/HLA/Chong_2018_PXD006939",
           "/storage/data/HLA/Chong_2020_PXD013649",
           "/storage/data/HLA/Gerlinger_2019_PXD014017",
           "/storage/data/HLA/Gfeller_2018_PXD009925",
           "/storage/data/HLA/Neidert_2021_PXD019643",
           "/storage/data/HLA/Neidert_2021_PXD020186",
           "/storage/data/HLA/Pandey_2020_PXD015039",
           "/storage/data/HLA/Purcell_2021_PXD025877",
           # "/storage/data/HLA/Racle_2019_PXD012308",
           "/storage/data/HLA/2016_Bassani_PXD004894",
           "/storage/data/HLA/2019_Bassani_PXD013831",
           "/storage/data/HLA/Bassani_2015_PXD000394",
           ]


def main(folders):
    """

    :param folders:
    :type folders:
    :return:
    :rtype:
    """
    for folder in folders:
        single_folder(folder)


def single_folder(copy_folder):
    """

    :return:
    :rtype:
    """
    # pxd = re.search('(PXD[0-9]+)', copy_folder).group(1)

    copy_folder = pathlib.Path(copy_folder)
    data_name = "HLA_" + os.path.basename(copy_folder)
    destination_pxd = pathlib.Path(DESTINATION) / data_name
    print('destination dir {}'.format(destination_pxd))

    if not os.path.exists(destination_pxd):
        os.makedirs(destination_pxd)
    closed_dir = destination_pxd / 'Closed'
    open_dir = destination_pxd / 'Open'
    if not os.path.exists(closed_dir):
        os.makedirs(closed_dir)
        os.makedirs(open_dir)
        os.makedirs(destination_pxd / 'mzBIN')

    mzml_files = [e.resolve() for e in copy_folder.glob('*.mzML')]
    print('got {} mzmls in folder {}'.format(len(mzml_files), copy_folder))
    if len(mzml_files) == 0:
        c1path = copy_folder / 'class-I'
        c2path = copy_folder / 'class-II'
        class1 = [e.resolve() for e in c1path.glob('*.mzML')]
        class2 = [e.resolve() for e in c2path.glob('*.mzML')]
        mzml_files = class1
        mzml_files.extend(class2)
        print('got {} mzmls in folder {}'.format(len(mzml_files), copy_folder))

    # softlink
    for mzml in mzml_files:
        # print('softlinking {}'.format(mzml))
        basename = os.path.basename(mzml)
        os.symlink(mzml, closed_dir / basename)
        os.symlink(mzml, open_dir / basename)
    print('done softlinking')


if __name__ == '__main__':
    main(FOLDERS)
