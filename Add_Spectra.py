"""
quick script to add one spectrum to another.
"""

MGF_PATH1 = r"C:\Users\dpolasky\Documents\logs_misc\22032.mgf"
MGF_PATH2 = r"C:\Users\dpolasky\Documents\logs_misc\19774.mgf"
OUT = r"C:\Users\dpolasky\Documents\logs_misc\combined.mgf"
PPM_TOL = 20


def read_mgf(mgf_path):
    """
    read an mgf and return a list of spectra, where each spectrum is a list of lines
    :param mgf_path:
    :type mgf_path:
    :return:
    :rtype:
    """
    spectra = []
    with open(mgf_path, 'r') as readfile:
        current_spectrum = []
        for line in readfile:
            if line.strip() == "BEGIN IONS":
                current_spectrum = [line]
            elif line.strip() == "END IONS":
                current_spectrum.append(line)
                spectra.append(current_spectrum)
            else:
                current_spectrum.append(line)
    return spectra


def extract_peaks(spectrum):
    """
    Extract m/z and intensity pairs from a spectrum (list of lines).

    :param spectrum: List of lines representing a spectrum
    :return: List of tuples (m/z, intensity)
    """
    peaks = []
    for line in spectrum:
        line = line.strip()
        # Skip header lines and empty lines
        if line.startswith('BEGIN') or line.startswith('END') or line.startswith('TITLE') or \
           line.startswith('RTINSECONDS') or line.startswith('PEPMASS') or line.startswith('CHARGE') or \
           not line or '=' in line:
            continue
        # Parse m/z and intensity
        parts = line.split()
        if len(parts) >= 2:
            try:
                mz = float(parts[0])
                intensity = float(parts[1])
                peaks.append((mz, intensity))
            except ValueError:
                continue
    return peaks


def calculate_ppm_tolerance(mz, ppm):
    """
    Calculate the absolute mass tolerance for a given m/z and PPM tolerance.

    :param mz: The m/z value
    :param ppm: The PPM tolerance
    :return: The absolute tolerance
    """
    return (mz * ppm) / 1e6


def add_spectra(spectra1, spectra2, ppm_tol=PPM_TOL):
    """
    Add two lists of spectra together, combining intensities of peaks within ppm_tol.

    :param spectra1: First list of spectra (each spectrum is a list of lines)
    :param spectra2: Second list of spectra (each spectrum is a list of lines)
    :param ppm_tol: PPM tolerance for matching peaks
    :return: List of combined spectra
    """
    combined_spectra = []

    # Assume we're combining spectra pairwise (or all into one)
    # For simplicity, let's combine all spectra from both lists into a single spectrum
    all_peaks = []

    # Extract peaks from all spectra in both lists
    for spectrum in spectra1:
        all_peaks.extend(extract_peaks(spectrum))

    for spectrum in spectra2:
        all_peaks.extend(extract_peaks(spectrum))

    # Sort peaks by m/z
    all_peaks.sort(key=lambda x: x[0])

    # Combine peaks within PPM tolerance
    combined_peaks = []
    if not all_peaks:
        return combined_spectra

    current_mz = all_peaks[0][0]
    current_intensity = all_peaks[0][1]
    peak_group = [all_peaks[0]]

    for i in range(1, len(all_peaks)):
        mz, intensity = all_peaks[i]
        tolerance = calculate_ppm_tolerance(current_mz, ppm_tol)

        # Check if this peak is within tolerance of the current group
        if abs(mz - current_mz) <= tolerance:
            # Add to current group
            peak_group.append((mz, intensity))
            current_intensity += intensity
        else:
            # Finalize current group (use weighted average for m/z)
            total_intensity = sum(p[1] for p in peak_group)
            weighted_mz = sum(p[0] * p[1] for p in peak_group) / total_intensity if total_intensity > 0 else current_mz
            combined_peaks.append((weighted_mz, total_intensity))

            # Start new group
            current_mz = mz
            current_intensity = intensity
            peak_group = [(mz, intensity)]

    # Add the last group
    if peak_group:
        total_intensity = sum(p[1] for p in peak_group)
        weighted_mz = sum(p[0] * p[1] for p in peak_group) / total_intensity if total_intensity > 0 else current_mz
        combined_peaks.append((weighted_mz, total_intensity))

    # Create a new spectrum with the combined peaks
    combined_spectrum = ["BEGIN IONS\n", "TITLE=Combined Spectrum\n"]
    for mz, intensity in combined_peaks:
        combined_spectrum.append(f"{mz:.6f} {intensity:.2f}\n")
    combined_spectrum.append("END IONS\n")

    combined_spectra.append(combined_spectrum)

    return combined_spectra


def print_java_arrays(peaks, spectrum_name):
    """
    Print Java array initialization strings for m/z and intensity values.

    :param peaks: List of tuples (m/z, intensity)
    :param spectrum_name: Name/label for the spectrum
    """
    mz_values = [str(peak[0]) + 'f' for peak in peaks]
    intensity_values = [str(peak[1]) + 'f' for peak in peaks]

    print(f"\n// {spectrum_name} - m/z values")
    print(f"float[] mz_{spectrum_name.replace(' ', '_').replace('-', '_')} = {{{', '.join(mz_values)}}};")

    print(f"\n// {spectrum_name} - intensity values")
    print(f"float[] intensity_{spectrum_name.replace(' ', '_').replace('-', '_')} = {{{', '.join(intensity_values)}}};")


def main():
    spectra1 = read_mgf(MGF_PATH1)
    spectra2 = read_mgf(MGF_PATH2)

    # Print Java arrays for spectrum 1
    if spectra1:
        peaks1 = extract_peaks(spectra1[0])
        print_java_arrays(peaks1, "spectrum1")

    # Print Java arrays for spectrum 2
    if spectra2:
        peaks2 = extract_peaks(spectra2[0])
        print_java_arrays(peaks2, "spectrum2")

    # Combine spectra
    combined_spectra = add_spectra(spectra1, spectra2)

    # Print Java arrays for combined spectrum
    if combined_spectra:
        combined_peaks = extract_peaks(combined_spectra[0])
        print_java_arrays(combined_peaks, "combined")

    # Write combined spectrum to file
    with open(OUT, 'w') as writefile:
        for spectrum in combined_spectra:
            for line in spectrum:
                writefile.write(line)


if __name__ == '__main__':
    main()
