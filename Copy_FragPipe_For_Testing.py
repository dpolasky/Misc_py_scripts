"""
convenience script
"""
import os
import pathlib
import re
import shutil
import update_Fragpipe_Shortcut

# FRAGPIPE_REPO = r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\build\install\fragpipe"
FRAGPIPE_REPO = r"C:\Users\dpolasky\Repositories\FragPipe\MSFragger-GUI\build\install"
MSFRAGGER_DIR = r"C:\Users\dpolasky\Repositories\MSFragger\target"

# TEST_DIR = r"Z:\dpolasky\projects\_BuildTests\tools"
# SKIP_VERSION = False
TEST_DIR = r"Z:\dpolasky\tools\_FragPipes\a_current"
SKIP_VERSION = True
# COPY_MSF_TOO = True
COPY_MSF_TOO = False
TOOLS_DIR = r"Z:\dpolasky\tools"


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


def get_version_new(fragpipe_path):
    """
    get version from new FragPipe, where it is printed right in the path
    """
    pattern = re.compile(r"(fragpipe-[\d.]+-build[\d]+)")
    match = re.search(pattern, fragpipe_path)
    return match.group(1)


def main():
    """

    :return:
    :rtype:
    """
    fragpipe_bin_path = update_Fragpipe_Shortcut.find_fragpipe_bin(FRAGPIPE_REPO)
    fragpipe_dir_path = pathlib.Path(fragpipe_bin_path).parent.parent

    if COPY_MSF_TOO:
        msf_files = [os.path.join(MSFRAGGER_DIR, x) for x in os.listdir(MSFRAGGER_DIR) if 'msfragger' in x and 'proguard' not in x and 'original' not in x]
        msf_src = pathlib.Path(msf_files[0])
        msf_dest = pathlib.Path(TOOLS_DIR, os.path.basename(msf_src))
        print('copying {} to {}'.format(msf_src, msf_dest))
        shutil.copy(msf_src, msf_dest)

    version = get_version_new(fragpipe_bin_path)
    if SKIP_VERSION:
        copy_path = pathlib.Path(TEST_DIR)
    else:
        copy_path = pathlib.Path(TEST_DIR) / version
    print('copying...')
    if os.path.exists(copy_path):
        shutil.rmtree(copy_path)
    shutil.copytree(fragpipe_dir_path, copy_path)
    print('done!')


if __name__ == '__main__':
    main()
