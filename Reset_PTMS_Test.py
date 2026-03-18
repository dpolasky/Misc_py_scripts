"""
Reset the PTM-S glycan assignment testing psm.tsv
"""
import os
import shutil
import pathlib

# FILE_TO_COPY = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm_newNames.tsv"
# FILE_TO_COPY = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm - Copy.tsv"            # PTMS
# PSM_FILE = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm.tsv"
# FILE_TO_COPY = r"C:\_Local\_software-tests\PTMS_tests\psm_10psms.tsv"           # PTMS
# FILE_TO_COPY = r"C:\_Local\_software-tests\PTMS_tests\psm - Copy.tsv"           # PTMS
# FILE_TO_COPY = r"C:\_Local\_software-tests\PTMS_tests\2025-07-16_yeast-nh4_psm - Copy.tsv"
# FILE_TO_COPY = r"C:\_Local\_software-tests\PTMS_tests\2025-07-23_yeast-3467_psm - Copy.tsv"
FILE_TO_COPY = r"C:\_Local\_software-tests\PTMS_tests\mbg_psm - Copy.tsv"
# PSM_FILE = r"C:\_Local\_software-tests\PTMS_tests\psm.tsv"
PSM_FILE = r"C:\_Local\_software-tests\PTMS_tests\psm_mbg.tsv"
# SAVE_NAME_APPEND = "LDA_psm"
# SAVE_NAME_APPEND = "base_psm"
SAVE_NAME_APPEND = None

# FILE_TO_COPY = r"E:\Project_Data\Glyco\_PTMShep_assign_testing\psm_mbg-test-data.tsv"     # MBG
# FILE_TO_COPY = r"C:\_Local\_software-tests\MBG_tests\2025-06-25_HGI-data_2files_many-adducts\1\psm - Copy.tsv"
# PSM_FILE = r"C:\_Local\_software-tests\MBG_tests\2025-06-25_HGI-data_2files_many-adducts\1\psm.tsv"

# FILE_TO_COPY = r"C:\_Local\_software-tests\opair\psm - Copy.tsv"             # OPair
# PSM_FILE = r"C:\_Local\_software-tests\opair\psm.tsv"


def main():
    """

    :return:
    :rtype:
    """
    if os.path.exists(PSM_FILE):
        if SAVE_NAME_APPEND is not None:
            save_name = os.path.splitext(PSM_FILE)[0] + '_' + SAVE_NAME_APPEND + os.path.splitext(PSM_FILE)[1]
            shutil.move(PSM_FILE, save_name)
        else:
            os.remove(PSM_FILE)
    shutil.copy(FILE_TO_COPY, PSM_FILE)

    # handle unfiltered_psm.tsv if present
    output_dir = pathlib.Path(PSM_FILE).parent / 'ptm-shepherd-output'
    if os.path.exists(output_dir):
        possible_paths = [os.path.join(output_dir, x) for x in os.listdir(output_dir) if x.endswith('unfiltered_psm.tsv')]
        if len(possible_paths) == 1:
            print('removing unfiltered psm file at {}'.format(possible_paths[0]))
            os.remove(possible_paths[0])


if __name__ == '__main__':
    main()
