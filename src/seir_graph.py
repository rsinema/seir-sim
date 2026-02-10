import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from seir_agent import SEIRState, SEIRAgent, color_map
from seir_config import GraphType, SEIRConfig
from seir_population_state import SEIRPopulationState

class SEIRGraph:
    def __init__(self, config: SEIRConfig):
        self.config = config
        self.seed = config.seed
        if self.seed is not None and self.config.set_seed:
            random.seed(self.seed)
        self.graph = self._build_graph()
        self.agents = [SEIRAgent(i, self.config.p1_c, self.config.beta) for i in range(self.graph.number_of_nodes())]
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
        self.peak_infections = 0
        self.time_to_peak = 0
        self.save_graph_state()
        if self.config.graph_type == GraphType.CIRCULANT:
            self.pos = nx.circular_layout(self.graph)
        elif self.config.graph_type == GraphType.COMPLETE:
            self.pos = nx.spring_layout(self.graph)
        elif self.config.graph_type == GraphType.LATTICE:
            self.pos = nx.spring_layout(self.graph)
        elif self.config.graph_type == GraphType.SCALE_FREE:
            self.pos = nx.spring_layout(self.graph)
        elif self.config.graph_type == GraphType.INFECT_DUBLIN:
            self.pos = nx.spring_layout(self.graph)
        self.draw_graph()

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
        if self.config.graph_type == GraphType.LATTICE:
            for node in self.graph.nodes:
                row, col = node
                neighbors = [self.agents[nr * self.config.lattice_cols + nc] for nr, nc in self.graph.neighbors(node)]
                self.agents[row * self.config.lattice_cols + col].set_neighbors(neighbors)
        elif self.config.graph_type == GraphType.INFECT_DUBLIN:
            for node in self.graph.nodes:
                neighbors_idx = list(self.graph.neighbors(node))
                neighbors = [self.agents[i-1] for i in neighbors_idx]
                self.agents[node-1].set_neighbors(neighbors)
        else:
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

        # Track peak infections
        current_infectious = sum(1 for agent in self.agents if agent.state == SEIRState.INFECTIOUS)
        if current_infectious > self.peak_infections:
            self.peak_infections = current_infectious
            self.time_to_peak = self.step_count

        self.save_graph_state()
        self.draw_graph()

    def run(self, num_steps: int = None):
        if num_steps is None:
            num_steps = self.config.num_steps
        for _ in range(num_steps):
            self.step()
        self.describe_graph()

    # save the population state at each step and then plot/animate it after simulation ends
    def save_graph_state(self):
        population_state = SEIRPopulationState()
        for i, agent in enumerate(self.agents):
            if agent.state == SEIRState.SUSCEPTIBLE:
                population_state.susceptible_nodes.append(i)
            elif agent.state == SEIRState.EXPOSED:
                population_state.exposed_nodes.append(i)
            elif agent.state == SEIRState.INFECTIOUS:
                population_state.infectious_nodes.append(i)
            elif agent.state == SEIRState.RECOVERED:
                population_state.recovered_nodes.append(i)
        population_state.save(self.config.out_dir + "graph_state/" + str(self.step_count) + ".json")

    def draw_graph(self):
        # save the graph image
        nx.draw(self.graph, self.pos, node_size=50, node_color=[color_map[agent.state] for agent in self.agents])
        plt.savefig(self.config.out_dir + "graph_images/" + str(self.step_count) + ".png")
        plt.close()

    def describe_graph(self):
        # Please include the following
        # information about each network: a figure or a description of the degree distribution, the maximum degree, the average degree, the diameter of the graph, the radius of the graph, and the density (connectance) of the graph

        # plot the degree distribution
        degrees = [self.graph.degree(node) for node in self.graph.nodes]
        plt.hist(degrees, bins=range(max(degrees) + 1))
        plt.xlabel("Degree")
        plt.ylabel("Frequency")
        plt.title("Degree Distribution")
        plt.savefig(self.config.out_dir + "degree_distribution.png")
        plt.close()

        def get_degree_count_dictionary(G):
            degree_counts = {}
            for node in G.nodes():
                degree = G.degree(node)
                if degree in degree_counts:
                    degree_counts[degree] += 1
                else:
                    degree_counts[degree] = 1
            return degree_counts

        degree_pairs: dict[int,int] = sorted(get_degree_count_dictionary(self.graph).items())
        x = [degree for degree, _ in degree_pairs]
        y = [count for _, count in degree_pairs]
        if 0 not in x:
            x.insert(0,0)
            y.insert(0,0)
        y = y / np.sum(y)
        plt.loglog(x,y,'b-o')
        plt.xlabel('Node degree')
        plt.ylabel('Probability')
        plt.savefig(self.config.out_dir + "degree_distribution_loglog.png")
        plt.close()

        def get_uninfected_nodes():
            uninfected_nodes = []
            for i, agent in enumerate(self.agents):
                if agent.state == SEIRState.SUSCEPTIBLE:
                    uninfected_nodes.append(i)
            return len(uninfected_nodes)

        # save the rest of the information to a file
        with open(self.config.out_dir + "graph_description.txt", "w") as f:
            f.write("Degree Distribution: " + str(degrees) + "\n")
            f.write("Maximum Degree: " + str(max(degrees)) + "\n")
            f.write("Average Degree: " + str(sum(degrees) / len(degrees)) + "\n")
            f.write("Diameter: " + str(nx.diameter(self.graph)) + "\n")
            f.write("Radius: " + str(nx.radius(self.graph)) + "\n")
            f.write("Density: " + str(nx.density(self.graph)) + "\n")
            f.write("Uninfected nodes: " + str(get_uninfected_nodes()) + "\n")
            f.write("Peak Infections: " + str(self.peak_infections) + "\n")
            f.write("Time to Peak: " + str(self.time_to_peak) + "\n")

if __name__ == "__main__":
    graph = SEIRGraph(SEIRConfig("config/example.yaml"))
    graph.run()