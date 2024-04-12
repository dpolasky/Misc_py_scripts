"""
given a set of FragPipe results folders, copy all the MSFragger or PP/Perc results and their directory
structure to a provided final result folder to allow for combined protein inference/reports.
Used when not all files can be run together (e.g., mixed IM and non-IM instruments, high/low res, etc)

NOTE: all experiment names must be unique between fragpipe dirs, otherwise results will get overwritten
"""
import tkinter
import tkfilebrowser
import os
import shutil

INPUT = [r"Z:\dpolasky\projects\Glyco\ABRF\Beer_full-dataset\__FraggerResults\2024-04-02_all_closed-semi-highRes-phil",
         r"Z:\dpolasky\projects\Glyco\ABRF\Beer_full-dataset\__FraggerResults\2024-04-02_all_closed-semi-IM",
         r"Z:\dpolasky\projects\Glyco\ABRF\Beer_full-dataset\__FraggerResults\2024-04-02_all_closed-semi-lowRes-phil"
         ]
OUTPUT = r"Z:\dpolasky\projects\Glyco\ABRF\Beer_full-dataset\__FraggerResults\2024-04-05_Combined-inference-phil"
COPY_FILETYPE = ".pep.xml"


def move_files(fragpipe_dirs, output_dir):
    """

    :param fragpipe_dirs:
    :type fragpipe_dirs:
    :param output_dir:
    :type output_dir:
    :return:
    :rtype:
    """
    directory_names_to_make = []
    copy_paths = {}
    for fragpipe_dir in fragpipe_dirs:
        for dirpath, dirnames, filenames in os.walk(fragpipe_dir):
            for dirname in dirnames:
                directory_names_to_make.append(dirname)
            for file in filenames:
                if file.endswith(COPY_FILETYPE) and 'combined' not in file:
                    copy_paths[os.path.join(dirpath, file)] = os.path.join(output_dir, os.path.basename(dirpath), file)

    # make experiment dirs
    for dirname in directory_names_to_make:
        copy_dir = os.path.join(output_dir, dirname)
        if not os.path.exists(copy_dir):
            os.makedirs(copy_dir)

    # copy result files
    index = 1
    for src, dst in copy_paths.items():
        print("copying file {} of {}".format(index, len(copy_paths)))
        index += 1
        shutil.copy(src, dst)


if __name__ == '__main__':
    # root = tkinter.Tk()
    # root.withdraw()
    #
    # resultsdirs = tkfilebrowser.askopendirnames()
    move_files(INPUT, OUTPUT)
