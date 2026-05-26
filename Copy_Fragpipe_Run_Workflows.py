"""
script for generating new copies of existing fragpipe workflows for batch runs
"""
import tkinter
from tkinter import filedialog
import shutil


REPLACE_TEXT = {
    # "2026-05-15": "2026-05-19",
    "_fdr5": "_fdr5-gslib"
}


def copy_file(file, replace_text_list):
    """
    replace all the text entries in the filename with the new text and save it as a new file
    """
    original_path = file
    for text in replace_text_list.keys():
        file = file.replace(text, replace_text_list[text])
    print('copying {} to {}'.format(original_path, file))
    shutil.copy(original_path, file)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    files = filedialog.askopenfilenames()
    for f in files:
        copy_file(f, REPLACE_TEXT)
