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

    # Calculate statistics
    peak_infections = np.max(i_all, axis=1)  # Peak for each run
    peak_timesteps = np.argmax(i_all, axis=1)  # Timestep of peak for each run
    never_infected = s_all[:, -1]  # Susceptible at final timestep for each run

    mean_peak_infections = np.mean(peak_infections)
    mean_peak_timestep = np.mean(peak_timesteps)
    mean_never_infected = np.mean(never_infected)

    # Create figure with main plot and space for text box on the right
    fig, ax = plt.subplots(figsize=(12, 6))

    for data, label, color in datasets:
        mean = np.mean(data, axis=0)
        q25 = np.quantile(data, 0.25, axis=0)
        q75 = np.quantile(data, 0.75, axis=0)

        ax.plot(steps, mean, label=label, color=color)
        ax.fill_between(steps, q25, q75, color=color, alpha=0.2)

    ax.set_title(f"SEIR Model - {config.exp_name}")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Count")
    ax.legend()

    # Add statistics text box to the right of the plot
    stats_text = (
        f"Peak Infections (mean):\n  {mean_peak_infections:.1f}\n\n"
        f"Peak Timestep (mean):\n  {mean_peak_timestep:.1f}\n\n"
        f"Never Infected (mean):\n  {mean_never_infected:.1f}"
    )

    # Position text box on the right side
    fig.text(0.78, 0.5, stats_text, ha='left', va='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
             fontsize=9, family='monospace')

    plt.tight_layout(rect=[0, 0, 0.75, 1])
    plt.savefig(f"out/{config.exp_name}/plot.png")
    plt.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config", type=str, help="Path to config file")
    config = SEIRConfig(argparser.parse_args().config)
    plot_simulation(config)
