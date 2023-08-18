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
# Output: csv with overtime data
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

    SCHEMES = ['TRUNCATION','TOURNAMENT','FITSHARING_G','FITSHARING_P','LEXICASE','NONDOMINATED','NOVELTY','RANDOM']
    SEED = params.GetSeedLists(exp,offs)

    # gens we are expecting
    GEN_LIST = [x for x in range(int(params.GENERATIONS)+1) if x % params.RESOLUTION == 0]

    # collect all data
    DF_LIST = []

    print('Full data Dir=', DIA_DIR + 'SEED' + '/', flush=True)
    print('Now checking data replicates sub directories', flush=True)

    for i in range(len(SCHEMES)):
        scheme = SCHEMES[i]
        for seed in SEED[i]:

            FILE_DIR = DIA_DIR + scheme + '/' + str(seed) + '/'
            print(FILE_DIR, flush=True)
            FILE_DIR += '/data.csv'

            # get data from file and check if can store it
            df = pd.read_csv(FILE_DIR)
            df = df.iloc[::params.RESOLUTION, :]

            if val:
                DF_LIST.append(pd.DataFrame(
                {   'gen': pd.Series(GEN_LIST),
                    params.POP_FIT_MAX:   pd.Series(df[params.POP_FIT_MAX].tolist()),
                    params.POP_OPT_MAX:   pd.Series(df[params.POP_OPT_MAX].tolist()),
                    params.POP_UNI_OBJ:   pd.Series(df[params.POP_UNI_OBJ].tolist()),
                    params.POP_STR_MAX:   pd.Series(df[params.POP_STR_MAX].tolist()),
                    params.ARC_ACTI_GENE: pd.Series(df[params.ARC_ACTI_GENE].tolist()),
                    params.OVERLAP:       pd.Series(df[params.OVERLAP].tolist()),
                    params.UNI_STR_POS:   pd.Series(df[params.UNI_STR_POS].tolist()),
                    params.ELE_BIG_PEAK:   pd.Series(df[params.ELE_BIG_PEAK].tolist()),
                    params.ELE_STK_CNT:   pd.Series(df[params.ELE_STK_CNT].tolist()),
                    'acro':               pd.Series([params.GetSchemeAcro(scheme)] * len(GEN_LIST)),
                    'scheme':             pd.Series([params.GetSchemeName(scheme)] * len(GEN_LIST))
                }))

            else:
                DF_LIST.append(pd.DataFrame(
                {   'gen': pd.Series(GEN_LIST),
                    params.POP_FIT_MAX:   pd.Series(df[params.POP_FIT_MAX].tolist()),
                    params.POP_OPT_MAX:   pd.Series(df[params.POP_OPT_MAX].tolist()),
                    params.POP_UNI_OBJ:   pd.Series(df[params.POP_UNI_OBJ].tolist()),
                    params.POP_STR_MAX:   pd.Series(df[params.POP_STR_MAX].tolist()),
                    params.ARC_ACTI_GENE: pd.Series(df[params.ARC_ACTI_GENE].tolist()),
                    params.OVERLAP:       pd.Series(df[params.OVERLAP].tolist()),
                    params.UNI_STR_POS:   pd.Series(df[params.UNI_STR_POS].tolist()),
                    params.ELE_STK_CNT:   pd.Series(df[params.ELE_STK_CNT].tolist()),
                    'acro':               pd.Series([params.GetSchemeAcro(scheme)] * len(GEN_LIST)),
                    'scheme':             pd.Series([params.GetSchemeName(scheme)] * len(GEN_LIST))
                }))

    fin_df = pd.concat(DF_LIST)

    fin_df.to_csv(path_or_buf= dump + 'over-time.csv', index=False)

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