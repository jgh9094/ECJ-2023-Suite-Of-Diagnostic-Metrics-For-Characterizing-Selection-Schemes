#####################################################################################################
#####################################################################################################
# Will hold all of the data that we share across python scripts
#
# python3
#####################################################################################################
#####################################################################################################

import sys
import os

# diagnostics
DIAGNOSTICS = ['EXPLOITATION_RATE','ORDERED_EXPLOITATION','CONTRADICTORY_OBJECTIVES','MULTIPATH_EXPLORATION']

# variables we are testing for each replicate range
TR_LIST = ['1','2','4','8','16','32','64','128','256']
TS_LIST = ['2','4','8','16','32','64','128','256','512']
FS_LIST = ['0.0','0.1','0.3','0.6','1.2','2.5','5.0']
ND_LIST = ['0.0','0.1','0.3','0.6','1.2','2.5','5.0']
NS_LIST = ['1','2','4','8','15','30']

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
ELE_BIG_PEAK = 'ele_big_peak'
ELE_STK_CNT = 'ele_stk_cnt'

# seed experiements replicates range
REPLICATES = 50
GENERATIONS = 50000
RESOLUTION = 100
DIMENSIONALITY = 100

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

# return appropiate string dir name (based off run.sb file naming system)
def GetDiagnosticAcro(d):
    # case by case
    if d == 0:
        return 'exp'
    elif d == 1:
        return 'ord'
    elif d == 2:
        return 'con'
    elif d == 3:
        return 'mpe'
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

def GetSchemeAcro(s):
    # case by case
    if s == 'TRUNCATION' or s == 0:
        return 'tru'

    elif s == 'TOURNAMENT' or s == 1:
        return 'tor'

    elif s == 'FITSHARING_G' or s == 2:
        return 'gfs'

    elif s == 'FITSHARING_P' or s == 3:
        return 'pfs'

    elif s == 'LEXICASE':
        return 'lex'

    elif s == 'NONDOMINATED' or s == 4:
        return 'nds'

    elif s == 'NOVELTY' or s == 5:
        return 'nov'

    elif s == 'RANDOM':
        return 'ran'

    else:
        sys.exit("UNKNOWN VARIABLE LIST")

def GetSweepScheme(s):
    #case by case
    if s == 0:
        return 'TRUNCATION'
    
    elif s == 1:
        return 'TOURNAMENT'
    
    elif s ==  2:
        return 'FITSHARING_G'

    elif s == 3:
        return 'FITSHARING_P'

    elif s == 4:
        return 'NONDOMINATED'

    elif s == 5:
        return 'NOVELTY'
        
def GetSweepSeedLists(offs,sch):
    #case by case
    seed = []
    
    # truncation, tournament: 450 replidates
    if sch == 0 or sch == 1:
        seed.append([x + offs for x in range(1,451)])
        seed.append([x + offs + 500 for x in range(1,451)])
        seed.append([x + offs + 1000 for x in range(1,451)])
        seed.append([x + offs + 1500 for x in range(1,451)])
        return seed
    
    # fitness sharing, nondominated sorting
    elif sch ==  2 or sch == 3 or sch == 4:
        seed.append([x + offs for x in range(1,351)])
        seed.append([x + offs + 500 for x in range(1,351)])
        seed.append([x + offs + 1000 for x in range(1,351)])
        seed.append([x + offs + 1500 for x in range(1,351)])
        return seed

    # novelty search
    elif sch == 5:
        seed.append([x + offs for x in range(1,301)])
        seed.append([x + offs + 500 for x in range(1,301)])
        seed.append([x + offs + 1000 for x in range(1,301)])
        seed.append([x + offs + 1500 for x in range(1,301)])
        return seed

    else:
        sys.exit('SEED SELECTION UNKNOWN')

def GetSchemeParam(sch):
    # truncation, tournament
    if sch == 0 or sch == 1:
        return 'T'
    
    # fitness sharing, nondominated sorting
    elif sch ==  2 or sch == 3 or sch == 4:
        return 'Sigma'

    # novelty search
    elif sch == 5:
        return 'K'

    else:
        sys.exit('SEED SELECTION UNKNOWN')
        
def GetSchemeSeedBound(sch):
    # truncation, tournament
    if sch == 0 or sch == 1:
        return 450
    
    # fitness sharing, nondominated sorting
    elif sch ==  2 or sch == 3 or sch == 4:
        return 350

    # novelty search
    elif sch == 5:
        return 300

    else:
        sys.exit('SEED SELECTION UNKNOWN')
        
def GetSchemeParamSet(sch):
    # truncation
    if sch == 0:
        return TR_LIST
    # truncation
    elif sch == 1:
        return TS_LIST
    # fitness sharing
    elif sch ==  2 or sch == 3:
        return FS_LIST
    # nondominated sorting
    elif sch == 4:
        return ND_LIST
    # novelty search
    elif sch == 5:
        return NS_LIST
    else:
        sys.exit('SEED SELECTION UNKNOWN')

def GetSchemeName(s):
    # case by case
    if s == 'TRUNCATION':
        return 'Truncation (tru)'

    elif s == 'TOURNAMENT':
        return 'Tournament (tor)'

    elif s == 'FITSHARING_G':
        return 'Genotypic Fitness Sharing (gfs)'

    elif s == 'FITSHARING_P':
        return 'Phenotypic Fitness Sharing (pfs)'

    elif s == 'LEXICASE':
        return 'Lexicase (lex)'

    elif s == 'NONDOMINATED':
        return 'Nondominated Sorting (nds)'

    elif s == 'NOVELTY':
        return 'Novelty Search (nov)'

    elif s == 'RANDOM':
        return 'Random (ran)'

    else:
        sys.exit("UNKNOWN VARIABLE LIST")

def GetDataList(val):

    if val:
        return [POP_FIT_MAX,POP_OPT_MAX,POP_UNI_OBJ,POP_STR_MAX,UNI_STR_POS,ARC_ACTI_GENE,OVERLAP,ELE_BIG_PEAK,ELE_STK_CNT]

    else:
        return [POP_FIT_MAX,POP_OPT_MAX,POP_UNI_OBJ,POP_STR_MAX,UNI_STR_POS,ARC_ACTI_GENE,OVERLAP,ELE_STK_CNT]