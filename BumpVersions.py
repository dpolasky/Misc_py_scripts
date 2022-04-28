"""
convenience script for version bumping
"""
import os

FRAGPIPE_LOCS = [r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\src\com\dmtavt\fragpipe\Bundle.properties",
                 r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\src\umich\msfragger\gui\Bundle.properties",
                 r"C:\Users\dpolasky\GitRepositories\FragPipe\FragPipe\MSFragger-GUI\build.gradle"]
PTMS_LOCS = []
MSFRAGGER_LOCS = []
TMT_INTEGRATOR_LOCS = []

# edit this for use
TOOLS_TO_BUMP = [FRAGPIPE_LOCS]


def bump_versions(tool_list):
    """
    Read files and bump versions
    :param tool_list:
    :type tool_list:
    :return:
    :rtype:
    """
    for tool_loc_list in tool_list:
        for file in tool_loc_list:
            # FragPipe
            if 'Bundle.properties' in file:
                output = []
                with open(file, 'r') as readfile:
                    for line in list(readfile):
                        if 'gui.version=' in line:
                            splits = line.split('=')
                            prev_detected_version = splits[1]
                            build_splits = prev_detected_version.split('build')
                            new_build_num = int(build_splits[1]) + 1
                            newline = splits[0] + '={}build{}\n'.format(build_splits[0], new_build_num)
                        else:
                            newline = line
                        output.append(newline)
                with open(file, 'w') as writefile:
                    for line in output:
                        writefile.write(line)
            # FragPipe
            if 'build.gradle' in file:
                output = []
                with open(file, 'r') as readfile:
                    for line in list(readfile):
                        if 'version = ' in line:
                            splits = line.split('=')
                            prev_detected_version = splits[1].replace('\'', '')
                            build_splits = prev_detected_version.split('build')
                            new_build_num = int(build_splits[1]) + 1
                            newline = splits[0] + '= \'{}build{}\'\n'.format(build_splits[0].strip(), new_build_num)
                        else:
                            newline = line
                        output.append(newline)
                    with open(file, 'w') as writefile:
                        for line in output:
                            writefile.write(line)


if __name__ == '__main__':
    bump_versions(TOOLS_TO_BUMP)
