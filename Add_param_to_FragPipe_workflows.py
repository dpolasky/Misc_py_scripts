"""
Similar to update_fragpipe_workflows.py, but for adding a new param to all workflows with a set default value,
rather than adding specified values of a param (done manually in the GUI) to specific workflows.
"""
import os

REPO_DIRS = [r"C:\Users\dpolasky\Repositories\FragPipe\FragPipe-GUI\workflows",
             r"C:\Users\dpolasky\Repositories\FragPipe\FragPipe-GUI\src\resources\workflows"]

NEW_BUILD_VERSION = '23.0-build7'

# dict of tool name: [param = value]. NO SPACES around '='
# NEW_PARAMS = {'fpop': ['coadaptr.fpop.run-fpop-coadaptr=false',
#                        'coadaptr.fpop.fpop_masses=']
#               }
NEW_PARAMS = {}

# REMOVE_PARAMS = ['msfragger.mass_offset_file']          # list of full param names to remove
REMOVE_PARAMS = ['speclibgen.easypqp.ignore_unannotated']
# REMOVE_PARAMS = []

# NEW_PARAMS = {'ptmshepherd': ['remove_glycan_delta_mass=true']}       # dict of tool name: [param = value]. NO SPACES around '='
# NEW_PARAMS = {
#     'fpop': [
#         'fpop-tmt=false',
#         'label_control=',
#         'label_fpop=',
#         'region_size=1',
#         'run-fpop=false',
#         'subtract-control=false'
#     ],
#     'msfragger': ['output_report_topN_wwa=5'],
#     'tmtintegrator': ['abn_type=0'],
#     'workflow': ['misc.save-sdrf=true']
# }
# 'ptmshepherd':
#     ['prob_dhexOx=2,0.5,0.1',
#      'prob_dhexY=2,0.5',
#      'prob_neuacOx=2,0.05,0.2',
#      'prob_neugcOx=2,0.05,0.2',
#      'prob_phosphoOx=2,0.05,0.2',
#      'prob_regY=5,0.5',
#      'prob_sulfoOx=2,0.05,0.2']}
# NEW_PARAMS = {'opair': ['activation1=HCD',
#                         'activation2=ETD',
#                         'glyco_db=',
#                         'max_glycans=4',
#                         'max_isotope_error=2',
#                         'min_isotope_error=0',
#                         'ms1_tol=20',
#                         'ms2_tol=20',
#                         'reverse_scan_order=false',
#                         'run-opair=false',
#                         'single_scan_type=false']}


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


# def edit_params(file, new_param_dict):
#     """
#
#     :param file:
#     :type file:
#     :param new_param_dict:
#     :type new_param_dict:
#     :return:
#     :rtype:
#     """
#     output = []
#     tool_outputs = {}
#     with open(file, 'r') as readfile:
#         for line in list(readfile):
#             if '.' in line:
#                 # tool-specific line
#                 splits = line.split('.', 1)
#                 if splits[0] in tool_outputs.keys():
#                     tool_outputs[splits[0]].append(splits[1])
#                 else:
#                     tool_outputs[splits[0]] = [splits[1]]
#             else:
#                 # headers
#                 output.append(line)
#
#     # add new params and sort alphabetically within tools
#     for tool_name, param in new_param_dict.items():
#         tool_outputs[tool_name].append(param)
#
#     for tool_name, param_list in tool_outputs.items():
#         for param in sorted(param_list):
#             output.append('{}.{}'.format(tool_name, param))
#
#     with open(file, 'w') as writefile:
#         for line in output:
#             writefile.write(line)


def edit_params(file, new_param_dict, remove_param_list):
    """

    :param file: file to edit
    :type file: str
    :param new_param_dict: dict of tool name: [param = value]
    :type new_param_dict: dict
    :param remove_param_list: params to remove
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
                param_splits = line.split('=')
                if param_splits[0] in remove_param_list:
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
    main(REPO_DIRS, NEW_PARAMS, REMOVE_PARAMS)
