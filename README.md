# SEIR Model Contagion Simulation

This repo contains a simulation of the SEIR model for contagion spread on a graph.

This is for Project 1 for CS575 Graph Data Science at BYU.

## Figures

Figures for each experiment can be found in the `out/` directory under each experiment's folder.
Animations for each experiment can be found in the `animations/` directory under each experiment's folder.

## Experiments

5 network topologies are tested:

1. Complete
2. Lattice 10x10
3. Scale-Free (Barabasi-Albert) with 100 nodes and _m_ = 2
4. Scale-Free (Barabasi-Albert) with 410 nodes and _m_ = 2
5. Infect Dublin (real-world network found [here](https://networkrepository.com/ia-infect-dublin.php))

Each are tested with 2 different infection parameter sets:

1. $\textit{p}_{1c} = 0.12, \mu^{I} = 2.25$
2. $\textit{p}_{1c} = 0.06, \mu^{I} = 4.5$

Which represent the probability of infection on contact, and the average number of days an individual stays infected, respectively.

## Code

SEIR model and all code to generate figures is found in the `src/` directory.
