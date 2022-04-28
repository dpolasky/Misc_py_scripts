"""
Similar to update_fragpipe_workflows.py, but for adding a new param to all workflows with a set default value,
rather than adding specified values of a param (done manually in the GUI) to specific workflows.
"""
import os

REPO_DIRS = [r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\resources\workflows",
             r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\workflows"]
NEW_PARAMS = {'msfragger': ['activation_types=all']}       # dict of tool name: [param = value]. NO SPACES around '='


def main(repo_dirs, new_param_dict):
    """
    Edit filenames in the edit_dir, then save them to the repo dir. Overwrite existing files of same name in
    each case. Filenames must have required_string to be edited
    :param repo_dirs: list of dir paths in which to save output
    :type repo_dirs: list
    :param new_param_dict: dict of tool name: [param = value]
    :type new_param_dict: dict
    :return: void
    :rtype:
    """
    for repo_dir in repo_dirs:
        init_files = [os.path.join(repo_dir, x) for x in os.listdir(repo_dir) if x.endswith('.workflow')]
        filepaths_to_copy = []
        for file in init_files:
            # edit file and save
            print('editing workflow {}'.format(file))
            edit_params(file, new_param_dict)


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


def edit_params(file, new_param_dict):
    """

    :param file: file to edit
    :type file: str
    :param new_param_dict: dict of tool name: [param = value]
    :type new_param_dict: dict
    :return: void
    :rtype:
    """
    output = []
    current_file_copy = {k: [x for x in v] for k, v in new_param_dict.items()}      # deep copy
    with open(file, 'r') as readfile:
        for line in list(readfile):
            skip_append = False
            if '.' in line:
                # tool-specific line
                tool_splits = line.split('.', 1)
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
            if not skip_append:
                output.append(line)

    with open(file, 'w') as writefile:
        for line in output:
            writefile.write(line)


if __name__ == '__main__':
    main(REPO_DIRS, NEW_PARAMS)
