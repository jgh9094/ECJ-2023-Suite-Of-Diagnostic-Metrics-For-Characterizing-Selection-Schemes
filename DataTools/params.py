#####################################################################################################
#####################################################################################################
# Will hold all of the data that we share across python scripts
#
# python3
#####################################################################################################
#####################################################################################################

import sys
import os

# variables we are testing for each replicate range
TR_LIST = ['1','2','4','8','16','32','64','128','256']
TS_LIST = ['2','4','8','16','32','64','128','256']
LX_LIST = ['0.0']
FS_LIST = ['0.0','0.1','0.3','0.6','1.2','2.5','5.0']
ND_LIST = ['0.0','0.1','0.3','0.6','1.2','2.5','5.0']
NS_LIST = ['0','1','2','4','8','15','30']

# columns we are interested in grabbing
GENERATION = 'gen'
# pop level
POP_FIT_MAX = 'pop_fit_max'
POP_OPT_MAX = 'pop_opt_max'
POP_UNI_OBJ = 'pop_uni_obj'
POP_STR_MAX = 'pop_str_max'
# trait coverage
UNI_STR_POS = 'uni_str_pos'
# novelty data
ARC_ACTI_GENE = 'arc_acti_gene'
OVERLAP = 'overlap'
POP_MAX_TRT = 'pop_max_trt'
POP_MAX_GENE = 'pop_max_gene'

# collection of data in list
DATA_LIST = [POP_FIT_MAX,POP_OPT_MAX,POP_UNI_OBJ,POP_STR_MAX,UNI_STR_POS,ARC_ACTI_GENE,OVERLAP,POP_MAX_TRT,POP_MAX_GENE]

# seed experiements replicates range
REPLICATES = 50
GENERATIONS = 50000
RESOLUTION = 100

# return appropiate string dir name (based off run.sb file naming system)
def GetDiagnostic(d):
    # case by case
    if d == 0:
        return 'EXPLOITATION_RATE'
    elif d == 1:
        return 'ORDERED_EXPLOITATION'
    elif d == 2:
        return 'CONTRADICTORY_OBJECTIVES'
    elif d == 3:
        return 'MULTIPATH_EXPLORATION'
    else:
        sys.exit('UNKNOWN DIAGNOSTIC')

# return the correct amount of seed ran by experiment treatment
def GetSeedLists(e,offs):

    # diagnostic/selection treatments
    if e == 0 or e == 1:
        seed = []
        seed.append([x + offs for x in range(1,51)])
        seed.append([x + offs for x in range(51,101)])
        seed.append([x + offs for x in range(101,151)])
        seed.append([x + offs for x in range(151,201)])
        seed.append([x + offs for x in range(201,251)])
        seed.append([x + offs for x in range(251,301)])
        seed.append([x + offs for x in range(301,351)])
        seed.append([x + offs for x in range(351,401)])
        return seed

    else:
        sys.exit('SEED SELECTION UNKNOWN')

# set the appropiate list of variables we are checking for
def GetSchemeVarList(s):
    # case by case
    if s == 0:
        return TR_LIST
    elif s == 1:
        return TS_LIST
    elif s == 2:
        return FS_LIST
    elif s == 3:
        return LX_LIST
    elif s == 4:
        return FS_LIST
    elif s == 5:
        return NS_LIST
    else:
        sys.exit("UNKNOWN VARIABLE LIST")

# selection scheme list to get dependent on experiment running
def GetSchemeList(e):
    # case by case
    if e == 0 or e == 1:
        return ['TRUNCATION','TOURNAMENT','FITSHARING_G','FITSHARING_P','LEXICASE','NONDOMINATED','NOVELTY','RANDOM']
    else:
        sys.exit("UNKNOWN VARIABLE LIST")