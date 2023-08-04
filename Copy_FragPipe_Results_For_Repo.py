"""
script to copy results from a set of FragPipe results folders to a single organized directory for data deposition/repository
upload using a template file.
"""

import os
import shutil

# TEMPLATE_PATH = r"\\corexfs.med.umich.edu\proteomics\dpolasky\manuscripts\2022_Labile_PTMs\_Processed-data-for-submission\_revision1\Filecopy_template.csv"
TEMPLATE_PATH = r"\\corexfs.med.umich.edu\proteomics\dpolasky\manuscripts\2022_Georges_HLA-atlas\Filecopy_template.csv"

MANIFEST_NAME = 'fragpipe-files.fp-manifest'
FILES_TO_COPY = [
    # 'fragpipe.workflow',
    # MANIFEST_NAME,
    # 'protein.fas',
    # 'ion.tsv',
    'peptide.tsv',
    'protein.tsv',
    'psm.tsv'
]


def copy_results(template_path, files_list):
    """
    read the template and copy the files
    :param template_path:
    :type template_path:
    :param files_list:
    :type files_list:
    :return:
    :rtype:
    """
    with open(template_path, 'r') as readfile:
        for index, line in enumerate(list(readfile)):
            print('copying files for results directory {}...'.format(index + 1))
            if line.startswith('#'):
                continue
            splits = line.split(',')
            source_dir = splits[0]

            # make destination dir
            destination_dir = os.path.join(*splits[1:]).rstrip('\n')
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            # copy files
            is_multi_experiment = not os.path.exists(os.path.join(source_dir, 'psm.tsv'))
            if is_multi_experiment:
                for filename in files_list[:2]:
                    shutil.copy(os.path.join(source_dir, filename), os.path.join(destination_dir, filename))

                # get all sub-directories and copy them with structure
                subdirs = [os.path.join(source_dir, x) for x in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, x))]
                for sub_index, subdir in enumerate(subdirs):
                    print('\tcopying sub-directory {} of {}'.format(sub_index + 1, len(subdirs)))
                    subdir_destination = os.path.join(destination_dir, os.path.basename(subdir))
                    if not os.path.exists(subdir_destination):
                        os.makedirs(subdir_destination)
                    for filename in files_list[2:]:
                        shutil.copy(os.path.join(subdir, filename), os.path.join(subdir_destination, filename))

            else:
                for filename in files_list:
                    shutil.copy(os.path.join(source_dir, filename), os.path.join(destination_dir, filename))

            # edit manifest file
            if MANIFEST_NAME in FILES_TO_COPY:
                edit_manifest(destination_dir)


def edit_manifest(directory):
    """
    Edit the manifest file in this directory, changing all absolute paths to relative paths. Intended to remove
    system paths from the generator's computer before uploading to a repo and make it easier to access for downloaders.
    NOTE: assumes input paths are using Unix separators (/)
    :param directory: directory where the manifest file is located
    :type directory: str
    :return: void
    :rtype:
    """
    output = []
    with open(os.path.join(directory, MANIFEST_NAME), 'r') as readfile:
        for line in list(readfile):
            splits = line.split('/')
            if len(splits) > 0:
                line = '.\\{}'.format(splits[-1])
                output.append(line)

    with open(os.path.join(directory, MANIFEST_NAME), 'w') as writefile:
        for line in output:
            writefile.write(line)


if __name__ == '__main__':
    copy_results(TEMPLATE_PATH, FILES_TO_COPY)
