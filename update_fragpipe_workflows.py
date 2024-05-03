"""
helper script for updating Fragpipe workflow names since we can't save as default.
Given a starting folder, takes all names with a space in them, removes the space and anything
after it, and saves over any existing files with the resulting truncated name. Those
updated files can then be saved to the github repo.
TO USE: Save new workflow settings with a space (and whatever else) at the end of the filename, then run
"""

import os
import shutil

# WORKFLOW_DIR = r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\build\classes\java\workflows"
WORKFLOW_DIR = r"C:\Users\dpolasky\Repositories\FragPipe\MSFragger-GUI\build\install\fragpipe\workflows"
REPO_DIRS = [r"C:\Users\dpolasky\Repositories\FragPipe\MSFragger-GUI\resources\workflows",
             r"C:\Users\dpolasky\Repositories\FragPipe\MSFragger-GUI\workflows"]

REQUIRED_STRINGS = ['glyco', 'Labile', 'FPOP']
EDIT_EXISTING_DEFAULTS = False   # if true, edit files with no spaces as well as with spaces
# EDIT_EXISTING_DEFAULTS = True   # if true, edit files with no spaces as well as with spaces


def main(edit_dir, save_dir_list, required_strings, edit_existing_defaults):
    """
    Edit filenames in the edit_dir, then save them to the repo dir. Overwrite existing files of same name in
    each case. Filenames must have required_string to be edited
    :param edit_dir: dir path with files to edit
    :type edit_dir: str
    :param save_dir_list: list of dir paths in which to save output
    :type save_dir_list: list
    :param required_strings: lsit of possible strings that must be in filename to edit
    :type required_strings: list
    :param edit_existing_defaults: if true, edit files with no spaces as well as with spaces
    :type edit_existing_defaults: bool
    :return: void
    :rtype:
    """
    init_files = [x for x in os.listdir(edit_dir) if x.endswith('.workflow')]
    filepaths_to_copy = []
    for file in init_files:
        for required_string in required_strings:
            if required_string in file:
                # edit file and save
                splits = os.path.splitext(file)[0].split(' ')
                if not edit_existing_defaults:
                    if len(splits) == 1:
                        # this is not an update file (either a default or has already been overwritten)
                        continue
                new_filename = os.path.join(edit_dir, splits[0] + os.path.splitext(file)[1])
                print('copying workflow {}'.format(new_filename))

                # edit the file to change the saved filename comment at the top
                stripped_filename = os.path.splitext(os.path.basename(new_filename))[0]
                edit_fileheader(os.path.join(edit_dir, file), stripped_filename)

                # move the file
                shutil.move(os.path.join(edit_dir, file), new_filename)
                filepaths_to_copy.append(new_filename)
                break

    # copy to final dir
    for file in filepaths_to_copy:
        for save_dir in save_dir_list:
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
            elif line.startswith("# Please"):
                continue
            elif line.startswith('# In Windows'):
                continue
            # don't write database paths to the built-ins
            elif line.startswith('database.db-path'):
                continue
            else:
                output.append(line)

    with open(workflow_file, 'w') as writefile:
        for line in output:
            writefile.write(line)


if __name__ == '__main__':
    main(WORKFLOW_DIR, REPO_DIRS, REQUIRED_STRINGS, EDIT_EXISTING_DEFAULTS)
