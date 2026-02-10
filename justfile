# https://just.systems

run:
    uv run src/run_simulation.py --config config/scale_free_100_p1c_0_06_i_4_5.yaml

plot:
    uv run src/plot_simulation.py --config config/scale_free_100_p1c_0_06_i_4_5.yaml

run-all:
    uv run src/run_simulation.py --config config/complete.yaml
    uv run src/run_simulation.py --config config/lattice.yaml
    uv run src/run_simulation.py --config config/scale_free_100.yaml
    uv run src/run_simulation.py --config config/scale_free_410.yaml
    uv run src/run_simulation.py --config config/infect_dublin.yaml
    uv run src/run_simulation.py --config config/complete_p1c_0_06_i_4_5.yaml
    uv run src/run_simulation.py --config config/infect_dublin_p1c_0_06_i_4_5.yaml
    uv run src/run_simulation.py --config config/lattice_p1c_0_06_i_4_5.yaml
    uv run src/run_simulation.py --config config/scale_free_100_p1c_0_06_i_4_5.yaml
    uv run src/run_simulation.py --config config/scale_free_410_p1c_0_06_i_4_5.yaml

plot-all:
    uv run src/plot_simulation.py --config config/complete.yaml
    uv run src/plot_simulation.py --config config/lattice.yaml
    uv run src/plot_simulation.py --config config/scale_free_100.yaml
    uv run src/plot_simulation.py --config config/scale_free_410.yaml
    uv run src/plot_simulation.py --config config/infect_dublin.yaml
    uv run src/plot_simulation.py --config config/complete_p1c_0_06_i_4_5.yaml
    uv run src/plot_simulation.py --config config/infect_dublin_p1c_0_06_i_4_5.yaml
    uv run src/plot_simulation.py --config config/lattice_p1c_0_06_i_4_5.yaml
    uv run src/plot_simulation.py --config config/scale_free_100_p1c_0_06_i_4_5.yaml
    uv run src/plot_simulation.py --config config/scale_free_410_p1c_0_06_i_4_5.yaml

animate-all:
    uv run src/animate_contagion.py -e complete
    uv run src/animate_contagion.py -e lattice
    uv run src/animate_contagion.py -e scale_free_100
    uv run src/animate_contagion.py -e scale_free_410
    uv run src/animate_contagion.py -e infect_dublin
    uv run src/animate_contagion.py -e complete_p1c_0_06_i_4_5
    uv run src/animate_contagion.py -e infect_dublin_p1c_0_06_i_4_5
    uv run src/animate_contagion.py -e lattice_p1c_0_06_i_4_5
    uv run src/animate_contagion.py -e scale_free_100_p1c_0_06_i_4_5
    uv run src/animate_contagion.py -e scale_free_410_p1c_0_06_i_4_5
