"""
script to find all parameters that are unique in a given MSFragger fragger.params file vs a list of other files.
"""
import os

ROOT_DIR = r"Z:\dpolasky\projects\_BuildTests\_results\2026-03-13_msf-extAA-fix-loops"
INPUT_FILE = r"Z:\dpolasky\projects\_BuildTests\_results\2026-03-13_msf-extAA-fix-loops\Labile_phospho\fraggerLABILE-PHOSPHO.params"


def find_files_from_build_tests(root_dir):
    """
    return a list of all fragger.params files in the given root directory
    """
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'fragger.params':
                all_files.append(os.path.join(root, file))
    return all_files


def parse_param_file(param_file):
    """
    Parse a fragger.params file into a dict of {param_name: full_line}.
    Skips blank lines and comment lines (starting with #).
    """
    params = {}
    with open(param_file, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if '=' in line:
                param_name = line.split('=')[0].strip()
                params[param_name] = line
    return params


def find_unique_params(input_param_file, other_param_file_list):
    """
    Find all params that are unique in the input_param_file from all other param files in the other_param_file_list.
    Prints any parameter line whose value is not shared by ANY of the other param files.
    """
    input_params = parse_param_file(input_param_file)

    # Parse all other param files once
    other_params_list = [parse_param_file(f) for f in other_param_file_list]

    unique_params = []
    for param_name, input_line in input_params.items():
        # Check if any other file has the exact same line for this parameter
        shared = any(
            other_params.get(param_name) == input_line
            for other_params in other_params_list
        )
        if not shared:
            unique_params.append(input_line)

    print(f"Unique parameters in {input_param_file} (not shared by any other file):")
    for line in unique_params:
        print(f"  {line}")
    return unique_params


if __name__ == "__main__":
    param_files = find_files_from_build_tests(ROOT_DIR)
    unique_params = find_unique_params(INPUT_FILE, param_files)
