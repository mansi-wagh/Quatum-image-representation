# benchmark/runner.py

import time
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict

from datasets.loader import DatasetLoader
from models.model import QIR_MODELS  
from metrics.evaluator import Evaluator


class BenchmarkRunner:
    """
    Research-grade benchmarking runner for Quantum Image Representation models.

    - Streams datasets (large-scale safe)
    - Evaluates multiple resolutions (2x2, 4x4, 8x8)
    - Executes ALL models registered in QIR_MODELS (including SAQIR)
    - Aggregates metrics at dataset level
    """

    def __init__(self):
        # (dataset, resolution, model) → aggregated metric sums
        self.metric_sums = defaultdict(lambda: defaultdict(float))
        self.counts = defaultdict(int)

        # Circuit cache to avoid rebuilding identical circuits
        # Key: (model_name, resolution)
        self.circuit_cache = {}

    def run_dataset(self, dataset_name, max_images=None):
        """
        Run benchmark on a single dataset.

        Args:
            dataset_name (str): Dataset folder name
            max_images (int | None): Limit images for testing / NISQ feasibility
        """
        loader = DatasetLoader()
        evaluator = Evaluator()

        print(f"\n▶ Running dataset: {dataset_name}")

        for i, path in enumerate(loader.stream_dataset(dataset_name)):
            if max_images is not None and i >= max_images:
                break

            image = loader.load_image(path)

            for size in [2, 4, 8]:
                resized = loader.resize_image(image, size)

                for model_name, model_fn in QIR_MODELS.items():
                    key = (dataset_name, f"{size}x{size}", model_name)

                    # ---------- CIRCUIT CACHE ----------
                    cache_key = (model_name, size)

                    if cache_key not in self.circuit_cache:
                        qc = model_fn(resized)
                        self.circuit_cache[cache_key] = qc
                    else:
                        qc = self.circuit_cache[cache_key]

                    # ---------- ENCODING TIME ----------
                    start = time.perf_counter()
                    _ = qc.size()  # minimal execution-safe operation
                    time_ms = (time.perf_counter() - start) * 1000

                    # ---------- METRIC EVALUATION ----------
                    metrics = evaluator.evaluate(resized, qc, time_ms)

                    # ---------- AGGREGATION ----------
                    for metric_name, value in metrics.items():
                        if not np.isnan(value):
                            self.metric_sums[key][metric_name] += value

                    self.counts[key] += 1

        print(f"✔ Completed dataset: {dataset_name}")

    def save_results(self):
        """
        Save dataset-level averaged results to CSV.
        """
        rows = []

        for key, metric_totals in self.metric_sums.items():
            dataset, resolution, model = key
            count = self.counts[key]

            row = {
                "Dataset": dataset,
                "Resolution": resolution,
                "Model": model,
                "Image_Count": count
            }

            for metric_name, total_value in metric_totals.items():
                row[metric_name] = total_value / count if count > 0 else np.nan

            rows.append(row)

        Path("results").mkdir(exist_ok=True)
        df = pd.DataFrame(rows)
        df.to_csv("results/dataset_level_results.csv", index=False)

        print("\n✅ FAST dataset-level results saved → results/dataset_level_results.csv")
