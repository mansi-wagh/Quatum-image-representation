from qiskit import QuantumCircuit
import math

def frqi_encode(image):
    num_pixels = image.size
    n = int(math.log2(num_pixels))

    qc = QuantumCircuit(n + 1)
    qc.h(range(n))

    for intensity in image.flatten():
        qc.ry(2 * intensity * math.pi, n)

    return qc, n + 1

