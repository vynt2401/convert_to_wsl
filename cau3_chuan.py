import numpy as np
import pandas as pd
from PIL import Image

# Câu 3: Zigzag (giữ nguyên)
zig_order = [
    (0,0), (0,1), (1,0), (2,0), (1,1), (0,2), (0,3), (1,2),
    (2,1), (3,0), (4,0), (3,1), (2,2), (1,3), (0,4), (0,5),
    (1,4), (2,3), (3,2), (4,1), (5,0), (6,0), (5,1), (4,2),
    (3,3), (2,4), (1,5), (0,6), (0,7), (1,6), (2,5), (3,4),
    (4,3), (5,2), (6,1), (7,0), (7,1), (6,2), (5,3), (4,4),
    (3,5), (2,6), (1,7), (2,7), (3,6), (4,5), (5,4), (6,3),
    (7,2), (7,3), (6,4), (5,5), (4,6), (3,7), (4,7), (5,6),
    (6,5), (7,4), (7,5), (6,6), (5,7), (6,7), (7,6), (7,7)
]

def zigzag_scan(block):
    return np.array([block[pos[0], pos[1]] for pos in zig_order])

block = np.arange(64).reshape(8,8)

print("Block:\n", block)

print("\n======================================\n")
zig = zigzag_scan(block)
print("Zigzag:\n", zig)


def inverse_zigzag_scan(zig):
    inv_block = np.zeros((8,8))
    for k, pos in enumerate(zig_order):
        inv_block[pos[0], pos[1]] = zig[k]
    return inv_block

print("\n======================================\n")
zig_inverse = inverse_zigzag_scan(zig)
print("\nZigzag Inverse:\n", zig_inverse)
