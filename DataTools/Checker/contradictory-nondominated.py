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
def CheckDir(dir,offs):

    # check if data dir exists
    if os.path.isdir(dir):
        print('Data dirctory exists=', dir, flush=True)
    else:
        print('DOES NOT EXIST=', dir, flush=True)
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # check if diagnostic data folder exists
    DIA_DIR = dir + 'CONTRADICTORY_NONDOMINATED/'

    if os.path.isdir(DIA_DIR):
        print('Selection scheme data folder exists', DIA_DIR, flush=True)
    else:
        sys.exit('SELECTION DATA DIRECTORY DOES NOT EXIST' + DIA_DIR)

    # create seed data directories and check if exist
    SCHEMES = ['FITSHARING_P','NONDOMINATED_SORTIN','NONDOMINATED_SORTIN']
    DIR_DNE = []
    DAT_DNE = []
    DAT_DNF = []

    SEED = []
    # phenotypic fitness sharing
    SEED.append([x + offs for x in range(1,51)])
    # nondominated sorting
    SEED.append([x + offs for x in range(51,101)])
    # nondominated front ranking
    SEED.append([x + offs for x in range(101,151)])
        
    print('Full data Dir=', DIA_DIR + 'SEED' + '/', flush=True)
    print('Now checking data replicates sub directories', flush=True)

    for i in range(len(SCHEMES)):
        scheme = SCHEMES[i]
        for seed in SEED[i]:

            FILE_DIR = DIA_DIR + scheme + '/' + str(seed) + '/'
            print(FILE_DIR, flush=True)

            if os.path.isdir(FILE_DIR) == False:
                DIR_DNE.append(seed)
                continue

            FILE_DIR += '/data.csv'

            # now check if the data file exists in full data director
            if os.path.isfile(FILE_DIR) == False:
                DAT_DNE.append(seed)
                continue

            # make sure that the data.csv file did in fact finish all generations
            if CountRows(FILE_DIR) != int(params.GENERATIONS):
                DAT_DNF.append(seed)
                continue

    fin = DIR_DNE + DAT_DNF + DAT_DNE
    fin.sort()
    fins = ''
    for x in fin:
        fins = fins + str(x - offs) + ','
    # print out the sorted list
    print('OFFSET:',offs)
    print(fins[:len(fins)-1])

# runner
def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str,  help="Target experiment directory.")
    parser.add_argument("seed_offset",    type=int,  help="Experiment seed offset.")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_directory.strip()
    print('Data directory=',data_dir, flush=True)
    offset = int(args.seed_offset)
    print('Offset=', offset, flush=True)


    # Get to work!
    print("\nChecking all related data directories now!", flush=True)
    CheckDir(data_dir,offset)

if __name__ == "__main__":
    main()