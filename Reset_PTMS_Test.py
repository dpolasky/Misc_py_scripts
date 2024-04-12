"""
Reset the PTM-S glycan assignment testing psm.tsv
"""
import os
import shutil

# FILE_TO_COPY = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm_newNames.tsv"
FILE_TO_COPY = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm - Copy.tsv"            # PTMS
PSM_FILE = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm.tsv"
# FILE_TO_COPY = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm_mbg-test-data.tsv"     # MBG
# FILE_TO_COPY = r"E:\_Software_Tests\OPair_library-for-MSF\_test\psm - Copy.tsv"             # OPair
# PSM_FILE = r"E:\_Software_Tests\OPair_library-for-MSF\_test\psm.tsv"


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
