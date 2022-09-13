"""
Glycan type and mass comparisons
"""
import numpy as np
import pandas as pd
import os
from enum import Enum

DIR1 = r"Z:\data\HLA\_Results\Bassani_2021_Proteome_Nglyc_glycFDR"
DIR2 = r"Z:\data\HLA\_Results\Bassani_2021_PXD020079_glycFDR"
GLYCAN_COL = 'Observed Modifications'
GLYCAN_QVAL_COL = 'Glycan q-value'
PEP_COL = 'Peptide'
PROT_COL = 'Protein'
GLYC_QVAL_THR = 0.05
LRP1 = 'sp|Q07954|LRP1_HUMAN'


class GlycanResidue(Enum):
    N = 'HexNAc'
    H = 'Hex'
    F = 'Fucose'
    A = 'NeuAc'
    G = 'NeuGc'
    P = 'Phospho'


class GlycanType(Enum):
    OGlyc = 'OGlycan'
    Other = 'Other'
    HM = 'High Mannose'
    Trunc = 'Truncated'
    Comp = 'Complex/Hybrid'
    NA = 'Not a Glycan'


def mass_compare(psm_df_dict, q_val_threshold, output_dir):
    """
    Plot average glycan mass for each analysis provided
    :param psm_df_dict: dict of analysis name: psm table (as dataframe)
    :type psm_df_dict: dict
    :return: void
    :rtype:
    """
    avg_masses = {}
    for analysis_name, df in psm_df_dict.items():
        # df = df.dropna(subset=['Glycan Score'])
        filtered_df = df.loc[(df[GLYCAN_QVAL_COL] <= q_val_threshold)]
        avg_masses[analysis_name] = np.average(filtered_df[GLYCAN_COL].apply(parse_glycan_mass))

    # save results for plotting
    output_path = os.path.join(output_dir, '_mass-compare.tsv')
    with open(output_path, 'w') as outfile:
        outfile.write('Analysis\tAvg Glycan Mass (Da)\n')
        for analysis_name, mass in avg_masses.items():
            outfile.write('{}\t{:.2f}\n'.format(analysis_name, mass))


def parse_glycan_mass(glycan_str):
    """
    Byonic format only
    :param glycan_str: input string from observed mods
    :type glycan_str: str
    :return: glycan mass
    :rtype: float
    """
    splits = glycan_str.split('%')
    return float(splits[1])


def determine_glycan_type(glycan_str):
    """
    Determine glycan type (from Byonic format)
    Rules:
     - presence of phospho or NeuGc         -> Other
     - HexNAc < 2                           -> OGlycan
     - HexNAc >= 2 and presence of NeuAc    -> Complex/Hybrid
     - HexNAc = 2 & Hex < 5                 -> Trucated
     - HexNAc = 3 & Hex < 4                 -> Truncated
     - HexNAc = 2 and Hex >= 5              -> High Mannose
     - HexNAc > 2 and Hex >= 4              -> Complex/Hybrid
    :param glycan_str:
    :type glycan_str:
    :return:
    :rtype:
    """
    glycan_comp = {}
    splits = glycan_str.split('%')
    if not len(splits) == 2:
        return GlycanType.NA

    glyc_splits = splits[0].strip().split(')')
    for glyc_info in glyc_splits:
        if glyc_info is '':
            continue
        count_split = glyc_info.split('(')
        glycan_comp[count_split[0]] = int(count_split[1])

    # determine type
    if glycan_comp[GlycanResidue.N.value] < 2:
        glyc_type = GlycanType.OGlyc
    elif glycan_comp[GlycanResidue.N.value] == 2:
        if GlycanResidue.P.value in glycan_comp.keys() or GlycanResidue.G.value in glycan_comp.keys():
            glyc_type = GlycanType.Other
        else:
            if GlycanResidue.A.value in glycan_comp.keys():
                glyc_type = GlycanType.Comp
            else:
                if glycan_comp[GlycanResidue.H.value] > 4:
                    glyc_type = GlycanType.HM
                else:
                    glyc_type = GlycanType.Trunc
    else:
        # HexNAc > 2
        if GlycanResidue.P.value in glycan_comp.keys() or GlycanResidue.G.value in glycan_comp.keys():
            glyc_type = GlycanType.Other
        else:
            if glycan_comp[GlycanResidue.N.value] == 3 and glycan_comp[GlycanResidue.H.value] < 4:
                glyc_type = GlycanType.Trunc
            else:
                glyc_type = GlycanType.Comp
    return glyc_type.value


def glycan_type_compare(psm_df_dict, q_val_threshold, output_dir, protein=''):
    """
    Plot bar graph of glycan types for each input psm table
    :param psm_df_dict: dict of analysis name: psm table (as dataframe)
    :type psm_df_dict: dict
    :param q_val_threshold:
    :type q_val_threshold:
    :param output_dir:
    :type output_dir:
    :return: void
    :rtype:
    """
    glycan_types = {}
    for analysis_name, df in psm_df_dict.items():
        glycan_types[analysis_name] = {}
        filtered_df = df.loc[(df[GLYCAN_QVAL_COL] <= q_val_threshold)]
        if protein is not '':
            filtered_df = filtered_df.loc[filtered_df[PROT_COL] == protein]
        filtered_df['Glyc Type'] = filtered_df[GLYCAN_COL].apply(determine_glycan_type)
        type_counts = filtered_df['Glyc Type'].value_counts()
        for glycan_type in GlycanType:
            if glycan_type.value in type_counts.keys():
                glycan_types[analysis_name][glycan_type] = type_counts[glycan_type.value]
            else:
                glycan_types[analysis_name][glycan_type] = 0

    # save results
    if protein is not '':
        output_path = os.path.join(output_dir, '_glycan-compare-{}.tsv'.format(protein.split('|')[-1]))
    else:
        output_path = os.path.join(output_dir, '_glycan-compare.tsv')
    with open(output_path, 'w') as outfile:
        outfile.write('Analysis\t{}\n'.format('\t'.join([x.value for x in GlycanType])))
        for analysis_name, type_dict in glycan_types.items():
            outfile.write('{}\t{}\n'.format(analysis_name, '\t'.join([str(x) for x in type_dict.values()])))


def main(analysis_dirs):
    df_dict = {}
    output_dir = os.path.dirname(analysis_dirs[0])
    for index, analysis_dir in enumerate(analysis_dirs):
        print('parsing file {} of {}'.format(index + 1, len(analysis_dirs)))
        psm_file = os.path.join(analysis_dir, 'psm.tsv')
        df = pd.read_csv(psm_file, sep='\t', header=0, low_memory=False)
        glyco_df = df.dropna(subset=['Glycan Score'])
        glyco_df = glyco_df[~glyco_df[PROT_COL].str.contains('rev_')]
        analysis_name = os.path.basename(analysis_dir)
        df_dict[analysis_name] = glyco_df

    mass_compare(df_dict, GLYC_QVAL_THR, output_dir)
    glycan_type_compare(df_dict, GLYC_QVAL_THR, output_dir)
    glycan_type_compare(df_dict, GLYC_QVAL_THR, output_dir, LRP1)


if __name__ == '__main__':
    dirs = [DIR1, DIR2]
    main(dirs)
