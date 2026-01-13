import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_CSV = "results/dataset_level_results.csv"
GRAPH_DIR = "results/graphs"

os.makedirs(GRAPH_DIR, exist_ok=True)

def plot_bar(metric, ylabel, title):
    df = pd.read_csv(RESULTS_CSV)

    models = df["Model"]
    values = df[metric]

    plt.figure(figsize=(11, 5))
    plt.bar(models, values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()

    path = f"{GRAPH_DIR}/{metric}.png"
    plt.savefig(path)
    plt.close()

    print(f"✔ Saved: {path}")

def generate_all_plots():

    plot_bar(
        metric="Qubit_Count",
        ylabel="Number of Qubits",
        title="Qubit Usage Comparison Across QIR Models"
    )

    plot_bar(
        metric="Circuit_Depth",
        ylabel="Circuit Depth",
        title="Circuit Depth Comparison Across QIR Models"
    )

    plot_bar(
        metric="Gate_Count",
        ylabel="Total Gates",
        title="Gate Count Comparison Across QIR Models"
    )

    plot_bar(
        metric="Encoding_Time_ms",
        ylabel="Encoding Time (ms)",
        title="Encoding Time Comparison Across QIR Models"
    )

    plot_bar(
        metric="Information_Loss",
        ylabel="Information Loss",
        title="Information Loss Across QIR Models"
    )

    plot_bar(
        metric="NISQ_Suitability",
        ylabel="NISQ Suitability Score",
        title="NISQ Suitability Comparison"
    )
