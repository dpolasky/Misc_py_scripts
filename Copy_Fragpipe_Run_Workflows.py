"""
script for generating new copies of existing fragpipe workflows for batch runs
"""
import tkinter
from tkinter import filedialog
import shutil


REPLACE_TEXT = {
    "_base": ["_HGI-A", "_CPTAC", "_MBG", "_yeast", "_Riley", "_pG2mouse", "_Coon"],
    # "_base": ["_HGI-A", "_CPTAC", "_MBG", "_yeast"],
    # "_mouse": ["_Riley", "_pG2mouse", "_Coon"],
    # "_fdr5": ["_fdr5-gslib"]
}


def copy_file(file, replace_text_list):
    """
    replace all the text entries in the filename with the new text and save it as a new file
    """
    original_path = file
    for text in replace_text_list.keys():
        for new_text in replace_text_list[text]:
            file = original_path
            file = file.replace(text, new_text)
            print('copying {} to {}'.format(original_path, file))
            try:
                shutil.copy(original_path, file)
            except shutil.SameFileError:
                print('warning: unable to edit file {} using replace text {}'.format(original_path, new_text))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames()
    for f in files:
        copy_file(f, REPLACE_TEXT)
