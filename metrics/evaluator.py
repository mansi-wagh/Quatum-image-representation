# metrics/evaluator.py

import numpy as np

class Evaluator:
    """
    Fast evaluator using analytical proxies.
    No expensive Qiskit graph operations.
    """

    def evaluate(self, image, qc, time_ms):
        qubits = qc.num_qubits
        gates = qc.size()

        # 🔥 FAST depth proxy (Strategy 2)
        circuit_depth = max(1, gates // max(1, qubits))

        recon_acc = 1 / (1 + qubits / image.size)
        pixel_acc = 1 / (1 + gates / image.size)
        info_loss = 1 - recon_acc

        return {
            "Qubit_Count": qubits,
            "Gate_Count": gates,
            "Circuit_Depth": circuit_depth,
            "Encoding_Time_ms": time_ms,

            "Gate_Fidelity_Impact": 1 / (1 + gates),
            "Noise_Robustness": 1 / (1 + circuit_depth),

            "PSNR": np.nan,
            "SSIM": np.nan,

            "Reconstruction_Accuracy": recon_acc,
            "Pixel_Accuracy": pixel_acc,
            "Information_Loss": info_loss,

            "Scalability_Image_Size": np.log2(image.size),
            "Scalability_Image_Count": 1 / image.size,
            "Memory_Efficiency": image.size / qubits,

            "Transformation_Supportability": 7,
            "NISQ_Suitability": 10 / (1 + circuit_depth)
        }
