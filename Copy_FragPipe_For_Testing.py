"""
convenience script
"""
import os
import pathlib
import re
import shutil

FRAGPIPE_REPO = r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\build\install\fragpipe"
# TEST_DIR = r"Z:\dpolasky\projects\_BuildTests\tools"
TEST_DIR = r"Z:\dpolasky\tools\_FragPipes\a_current"
SKIP_VERSION = True


def get_version(fragpipe_path):
    """
    find the version
    :return:
    :rtype:
    """
    version_pattern = re.compile(r"CLASSPATH=.+(fragpipe-[\d.]+-build[\d]+)\.jar|CLASSPATH=.+(fragpipe-[\d.]+)\.jar")
    with open(pathlib.Path(fragpipe_path) / 'bin' / 'fragpipe', 'r') as readfile:
        for line in readfile:
            match = re.search(version_pattern, line)
            if match:
                match1 = match.group(1)
                match2 = match.group(2)
                if match1 is not None:
                    return match1
                else:
                    return match2
    return None


def main():
    """

    :return:
    :rtype:
    """
    version = get_version(FRAGPIPE_REPO)
    if SKIP_VERSION:
        copy_path = pathlib.Path(TEST_DIR)
    else:
        copy_path = pathlib.Path(TEST_DIR) / version
    print('copying...')
    if os.path.exists(copy_path):
        shutil.rmtree(copy_path)
    shutil.copytree(FRAGPIPE_REPO, copy_path)
    print('done!')


if __name__ == '__main__':
    main()
