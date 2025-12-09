import numpy as np
import pandas as pd
from PIL import Image

# Câu 1: DCT thủ công
def get_epsilon(k):
    return 1 / np.sqrt(2) if k == 0 else 1

def dct2(block):
    N = block.shape[0]
    result = np.zeros((N, N))
    for u in range(N):
        for v in range(N):
            sum_val = 0.0
            for x_ in range(N):
                for y_ in range(N):
                    cos_x = np.cos((2 * x_ + 1) * u * np.pi / (2 * N))
                    cos_y = np.cos((2 * y_ + 1) * v * np.pi / (2 * N))
                    sum_val += block[x_, y_] * cos_x * cos_y
            result[u, v] = (2 / N) * get_epsilon(u) * get_epsilon(v) * sum_val
    return result

def idct2(block):
    N = block.shape[0]
    result = np.zeros((N, N))
    for x in range(N):
        for y in range(N):
            sum_val = 0.0
            for u in range(N):
                for v in range(N):
                    cos_x = np.cos((2 * x + 1) * u * np.pi / (2 * N))
                    cos_y = np.cos((2 * y + 1) * v * np.pi / (2 * N))
                    sum_val += get_epsilon(u) * get_epsilon(v) * block[u, v] * cos_x * cos_y
            result[x, y] = (2 / N) * sum_val
    return result





#test với random ma trận 8x8
block = np.random.randint(0, 256, (8, 8))
print("random block: \n", block)
print("\n======================================\n")
dct_block = dct2(block)
print("DCT block:\n", dct_block)
