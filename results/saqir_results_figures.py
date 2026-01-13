"""
SAQIR Preprocessing & Analysis Visualization
--------------------------------------------
This script generates a single, high-resolution, academic-quality figure with
three subplots illustrating the preprocessing and entropy analysis phase of the
SAQIR framework, using a synthetic SAR-like grayscale image.

Requirements:
- No external files
- Uses matplotlib, numpy, scipy
- One synthetic SAR-style input image
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy

# =========================
# Global plotting style (academic / Springer–IEEE friendly)
# =========================
plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 12,
    "axes.titlesize": 13,
    "figure.dpi": 300
})

# =========================
# Step 1: Generate a synthetic SAR-like image (256 x 256)
# =========================
np.random.seed(7)
N = 256

# Base smooth background (low entropy)
x = np.linspace(0, 1, N)
gradient = np.outer(x, x)

# High-entropy SAR-like speckle noise regions
speckle = np.random.rayleigh(scale=0.3, size=(N, N))

# Sharp edge / structure (simulating man-made objects)
checker = np.indices((N, N)).sum(axis=0) % 2
checker = checker * 0.6

# Combine regions
image = gradient.copy()
image[64:192, 64:192] += speckle[64:192, 64:192]
image[32:96, 160:224] += checker[32:96, 160:224]

# Normalize to [0,1]
image = image - image.min()
image = image / image.max()

# =========================
# Step 2: Partitioning and entropy computation
# =========================
block_size = 16
num_blocks = N // block_size
entropy_map = np.zeros((num_blocks, num_blocks))

for i in range(num_blocks):
    for j in range(num_blocks):
        block = image[
            i * block_size:(i + 1) * block_size,
            j * block_size:(j + 1) * block_size
        ]
        hist, _ = np.histogram(block.flatten(), bins=256, range=(0, 1), density=True)
        hist = hist[hist > 0]
        entropy_map[i, j] = entropy(hist, base=2)

# =========================
# Step 3: Visualization (3 subplots)
# =========================
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# --- (a) Input Image ---
ax = axes[0]
im0 = ax.imshow(image, cmap="gray")
ax.set_title("(a) Input Image")
ax.axis("off")

# --- (b) Block Partitioning ---
ax = axes[1]
ax.imshow(image, cmap="gray")
for k in range(0, N, block_size):
    ax.axhline(k - 0.5, color="cyan", linewidth=0.4)
    ax.axvline(k - 0.5, color="cyan", linewidth=0.4)
ax.set_title("(b) Block Partitioning")
ax.axis("off")

# --- (c) Entropy Heatmap ---
ax = axes[2]
im2 = ax.imshow(entropy_map, cmap="viridis")
ax.set_title("(c) Entropy Heatmap")
ax.axis("off")
cbar = fig.colorbar(im2, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Shannon Entropy (bits)")

plt.tight_layout()
plt.show()
