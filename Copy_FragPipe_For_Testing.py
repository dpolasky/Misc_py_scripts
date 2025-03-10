"""
convenience script
"""
import os
import pathlib
import re
import shutil
import sys
import zipfile

import update_Fragpipe_Shortcut
import time

# FRAGPIPE_REPO = r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\FragPipe-GUI\build\install\fragpipe"
FRAGPIPE_REPO = r"C:\Users\dpolasky\Repositories\FragPipe\FragPipe-GUI\build\install"
MSFRAGGER_DIR = r"C:\Users\dpolasky\Repositories\MSFragger\target"
FRAGPIPE_ZIP = r"C:\Users\dpolasky\Repositories\FragPipe\FragPipe-GUI\build\github-release"

# SKIP_VERSION = False
TEST_DIR = r"Z:\dpolasky\projects\_BuildTests\tools"
SKIP_VERSION = True     # new copy method generates the folder w/version name because of the unzip, so no need to detect and name version with py script
# TEST_DIR = r"Z:\dpolasky\tools\_FragPipes\a_current"
# SKIP_VERSION = True
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
    pattern = re.compile(r"([Ff]rag[Pp]ipe-[\d.]+-build\d+)")
    match = re.search(pattern, fragpipe_path)
    return match.group(1)


def zip_directory(source_dir, zip_file_path):
    """Zip the directory at `source_dir` to `zip_file_path`."""
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Use relative path to store in the zip file
                zipf.write(file_path, os.path.relpath(file_path, source_dir))


def unzip_file(zip_file_path, extract_dir):
    """Unzip the `zip_file_path` into the directory `extract_dir`."""
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


def main():
    """

    :return:
    :rtype:
    """
    if COPY_MSF_TOO:
        msf_start = time.time()
        msf_files = [os.path.join(MSFRAGGER_DIR, x) for x in os.listdir(MSFRAGGER_DIR) if 'msfragger' in x and 'proguard' not in x and 'original' not in x]
        msf_src = pathlib.Path(msf_files[0])
        msf_dest = pathlib.Path(TOOLS_DIR, os.path.basename(msf_src))
        print('copying {} to {}'.format(msf_src, msf_dest))
        shutil.copy(msf_src, msf_dest)
        print('done in {:.1f}s'.format(time.time() - msf_start))

    # fragpipe_bin_path = update_Fragpipe_Shortcut.find_fragpipe_bin(FRAGPIPE_REPO)
    # fragpipe_dir_path = pathlib.Path(fragpipe_bin_path).parent.parent

    paths = [os.path.join(FRAGPIPE_ZIP, x) for x in os.listdir(FRAGPIPE_ZIP) if '-jre' not in x]
    if len(paths) != 1:
        print('install dir is empty, need to build FragPipe first')
        sys.exit(1)
    fragpipe_dir_path = str(pathlib.Path(paths[0]))

    version = get_version_new(str(fragpipe_dir_path))
    if SKIP_VERSION:
        copy_path = pathlib.Path(TEST_DIR)
    else:
        copy_path = pathlib.Path(TEST_DIR) / version

    start = time.time()
    if os.path.exists(copy_path):
        print('removing old fragpipe at {}'.format(copy_path))
        shutil.rmtree(copy_path)
        print('deleted in {:.1f}s'.format(time.time() - start))

    # print('copying...')
    # shutil.copytree(fragpipe_dir_path, copy_path, copy_function=shutil.copy2)

    # zip
    # temp = time.time()
    # zip_path = str(fragpipe_dir_path) + '.zip'
    # zip_directory(fragpipe_dir_path, zip_path)
    # print('zipped in {:.1f}s'.format(time.time() - temp))

    zip_path = fragpipe_dir_path

    # copy
    temp = time.time()
    zip_copy_path = str(copy_path) + '.zip'
    shutil.copy2(zip_path, zip_copy_path)
    print('copied in {:.1f}s'.format(time.time() - temp))

    # unzip
    temp = time.time()
    unzip_file(zip_copy_path, copy_path)
    print('unzipped in {:.1f}s'.format(time.time() - temp))

    print('done in {:.1f}s'.format(time.time() - start))


if __name__ == '__main__':
    main()
