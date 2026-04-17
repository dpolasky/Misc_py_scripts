"""
convenience script for version bumping
"""
import os
import re
import shutil
import subprocess

# WHICH_TOOLS = ['fragpipe']
# WHICH_TOOLS = ['ptms']
# WHICH_TOOLS = ['msfragger']
WHICH_TOOLS = ['batmass']

AUTO_COMMIT = True
COPY_TO_FRAGPIPE = True

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

FRAGPIPE_COPY_PATH = r"C:\Users\dpolasky\FragPipe\tools"
PTMS_FRAGPIPE_LOCS = [r"C:\Users\dpolasky\FragPipe\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\cmd\CmdPtmshepherd.java"]
BATMASS_FRAGPIPE_LOCS = [r"C:\Users\dpolasky\FragPipe\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\cmd\ToolingUtils.java",
                         r"C:\Users\dpolasky\FragPipe\FragPipe-GUI\build.gradle"]

PTMS_BUILD_DIR = r"C:\Users\dpolasky\Repositories\PTM-Shepherd"
PTMS_GRADLE_TASK = "shadowJar"

BATMASS_BUILD_DIR = r"C:\Users\dpolasky\Repositories\batmass-io\batmass-io-java\batmass-io"
BATMASS_GRADLE_TASK = "shadowJar"


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


def stage_and_commit(locs, version):
    """Stage all files in locs and create a git commit with the bumped version."""
    cwd = os.path.dirname(locs[0])
    for f in locs:
        subprocess.run(['git', 'add', f], cwd=cwd, check=True)
    subprocess.run(['git', 'commit', '-m', 'Bump to {}'.format(version)], cwd=cwd, check=True)


# ---------------------------------------------------------------------------
# Per-tool bump functions — each returns the new version string
# ---------------------------------------------------------------------------

def bump_fragpipe():
    new_version = None
    for file in FRAGPIPE_LOCS:
        if 'Bundle.properties' in file:
            def process(line):
                nonlocal new_version
                if 'gui.version=' not in line:
                    return line
                splits = line.split('=')
                new_num, parts = get_new_version_num(splits[1], FRAGPIPE_STR)
                new_version = '{}{}{}'.format(parts[0], FRAGPIPE_STR, new_num)
                return splits[0] + '={}\n'.format(new_version)
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

    return new_version


def bump_ptms():
    """PTM-Shepherd uses plain dotted versions (e.g. 3.0.14); bump the patch component."""
    new_version = None
    for file in PTMS_LOCS:
        if file.endswith('.java'):
            def process(line):
                nonlocal new_version
                m = re.match(r'(\s*public static final String version = ")([\d.]+)(";)', line)
                if not m:
                    return line
                new_version = bump_patch_version(m.group(2))
                return m.group(1) + new_version + m.group(3) + '\n'
            edit_file(file, process)

        elif 'build.gradle' in file:
            def process(line):
                m = re.match(r"(version = ')([\d.]+)(')", line)
                if not m:
                    return line
                new_ver = bump_patch_version(m.group(2))
                return m.group(1) + new_ver + m.group(3) + '\n'
            edit_file(file, process)

    return new_version


def bump_msfragger():
    new_version = None
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
                    new_version = '{}{}{}'.format(parts[0], MSFRAGGER_STR, new_num)
                    line = line.replace(version_str, new_version)
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

    return new_version


def bump_batmass():
    """Batmass uses plain dotted versions (e.g. 1.36.10); bump the patch component."""
    new_version = None
    for file in BATMASS_LOCS:
        if file.endswith('.java'):
            def process(line):
                nonlocal new_version
                m = re.match(r'(\s*public static final String version = ")([\d.]+)(";)', line)
                if not m:
                    return line
                new_version = bump_patch_version(m.group(2))
                return m.group(1) + new_version + m.group(3) + '\n'
            edit_file(file, process)

        elif 'build.gradle' in file:
            def process(line):
                m = re.match(r"(version = ')([\d.]+)(')", line)
                if not m:
                    return line
                new_ver = bump_patch_version(m.group(2))
                return m.group(1) + new_ver + m.group(3) + '\n'
            edit_file(file, process)

    return new_version


# ---------------------------------------------------------------------------
# Build, copy, and FragPipe reference update helpers
# ---------------------------------------------------------------------------

def gradle_build(build_dir, task):
    """Run a gradle task in build_dir using the local gradle wrapper."""
    gradlew = os.path.join(build_dir, 'gradlew.bat')
    subprocess.run([gradlew, task], cwd=build_dir, check=True)


def copy_jar_to_fragpipe(build_dir, jar_name):
    """Copy the built jar from build/libs to the FragPipe tools directory."""
    src = os.path.join(build_dir, 'build', 'libs', jar_name)
    dst = os.path.join(FRAGPIPE_COPY_PATH, jar_name)
    shutil.copy2(src, dst)
    print('Copied {} -> {}'.format(src, dst))


def update_fragpipe_ptms(new_version):
    """Update SHEPHERD_VERSION in CmdPtmshepherd.java to new_version."""
    for file in PTMS_FRAGPIPE_LOCS:
        def process(line):
            m = re.match(r'(\s*public static final String SHEPHERD_VERSION = ")([\d.]+)(";)', line)
            if not m:
                return line
            return m.group(1) + new_version + m.group(3) + '\n'
        edit_file(file, process)


def update_fragpipe_batmass(new_version):
    """Update batmass-io jar references in ToolingUtils.java and FragPipe's build.gradle."""
    for file in BATMASS_FRAGPIPE_LOCS:
        if file.endswith('.java'):
            def process(line):
                m = re.match(r'(\s*public static final String BATMASS_IO_JAR = "batmass-io-)([\d.]+)(\.jar";)', line)
                if not m:
                    return line
                return m.group(1) + new_version + m.group(3) + '\n'
            edit_file(file, process)
        elif 'build.gradle' in file:
            def process(line):
                return re.sub(
                    r'(implementation files\("\.\./tools/batmass-io-)[\d.]+(\.jar"\))',
                    lambda m: m.group(1) + new_version + m.group(2),
                    line
                )
            edit_file(file, process)


# ---------------------------------------------------------------------------

TOOL_LOCS = {
    'fragpipe': FRAGPIPE_LOCS,
    'ptms': PTMS_LOCS,
    'msfragger': MSFRAGGER_LOCS,
    'batmass': BATMASS_LOCS,
}

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
            new_ver = fn()
            if not new_ver:
                print('Warning: could not determine new version for {}; skipping remaining steps'.format(name))
                continue
            if AUTO_COMMIT:
                stage_and_commit(TOOL_LOCS[name], new_ver)
            if COPY_TO_FRAGPIPE:
                if name == 'ptms':
                    gradle_build(PTMS_BUILD_DIR, PTMS_GRADLE_TASK)
                    copy_jar_to_fragpipe(PTMS_BUILD_DIR, 'ptmshepherd-{}.jar'.format(new_ver))
                    update_fragpipe_ptms(new_ver)
                elif name == 'batmass':
                    gradle_build(BATMASS_BUILD_DIR, BATMASS_GRADLE_TASK)
                    copy_jar_to_fragpipe(BATMASS_BUILD_DIR, 'batmass-io-{}.jar'.format(new_ver))
                    update_fragpipe_batmass(new_ver)
        else:
            print('invalid tool: {}'.format(name))
