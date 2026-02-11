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

    # Arrays to store statistics from each run
    peak_infections_runs = []
    time_to_peak_runs = []
    never_infected_runs = []
    time_to_steady_state_runs = []
    max_degree_runs = []
    density_runs = []
    avg_degree_runs = []
    radius_runs = []
    diameter_runs = []

    for run_idx in range(config.num_runs):
        # Read peak infections and time to peak from graph_description.txt
        desc_path = f"out/{config.exp_name}/run_{run_idx}/graph_description.txt"
        with open(desc_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("Peak Infections:"):
                    peak_infections_runs.append(int(line.split(":")[1].strip()))
                elif line.startswith("Time to Peak:"):
                    time_to_peak_runs.append(int(line.split(":")[1].strip()))
                elif line.startswith("Uninfected nodes:"):
                    never_infected_runs.append(int(line.split(":")[1].strip()))
                elif line.startswith("Time to Steady State:"):
                    value = line.split(":")[1].strip()
                    if value == "Not reached":
                        time_to_steady_state_runs.append(None)
                    else:
                        time_to_steady_state_runs.append(int(value))
                elif line.startswith("Maximum Degree: "):
                    max_degree_runs.append(int(line.split(":")[1].strip()))
                elif line.startswith("Density: "):
                    density_runs.append(float(line.split(":")[1].strip()))
                elif line.startswith("Average Degree: "):
                    avg_degree_runs.append(float(line.split(":")[1].strip()))
                elif line.startswith("Radius: "):
                    radius_runs.append(float(line.split(":")[1].strip()))
                elif line.startswith("Diameter: "):
                    diameter_runs.append(float(line.split(":")[1].strip()))

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

    plt.tight_layout()
    plt.savefig(f"out/{config.exp_name}/plot.png")
    plt.close()

    # Calculate averages from the collected statistics
    avg_peak_infections = np.mean(peak_infections_runs)
    avg_time_to_peak = np.mean(time_to_peak_runs)
    avg_never_infected = np.mean(never_infected_runs)

    # Calculate average time to steady state (only for runs that reached it)
    steady_state_values = [t for t in time_to_steady_state_runs if t is not None]
    if steady_state_values:
        avg_time_to_steady_state = np.mean(steady_state_values)
        num_reached_steady_state = len(steady_state_values)
    else:
        avg_time_to_steady_state = None
        num_reached_steady_state = 0

    # Calculate average maximum degree
    max_degree_values = [d for d in max_degree_runs if d is not None]
    if max_degree_values:
        avg_max_degree = np.mean(max_degree_values)
    else:
        avg_max_degree = None
    
    # Calculate average density
    density_values = [d for d in density_runs if d is not None]
    if density_values:
        avg_density = np.mean(density_values)
    else:
        avg_density = None
    
    # Calculate average average degree
    avg_degree_values = [d for d in avg_degree_runs if d is not None]
    if avg_degree_values:
        avg_avg_degree = np.mean(avg_degree_values)
    else:
        avg_avg_degree = None
    
    # Calculate average radius
    radius_values = [r for r in radius_runs if r is not None]
    if radius_values:
        avg_radius = np.mean(radius_values)
    else:
        avg_radius = None
    
    # Calculate average diameter
    diameter_values = [d for d in diameter_runs if d is not None]
    if diameter_values:
        avg_diameter = np.mean(diameter_values)
    else:
        avg_diameter = None

    # Write statistics to a summary file
    summary_path = f"out/{config.exp_name}/experiment_statistics.txt"
    with open(summary_path, 'w') as f:
        f.write(f"Experiment: {config.exp_name}\n")
        f.write(f"Number of runs: {config.num_runs}\n")
        f.write(f"\n")
        f.write(f"Average Peak Infections: {avg_peak_infections:.2f}\n")
        f.write(f"Average Time to Peak: {avg_time_to_peak:.2f}\n")
        f.write(f"Average Never Infected: {avg_never_infected:.2f}\n")
        if avg_time_to_steady_state is not None:
            f.write(f"Average Time to Steady State: {avg_time_to_steady_state:.2f} ({num_reached_steady_state}/{config.num_runs} runs reached)\n")
        else:
            f.write(f"Average Time to Steady State: Not reached in any run\n")
        f.write(f"\n")
        f.write(f"Individual Run Statistics:\n")
        f.write(f"-" * 40 + "\n")
        for run_idx in range(config.num_runs):
            steady_state_str = str(time_to_steady_state_runs[run_idx]) if time_to_steady_state_runs[run_idx] is not None else "Not reached"
            f.write(f"Run {run_idx}: Peak Infections = {peak_infections_runs[run_idx]}, Time to Peak = {time_to_peak_runs[run_idx]}, Never Infected = {never_infected_runs[run_idx]}, Time to Steady State = {steady_state_str}\n")
        f.write(f"\n")
        f.write(f"Average Maximum Degree: {avg_max_degree:.5f}\n")
        f.write(f"Average Density: {avg_density:.5f}\n")
        f.write(f"Average Average Degree: {avg_avg_degree:.5f}\n")
        f.write(f"Average Radius: {avg_radius:.5f}\n")
        f.write(f"Average Diameter: {avg_diameter:.5f}\n")

    print(f"Experiment statistics written to {summary_path}")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config", type=str, help="Path to config file")
    config = SEIRConfig(argparser.parse_args().config)
    plot_simulation(config)
