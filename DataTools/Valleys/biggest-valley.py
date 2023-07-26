#####################################################################################################
#
# Will list all of the incomplete run id's that need to finish running, per diagnotic/selection treatment
# Script will go through each replicate for a specific selection/diagnostic treatment
#
# Command Line Inputs:
#
# data_directory: directory where data is located
#     diagnostic: diagnostic used
#    seed_offset: seed offset (if any)
#   valley_cross: was there valley crossing involved? (0) no & (1) yes
#
# Output: list of seeds that need to be reran in terminal display
#
# python3
#####################################################################################################

######################## IMPORTS ########################
import argparse
import pandas as pd
import sys
import os
import numpy as np

# file location for params.py file
sys.path.insert(1, '../')
import params

peaks_set = [8.0, 9.0, 11.0, 14.0, 18.0, 23.0, 29.0, 36.0, 44.0, 53.0, 63.0, 74.0, 86.0, 99.0]

# largest peak crossed in the whole phenotype
def PeakCrossedCount(phenotype):
    peaks = 0

    # go through each trait
    for trait in phenotype:
        p = 0
        while p < len(peaks_set):
            if peaks_set[p] <= trait:
                p += 1
            else:
                break

        if peaks < p:
            peaks = p

    return peaks

# ordered exploitation
def OrderedExploitation(g):
    # Find where descending order breaks
    sorted_index = 1
    for i in range(len(g) - 1):
        if g[i] >= g[i + 1]:
            sorted_index += 1
            continue

        break

    # If sorted, return the same list
    if sorted_index == len(g):
        phenotype = g.copy()

    # Else, fill in appropriately
    else:
        # Initialize phenotype to the same size
        --sorted_index
        phenotype = [0.0] * len(g)

        # Everything up to the unsorted part
        for i in range(sorted_index):
            phenotype[i] = g[i]

        # Everything after the unsorted part
        for i in range(sorted_index, len(phenotype)):
            phenotype[i] = 0.0

    # final checks to make sure phenotype follows decreasing ordering
    if all(phenotype[i] >= phenotype[i+1] for i in range(len(phenotype)-1)):
            return phenotype
    else:
        sys.exit('UNKNOWN DIAGNOSTIC')('NON-DECREASING ORDER')

# contradictory objectives
def ContradictoryObjectives(g):
    # Initialize phenotype vector
    phenotype = [0.0] * len(g)

    # Find max value position
    max_gene = g.index(max(g))

    # Set all phenotype vector values
    for i in range(len(phenotype)):
        if i == max_gene:
            phenotype[i] = g[max_gene]
        else:
            phenotype[i] = 0.0

    # check that the phenotype has only one max gene / contradictory objective
    if sum(phenotype) == g[max_gene]:
            return phenotype
    else:
        sys.exit('UNKNOWN DIAGNOSTIC')('MORE THAN ONE CONTRADICTORY TRAIT IN PHENOTYPE')

# multi-path exploration
def MultipathExploration(g):
    # Initialize vector with size g
    phenotype = [0.0] * len(g)

    # Find max value position
    opti = g.index(max(g))

    # Find where order breaks on the right side of the optimal value
    sort = len(g)
    for i in range(opti + 1, len(g)):
        if g[i] > g[i - 1]:
            sort = i
            break

    # Left of optimal value found
    for i in range(opti):
        phenotype[i] = 0.0

    # Middle of optimal value till order broken
    for i in range(opti, sort):
        phenotype[i] = g[i]

    # Right of order broken
    for i in range(sort, len(phenotype)):
        phenotype[i] = 0.0

    # make sure active region follows a decreasing order
    if all(phenotype[i] >= phenotype[i+1] for i in range(opti,sort-1)) == False:
        sys.exit('UNKNOWN DIAGNOSTIC')('MULTIPATH: ACTIVE REGION IS NOT IN DECREASING ORDER')

    # make sure inactive regions are 0.0 in phenotype
    if 0 < len(phenotype[:opti]):
        if sum(phenotype[:opti]) != 0.0:
            sys.exit('UNKNOWN DIAGNOSTIC')('MULTIPATH: LEFT INACTIVE REGION IS BROKEN')

        # make sure left inactive region has no larger value
        if max(g[:opti]) > max(g[opti:sort]):
            sys.exit('UNKNOWN DIAGNOSTIC')('MULTIPATH: LEFT INACTIVE REGION HAS A LARGER VALUE')

    if 0 < len(phenotype[sort:]):
        if sum(phenotype[sort:]) != 0.0:
            sys.exit('UNKNOWN DIAGNOSTIC')('MULTIPATH: LEFT INACTIVE REGION IS BROKEN')

    return phenotype

