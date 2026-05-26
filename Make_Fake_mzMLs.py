"""
module to read a psm.tsv and make fake mzML files for each raw file name in the psm.tsv to enable
ptm-shepherd debugging without having the raw data
"""
import os

PSM_FILE = r"C:\_Local\_software-tests\PTMS_tests\2026-05-04_FP2771-testing\psm.tsv"


def parse_psm_rawfiles(psms_file):
    """
    read all the raw filenames from the psm.tsv file
    """
    raw_names = set()
    with open(psms_file) as f:
        for line in f:
            if line.startswith('Spectrum'):
                continue
            parts = line.strip().split('\t')
            spectrum = parts[0]
            raw_name = spectrum.split('.')[0]
            raw_names.add(raw_name)
    return raw_names


def make_fake_files(raw_names, directory):
    """
    make a fake file for each raw file name in the psm.tsv file in the provided directory
    """
    for raw_name in raw_names:
        output_path = os.path.join(directory, raw_name + '.mzML')
        with open(output_path, 'w') as f:
            f.write('This is a fake mzML file for raw file: {}'.format(raw_name))
        print('Made fake mzML file at {}'.format(output_path))


if __name__ == '__main__':
    raws = parse_psm_rawfiles(PSM_FILE)
    make_fake_files(raws, os.path.dirname(PSM_FILE))
