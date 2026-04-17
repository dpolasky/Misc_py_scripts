"""
convenience script for version bumping
"""
import re

# WHICH_TOOLS = ['fragpipe']
# WHICH_TOOLS = ['ptms']
# WHICH_TOOLS = ['msfragger']
WHICH_TOOLS = ['batmass']

FRAGPIPE_LOCS = [
    r"C:\Users\dpolasky\FragPipe\FragPipe-GUI\fragpipe-installer.iss",
    r"C:\Users\dpolasky\FragPipe\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\Bundle.properties",
    r"C:\Users\dpolasky\FragPipe\FragPipe-GUI\build.gradle",
]
FRAGPIPE_STR = "build"

PTMS_LOCS = [
    r"C:\Users\dpolasky\Repositories\PTM-Shepherd\src\edu\umich\andykong\ptmshepherd\PTMShepherd.java",
    r"C:\Users\dpolasky\Repositories\PTM-Shepherd\build.gradle",
]

MSFRAGGER_LOCS = [
    r"C:\Users\dpolasky\Repositories\MSFragger\pom.xml",
    r"C:\Users\dpolasky\Repositories\MSFragger\src\edu\umich\andykong\msfragger\MSFragger.java",
]
MSFRAGGER_STR = "rc"

BATMASS_LOCS = [
    r"C:\Users\dpolasky\Repositories\batmass-io\batmass-io-java\batmass-io\src\main\java\umich\ms\msfiletoolbox\MsftbxInfo.java",
    r"C:\Users\dpolasky\Repositories\batmass-io\batmass-io-java\batmass-io\build.gradle",
]


def get_new_version_num(prev_detected_version, build_string):
    """Parse a version containing build_string + numeric suffix; return incremented version."""
    if build_string in prev_detected_version:
        build_splits = prev_detected_version.split(build_string)
    else:
        build_splits = ['', prev_detected_version]
    extra = '";' if '";\n' in build_splits[1] else ''
    new_build_num = int(re.sub(r'[\";\n]+', '', build_splits[1])) + 1
    if new_build_num < 10 and '0' in build_splits[1]:
        new_build_num = '0{}'.format(new_build_num)
    return '{}{}'.format(new_build_num, extra), build_splits


def bump_patch_version(version_str):
    """Bump the last numeric component of a dotted version string (e.g. 1.36.10 -> 1.36.11)."""
    parts = version_str.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)


def edit_file(file_path, line_fn):
    """Apply line_fn to every line in file_path and write the result back."""
    with open(file_path, 'r') as f:
        lines = list(f)
    with open(file_path, 'w') as f:
        f.writelines(line_fn(line) for line in lines)


# ---------------------------------------------------------------------------
# Per-tool bump functions
# ---------------------------------------------------------------------------

def bump_fragpipe():
    for file in FRAGPIPE_LOCS:
        if 'Bundle.properties' in file:
            def process(line):
                if 'gui.version=' not in line:
                    return line
                splits = line.split('=')
                new_num, parts = get_new_version_num(splits[1], FRAGPIPE_STR)
                return splits[0] + '={}{}{}\n'.format(parts[0], FRAGPIPE_STR, new_num)
            edit_file(file, process)

        elif 'fragpipe-installer.iss' in file:
            def process(line):
                if '#define AppVersion' not in line:
                    return line
                splits = line.split('AppVersion ')
                new_num, parts = get_new_version_num(splits[1].replace("'", ''), FRAGPIPE_STR)
                return splits[0] + 'AppVersion {}{}{}\"\n'.format(parts[0].strip(), FRAGPIPE_STR, new_num)
            edit_file(file, process)

        elif 'build.gradle' in file:
            def process(line):
                if not line.startswith('version = '):
                    return line
                splits = line.split('=')
                new_num, parts = get_new_version_num(splits[1].replace("'", ''), FRAGPIPE_STR)
                return splits[0] + "= '{}{}{}\'\n".format(parts[0].strip(), FRAGPIPE_STR, new_num)
            edit_file(file, process)


def bump_ptms():
    """PTM-Shepherd uses plain dotted versions (e.g. 3.0.14); bump the patch component."""
    for file in PTMS_LOCS:
        if file.endswith('.java'):
            def process(line):
                m = re.match(r'(\s*public static final String version = ")([\d.]+)(";)', line)
                if not m:
                    return line
                new_ver = bump_patch_version(m.group(2))
                return m.group(1) + new_ver + m.group(3) + '\n'
            edit_file(file, process)

        elif 'build.gradle' in file:
            def process(line):
                m = re.match(r"(version = ')([\d.]+)(')", line)
                if not m:
                    return line
                new_ver = bump_patch_version(m.group(2))
                return m.group(1) + new_ver + m.group(3) + '\n'
            edit_file(file, process)


def bump_msfragger():
    for file in MSFRAGGER_LOCS:
        if file.endswith('pom.xml'):
            with open(file, 'r') as f:
                lines = list(f)
            output = []
            activated = False
            for line in lines:
                if '<version>' in line and activated:
                    version_str = re.search(r'<version>(.*)</version>', line).group(1)
                    new_num, parts = get_new_version_num(version_str, MSFRAGGER_STR)
                    line = line.replace(version_str, '{}{}{}'.format(parts[0], MSFRAGGER_STR, new_num))
                activated = 'msfragger' in line
                output.append(line)
            with open(file, 'w') as f:
                f.writelines(output)

        elif file.endswith('.java'):
            def process(line):
                if 'String version = ' not in line:
                    return line
                splits = line.split('=')
                new_num, parts = get_new_version_num(splits[1].replace("'", ''), MSFRAGGER_STR)
                return splits[0] + '= {}{}{}\n'.format(parts[0].strip(), MSFRAGGER_STR, new_num)
            edit_file(file, process)


def bump_batmass():
    """Batmass uses plain dotted versions (e.g. 1.36.10); bump the patch component."""
    for file in BATMASS_LOCS:
        if file.endswith('.java'):
            def process(line):
                m = re.match(r'(\s*public static final String version = ")([\d.]+)(";)', line)
                if not m:
                    return line
                new_ver = bump_patch_version(m.group(2))
                return m.group(1) + new_ver + m.group(3) + '\n'
            edit_file(file, process)

        elif 'build.gradle' in file:
            def process(line):
                m = re.match(r"(version = ')([\d.]+)(')", line)
                if not m:
                    return line
                new_ver = bump_patch_version(m.group(2))
                return m.group(1) + new_ver + m.group(3) + '\n'
            edit_file(file, process)


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    dispatch = {
        'fragpipe': bump_fragpipe,
        'ptms': bump_ptms,
        'msfragger': bump_msfragger,
        'batmass': bump_batmass,
    }
    for name in WHICH_TOOLS:
        fn = dispatch.get(name)
        if fn:
            fn()
        else:
            print('invalid tool: {}'.format(name))
