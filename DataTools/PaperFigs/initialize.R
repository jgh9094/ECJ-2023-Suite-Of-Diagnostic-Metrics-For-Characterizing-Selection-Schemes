# data diractory for local testing
DATA_DIR = '~/Desktop/Repositories//ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/DATA/'

# graph variables
SHAPE <- c(5,3,1,2,6,0,4,20,1)
cb_palette <- c('#332288','#88CCEE','#EE7733','#EE3377','#117733','#882255','#44AA99','#CCBB44', '#000000')
TSIZE <- 22
p_theme <- theme(
  text = element_text(size = 22),
  plot.title = element_text( face = "bold", size = 22, hjust=0.5),
  panel.border = element_blank(),
  panel.grid.minor = element_blank(),
  legend.title = element_text(size=22),
  legend.text = element_text(size=22),
  axis.title = element_text(size=22),
  axis.text = element_text(size=22),
  legend.position = "bottom",
  panel.background = element_rect(fill = "#f1f2f5",
                                  colour = "white",
                                  linewidth = 0.5, linetype = "solid")
)

# default variables
REPLICATES <- 50
DIMENSIONALITY <- 100
GENERATIONS <- 50000

# selection scheme related stuff
ACRO <- c('tru','tor','lex','gfs','pfs','nds','nov','ran')
NAMES <- c('Truncation (tru)','Tournament (tor)','Lexicase (lex)', 'Genotypic Fitness Sharing (gfs)','Phenotypic Fitness Sharing (pfs)','Nondominated Sorting (nds)','Novelty Search (nov)','Random (ran)')
legend_title <- 'Selection \n Scheme'