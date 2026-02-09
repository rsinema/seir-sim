from enum import Enum
import os
import random

import yaml

class GraphType(Enum):
    CIRCULANT = "circulant"
    COMPLETE = "complete"
    LATTICE = "lattice"
    SCALE_FREE = "scale_free"
    INFECT_DUBLIN = "infect_dublin"
    
class SEIRConfig:
    def __init__(self, file_path: str):
        # read config in from yaml
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)

        self.config = config
        
        self.seed = config.get('seed')
        if self.seed is None:
            self.seed = random.randint(0, 1000000)
        self.exp_name = config.get('exp_name')
        self.num_agents = config['simulation']['num_agents']
        self.num_steps = config['simulation'].get('num_steps', 100)
        self.graph_type = GraphType(config['graph']['type'])
        self._extract_graph_config(self.graph_type)
        self.susceptible_percent = config['initial_population']['susceptible']
        self.exposed_percent = config['initial_population']['exposed']
        self.infectious_percent = config['initial_population']['infectious']

        self.out_dir = "out/" + self.exp_name + "/"
        os.makedirs(self.out_dir, exist_ok=True)
        os.makedirs(self.out_dir + "graph_state/", exist_ok=True)

    def _extract_graph_config(self, graph_type):
        if graph_type == GraphType.CIRCULANT:
            self.num_neighbors = self.config['graph']['neighbors']
        elif graph_type == GraphType.COMPLETE:
            pass
        elif graph_type == GraphType.LATTICE:
            self.lattice_rows = self.config['graph']['rows']
            self.lattice_cols = self.config['graph']['cols']
        elif graph_type == GraphType.SCALE_FREE:
            self.m = self.config['graph']['m']
        elif graph_type == GraphType.INFECT_DUBLIN:
            self.dublin_path = self.config['graph']['dublin_path']



if __name__ == "__main__":
    config = SEIRConfig("config/example.yaml")
    print(config.seed)
    print(config.exp_name)
    print(config.num_agents)
    print(config.num_steps)
    print(config.graph_type)
    print(config.num_neighbors)
    print(config.susceptible_percent)
    print(config.exposed_percent)
    print(config.infectious_percent)
    print(config.recovered_percent)
