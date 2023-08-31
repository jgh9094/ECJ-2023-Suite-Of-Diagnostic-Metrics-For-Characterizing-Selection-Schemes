#clean up memory
rm(list = ls())
cat("\014")

# assuming working dir is root of repository
source('./DataTools/PaperFigs/initialize.R')


# libraries we are using
library(ggplot2)
library(cowplot)
library(dplyr)
library(PupillometryR)

# get data frames

DIR = paste(DATA_DIR,'CONTRADICTORY_NONDOMINATED/', sep = "", collapse = NULL)
over_time <- read.csv(paste(DIR,'over-time.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
over_time$scheme <- factor(over_time$scheme, levels = c('Phenotypic fitness sharing (pfs)','Nondominated front ranking (nfr)','Nondominated sorting (nds)'))
over_time$acro <- factor(over_time$acro, levels = c('pfs','nfr','nds'))

# make exploitation rate figures

lines = over_time %>%
  group_by(scheme, gen) %>%
  dplyr::summarise(
    min = min(pop_uni_obj),
    mean = mean(pop_uni_obj),
    max = max(pop_uni_obj)
  )

sat_ot = ggplot(lines, aes(x=gen, y=mean, group = scheme, fill = scheme, color = scheme, shape = scheme)) +
  geom_ribbon(aes(ymin = min, ymax = max), alpha = 0.1) +
  geom_line(size = 0.5) +
  geom_point(data = filter(lines, gen %% 2000 == 0 & gen != 0), size = 1.5, stroke = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    limits=c(0, 100),
    breaks=seq(0,100, 25),
    labels=c("0", "25", "50", "75", "100")
  ) +
  scale_x_continuous(
    name="Generations",
    limits=c(0, 50000),
    breaks=c(0, 10000, 20000, 30000, 40000, 50000),
    labels=c("0e+4", "1e+4", "2e+4", "3e+4", "4e+4", "5e+4")
  ) +
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('Population satisfactory trait coverage')+
  p_theme

# plot it: legend
legend <- cowplot::get_legend(
  sat_ot +
    guides(
      shape=guide_legend(nrow=2,title=legend_title),
      color=guide_legend(nrow=2,title=legend_title),
      fill=guide_legend(nrow=2,title=legend_title)
    )
)

### max of run plot

sat_end = filter(over_time, gen == 50000) %>%
  ggplot(., aes(x = acro, y = pop_uni_obj, color = acro, fill = acro, shape = acro)) +
  geom_flat_violin(position = position_nudge(x = .09, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .15, y = 0)) +
  geom_point(position = position_jitter(width = .02), size = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    limits=c(0, 100),
    breaks=seq(0,100, 25),
    labels=c("0", "25", "50", "75", "100")
  ) +
  scale_x_discrete(
    name="Scheme"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('Final satisfactory trait coverage')+
  p_theme + coord_flip()



plot = plot_grid(
  sat_end + theme(legend.position = "None"),
  legend,
  nrow=2,
  rel_heights = c(2,.45),
  label_size = TSIZE
)

save_plot(
  paste(filename ="DataTools/PaperFigs/nondominated-parts.pdf"),
  plot,
  base_width=15,
  base_height=4.0
)
