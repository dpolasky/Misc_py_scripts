"""
convenience script
"""

import pathlib
import re
import shutil

FRAGPIPE_REPO = r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\build\install\fragpipe"
TEST_DIR = r"Z:\dpolasky\projects\_BuildTests\tools"


def get_version(fragpipe_path):
    """
    find the version
    :param fragpipe_path:
    :type fragpipe_path:
    :return:
    :rtype:
    """
    version_pattern = re.compile(r"CLASSPATH=.+(fragpipe-[\d.]+-build[\d]+)\.jar|CLASSPATH=.+(fragpipe-[\d.]+)\.jar")
    with open(pathlib.Path(fragpipe_path) / 'bin' / 'fragpipe', 'r') as readfile:
        for line in readfile:
            match = re.search(version_pattern, line)
            if match:
                return match.group(1)


def main():
    """

    :return:
    :rtype:
    """
    version = get_version(FRAGPIPE_REPO)
    copy_path = pathlib.Path(TEST_DIR) / version
    print('copying...')
    shutil.copytree(FRAGPIPE_REPO, copy_path)
    print('done!')


if __name__ == '__main__':
    main()
