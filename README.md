# ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes

## Overview

This repository is associated with our submission for the [Evolutionary Computation Journal](https://direct.mit.edu/evco): *A suite of diagnostic metrics for characterizing selection schemes*.
All code used for this submission can be found within this repository.

**Repository Guide:**

[DataTools/](https://github.com/jgh9094/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/tree/main/DataTools)

- This directory contains all tools used in this work to 
check ([Checker/](https://github.com/jgh9094/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/tree/main/DataTools/Checker)) and 
collect ([Collector](https://github.com/jgh9094/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/tree/main/DataTools/Collector)) data
- A combination of Python and R scripts were used.
- [PaperFigs](https://github.com/jgh9094/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/tree/main/DataTools/PaperFigs) contains R scripts to generate the plots found in the submission.

[Experiments/](https://github.com/jgh9094/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/tree/main/Experiments)

- This directory contatins the different sets of experiments we ran for this submission.

- The directories that were used for execution on the [MSU HPCC](https://docs.icer.msu.edu/) follow: /EXPERIMENT_TYPE/TREATMENT/Hpcc/scripts.sb.

- The directories that were used to generate our supplementary material on Github follow: /EXPERIMENT_TYPE/TREATMENT/Analysis/results.Rmd.
    
[Source/](https://github.com/jgh9094/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/tree/main/Source)

- This directory contains the source code (C++) for all experiments associated with this work.

## Authors

- [Jose Guadalupe Hernandez](https://jgh9094.github.io/)
- [Charles Ofria](http://ofria.com)
- [Alexander Lalejini](https://lalejini.com)

## Abstract

Benchmark suites provide useful assessments of an evolutionary algorithm's problem-solving capacity, but the constituent problems are often too complex to cleanly identify an algorithm's strengths and weaknesses.
Here, we introduce the diagnostic suite DOSSIER (``Diagnostic Overview of Selection Schemes In Evolutionary Runs'') for empirically analyzing selection schemes.
The DOSSIER suite initially comprises eight handcrafted diagnostics, each designed to measure specific aspects of exploitation and exploration, and their interactions.
Exploitation is fundamentally hill-climbing, and we consider both unconstrained and constrained forms of exploitation.
Exploration is necessary when the optimization path through the search space is less clear; we divide exploration into two aspects: diversity exploration (the ability to simultaneously explore multiple pathways) and valley-crossing exploration (the ability to cross fitness valleys).
We apply our diagnostics to six popular selection schemes: truncation, tournament, fitness sharing, lexicase, nondominated sorting, and novelty search.
We found that simple schemes (\textit{e.g.}, tournament and truncation) emphasized exploitation, as expected from theoretical predictions.
For more sophisticated selection schemes, our diagnostics revealed interesting dynamics.
For example, lexicase selection performed moderately well across diagnostics that did not incorporate valley crossing, while fitness sharing was the only selection scheme to contend with valley crossing, but struggled with the other diagnostics.
Our work demonstrates the value of diagnostics for building an intuitive understanding of selection scheme characteristics, which can then be used to improve and develop new selection methods.

### TL;DR (_i.e._, the abstract is _sooo_ long and technical, what does it say in three sentences?)

- [Evolutionary algorithms](https://en.wikipedia.org/wiki/Evolutionary_algorithm) provide an effective general purpose technique for optimization problems and typically follow three phases: evaluation, selection, and reproduction.
- Each phase plays a crucial role in guiding an evolutionary search and interact with one another, making it difficult to isolate each individual components impact.
- We isolate the [selection scheme](https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)), and characterize its abilities on exploitation, exploration, and valley crossing with our set of diagnostic metrics.

## Diagnostic Problems

Our diagnostics use a handcrafted search space where each space possesses unique calculated features, topology, and fitness distribution; these diagnostics help us to disentangle how a selection scheme trade-offs between exploitation and exploration.
Some diagnostics can be minor alterations of other ones; if a selection scheme performs differently on such diagnostics, that difference can be attributed to the specific alteration, isolating the effect.
Each diagnostic specifies a transformation from a solution's numerical vector (genotype) of a designated dimensionality to an evalutated numerical vector (phenotype) of the same cardinality.
Specifically, our two exploitation focused diagnostics (exploitaiton rate diagnostic and ordered exploitation diagnostic) focus on measuring two different flavors of exploitation: pure exploitation and ordered exploitation.
Conversely, our two exploration focused diagnostics (contradictory objectives diagnostic and multi-path exploration diagnostic) focus on measuring two flavors of exploration: exploration of optima with a smooth gradient of similar fitness and exploration of optima, each with a sigle narrow gradient that leads to a differing fitness peak.
Additionally, we include a valley-crossing diagnostic that transforms a pre-evaluated phenotype into a new phenotype with integrated fitness vallyes.

- Exploitation Rate Diagnostic:
    - Measures a selection scheme's ability to exploit a smooth fitness gradient.
- Ordered Exploitation Diagnostic:
    - Measures a selection scheme's ability to pursue a single, narrow gradient that leads toward a single global optimum.
- Contradictory Objectives Diagnostic:
    - Measures a selection scheme's ability to locate and optimize conflicting objectives.
- Multi-path Exploration Diagnostic:
    - Measures a selection scheme's ability to maintain and simultaneously exploit multiple gradients of differing fitness peaks.
- Valley-crossing diagnostic:
    - Measures a selection scheme's ability to cross fitness valleys with search space toplogies from the previous four diagnostics.

## Selection Schemes

Below are the selection schemes analyzed in depth:

- Truncation Selection
- Tournament Selection
- Genotypic and Phenotypic Fitness Sharing
- Novelty Search
- Lexicase Selection
- Nondominated Sorting
- Random selection (control)

## Experimental Setup

We use a simple evolutionary algorithm to diagnose a selection scheme's abilities.
We repeat the evolutionary cycle below for 50,000 generations with a population of 512 solutions.
Once a selection scheme determines the set of parents, each parent reproduces asexually and point mutations are applied to offspring.
Point mutations consist of numbers from a normal distribution with a mean of 0.0 and standard deviation of 1.0.
Note that the completion of each cycle is one generation.

1. **Evaluate** all candidate solutions on a given diagnostic
2. **Select** parents from population of candidate solutions
3. **Reproduce** offspring asexually from each identified parent

## Experiment Source Code

The source code and configs for this work be found here: [Source/](https://github.com/jgh9094/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/tree/main/Source).

This work is implemented in C++ using the [Empirical library](https://github.com/devosoft/Empirical), which is required to compile and re-run the experiments.

**WARNING:** the Empirical library is under development, and as a result, it can often change in ways that may break the code used for the experiments used in this work.
I make no promises that I will keep these problems up to date with the latest changes to the Empirical library.
However, **I am more than happy to update the code upon request**.
Just submit an issue/email me (jgh9094@gmail.com).

## Results

We conduct three sets of experiments in our work.
Each focuses on a different set analysis.

1. [Base diagnostics](https://jgh9094.github.io/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/Base-Diagnostics/):
    - We evalate the previously mentioned selection schemes on the exploitaiton rate, ordered exploitaiton, contradictory obejctives, and multi-path exploration diagnositcs.

2. [Valley crossing diagnostics](https://jgh9094.github.io/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/MVC-Diagnostics/):
    - We evalate the previously mentioned selection schemes on the exploitaiton rate, ordered exploitaiton, contradictory obejctives, and multi-path exploration diagnositcs with valleys integrated through the valley-crossing diagnostics.

3. [Selection scheme parameter sweep](https://jgh9094.github.io/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/Selection-Scheme-Parameter-Sweep/):
    - We evalate different parameterization of the previously mentioned selection schemes on the exploitaiton rate, ordered exploitaiton, contradictory obejctives, and multi-path exploration diagnositcs.

## Reference

Hernandez, J. G., Lalejini, A., & Ofria, C. (2022). A suite of diagnostic metrics for characterizing selection schemes. arXiv preprint arXiv:2204.13839.