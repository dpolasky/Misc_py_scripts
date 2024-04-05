"""
Script to quickly edit param file titles
"""

import tkinter
from tkinter import filedialog
import os
import shutil

NEW_DATE = '2020_10_19-Criscuolo'
PTMS_DATE = '1008'
PTMS_VERSION = '1.2.5'

KEEP_LIST = ['brain', 'heart', 'liver', 'kidney', 'lung']
NEW_NAME = 'peptide-ion_fig5-mouse'

# REMOVE_OLD_DATE = True
REMOVE_OLD_DATE = False
append = '_HCD'
# append = ''
REMOVE = ['#', ',', ' ']

REPLACE = {'AI-ETD': 'AIETD'}

FPOP_DICT = {
    '1pAZ_Control_second_L1': '1pAZ_Control_BR1_L1',
    '1pAZ_Control_second_L2': '1pAZ_Control_BR1_L2',
    '1pAZ_Control_second_L3': '1pAZ_Control_BR1_L3',
    '1pAZ_Control_second_NL1': '1pAZ_Control_BR1_NL1',
    '1pAZ_Control_second_NL2': '1pAZ_Control_BR1_NL2',
    '1pAZ_Control_second_NL3': '1pAZ_Control_BR1_NL3',
    '1pAZ_Control_second_W1': '1pAZ_Control_BR1_W1',
    '1pAZ_Control_second_W2': '1pAZ_Control_BR1_W2',
    '1pAZ_Control_second_W3': '1pAZ_Control_BR1_W3',
    '1pAZ_second_L1': '1pAZ_sample_BR1_L1',
    '1pAZ_second_L2': '1pAZ_sample_BR1_L2',
    '1pAZ_second_L3': '1pAZ_sample_BR1_L3',
    '1pAZ_second_NL1': '1pAZ_sample_BR1_NL1',
    '1pAZ_second_NL2': '1pAZ_sample_BR1_NL2',
    '1pAZ_second_NL3': '1pAZ_sample_BR1_NL3',
    '1pAZ_second_W1': '1pAZ_sample_BR1_W1',
    '1pAZ_second_W2': '1pAZ_sample_BR1_W2',
    '1pAZ_second_W3': '1pAZ_sample_BR1_W3',
    'CPE_1pAZBR2_L1': '1pAZ_sample_BR2_L1',
    'CPE_1pAZBR2_L2': '1pAZ_sample_BR2_L2',
    'CPE_1pAZBR2_L3': '1pAZ_sample_BR2_L3',
    'CPE_1pAZBR2_NL1': '1pAZ_sample_BR2_NL1',
    'CPE_1pAZBR2_NL2': '1pAZ_sample_BR2_NL2',
    'CPE_1pAZBR2_NL3': '1pAZ_sample_BR2_NL3',
    'CPE_1pAZBR2_W1': '1pAZ_sample_BR2_W1',
    'CPE_1pAZBR2_W2': '1pAZ_sample_BR2_W2',
    'CPE_1pAZBR2_W3': '1pAZ_sample_BR2_W3',
    'CPE_ControlBR2_L1': '1pAZ_control_BR2_L1',
    'CPE_ControlBR2_L2': '1pAZ_control_BR2_L2',
    'CPE_ControlBR2_L3': '1pAZ_control_BR2_L3',
    'CPE_ControlBR2_NL1': '1pAZ_control_BR2_NL1',
    'CPE_ControlBR2_NL2': '1pAZ_control_BR2_NL2',
    'CPE_ControlBR2_NL3': '1pAZ_control_BR2_NL3',
    'CPE_ControlBR2_W1': '1pAZ_control_BR2_W1',
    'CPE_ControlBR2_W2': '1pAZ_control_BR2_W2',
    'CPE_ControlBR2_W3-2nd': '1pAZ_control_BR2_W3',
    'CN_05AZnOA_BR1': '2CPE_control_BR1_L1',
    'CN_05AZnOA_BR1_L2': '2CPE_control_BR1_L2',
    'CN_05AZnOA_BR1_L3': '2CPE_control_BR1_L3',
    'CN_05AZnOA_BR1_NL1': '2CPE_control_BR1_NL1',
    'CN_05AZnOA_BR1_NL2': '2CPE_control_BR1_NL2',
    'CN_05AZnOA_BR1_NL3': '2CPE_control_BR1_NL3',
    'CN_05AZnOA_BR1_W1_20190824182203': '2CPE_control_BR1_W1',
    'CN_05AZnOA_BR1_W2': '2CPE_control_BR1_W2',
    'CN_05AZnOA_BR1_W3': '2CPE_control_BR1_W3',
    'CPE_05AZnOA_BR1_L1': '2CPE_sample_BR1_L1',
    'CPE_05AZnOA_BR1_L2': '2CPE_sample_BR1_L2',
    'CPE_05AZnOA_BR1_L3': '2CPE_sample_BR1_L3',
    'CPE_05AZnOA_BR1_NL1': '2CPE_sample_BR1_NL1',
    'CPE_05AZnOA_BR1_NL2': '2CPE_sample_BR1_NL2',
    'CPE_05AZnOA_BR1_NL3': '2CPE_sample_BR1_NL3',
    'CPE_05AZnOA_BR1_W1': '2CPE_sample_BR1_W1',
    'CPE_05AZnOA_BR1_W2': '2CPE_sample_BR1_W2',
    'CPE_05AZnOA_BR1_W3': '2CPE_sample_BR1_W3',
    '2CPEs_BR2_L1': '2CPE_sample_BR2_L1',
    '2CPEs_BR2_L2': '2CPE_sample_BR2_L2',
    '2CPEs_BR2_L3': '2CPE_sample_BR2_L3',
    '2CPEs_BR2_NL1': '2CPE_sample_BR2_NL1',
    '2CPEs_BR2_NL2': '2CPE_sample_BR2_NL2',
    '2CPEs_BR2_NL3': '2CPE_sample_BR2_NL3',
    '2CPEs_BR2_W1': '2CPE_sample_BR2_W1',
    '2CPEs_BR2_W2': '2CPE_sample_BR2_W2',
    '2CPEs_BR2_W3': '2CPE_sample_BR2_W3',
    '2CPEsControl_BR2_L1': '2CPE_control_BR2_L1',
    '2CPEsControl_BR2_L2': '2CPE_control_BR2_L2',
    '2CPEsControl_BR2_L3': '2CPE_control_BR2_L3',
    '2CPEsControl_BR2_NL1': '2CPE_control_BR2_NL1',
    '2CPEsControl_BR2_NL2': '2CPE_control_BR2_NL2',
    '2CPEsControl_BR2_NL3': '2CPE_control_BR2_NL3',
    '2CPEsControl_BR2_W1': '2CPE_control_BR2_W1',
    '2CPEsControl_BR2_W2': '2CPE_control_BR2_W2',
    '2CPEsControl_BR2_W3': '2CPE_control_BR2_W3',
}


