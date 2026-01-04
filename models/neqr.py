from qiskit import QuantumCircuit
import math

def neqr_encode(image):
    num_pixels = image.size
    n = int(math.log2(num_pixels))

    qc = QuantumCircuit(n + 8)
    qc.h(range(n))

    pixels = (image.flatten() * 255).astype(int)
    for p in pixels:
        bits = format(p, "08b")
        for i, bit in enumerate(bits):
            if bit == "1":
                qc.x(n + i)

    return qc, n + 8
