"""
helper script for updating Fragpipe workflow names since we can't save as default.
Given a starting folder, takes all names with a space in them, removes the space and anything
after it, and saves over any existing files with the resulting truncated name. Those
updated files can then be saved to the github repo.
"""

import os
import shutil

WORKFLOW_DIR = r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\build\classes\java\workflows"
REPO_DIR = r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\resources\workflows"
REQUIRED_STRING = 'glyco'
EDIT_EXISTING_DEFAULTS = False   # if true, edit files with no spaces as well as with spaces
# EDIT_EXISTING_DEFAULTS = True   # if true, edit files with no spaces as well as with spaces


def main(edit_dir, save_dir, required_string, edit_existing_defaults):
    """
    Edit filenames in the edit_dir, then save them to the repo dir. Overwrite existing files of same name in
    each case. Filenames must have required_string to be edited
    :param edit_dir: dir path with files to edit
    :type edit_dir: str
    :param save_dir: dir path to save output
    :type save_dir: str
    :param required_string: string that must be in filename to edit
    :type required_string: str
    :param edit_existing_defaults: if true, edit files with no spaces as well as with spaces
    :type edit_existing_defaults: bool
    :return: void
    :rtype:
    """
    init_files = [x for x in os.listdir(edit_dir) if x.endswith('.workflow')]
    filepaths_to_copy = []
    for file in init_files:
        if required_string in file:
            # edit file and save
            splits = os.path.splitext(file)[0].split(' ')
            if not edit_existing_defaults:
                if len(splits) == 1:
                    # this is not an update file (either a default or has already been overwritten)
                    continue
            new_filename = os.path.join(edit_dir, splits[0] + os.path.splitext(file)[1])

            # edit the file to change the saved filename comment at the top
            stripped_filename = os.path.splitext(os.path.basename(new_filename))[0]
            edit_fileheader(os.path.join(edit_dir, file), stripped_filename)

            # move the file
            shutil.move(os.path.join(edit_dir, file), new_filename)
            filepaths_to_copy.append(new_filename)

    # copy to final dir
    for file in filepaths_to_copy:
        savepath = os.path.join(save_dir, os.path.basename(file))
        shutil.copy(file, savepath)


def edit_fileheader(workflow_file, new_filename_str):
    """
    open the workflow file and edit the comment thing at the type that holds the saved filename
    to match the new filename
    :param workflow_file: full path of workflow file to edit
    :type workflow_file: str
    :param new_filename_str: stripped down new filename (NOT full path)
    :type new_filename_str: str
    :return: void
    :rtype:
    """
    output = []
    with open(workflow_file, 'r') as readfile:
        for line in list(readfile):
            if line.startswith('# Workflow'):
                # edit
                splits = line.split(':')
                newline = '{}: {}\n'.format(splits[0], new_filename_str)
                output.append(newline)
            else:
                output.append(line)

    with open(workflow_file, 'w') as writefile:
        for line in output:
            writefile.write(line)


if __name__ == '__main__':
    main(WORKFLOW_DIR, REPO_DIR, REQUIRED_STRING, EDIT_EXISTING_DEFAULTS)
