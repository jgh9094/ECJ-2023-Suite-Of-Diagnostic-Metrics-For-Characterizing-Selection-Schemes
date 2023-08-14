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
# Output: csv with all the best values found for data variable
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
def CheckDir(dir,dump,sch,offs,val):

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

    # gens we are expecting
    GEN_LIST = [x for x in range(int(params.GENERATIONS)+1) if x % params.RESOLUTION == 0]

    # collect all data
    DF_LIST = []

    for i in range(len(params.DIAGNOSTICS)):
        diagnostic = params.DIAGNOSTICS[i]
        for s in range(len(SEED[i])):
            
            seed = SEED[i][s]            
            FILE_DIR = DIA_DIR 
            
            if val == True:
                FILE_DIR += 'MVC_' + diagnostic + '/' + str(seed) + '/'
            else:
                FILE_DIR += diagnostic + '/' + str(seed) + '/'
            
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
                    params.GetSchemeParam(sch):pd.Series([params.GetSchemeParamSet(sch)[int(((s % params.GetSchemeSeedBound(sch)))/params.REPLICATES)]] * len(GEN_LIST)),
                    'acro':pd.Series([params.GetDiagnosticAcro(i)] * len(GEN_LIST))
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
                    params.GetSchemeParam(sch):pd.Series([params.GetSchemeParamSet(sch)[int(((s % params.GetSchemeSeedBound(sch)))/params.REPLICATES)]] * len(GEN_LIST)),
                    'acro':pd.Series([params.GetDiagnosticAcro(i)] * len(GEN_LIST))
                }))

    print('SAVING DATA NOW...')
    fin_df = pd.concat(DF_LIST)
    fin_df.to_csv(path_or_buf= dump + params.GetSchemeAcro(sch) + '.csv', index=False)

# runner
def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str,  help="Target experiment directory.")
    parser.add_argument("dump_directory", type=str,  help="Data directory where we are placing stuff at.")
    parser.add_argument("scheme",           type=int,  help="Which selection are we doing? \n0: Truncation\n1: Tournament\n2: Fitness Sharing G\n3: Fitness Sharing P\n4: Nondominated Sorting\n5: Novelty Search.")
    parser.add_argument("seed_offset",      type=int,  help="Experiment seed offset.")
    parser.add_argument("valleys",          type=int,  help="True (1) or False (0) on whether or not valleys are applied")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_directory.strip()
    print('Data directory=',data_dir, flush=True)
    dump_directory = args.dump_directory.strip()
    print('Dump directory=',dump_directory, flush=True)
    scheme = args.scheme
    print('Scheme=', params.GetSweepScheme(scheme))
    offset = int(args.seed_offset)
    print('Offset=', offset, flush=True)
    valleys = bool(args.valleys)
    print('valleys=', valleys, flush=True)

    # Get to work!
    print("\nChecking all related data directories now!", flush=True)
    CheckDir(data_dir,dump_directory,scheme,offset,valleys)

if __name__ == "__main__":
    main()