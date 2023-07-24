[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project is a work in progress, we want to learn the PDDL domain of Starcraft. If you work on a numeric multi-agent solver for PDDL or want to contribute to this project, please feel free to connect us.

# Getting Started

First, you will need to install StarCraft II. On windows or mac, follow the instructions on the [StarCraft website](https://starcraft2.com/en-gb/). For linux, you can use the bash script [here](https://github.com/benellis3/mappo/blob/main/install_sc2.sh).

Then simply install SMAC as a package:

```bash
pip install git+https://github.com/oxwhirl/smacv2.git
```

For more additional information please see the original [oxwhirl/smacv2 reposetory](https://github.com/oxwhirl/smacv2#getting-started).

# Usage

We use the gym_pddl.py to translate the gym actions to a PDDL game trace (see solutions/pfile0.trajectory).
You can run main.py to see an example of play and a new trace generated.