def rename_remove_msconvert_append(file_list):
    """
    remove weird extra filename pieces appended by MSConvert ("file-[weirdness].mzML")
    :param file_list:
    :type file_list:
    :return:
    :rtype:
    """
    for file in file_list:
        splits = file.split('-')
        new_filename = splits[0] + '.mzML'
        os.rename(file, new_filename)


def rename_ptms_configs(file_list, new_date, new_version=''):
    """
    Rename a set of PTM-S config files with new date and (optional) PTMS version. PTMS files assumed to be named
    according to convention: shp_[version]_[date]_rest-of-name.config
    :param file_list: list of files to rename
    :type file_list: list
    :param new_date: string
    :type new_date: str
    :param new_version: string
    :type new_version: str
    :return: void
    :rtype:
    """
    for file in file_list:
        filename = os.path.splitext(os.path.basename(file))[0]
        extension = os.path.splitext(file)[1]
        splits = filename.split('_')
        if new_version is not '':
            splits[1] = new_version
        splits[2] = new_date
        new_filename = os.path.join(os.path.dirname(file), '_'.join(splits)) + extension
        shutil.copy(file, new_filename)


def rename_from_dict(file_list, names_dict):
    """
    Rename a list of files from a provided dict of old name: new name.
    :param file_list: list of files to rename
    :type file_list: list
    :param names_dict: dict of old name: new name
    :type names_dict: dict
    :return: void
    :rtype:
    """
    for file in file_list:
        old_base = os.path.splitext(os.path.basename(file))[0]
        if old_base in names_dict:
            # include directory and file extenstion in new name
            new_name = os.path.join(os.path.dirname(file), names_dict[old_base]) + os.path.splitext(file)[1]
            os.rename(file, new_name)
        else:
            print('no match found for file {}'.format(file))


