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

# responsible for looking through the data directories for success
def CheckDir(dir,dump,dia,offs,val,exp):

    # check if data dir exists
    if os.path.isdir(dir):
        print('Data dirctory exists=', dir, flush=True)
    else:
        print('DOES NOT EXIST=', dir, flush=True)
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # check if diagnostic data folder exists
    DIA_DIR = ''
    if val:
        DIA_DIR +=  dir + 'MVC_' + params.GetDiagnostic(dia) + '/'
    else:
        DIA_DIR +=  dir + params.GetDiagnostic(dia) + '/'

    if os.path.isdir(DIA_DIR):
        print('Selection scheme data folder exists', DIA_DIR, flush=True)
    else:
        print('SELECTION DIRECTORY DOES NOT EXIST=', DIA_DIR, flush=True)
        sys.exit('SELECTION DATA DIRECTORY DOES NOT EXIST')

    # get seeds and schemes we are recording

    SCHEMES = params.GetSchemeList(exp)
    SEED = params.GetSeedLists(exp,offs)

    print('Full data Dir=', DIA_DIR + 'SEED' + '/', flush=True)
    print('Now checking data replicates sub directories', flush=True)

    # generation
    GEN = []
    # selection scheme
    SEL = []
    # scheme acronym
    ACR = []

    for i in range(len(SCHEMES)):
        scheme = SCHEMES[i]
        for seed in SEED[i]:

            FILE_DIR = DIA_DIR + scheme + '/' + str(seed) + '/'
            print(FILE_DIR, flush=True)
            FILE_DIR += '/data.csv'

            # get data from file and check if can store it
            df = pd.read_csv(FILE_DIR)

            # create subset of data frame with only winning solutions
            df = df[df[params.POP_OPT_MAX] == params.DIMENTIONALITY]
            gens = df[params.GENERATION].tolist()

            SEL.append(params.GetSchemeName(scheme))
            ACR.append(params.GetSchemeAcro(scheme))

            if(len(gens) == 0):
                GEN.append(params.GENERATIONS + 10000)
            else:
                GEN.append(gens[0])

    fin_df = pd.DataFrame({'gen':pd.Series(GEN),'scheme':pd.Series(SEL),'acro':pd.Series(ACR)})
    fin_df.to_csv(path_or_buf= dump + 'sol-fnd.csv', index=False)

# runner
def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str,  help="Target experiment directory.")
    parser.add_argument("dump_directory", type=str,  help="Data directory where we are placing stuff at.")
    parser.add_argument("diagnostic",     type=int,  help="Diagnostic we are looking for?\n0: Exploitation\n1: Ordered Exploitation\n2: Contradictory Objectives\n3: Multi-path Exploration\n4: Multi-valley Crossing")
    parser.add_argument("seed_offset",    type=int,  help="Experiment seed offset.")
    parser.add_argument("valleys",        type=int,  help="True (1) or False (0) on whether or not valleys are applied")
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
    valleys = bool(args.valleys)
    print('valleys=', valleys, flush=True)
    experiment = bool(args.experiment)
    print('experiment=', experiment, flush=True)

    # Get to work!
    print("\nChecking all related data directories now!", flush=True)
    CheckDir(data_dir,dump_directory,diagnostic,offset,valleys,experiment)

if __name__ == "__main__":
    main()