# responsible for looking through the data directories for success
def CheckDir(dir,dump,dia,offs,exp):

    # check if data dir exists
    if os.path.isdir(dir):
        print('Data dirctory exists=', dir, flush=True)
    else:
        sys.exit('DATA DIRECTORY DOES NOT EXIST: ' + dir)

    # check if diagnostic data folder exists
    DIA_DIR =  dir + 'MVC_' + params.GetDiagnostic(dia) + '/'


    if os.path.isdir(DIA_DIR):
        print('Selection scheme data folder exists', DIA_DIR, flush=True)
    else:
        sys.exit('SELECTION DATA DIRECTORY DOES NOT EXIST: ' + DIA_DIR)

    # create seed data directories and check if exist
    SCHEMES = params.GetSchemeList(exp)
    SEED = params.GetSeedLists(exp,offs)

    # valley peak
    VAL = []
    # selection scheme
    SEL = []
    # scheme acronym
    ACR = []

    print('Full data Dir=', DIA_DIR + 'SEED' + '/', flush=True)
    print('Now checking data replicates sub directories', flush=True)

    for i in range(len(SCHEMES)):
        scheme = SCHEMES[i]
        for seed in SEED[i]:

            FILE_DIR = DIA_DIR + scheme + '/' + str(seed) + '/'
            print(FILE_DIR, flush=True)
            FILE_DIR += '/elite-geno.csv'

            # get data from file and check if can store it
            df = pd.read_csv(FILE_DIR)
            df = df.values.tolist()

            peak_max = 0
            for row in df:
                cur_peak = 0
                geno = row[1:]

                # make sure that genotype is the correct dimensionality
                if len(geno) != params.DIMENSIONALITY:
                    sys.exit('GENOTYPE NOT THE CORRECT DIMENSIONALITY')

                if dia == 0:
                    cur_peak = PeakCrossedCount(geno)
                elif dia == 1:
                    cur_peak = PeakCrossedCount(OrderedExploitation(geno))
                elif dia == 2:
                    cur_peak = PeakCrossedCount(ContradictoryObjectives(geno))
                elif dia == 3:
                    cur_peak = PeakCrossedCount(MultipathExploration(geno))
                else:
                    sys.exit('UNKNOWN DIAGNOSTIC')

                if peak_max < cur_peak:
                    peak_max = cur_peak

            print('peak_max:', peak_max)

            VAL.append(peak_max)
            SEL.append(params.GetSchemeName(scheme))
            ACR.append(params.GetSchemeAcro(scheme))

    fin_df = pd.DataFrame({'peaks': pd.Series(VAL),'scheme':pd.Series(SEL),'acro':pd.Series(ACR)})

    fin_df.to_csv(path_or_buf= dump + 'valley.csv', index=False)

# runner
def main():

    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str,  help="Target experiment directory.")
    parser.add_argument("dump_directory", type=str,  help="Data directory where we are placing stuff at.")
    parser.add_argument("diagnostic",     type=int,  help="Diagnostic we are looking for?\n0: Exploitation\n1: Ordered Exploitation\n2: Contradictory Objectives\n3: Multi-path Exploration\n4: Multi-valley Crossing")
    parser.add_argument("seed_offset",    type=int,  help="Experiment seed offset.")
    parser.add_argument("experiment",     type=int,  help="What experiment are we running?: (0) Base Diagnostics, (1) MVC Diagnostics, (2) Parameter Sweep")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_directory.strip()
    print('Data directory=',data_dir, flush=True)
    dump_directory = args.dump_directory.strip()
    print('Dump directory=',dump_directory, flush=True)
    diagnostic = args.diagnostic
    print('Diagnostic=', params.GetDiagnostic(diagnostic))
    offset = int(args.seed_offset)
    print('Offset=', offset, flush=True)
    experiment = bool(args.experiment)
    print('experiment=', experiment, flush=True)

    # Get to work!
    print("\nChecking all related data directories now!", flush=True)
    CheckDir(data_dir,dump_directory,diagnostic,offset,experiment)

if __name__ == "__main__":
    main()