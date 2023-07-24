import numpy as np
from absl import logging
import time

from smacv2.env.starcraft2.wrapper import StarCraftCapabilityEnvWrapper

logging.set_verbosity(logging.DEBUG)

from gym_pddl import GymPDDL


def main():
    n_agents = 5
    n_enemies = 5

    distribution_config = {
        "n_units": n_agents,
        "team_gen": {
            "dist_type": "weighted_teams",
            "unit_types": ["marine"],
            "exception_unit_types": [""],
            "weights": [1],
            "observe": True,
        },
        "start_positions": {
            "dist_type": "reflect_position",
            "p": 0.5,
            "map_x": 32,
            "map_y": 32,
        },
        "n_enemies": n_enemies,
    }
    env = StarCraftCapabilityEnvWrapper(
        capability_config=distribution_config,
        map_name="10gen_terran",
        debug=False,
        conic_fov=False,
        obs_own_pos=True,
        use_unit_ranges=True,
        min_attack_range=2,
    )

    n_episodes = 1

    pddl = GymPDDL(n_agents, n_enemies)

    print("Training episodes")
    for e in range(n_episodes):
        env.reset()

        state = env.get_state()
        pddl.state_into_dict(state)
        pddl.start_record()

        terminated = False
        episode_reward = 0

        while not terminated:
            env.render()  # Uncomment for rendering

            actions = []
            for agent_id in range(n_agents):
                avail_actions = env.get_avail_agent_actions(agent_id)
                avail_actions_ind = np.nonzero(avail_actions)[0]
                action = np.random.choice(avail_actions_ind)
                actions.append(action)
            pddl.write_action(actions)
            reward, terminated, _ = env.step(actions)
            time.sleep(0.15)  # Comment for faster rendering
            episode_reward += reward

            state = env.get_state()
            pddl.state_into_dict(state)
            pddl.write_state()
        pddl.end_record()
        print("Total reward in episode {} = {}".format(e, episode_reward))


if __name__ == "__main__":
    main()
