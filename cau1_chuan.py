import numpy as np
import pandas as pd
from PIL import Image

# Câu 1: DCT thủ công vectorized (precompute cos, matrix multiply)
N = 8
x = np.arange(N)
cos_pre = np.cos((2 * x[:, None] + 1) * x * np.pi / 16)  # Cos matrix (N x N)
epsilon = np.ones((N, N)) / np.sqrt(N)
epsilon[0, :] /= np.sqrt(2)
epsilon[:, 0] /= np.sqrt(2)

def dct2(block):
    # Vectorized: F = epsilon * (cos_pre @ block @ cos_pre.T)
    temp = cos_pre @ block
    result = epsilon * (temp @ cos_pre.T)
    return result

def idct2(block):
    # Inverse: block = epsilon * block, then cos_pre.T @ block @ cos_pre
    temp = cos_pre.T @ (epsilon * block)
    result = temp @ cos_pre
    return result

#test với random ma trận 8x8
block = np.random.randint(0, 256, (8, 8))
print("random block: \n", block)
print("\n======================================\n")
dct_block = dct2(block)
print("DCT block:\n", dct_block)