"""
general script for copying FragPipe result folders (e.g., for alternate/rerun while preserving original)
"""

import shutil
import tkinter
import tkfilebrowser

NAME_APPEND = "_fdr-100"


def copy_append_name(result_path, append_string):
    """
    copy a result directory to a new path with the append string added to the pathname
    """
    new_path = result_path + append_string
    print('copying from {} to {}'.format(result_path, new_path))
    shutil.copytree(result_path, new_path)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    folders = tkfilebrowser.askopendirnames()
    for folder in folders:
        copy_append_name(folder, NAME_APPEND)
