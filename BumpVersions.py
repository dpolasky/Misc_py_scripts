"""
convenience script for version bumping
"""
import os
import re
import shutil
import subprocess

# WHICH_TOOLS = ['fragpipe']
# WHICH_TOOLS = ['ptms']
# WHICH_TOOLS = ['glycoshepherd']
# WHICH_TOOLS = ['msfragger']
# WHICH_TOOLS = ['batmass']
# WHICH_TOOLS = ['glycoreporter']
WHICH_TOOLS = ['fragviz']

AUTO_COMMIT = True
COPY_TO_FRAGPIPE = True
# COPY_TO_FRAGPIPE = False

FRAGPIPE_LOCS = [
    r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\fragpipe-installer.iss",
    r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\Bundle.properties",
    r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\build.gradle",
]
FRAGPIPE_STR = "build"
PTMS_LOCS = [
    r"C:\Users\dpolasky\Repositories\PTM-Shepherd\src\edu\umich\andykong\ptmshepherd\PTMShepherd.java",
    r"C:\Users\dpolasky\Repositories\PTM-Shepherd\build.gradle",
]
GLYCOSHEP_LOCS = [
    r"C:\Users\dpolasky\Repositories\GlycoShepherd\src\glycoshepherd\GlycoShepherd.java",
    r"C:\Users\dpolasky\Repositories\GlycoShepherd\build.gradle",
]
GLYCOREPORTER_LOCS = [
    r"C:\Users\dpolasky\Repositories\GlycoReporter\build.gradle",
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
FRAGVIZ_LOCS = [r"C:\Users\dpolasky\Repositories\FragViz\src-tauri\Cargo.lock",
                r"C:\Users\dpolasky\Repositories\FragViz\src-tauri\Cargo.toml",
                r"C:\Users\dpolasky\Repositories\FragViz\src-tauri\tauri.conf.json"
                ]

FRAGPIPE_COPY_PATH = r"C:\Users\dpolasky\Repositories\FragPipe-dev\tools"
PTMS_FRAGPIPE_LOCS = [r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\cmd\CmdPtmshepherd.java"]
GLYCOSHEP_FRAGPIPE_LOCS = [r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\cmd\CmdGlycoShepherd.java"]
GLYCOREPORTER_FRAGPIPE_LOCS = [r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\cmd\CmdGlycoReporter.java"]
BATMASS_FRAGPIPE_LOCS = [r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\src\main\java\org\nesvilab\fragpipe\cmd\ToolingUtils.java",
                         r"C:\Users\dpolasky\Repositories\FragPipe-dev\FragPipe-GUI\build.gradle"]

PTMS_BUILD_DIR = r"C:\Users\dpolasky\Repositories\PTM-Shepherd"
PTMS_GRADLE_TASK = "packageNoDeps"

BATMASS_BUILD_DIR = r"C:\Users\dpolasky\Repositories\batmass-io\batmass-io-java\batmass-io"
BATMASS_GRADLE_TASK = "shadowJar"

GLYCO_BUILD_DIR = r"C:\Users\dpolasky\Repositories\GlycoShepherd"
GLYCOSHEP_GRADLE_TASK = "packageNoDeps"

GLYCOREPORTER_BUILD_DIR = r"C:\Users\dpolasky\Repositories\GlycoReporter"
GLYCOREPORTER_GRADLE_TASK = "packageNoDeps"

FRAGVIZ_BUILD_DIR = r"C:\Users\dpolasky\Repositories\FragViz"
FRAGVIZ_FRAGPIPE_DIR = r"C:\Users\dpolasky\Repositories\FragPipe-dev\tools\fragviz"


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


def bump_fragviz():
    new_version = None
    for file in FRAGVIZ_LOCS:
        def process(line):
            nonlocal new_version
            m = re.match(r'(\s*\"version\": \")([\d.]+)(\",)', line)
            if not m:
                return line
            new_version = bump_patch_version(m.group(2))
            return m.group(1) + new_version + m.group(3) + '\n'
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


def bump_glycoshepherd():
    """GlycoShepherd uses plain dotted versions (e.g. 1.0.0); bump the patch component."""
    new_version = None
    for file in GLYCOSHEP_LOCS:
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


def bump_glycoreporter():
    """GlycoReporter uses plain dotted versions (e.g. 1.0.0); bump the patch component."""
    new_version = None
    for file in GLYCOREPORTER_LOCS:
        # if file.endswith('.java'):
        #     def process(line):
        #         nonlocal new_version
        #         m = re.match(r'(\s*public static final String version = ")([\d.]+)(";)', line)
        #         if not m:
        #             return line
        #         new_version = bump_patch_version(m.group(2))
        #         return m.group(1) + new_version + m.group(3) + '\n'
        #     edit_file(file, process)
        if 'build.gradle' in file:
            def process(line):
                nonlocal new_version
                m = re.match(r"(version = ')([\d.]+)(')", line)
                if not m:
                    return line
                new_version = bump_patch_version(m.group(2))
                return m.group(1) + new_version + m.group(3) + '\n'
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
    # Derive the base name (without version) to find and delete previous versions.
    # Jar names are expected to follow the pattern: <base>-<version>.jar
    # e.g. 'ptmshepherd-2.1.0.jar' -> base prefix is 'ptmshepherd-'
    jar_basename = jar_name[:-4]  # strip '.jar'
    parts = jar_basename.rsplit('-', 1)
    base_prefix = parts[0] + '-' if len(parts) == 2 else jar_basename
    for existing in os.listdir(FRAGPIPE_COPY_PATH):
        if existing.startswith(base_prefix) and existing.endswith('.jar') and existing != jar_name:
            old_path = os.path.join(FRAGPIPE_COPY_PATH, existing)
            os.remove(old_path)
            print('Deleted previous version: {}'.format(old_path))
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


def update_fragpipe_glycoshepherd(new_version):
    """Update GLYCOSHEPHERD_VERSION in CmdGlycoshepherd.java to new_version."""
    for file in GLYCOSHEP_FRAGPIPE_LOCS:
        def process(line):
            m = re.match(r'(\s*public static final String GLYCOSHEPHERD_VERSION = ")([\d.]+)(";)', line)
            if not m:
                return line
            return m.group(1) + new_version + m.group(3) + '\n'
        edit_file(file, process)


def update_fragpipe_glycoreporter(new_version):
    """Update GLYCOREPORTER_VERSION in CmdGlycoReporter.java to new_version."""
    for file in GLYCOREPORTER_FRAGPIPE_LOCS:
        def process(line):
            m = re.match(r'(\s*public static final String GLYCOREPORTER_VERSION = ")([\d.]+)(";)', line)
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


def build_fragviz():
    """Run FragViz's build.bat to produce the Windows (native) and Linux (via WSL) release binaries."""
    build_script = os.path.join(FRAGVIZ_BUILD_DIR, 'build.bat')
    subprocess.run([build_script], cwd=FRAGVIZ_BUILD_DIR, check=True)


def update_fragpipe_fragviz():
    """Copy the built FragViz Windows/Linux binaries into FragPipe's tools/fragviz directories."""
    windows_src = os.path.join(FRAGVIZ_BUILD_DIR, 'src-tauri', 'target', 'release', 'fragviz.exe')
    windows_dst = os.path.join(FRAGVIZ_FRAGPIPE_DIR, 'windows', 'fragviz-windows-x86_64.exe')
    if os.path.isfile(windows_src):
        shutil.copy2(windows_src, windows_dst)
        print('Copied {} -> {}'.format(windows_src, windows_dst))
    else:
        print('Warning: Windows FragViz binary not found at {}; skipping copy'.format(windows_src))

    linux_src = os.path.join(FRAGVIZ_BUILD_DIR, 'src-tauri', 'target', 'x86_64-unknown-linux-gnu', 'release', 'fragviz')
    linux_dst = os.path.join(FRAGVIZ_FRAGPIPE_DIR, 'linux', 'fragviz-linux-x86_64')
    if os.path.isfile(linux_src):
        shutil.copy2(linux_src, linux_dst)
        print('Copied {} -> {}'.format(linux_src, linux_dst))
    else:
        print('Warning: Linux FragViz binary not found at {} (WSL build may not be set up); skipping copy'.format(linux_src))


# ---------------------------------------------------------------------------

TOOL_LOCS = {
    'fragpipe': FRAGPIPE_LOCS,
    'ptms': PTMS_LOCS,
    'msfragger': MSFRAGGER_LOCS,
    'batmass': BATMASS_LOCS,
    'glycoshepherd': GLYCOSHEP_LOCS,
    'glycoreporter': GLYCOREPORTER_LOCS,
    'fragviz': FRAGVIZ_LOCS,
}

if __name__ == '__main__':
    dispatch = {
        'fragpipe': bump_fragpipe,
        'ptms': bump_ptms,
        'msfragger': bump_msfragger,
        'batmass': bump_batmass,
        'glycoshepherd': bump_glycoshepherd,
        'glycoreporter': bump_glycoreporter,
        'fragviz': bump_fragviz,
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
                elif name == 'glycoshepherd':
                    gradle_build(GLYCO_BUILD_DIR, GLYCOSHEP_GRADLE_TASK)
                    copy_jar_to_fragpipe(GLYCO_BUILD_DIR, 'glycoshepherd-{}.jar'.format(new_ver))
                    update_fragpipe_glycoshepherd(new_ver)
                elif name == 'glycoreporter':
                    gradle_build(GLYCOREPORTER_BUILD_DIR, GLYCOREPORTER_GRADLE_TASK)
                    copy_jar_to_fragpipe(GLYCOREPORTER_BUILD_DIR, 'glycoreporter-{}.jar'.format(new_ver))
                    update_fragpipe_glycoreporter(new_ver)
                elif name == 'fragviz':
                    build_fragviz()
                    update_fragpipe_fragviz()
        else:
            print('invalid tool: {}'.format(name))
