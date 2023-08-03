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

DIR = paste(DATA_DIR,'BASE_DIAGNOSTICS/MULTIPATH_EXPLORATION/', sep = "", collapse = NULL)
over_time <- read.csv(paste(DIR,'over-time.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
over_time$uni_str_pos = over_time$uni_str_pos + over_time$arc_acti_gene - over_time$overlap
over_time$scheme <- factor(over_time$scheme, levels = NAMES)
over_time$acro <- factor(over_time$acro, levels = ACRO)

best <- read.csv(paste(DIR,'best.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
best$acro <- factor(best$acro, levels = ACRO)

# make exploitation rate figures

lines = over_time %>%
  group_by(scheme, gen) %>%
  dplyr::summarise(
    min = min(pop_fit_max) / DIMENSIONALITY,
    mean = mean(pop_fit_max) / DIMENSIONALITY,
    max = max(pop_fit_max) / DIMENSIONALITY
  )

per_ot = ggplot(lines, aes(x=gen, y=mean, group = scheme, fill = scheme, color = scheme, shape = scheme)) +
  geom_ribbon(aes(ymin = min, ymax = max), alpha = 0.1) +
  geom_line(size = 0.5) +
  geom_point(data = filter(lines, gen %% 2000 == 0 & gen != 0), size = 1.5, stroke = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="    Average trait score",
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

### max of run plot

per_end = filter(over_time, gen == 50000) %>%
  ggplot(., aes(x = acro, y = pop_fit_max / DIMENSIONALITY, color = acro, fill = acro, shape = acro)) +
  geom_flat_violin(position = position_nudge(x = .09, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .15, y = 0)) +
  geom_point(position = position_jitter(width = .02), size = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="    Average trait score",
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
  ggtitle('Final satisfactory coverage')+
  p_theme



per_row =  plot_grid(
  per_ot +
    ggtitle("Performance over time") +
    theme(legend.position = "none", axis.title.x = element_blank(), axis.ticks.x = element_blank(), axis.text.x = element_blank()),
  per_end +
    ggtitle("Best performance") +
    theme(legend.position = "none", axis.title.y=element_blank(), axis.ticks.y = element_blank(), axis.text.y = element_blank(),
          axis.title.x = element_blank(), axis.ticks.x = element_blank(), axis.text.x = element_blank()),
  ncol=2,
  rel_widths = c(2,1.2),
  labels = c('       a','b'),
  label_size = TSIZE
)

# activation gene coverage plots

lines = over_time %>%
  group_by(scheme, gen) %>%
  dplyr::summarise(
    min = min(uni_str_pos),
    mean = mean(uni_str_pos),
    max = max(uni_str_pos)
  )

act_ot = ggplot(lines, aes(x=gen, y=mean, group = scheme, fill = scheme, color = scheme, shape = scheme)) +
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
  ggtitle('Population activation gene coverage')+
  p_theme

### final gen

act_end = filter(over_time, gen == 50000) %>%
  ggplot(., aes(x = acro, y = uni_str_pos, color = acro, fill = acro, shape = acro)) +
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
  ggtitle('Final activation coverage')+
  p_theme

ord_row =  plot_grid(
  act_ot +
    ggtitle("Population activation gene coverage") +
    theme(legend.position = "none"),
  act_end +
    ggtitle("Final activation coverage") +
    theme(legend.position = "none", axis.title.y=element_blank(), axis.ticks.y = element_blank(), axis.text.y = element_blank()),
  ncol=2,
  rel_widths = c(2,1.2),
  labels = c('       c','d'),
  label_size = TSIZE
)


# plot it: legend
legend <- cowplot::get_legend(
  per_ot +
    guides(
      shape=guide_legend(nrow=3,title=legend_title),
      color=guide_legend(nrow=3,title=legend_title),
      fill=guide_legend(nrow=3,title=legend_title)
    ) +
    theme(
      legend.position = "top",
      legend.box="verticle",
      legend.justification="center"
    )
)

# combine 

fig = plot_grid(
  per_row,
  ord_row,
  legend,
  nrow = 3,
  rel_heights = c(1,1.2,.3),
  label_size = TSIZE
)


save_plot(
  paste(filename ="multi-path-exploration-results.pdf"),
  fig,
  base_width=15,
  base_height=7
)