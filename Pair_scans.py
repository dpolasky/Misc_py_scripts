"""
Quick script to pair scans from a merged localization .tsv file, edited to have activation inserted as a second column
"""
import os

filepath = r"E:\_Software_Tests\OPair_library-for-MSF\2022-04-18_MSFragger_separate-activation-filtered\2019_09_16_StcEmix_35trig_EThcD25_rep1_MERGED.tsv"
primary = 'HCD'
secondary = 'EThcD'
# max_rt_diff = 0.1       # minutes in localization tsv file
MAX_SCAN_DIFF = 10


def pair_scans(input_file, primary_activation, other_activation):
    """
    pair scans and save output list
    :param input_file:
    :type input_file:
    :param primary_activation:
    :type primary_activation:
    :param other_activation:
    :type other_activation:
    :return:
    :rtype:
    """
    primary_scans_waiting_for_pair = {}     # precursor: (scannum, rt)
    scan_pairs = {}     # primary scannum : secondary scannum
    unpaired_secondary_count = 0
    with open(input_file, 'r') as readfile:
        for line in list(readfile):
            if line.startswith('scannum'):
                continue
            splits = line.split('\t')
            scannum = int(splits[0])
            activation = splits[1]
            precursor = round(float(splits[2]))
            rt = float(splits[3])
            if activation == primary_activation:
                primary_scans_waiting_for_pair[precursor] = scannum
            else:
                # look for possible pair for this secondary scan, assuming primary always comes first
                if precursor in primary_scans_waiting_for_pair.keys():
                    possible_pair_scannum = primary_scans_waiting_for_pair[precursor]
                    if scannum - possible_pair_scannum < MAX_SCAN_DIFF:
                        scan_pairs[possible_pair_scannum] = scannum          # pair the primary scan num with this scan num
                        primary_scans_waiting_for_pair.pop(precursor)   # remove this now that it's found
                else:
                    # no match found, sad
                    unpaired_secondary_count += 1

    # save output
    outpath = os.path.join(os.path.dirname(input_file), '_scan-pairs.tsv')
    with open(outpath, 'w') as outfile:
        for primary_scan, secondary_scan in scan_pairs.items():
            outfile.write('{}\t{}\n'.format(primary_scan, secondary_scan))
    print('unpaired 1o: {}, 2o: {}'.format(len(primary_scans_waiting_for_pair), unpaired_secondary_count))


if __name__ == '__main__':
    pair_scans(filepath, primary, secondary)
