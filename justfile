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

animate-all:
    uv run src/animate_contagion.py -e circulant_4n
    uv run src/animate_contagion.py -e circulant_8n
    uv run src/animate_contagion.py -e complete
    uv run src/animate_contagion.py -e lattice
    uv run src/animate_contagion.py -e scale_free_100
    uv run src/animate_contagion.py -e scale_free_410
    uv run src/animate_contagion.py -e infect_dublin
