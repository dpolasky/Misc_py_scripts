"""
Similar to update_fragpipe_workflows.py, but for adding a new param to all workflows with a set default value,
rather than adding specified values of a param (done manually in the GUI) to specific workflows.
"""
import os

REPO_DIRS = [r"C:\Users\dpolasky\FragPipe\workflows"]
# r"C:\Users\dpolasky\Repositories\FragPipe\FragPipe-GUI\src\resources\workflows"]

NEW_BUILD_VERSION = '23.2-build12'

# lists of new params and remove params
NEW_PARAMS = """mbg.allow_chimeric=false
mbg.expand_db=1
mbg.fdr=0.010
mbg.max_glycan_q=0.01
mbg.max_skips=0
mbg.min_glycans=2
mbg.min_psms=5
mbg.residues_to_add=HexNAc(1),Hex(1),Fuc(1),NeuAc(1),NH4(1),Na(1),Fe(1)
mbg.run-mbg=false
ptmshepherd.annotate_assigned_mods=false
ptmshepherd.glyco_lda=true
ptmshepherd.glyco_lda_features=yscore,oxo,mass
ptmshepherd.use_glycan_fragment_probs=true
ptmshepherd.use_msfragger_localization=false
"""
REMOVE_PARAMS = """ptmshepherd.iterloc_maxEpoch=100
ptmshepherd.iterloc_mode=false
tab-run.delete_calibrated_mzml=false
tmtintegrator.top3_pep=true
"""


# DEPRECATED: dict of tool name: [param = value]. NO SPACES around '='
# NEW_PARAMS = {'fpop': ['coadaptr.fpop.run-fpop-coadaptr=false',
#                        'coadaptr.fpop.fpop_masses=']
#               }
# NEW_PARAMS = {}

# REMOVE_PARAMS = ['msfragger.mass_offset_file']          # list of full param names to remove
# REMOVE_PARAMS = ['speclibgen.easypqp.ignore_unannotated']
# REMOVE_PARAMS = []


def parse_params(param_str, strip_value):
    """
    parse input copied from a workflow file into a dict of tool name: [param = value]
    Input should be like:
        mbg.allow_chimeric=false
        mbg.expand_db=1
        mbg.fdr=0.010
    """
    splits = param_str.split('\n')
    param_dict = {}
    for line in splits:
        if '.' in line:
            tool_splits = line.split('.', 1)
            if strip_value:
                tool_splits[1] = tool_splits[1].split('=')[0]

            if tool_splits[0] in param_dict.keys():
                param_dict[tool_splits[0]].append(tool_splits[1])
            else:
                param_dict[tool_splits[0]] = [tool_splits[1]]
    return param_dict


def main(repo_dirs, new_param_dict, remove_param_list):
    """
    Edit filenames in the edit_dir, then save them to the repo dir. Overwrite existing files of same name in
    each case. Filenames must have required_string to be edited
    :param repo_dirs: list of dir paths in which to save output
    :type repo_dirs: list
    :param new_param_dict: dict of tool name: [param = value]
    :type new_param_dict: dict
    :param remove_param_list: list of params to remove
    :return: void
    :rtype:
    """
    for repo_dir in repo_dirs:
        init_files = [os.path.join(repo_dir, x) for x in os.listdir(repo_dir) if x.endswith('.workflow')]
        filepaths_to_copy = []
        for file in init_files:
            # edit file and save
            print('editing workflow {}'.format(file))
            edit_params(file, new_param_dict, remove_param_list)


def edit_params(file, new_param_dict, remove_param_dict):
    """

    :param file: file to edit
    :type file: str
    :param new_param_dict: dict of tool name: [param = value]
    :type new_param_dict: dict
    :param remove_param_dict: dict of tool name: [param = value]
    :type remove_param_dict: dict
    :return: void
    :rtype:
    """
    output = []
    current_file_copy = {k: [x for x in v] for k, v in new_param_dict.items()}  # deep copy
    tools_found = []
    with open(file, 'r') as readfile:
        for line in list(readfile):
            skip_append = False
            if '.' in line:
                # tool-specific line
                tool_splits = line.split('.', 1)
                tools_found.append(tool_splits[0])

                # check for params to remove
                if tool_splits[0] in remove_param_dict.keys():
                    param_splits = tool_splits[1].split('=')
                    if param_splits[0] in remove_param_dict[tool_splits[0]]:
                        skip_append = True

                # check for adding totally new tool (find insert point)
                for tool_name in current_file_copy.keys():
                    if tool_name not in tools_found:
                        if tool_name < tools_found[-1]:
                            # if we've reached another tool that's alphabetically after this tool, need to insert it above this line
                            new_param_list = [x for x in current_file_copy[tool_name]]
                            for new_param in new_param_list:
                                newline = '{}.{}\n'.format(tool_name, new_param)
                                # remove from insert list when done
                                current_file_copy[tool_name].remove(new_param)
                                output.append(newline)

                if tool_splits[0] in current_file_copy.keys():
                    # check for possible insert point
                    for new_param in current_file_copy[tool_splits[0]]:
                        if new_param.split('=')[0] in tool_splits[1]:
                            # this param is already present! just edit instead of replacing
                            newline = '{}.{}\n'.format(tool_splits[0], new_param)
                            output.append(newline)
                            current_file_copy[tool_splits[0]].remove(new_param)
                            skip_append = True
                        elif new_param < tool_splits[1]:
                            # found alphabetical insert point: insert
                            newline = '{}.{}\n'.format(tool_splits[0], new_param)
                            # remove from insert list when done
                            current_file_copy[tool_splits[0]].remove(new_param)
                            output.append(newline)
                if 'saved-with-ver' in line:
                    newline = line.split('=')[0] + '=' + NEW_BUILD_VERSION
                    output.append(newline)
                    skip_append = True
            if not skip_append:
                output.append(line)

    with open(file, 'w') as writefile:
        for line in output:
            writefile.write(line)


if __name__ == '__main__':
    main(REPO_DIRS, parse_params(NEW_PARAMS, False), parse_params(REMOVE_PARAMS, True))
