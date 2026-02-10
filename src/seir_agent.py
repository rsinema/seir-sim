from enum import Enum
import math

import numpy as np

class SEIRState(Enum):
    SUSCEPTIBLE = 0
    EXPOSED = 1
    INFECTIOUS = 2
    RECOVERED = 3

color_map = {
    SEIRState.SUSCEPTIBLE: "blue",
    SEIRState.EXPOSED: "yellow",
    SEIRState.INFECTIOUS: "red",
    SEIRState.RECOVERED: "green"
}

class SEIRAgent:
    def __init__(self, agent_id, p1_c = 0.12, beta = -0.00504):
        self.agent_id = agent_id
        self.beta = beta
        self.p_1c = p1_c

        # sample from a lognormal distribution for exposed state duration
        mu_e = 1.0
        sigma_e = 1.0
        self.countdown_to_infectious = math.ceil(np.random.lognormal(mu_e, sigma_e))

        # sample from a lognormal distribution for infectious state duration
        mu_i = 2.25
        sigma_i = 0.105
        self.countdown_to_recovered = math.ceil(np.random.lognormal(mu_i, sigma_i))

        self.days_spent_infectious = 0
        self.state = SEIRState.SUSCEPTIBLE
        self.neighbors = []
    
    def set_neighbors(self, neighbors: list):
        self.neighbors = neighbors

    def get_infectious_prob(self):
        d = self.days_spent_infectious

        numerator = (self.p_1c / (1 - self.p_1c)) * np.exp(self.beta * (d**3 - 1))
        denominator = 1 + numerator
        prob_infect = numerator / denominator

        return prob_infect

    def step(self):
        if self.state == SEIRState.SUSCEPTIBLE:
            # check neighbors
            for neighbor in self.neighbors:
                if neighbor.state == SEIRState.INFECTIOUS:
                    if np.random.random() < self.get_infectious_prob():
                        self.state = SEIRState.EXPOSED
                        break
        elif self.state == SEIRState.EXPOSED:
            # decrement countdown
            self.countdown_to_infectious -= 1
            # check if exposed agent becomes infectious
            if self.countdown_to_infectious == 0:
                self.state = SEIRState.INFECTIOUS
        elif self.state == SEIRState.INFECTIOUS:
            # increment days spent infectious
            self.days_spent_infectious += 1
            # decrement countdown
            self.countdown_to_recovered -= 1
            # check if infectious agent recovers
            if self.countdown_to_recovered == 0:
                self.state = SEIRState.RECOVERED
        elif self.state == SEIRState.RECOVERED:
            pass

    def __str__(self):
        return f"Agent {self.agent_id}: {self.state.name}"

if __name__ == "__main__":
    agent = SEIRAgent(SEIRState.INFECTIOUS)
    print(agent.get_infectious_prob())