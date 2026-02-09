

from seir_config import SEIRConfig
from seir_population_state import SEIRPopulationState

class SEIRPlotting:
    def __init__(self, config: SEIRConfig):
        self.config = config
        self.population_states = []

    def load_population_states(self):
        for i in range(self.config.num_steps + 1):
            self.population_states.append(
                SEIRPopulationState.load(self.config.out_dir + "graph_state/" + str(i) + ".json")
            )

    def plot_population_states(self):
        for i, population_state in enumerate(self.population_states):
            print(f"Step {i}: {population_state}")

    def plot_time_series(self):
        pass

if __name__ == "__main__":
    plotting = SEIRPlotting(SEIRConfig("config/example.yaml"))
    plotting.load_population_states()
    plotting.plot_population_states()