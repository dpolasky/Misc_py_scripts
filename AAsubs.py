

from pyteomics import mass


AAs = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']


def get_aa_substitutions():
    aa_subs = {}
    for aa1 in AAs:
        for aa2 in AAs:
            if aa1 != aa2:
                massdiff = mass.fast_mass(sequence=aa2, charge=0) - mass.fast_mass(sequence=aa1, charge=0)
                aa_subs[(aa1, aa2)] = massdiff
    return aa_subs


if __name__ == '__main__':
    substitutions = get_aa_substitutions()
    for aa_pair, mass_diff in substitutions.items():
        print(f"{aa_pair[0]}\t{aa_pair[1]}\t{mass_diff:.4f} Da")