def copy_rename_original_folder(file_list, output_folder):
    """
    Copy a set of files to a single directory, renaming each with the name of its original containing folder.
    Intended for (e.g.) a group of psm.tsv (or etc) files that want to end up in the same place for combined analysis
    :param file_list: list of files
    :param output_folder: where to save all outputs
    :return: void
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index, file in enumerate(file_list):
        orig_folder = os.path.basename(os.path.dirname(file))
        new_name = '{}_{}'.format(orig_folder, os.path.basename(file))
        new_path = os.path.join(output_folder, new_name)
        print('copying file {} of {}...'.format(index + 1, len(file_list)))
        shutil.copy(file, new_path)


def rename_add_activation(file_list, activation, skip=None):
    """
    Add activation string to end of files
    :param file_list:
    :param skip
    :param activation:
    :return:
    """
    for file in file_list:
        filename = os.path.splitext(os.path.basename(file))[0]
        extension = os.path.splitext(file)[1]
        splits = filename.split('_')
        if skip is not None:
            if skip in splits:
                continue
        if activation is not '':
            splits.insert(len(splits), activation)
        new_filename = os.path.join(os.path.dirname(file), '_'.join(splits)) + extension
        os.rename(file, new_filename)


def copy_rename_date(file_list, new_date, filename_append, remove_chars, in_place=False):
    """
    Rename date based on naming convention of y_m_d_filename. Creates a copy of the files
    :param file_list: list of paths
    :param new_date: new date string
    :param filename_append: str
    :param remove_chars: if provided (list), remove these chars from filename
    :param in_place: if true, rename rather than copy
    :return: void
    """
    for file in file_list:
        filename = os.path.basename(file)
        splits = filename.split('_')
        # insert
        if filename_append is not '':
            splits.insert(len(splits) - 1, filename_append)

        # change date
        if new_date is not '':
            if REMOVE_OLD_DATE:
                new_filename = '{}_{}'.format(new_date, '_'.join(splits[3:]))
            else:
                new_filename = '{}_{}'.format(new_date, '_'.join(splits))
        else:
            new_filename = filename

        # remove chars
        for char in remove_chars:
            new_filename = new_filename.replace(char, '')

        if in_place:
            os.rename(file, os.path.join(os.path.dirname(file), new_filename))
        else:
            shutil.copy(file, os.path.join(os.path.dirname(file), new_filename))


def rename_replace_chars(file_list, replace_dict):
    """
    Replace any instances of keys in the replace dict with values
    :param file_list: list of file paths
    :type file_list: list
    :param replace_dict: dict of bad string: replacement string
    :type replace_dict: dict
    :return: void - renames in place
    :rtype:
    """
    for file in file_list:
        filename = os.path.basename(file)
        new_filename = filename
        for old_str, new_str in replace_dict.items():
            if old_str in filename:
                new_filename = new_filename.replace(old_str, new_str)
        os.rename(file, os.path.join(os.path.dirname(file), new_filename))


def remove_chars_only(file_list, remove_char_list):
    """
    remove chars from filename
    :param file_list: list of files
    :type file_list: list
    :param remove_char_list: list of strings to remove
    :type remove_char_list: list
    :return: void
    :rtype:
    """
    for file in file_list:
        # remove chars
        filename = os.path.basename(file)
        for char in remove_char_list:
            filename = filename.replace(char, '')
        os.rename(file, os.path.join(os.path.dirname(file), filename))


def remove_all_except_keep_list(file_list, keep_list, new_name):
    """
    Completely replace the entire filename except for the items in the keep list
    :param file_list: list of files to rename
    :type file_list: list
    :param keep_list: list of specific strings to keep in the name
    :type keep_list: list
    :return: void
    :rtype:
    """
    for file in file_list:
        for keep_str in keep_list:
            # only rename the one with this specific name from the keep list on this iteration
            if keep_str in os.path.basename(file.lower()):
                new_filename = '{}_{}{}'.format(new_name, keep_str, os.path.splitext(file)[1])
                new_path = os.path.join(os.path.dirname(file), new_filename)
                os.rename(file, new_path)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames()

    # new_dir = filedialog.askdirectory()
    # copy_rename_original_folder(files, new_dir)

    # copy_rename_date(files, new_date='', filename_append='')
    # copy_rename_date(files, new_date=NEW_DATE, filename_append='', remove_chars=REMOVE)
    # copy_rename_date(files, new_date=NEW_DATE, filename_append=append, remove_chars=REMOVE, in_place=True)

    # mydir = filedialog.askdirectory()
    # files = [x for x in os.listdir(mydir)]

    # rename_add_activation(files, 'HCD', skip='AIETD')
    # rename_add_activation(files, 'ETciD')

    # remove_chars_only(files, REMOVE)

    # rename_from_dict(files, FPOP_DICT)
    # rename_replace_chars(files, REPLACE)

    # rename_ptms_configs(files, PTMS_DATE, PTMS_VERSION)
    # remove_all_except_keep_list(files, KEEP_LIST, NEW_NAME)
    rename_remove_msconvert_append(files)
