"""
Reset the PTM-S glycan assignment testing psm.tsv
"""
import os
import shutil


FILE_TO_COPY = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm - Copy.tsv"
PSM_FILE = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm.tsv"


def main():
    """

    :return:
    :rtype:
    """
    if os.path.exists(PSM_FILE):
        os.remove(PSM_FILE)
    shutil.copy(FILE_TO_COPY, PSM_FILE)


if __name__ == '__main__':
    main()
