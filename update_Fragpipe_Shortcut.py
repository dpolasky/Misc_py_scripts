"""
update my fragpipe shortcut
"""

import os
import sys
import pathlib
from win32com.client import Dispatch

shortcut_path = r"C:\Users\dpolasky\Documents\fragpipe.exe.lnk"
# fragpipe_dir = r"C:\Users\dpolasky\Repositories\FragPipe\FragPipe-GUI\build\install"
fragpipe_dir = r"C:\Users\dpolasky\Repositories\FragPipe\FragPipe-GUI\build\install"


def find_fragpipe_bin(install_dir):
    """
    starting from .../build/install find the new fragpipe.exe
    """
    paths = [os.path.join(install_dir, x) for x in os.listdir(install_dir)]
    if len(paths) != 1:
        print('install dir is empty, need to build FragPipe first')
        sys.exit(1)
    bin_path = pathlib.Path(paths[0]) / 'bin'
    files = [os.path.join(bin_path, x) for x in os.listdir(bin_path) if x.endswith('.exe')]
    if len(files) == 1:
        return files[0]
    else:
        print('install dir is empty or could not find exe file. Do you need to build FragPipe first?')
        sys.exit(1)


def main():
    """
    find the new fragpipe.exe, then create a new shortcut at the location of the old one
    """
    new_fragpipe_path = find_fragpipe_bin(fragpipe_dir)
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = new_fragpipe_path
    shortcut.save()


if __name__ == '__main__':
    main()
