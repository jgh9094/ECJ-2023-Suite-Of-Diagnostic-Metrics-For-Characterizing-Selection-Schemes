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

# file location for params.py file
sys.path.insert(1, '../')
import params

# ordering of diagnostics


# return the number of rows in a csv file
def CountRows(file_name):
    # create pandas data frame of entire csv
    try:
        df = pd.read_csv(file_name)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()

    if(df.shape[0] == 0):
        return 0

    gens = df['gen'].to_list()

    return gens[-1]

# responsible for looking through the data directories for success
def CheckDir(dir,dia,offs,val):

    # check if data dir exists
    if os.path.isdir(dir):
        print('Data dirctory exists=', dir)
    else:
        print('DOES NOT EXIST=', dir)
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # check if diagnostic data folder exists
    DIA_DIR = dir + params.SetDiagnostic(dia) + '/'


    if os.path.isdir(DIA_DIR):
        print('Selection scheme data folder exists', DIA_DIR)
    else:
        print('SELECTION DIRECTORY DOES NOT EXIST=', DIA_DIR)
        # sys.exit('SELECTION DATA DIRECTORY DOES NOT EXIST')

    # create seed data directories and check if exist
    SCHEMES = ['TRUNCATION','TOURNAMENT','FITSHARING_G','FITSHARING_P','LEXICASE','NONDOMINATED','NOVELTY','RANDOM']
    DIR_DNE = []
    DAT_DNE = []
    DAT_DNF = []

    SEED = []
    SEED.append([x + offs for x in range(1,51)])
    SEED.append([x + offs for x in range(51,101)])
    SEED.append([x + offs for x in range(101,151)])
    SEED.append([x + offs for x in range(151,201)])
    SEED.append([x + offs for x in range(201,251)])
    SEED.append([x + offs for x in range(251,301)])
    SEED.append([x + offs for x in range(301,351)])
    SEED.append([x + offs for x in range(351,401)])

    print('Full data Dir=', DIA_DIR + 'SEED' + '/')
    print('Now checking data replicates sub directories')

    for i in range(8):
        scheme = SCHEMES[i]
        for seed in SEED[i]:

            FILE_DIR = ''

            if val:
                FILE_DIR += DIA_DIR + 'MVC_' + scheme + '/' + str(seed) + '/'
            else:
                FILE_DIR += DIA_DIR + scheme + '/' + str(seed) + '/'

            print(FILE_DIR)

            if os.path.isdir(FILE_DIR) == False:
                DIR_DNE.append(seed % 400)
                continue

            FILE_DIR += '/data.csv'

            # now check if the data file exists in full data director
            if os.path.isfile(FILE_DIR) == False:
                DAT_DNE.append(seed % 400)
                continue

            # make sure that the data.csv file did in fact finish all generations
            if CountRows(FILE_DIR) != int(params.GENERATIONS):
                DAT_DNF.append(seed % 400)
                continue

    # print out the list of incomplete seeds
    print('Directories that were not created:', DIR_DNE)
    print('Data files that do not exist:', DAT_DNE)
    print('Data files that did not finish:', DAT_DNF)
    print('')
    print('Total list of unfinished runs:')

    fin = DIR_DNE + DAT_DNF + DAT_DNE
    fin.sort()
    fins = ''
    for x in fin:
        fins = fins + str(x) + ','
    # print out the sorted list
    print(fins[:len(fins)-1])

# runner
def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str,  help="Target experiment directory.")
    parser.add_argument("diagnostic",     type=int,  help="Diagnostic we are looking for?\n0: Exploitation\n1: Ordered Exploitation\n2: Contradictory Objectives\n3: Multi-path Exploration\n4: Multi-valley Crossing")
    parser.add_argument("seed_offset",    type=int,  help="Experiment seed offset.")
    parser.add_argument("valleys",        type=int,  help="True (1) or False (0) on whether or not valleys are applied")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_directory.strip()
    print('Data directory=',data_dir)
    diagnostic = args.diagnostic
    print('Diagnostic=', params.SetDiagnostic(diagnostic))
    offset = int(args.seed_offset)
    print('Offset=', offset)
    valleys = bool(args.valleys)
    print('valleys=', valleys)

    # Get to work!
    print("\nChecking all related data directories now!")
    CheckDir(data_dir,diagnostic,offset,valleys)

if __name__ == "__main__":
    main()