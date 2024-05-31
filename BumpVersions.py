"""
convenience script for version bumping
"""

# edit this for use
WHICH_TOOLS = ['fragpipe']
# WHICH_TOOLS = ['ptms']
# WHICH_TOOLS = ['msfragger']


# FRAGPIPE_LOCS = [r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\src\com\dmtavt\fragpipe\Bundle.properties",
#                  r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\src\umich\msfragger\gui\Bundle.properties",
#                  r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\build.gradle"]
FRAGPIPE_LOCS = [r"C:\Users\dpolasky\Repositories\FragPipe\MSFragger-GUI\src\com\dmtavt\fragpipe\Bundle.properties",
                 r"C:\Users\dpolasky\Repositories\FragPipe\MSFragger-GUI\src\umich\msfragger\gui\Bundle.properties",
                 r"C:\Users\dpolasky\Repositories\FragPipe\MSFragger-GUI\build.gradle"]
FRAGPIPE_STR = "build"
# PTMS_LOCS = [r"C:\Users\dpolasky\IdeaProjects\PTM-Shepherd\src\edu\umich\andykong\ptmshepherd\PTMShepherd.java",
#              r"C:\Users\dpolasky\IdeaProjects\PTM-Shepherd\build.gradle"]
PTMS_LOCS = [r"C:\Users\dpolasky\Repositories\PTM-Shepherd\src\edu\umich\andykong\ptmshepherd\PTMShepherd.java",
             r"C:\Users\dpolasky\Repositories\PTM-Shepherd\build.gradle"]
PTMS_STR = "rc"
MSFRAGGER_LOCS = []
MSFRAGGER_STR = "rc"
TMT_INTEGRATOR_LOCS = []


def get_new_version_num(prev_detected_version, build_string):
    """
    Determine the new version number and return it
    :param build_string:
    :type build_string:
    :param prev_detected_version:
    :type prev_detected_version:
    :return:
    :rtype:
    """
    build_splits = prev_detected_version.split(build_string)
    if "\";\n" in build_splits[1]:
        extra = "\";"
    else:
        extra = ""
    new_build_num = int(build_splits[1].replace("\";\n", "")) + 1
    if new_build_num < 10 and '0' in build_splits[1]:
        new_build_num = '0{}'.format(new_build_num)
    return '{}{}'.format(new_build_num, extra), build_splits


def bump_versions(tool_list, build_string):
    """
    Read files and bump versions
    :param build_string:
    :type build_string:
    :param tool_list:
    :type tool_list:
    :return:
    :rtype:
    """
    for file in tool_list:
        # FragPipe
        if 'Bundle.properties' in file:
            output = []
            with open(file, 'r') as readfile:
                for line in list(readfile):
                    if 'gui.version=' in line:
                        splits = line.split('=')
                        new_build_num, build_splits = get_new_version_num(splits[1], build_string)
                        newline = splits[0] + '={}{}{}\n'.format(build_splits[0], build_string, new_build_num)
                    else:
                        newline = line
                    output.append(newline)
            with open(file, 'w') as writefile:
                for line in output:
                    writefile.write(line)
        # FragPipe or PTM-S
        if 'build.gradle' in file:
            output = []
            with open(file, 'r') as readfile:
                for line in list(readfile):
                    if line.startswith('version = '):
                        splits = line.split('=')
                        new_build_num, build_splits = get_new_version_num(splits[1].replace('\'', ''), build_string)
                        newline = splits[0] + '= \'{}{}{}\'\n'.format(build_splits[0].strip(), build_string, new_build_num)
                    else:
                        newline = line
                    output.append(newline)
                with open(file, 'w') as writefile:
                    for line in output:
                        writefile.write(line)
        # PTM-S or MSFragger
        if file.endswith('.java'):
            output = []
            with open(file, 'r') as readfile:
                for line in list(readfile):
                    if "String version = " in line:
                        splits = line.split('=')
                        new_build_num, build_splits = get_new_version_num(splits[1].replace('\'', ''), build_string)
                        newline = splits[0] + '= \"{}{}{}\"\n'.format(build_splits[0].strip(), build_string, new_build_num)
                    else:
                        newline = line
                    output.append(newline)
                with open(file, 'w') as writefile:
                    for line in output:
                        writefile.write(line)


if __name__ == '__main__':
    for name in WHICH_TOOLS:
        if name == 'fragpipe':
            bump_versions(FRAGPIPE_LOCS, FRAGPIPE_STR)
        elif name == 'ptms':
            bump_versions(PTMS_LOCS, PTMS_STR)
        elif name == 'msfragger':
            bump_versions(MSFRAGGER_LOCS, MSFRAGGER_STR)
        else:
            print('invalid tool!')
