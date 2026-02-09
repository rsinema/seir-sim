import os

from seir_graph import SEIRGraph
from seir_config import SEIRConfig


def run_simulation(config: SEIRConfig, num_runs: int):
    print("Running simulation for " + config.exp_name)
    print("Number of runs: " + str(num_runs))
    for i in range(num_runs):
        config.out_dir = "out/" + config.exp_name + "/run_" + str(i) + "/"
        os.makedirs(config.out_dir, exist_ok=True)
        os.makedirs(config.out_dir + "graph_state/", exist_ok=True)
        os.makedirs(config.out_dir + "graph_images/", exist_ok=True)
        graph = SEIRGraph(config)
        graph.run()

if __name__ == "__main__":
    run_simulation(SEIRConfig("config/circulant_4n.yaml"), 5)
