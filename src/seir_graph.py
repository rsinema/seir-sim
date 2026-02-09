import random

import networkx as nx
import matplotlib.pyplot as plt

from seir_config import GraphType
from seir_agent import SEIRState, SEIRAgent
from seir_agent import color_map
from seir_config import SEIRConfig


class SEIRGraph:
    def __init__(self, config: SEIRConfig):
        self.config = config
        self.seed = config.seed
        random.seed(self.seed)
        self.agents = [SEIRAgent(i) for i in range(config.num_agents)]
        self.graph = self._build_graph()
        print(self.graph.nodes)

        # set the initial population based on the config
        
        # sample the initial population
        exposed_agents = random.sample(
            self.agents,
            int(self.config.num_agents * self.config.exposed_percent)
        )
        infectious_agents = random.sample(
            self.agents,
            int(self.config.num_agents * self.config.infectious_percent)
        )

        # set the initial state of the agents
        for agent in exposed_agents:
            agent.state = SEIRState.EXPOSED
        for agent in infectious_agents:
            agent.state = SEIRState.INFECTIOUS

        self._set_neighbors()

        self.susceptible_counts = []
        self.exposed_counts = []
        self.infectious_counts = []
        self.recovered_counts = []

        self.step_count = 0
        self._count_population()

    def _build_graph(self):
        if self.config.graph_type == GraphType.CIRCULANT:
            return nx.circulant_graph(self.config.num_agents, list(range(1, self.config.num_neighbors // 2 + 1)))
        elif self.config.graph_type == GraphType.COMPLETE:
            return nx.complete_graph(self.config.num_agents)
        elif self.config.graph_type == GraphType.LATTICE:
            return nx.grid_2d_graph(self.config.lattice_rows, self.config.lattice_cols)
        elif self.config.graph_type == GraphType.SCALE_FREE:
            return nx.barabasi_albert_graph(self.config.num_agents, self.config.m)
        elif self.config.graph_type == GraphType.INFECT_DUBLIN:
            return self._read_graph_from_file(self.config.dublin_path)

    def _read_graph_from_file(self, file_path: str):
        fo = open(file_path, 'r')
        line = fo.readline() # Read file header
        line = fo.readline() # Number of vertices and edges
        if not line:
            print('error -- illegal format for input')
            return
        v = line.split(" ")
        numVertices = int(v[0])
        G = nx.Graph()
        G.add_nodes_from(range(1,numVertices+1))
        while True:
            line = fo.readline()
            if not line:
                break
            v = line.split(" ")
            v1 = int(v[0])
            v2 = int(v[1])
            G.add_edge(v1,v2)
            G.add_edge(v2,v1)
        fo.close()
        return G

    def _set_neighbors(self):
        for node in self.graph.nodes:
            neighbors_idx = list(self.graph.neighbors(node))
            neighbors = [self.agents[i] for i in neighbors_idx]
            self.agents[node].set_neighbors(neighbors)

    def step(self):
        self.step_count += 1
        changed_nodes = []
        for i, agent in enumerate(self.agents):
            agent_state = agent.state
            agent.step()
            if agent_state != agent.state:
                changed_nodes.append(i)
        self._count_population()

    def run(self, num_steps):
        for _ in range(num_steps):
            self.step()

    def _count_population(self):
        susceptible_count = 0
        exposed_count = 0
        infectious_count = 0
        recovered_count = 0
        for agent in self.agents:
            if agent.state == SEIRState.SUSCEPTIBLE:
                susceptible_count += 1
            elif agent.state == SEIRState.EXPOSED:
                exposed_count += 1
            elif agent.state == SEIRState.INFECTIOUS:
                infectious_count += 1
            elif agent.state == SEIRState.RECOVERED:
                recovered_count += 1
        self.susceptible_counts.append(susceptible_count)
        self.exposed_counts.append(exposed_count)
        self.infectious_counts.append(infectious_count)
        self.recovered_counts.append(recovered_count)

    # save the population state at each step and then plot/animate it after simulation ends

if __name__ == "__main__":
    graph = SEIRGraph(SEIRConfig("config/example.yaml"))
    graph.step()