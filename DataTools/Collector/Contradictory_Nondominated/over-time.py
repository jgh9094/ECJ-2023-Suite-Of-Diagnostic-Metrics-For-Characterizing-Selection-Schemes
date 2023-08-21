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
sys.path.insert(1, '../../')
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
def CheckDir(dir,dump,offs):

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
    SCHEMES = ['FITSHARING_P','NONDOMINATED_SORTING','NONDOMINATED_FRONTS']
    NAMES = ['Phenotypic fitness sharing (fsp)','Nondominated sorting (nds)','Nondominated front ranking (ndf)']
    ACRONYM = ['fsp','nds','ndf']
    
    # gens we are expecting
    GEN_LIST = [x for x in range(int(params.GENERATIONS)+1) if x % params.RESOLUTION == 0]

    # collect all data
    DF_LIST = []

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
        acro = ACRONYM[i]
        name = NAMES[i]
        for seed in SEED[i]:

            FILE_DIR = DIA_DIR + scheme + '/' + str(seed) + '/data.csv'
            print(FILE_DIR, flush=True)

            # get data from file and check if can store it
            df = pd.read_csv(FILE_DIR)

            # get data from file and check if can store it
            df = pd.read_csv(FILE_DIR)
            df = df.iloc[::params.RESOLUTION, :]

            DF_LIST.append(pd.DataFrame(
            {   'gen': pd.Series(GEN_LIST),
                params.POP_UNI_OBJ:   pd.Series(df[params.POP_UNI_OBJ].tolist()),
                params.UNI_STR_POS:   pd.Series(df[params.UNI_STR_POS].tolist()),
                'acro':               pd.Series([acro] * len(GEN_LIST)),
                'scheme':             pd.Series([name] * len(GEN_LIST))
            }))
            
    fin_df = pd.concat(DF_LIST)

    fin_df.to_csv(path_or_buf= dump + 'over-time.csv', index=False)


# runner
def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str,  help="Target experiment directory.")
    parser.add_argument("dump_directory", type=str,  help="Data directory where we are placing stuff at.")
    parser.add_argument("seed_offset",    type=int,  help="Experiment seed offset.")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_directory.strip()
    print('Data directory=',data_dir, flush=True)
    dump_directory = args.dump_directory.strip()
    print('Dump directory=',dump_directory, flush=True)
    offset = int(args.seed_offset)
    print('Offset=', offset, flush=True)


    # Get to work!
    print("\nChecking all related data directories now!", flush=True)
    CheckDir(data_dir,dump_directory,offset)

if __name__ == "__main__":
    main()