import os
import sys
import argparse
from seir_graph import SEIRGraph
from seir_config import SEIRConfig


def run_simulation(config: SEIRConfig):
    print("Running simulation for " + config.exp_name)
    print("Number of runs: " + str(config.num_runs))
    for i in range(config.num_runs):
        config.out_dir = "out/" + config.exp_name + "/run_" + str(i) + "/"
        os.makedirs(config.out_dir, exist_ok=True)
        os.makedirs(config.out_dir + "graph_state/", exist_ok=True)
        os.makedirs(config.out_dir + "graph_images/", exist_ok=True)
        graph = SEIRGraph(config)
        graph.run()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config", type=str, help="Path to config file")

    args = argparser.parse_args()
    run_simulation(SEIRConfig(args.config))
