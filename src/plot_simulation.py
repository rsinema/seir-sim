import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from seir_config import SEIRConfig
from seir_population_state import SEIRPopulationState


def plot_simulation(config: SEIRConfig):
    # Initialize arrays to hold counts for all runs: (num_runs, num_steps)
    s_all = np.zeros((config.num_runs, config.num_steps))
    e_all = np.zeros((config.num_runs, config.num_steps))
    i_all = np.zeros((config.num_runs, config.num_steps))
    r_all = np.zeros((config.num_runs, config.num_steps))

    for run_idx in range(config.num_runs):
        for step in range(config.num_steps):
            path = f"out/{config.exp_name}/run_{run_idx}/graph_state/{step}.json"
            state = SEIRPopulationState.load(path)
            s_all[run_idx, step] = len(state.susceptible_nodes)
            e_all[run_idx, step] = len(state.exposed_nodes)
            i_all[run_idx, step] = len(state.infectious_nodes)
            r_all[run_idx, step] = len(state.recovered_nodes)

    datasets = [
        (s_all, 'S', 'blue'),
        (e_all, 'E', 'orange'),
        (i_all, 'I', 'red'),
        (r_all, 'R', 'green')
    ]

    steps = np.arange(config.num_steps)
    for data, label, color in datasets:
        mean = np.mean(data, axis=0)
        q05 = np.quantile(data, 0.05, axis=0)
        q95 = np.quantile(data, 0.95, axis=0)
        
        plt.plot(steps, mean, label=label, color=color)
        plt.fill_between(steps, q05, q95, color=color, alpha=0.2)

    plt.title(f"SEIR Model - {config.exp_name}")
    plt.xlabel("Time Step")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig(f"out/{config.exp_name}/plot.png")
    plt.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config", type=str, help="Path to config file")
    config = SEIRConfig(argparser.parse_args().config)
    plot_simulation(config)
