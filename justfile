# https://just.systems

run:
    uv run src/run_simulation.py --config config/example.yaml

plot:
    uv run src/plot_simulation.py --config config/example.yaml

run-all:
    uv run src/run_simulation.py --config config/circulant_4n.yaml
    uv run src/run_simulation.py --config config/circulant_8n.yaml
    uv run src/run_simulation.py --config config/complete.yaml
    uv run src/run_simulation.py --config config/lattice.yaml
    uv run src/run_simulation.py --config config/scale_free_100.yaml
    uv run src/run_simulation.py --config config/scale_free_410.yaml
    uv run src/run_simulation.py --config config/infect_dublin.yaml

plot-all:
    uv run src/plot_simulation.py --config config/circulant_4n.yaml
    uv run src/plot_simulation.py --config config/circulant_8n.yaml
    uv run src/plot_simulation.py --config config/complete.yaml
    uv run src/plot_simulation.py --config config/lattice.yaml
    uv run src/plot_simulation.py --config config/scale_free_100.yaml
    uv run src/plot_simulation.py --config config/scale_free_410.yaml
    uv run src/plot_simulation.py --config config/infect_dublin.yaml
