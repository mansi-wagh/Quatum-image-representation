# main.py

from benchmark.runner import BenchmarkRunner
from metrics.plots import generate_all_plots




def main():
    runner = BenchmarkRunner()

    # Full datasets now feasible
    runner.run_dataset("mnist_png", max_images=None)
    runner.run_dataset("sar", max_images=None)
    runner.run_dataset("brain_tumor", max_images=None)

    runner.save_results()

generate_all_plots()

if __name__ == "__main__":
    main()
