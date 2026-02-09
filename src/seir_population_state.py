import json


class SEIRPopulationState:
    def __init__(
        self,
    ):
        self.susceptible_nodes = []
        self.exposed_nodes = []
        self.infectious_nodes = []
        self.recovered_nodes = []
    
    def __str__(self):
        return f"Susceptible: {len(self.susceptible_nodes)}, Exposed: {len(self.exposed_nodes)}, Infectious: {len(self.infectious_nodes)}, Recovered: {len(self.recovered_nodes)}"
    
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    @classmethod
    def load(cls, file_path: str):
        with open(file_path, 'r') as f:
            return cls(**json.load(f))
