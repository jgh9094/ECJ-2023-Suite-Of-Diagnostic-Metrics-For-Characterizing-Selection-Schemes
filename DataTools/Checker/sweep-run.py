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

missing = {'EXPLOITATION_RATE':[],'ORDERED_EXPLOITATION':[],'CONTRADICTORY_OBJECTIVES':[],'MULTIPATH_EXPLORATION':[]}


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
def CheckDir(dir,sch,offs,val):

    # check if data dir exists
    if os.path.isdir(dir):
        print('Data dirctory exists=', dir, flush=True)
    else:
        print('DOES NOT EXIST=', dir, flush=True)
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # check if diagnostic data folder exists
    DIA_DIR = dir + params.GetSweepScheme(sch) + '/'

    if os.path.isdir(DIA_DIR):
        print('Selection scheme data folder exists', DIA_DIR, flush=True)
    else:
        sys.exit('SELECTION DATA DIRECTORY DOES NOT EXIST' + DIA_DIR)

    SEED = params.GetSweepSeedLists(offs,sch)

    print('Full data Dir=', DIA_DIR + 'SEED' + '/', flush=True)
    print('Now checking data replicates sub directories', flush=True)

    for i in range(len(params.DIAGNOSTICS)):
        diagnostic = params.DIAGNOSTICS[i]
        for seed in SEED[i]:

            FILE_DIR = DIA_DIR 
            
            if val == True:
                FILE_DIR += 'MVC_' + diagnostic + '/' + str(seed) + '/'
            else:
                FILE_DIR += diagnostic + '/' + str(seed) + '/'
            
            print(FILE_DIR, flush=True)

            if os.path.isdir(FILE_DIR) == False:
                missing[diagnostic].append(seed % 500)
                continue

            FILE_DIR += '/data.csv'

            # now check if the data file exists in full data director
            if os.path.isfile(FILE_DIR) == False or CountRows(FILE_DIR) != int(params.GENERATIONS):
                missing[diagnostic].append(seed % 500)
                continue
            
    # print out the list of incomplete seeds
    print('Scheme:', params.GetSweepScheme(sch))
    print('Directories and seed that did not finish running:')
    
    for key,val in missing.items():
        print(key + ': ')
        val.sort()
        seeds = ''
        
        for x in val:
            seeds += str(x) + ','
        print(seeds)

# runner
def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory",   type=str,  help="Target experiment directory.")
    parser.add_argument("scheme",           type=int,  help="Which selection are we doing? \n0: Truncation\n1: Tournament\n2: Fitness Sharing G\n3: Fitness Sharing P\n4: Nondominated Sorting\n5: Novelty Search.")
    parser.add_argument("seed_offset",      type=int,  help="Experiment seed offset.")
    parser.add_argument("valleys",          type=int,  help="True (1) or False (0) on whether or not valleys are applied")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_directory.strip()
    print('Data directory=',data_dir, flush=True)
    scheme = args.scheme
    print('Scheme=', params.GetSweepScheme(scheme))
    offset = int(args.seed_offset)
    print('Offset=', offset, flush=True)
    valleys = bool(args.valleys)
    print('valleys=', valleys, flush=True)

    # Get to work!
    print("\nChecking all related data directories now!", flush=True)
    CheckDir(data_dir,scheme,offset,valleys)

if __name__ == "__main__":
    main()