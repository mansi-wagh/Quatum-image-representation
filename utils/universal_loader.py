import numpy as np
from PIL import Image
from scipy.io import loadmat
import cv2
import os

def load_image_any(path, size=(4,4)):
    ext = os.path.splitext(path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        img = Image.open(path).convert("L")
        img = img.resize(size)
        arr = np.array(img, dtype=float)

    elif ext == ".mat":
        mat = loadmat(path)
        key = [k for k in mat.keys() if not k.startswith("__")][0]
        arr = mat[key]
        arr = cv2.resize(arr, size)

    else:
        raise ValueError("Unsupported format")

    arr = arr - arr.min()
    if arr.max() != 0:
        arr = arr / arr.max()

    return arr
