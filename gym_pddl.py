from collections import OrderedDict
import numpy as np
import os


class GymPDDL:
    def __init__(self, n_agents, n_enemies, output_dir="solutions"):
        self.state_dict = OrderedDict(
            {
                "max_x": np.zeros(
                    (1,),
                    dtype=np.uint8,
                ),
                "max_y": np.zeros(
                    (1,),
                    dtype=np.uint8,
                ),
                "min_y": np.zeros(
                    (1,),
                    dtype=np.uint8,
                ),
                "min_x": np.zeros(
                    (1,),
                    dtype=np.uint8,
                ),
                "health": np.zeros(
                    (n_agents + n_enemies,),
                    dtype=np.uint8,
                ),
                "shield": np.zeros(
                    (n_agents + n_enemies,),
                    dtype=np.uint8,
                ),
                "coordinate_x": np.zeros(
                    (n_agents + n_enemies,),
                    dtype=np.uint8,
                ),
                "coordinate_y": np.zeros(
                    (n_agents + n_enemies,),
                    dtype=np.uint8,
                ),
            }
        )

        self.state_dict["max_x"][0] = 0.5 * 100 + 50
        self.state_dict["max_y"][0] = 0.5 * 100 + 50
        self.state_dict["min_x"][0] = -0.5 * 100 + 50
        self.state_dict["min_y"][0] = -0.5 * 100 + 50

        self.n_agents = n_agents
        self.n_enemies = n_enemies

        self.decode_action = {
            0: "nop ",
            1: "stop ",
            2: "move_up ",
            3: "move_down ",
            4: "move_right ",
            5: "move_left ",
            6: "attack ",
        }
        self.num_agents = 5

        i = 0
        while os.path.exists(f"{output_dir}/pfile{i}.trajectory"):
            i += 1
        self.file = open(f"{output_dir}/pfile{i}.trajectory", "w")

    def state_into_dict(self, state):
        """takes the state and puts it into model"""
        j = self.n_agents * 7
        for agent_id in range(self.n_agents + self.n_enemies):
            if agent_id < self.n_agents:
                i = agent_id * 7
                coordinate_x = round(state[i + 2] + 5e-4, 2)
                coordinate_y = round(state[i + 3] + 5e-4, 2)
            else:
                i = j + (agent_id - self.n_agents) * 6
                coordinate_x = round(state[i + 1] + 5e-4, 2)
                coordinate_y = round(state[i + 2] + 5e-4, 2)

            health = round(state[i] + 5e-4, 2)
            self.state_dict["health"][agent_id] = health * 100
            self.state_dict["coordinate_x"][agent_id] = coordinate_x * 100 + 50
            self.state_dict["coordinate_y"][agent_id] = coordinate_y * 100 + 50

    def write_action(self, actions):
        self.file.write(f"(operators:")
        for i, action in enumerate(actions):
            if action == 0:
                self.file.write(f" (nop )")
            elif action >= 6:
                self.file.write(f" (attack agent{i} enemy{action-6+len(actions)-1})")
            else:
                self.file.write(f" ({self.decode_action[action]} agent{i})")
        self.file.write(f")\n")

    def write_state(self):
        self.file.write("(:state")
        self.save_state()

    def save_state(self):
        for state, value in self.state_dict.items():
            if len(value) == 1:
                self.file.write(f" (= ({state}) {value[0]})")
            else:
                for i in range(len(value)):
                    if i < self.n_agents:
                        self.file.write(f" (= ({state} agent{i}) {value[i]})")
                    else:
                        self.file.write(
                            f" (= ({state} enemy{i-self.n_agents}) {value[i]})"
                        )
        self.file.write(")\n")

    def start_record(self):
        self.file.write("((:init")
        self.save_state()

    def end_record(self):
        self.file.write(")")
        self.file.close()
