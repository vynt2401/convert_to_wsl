import numpy as np
import pandas as pd
from PIL import Image


# Câu 2: BinDCT loại C (giữ nguyên, nhanh sẵn)
def bin_dct_1d(x):
    tmp0 = x[0] + x[7]; tmp7 = x[0] - x[7]
    tmp1 = x[1] + x[6]; tmp6 = x[1] - x[6]
    tmp2 = x[2] + x[5]; tmp5 = x[2] - x[5]
    tmp3 = x[3] + x[4]; tmp4 = x[3] - x[4]
    tmp16 = ((tmp5 * 3) >> 3) + tmp6
    tmp15 = ((tmp16 * 5) >> 3) - tmp5
    tmp10 = tmp0 + tmp3; tmp13 = tmp0 - tmp3
    tmp11 = tmp1 + tmp2; tmp12 = tmp1 - tmp2
    tmp14 = tmp4 + tmp15; tmp15_ = tmp4 - tmp15
    z = tmp16
    tmp16_ = tmp7 - tmp16
    tmp17 = z + tmp7
    tmp14 = (tmp17 >> 3) - tmp14
    tmp10 = tmp10 + tmp11
    tmp11 = (tmp10 >> 1) - tmp11
    tmp12 = ((tmp13 * 3) >> 3) - tmp12
    tmp13 = ((tmp12 * 3) >> 3) + tmp13
    tmp15 = ((tmp16_ * 7) >> 3) + tmp15_
    tmp16_ = (tmp15 >> 1) - tmp16_
    out = np.zeros(8, dtype=np.int32)
    out[0] = tmp10
    out[4] = tmp11
    out[6] = tmp12
    out[2] = tmp13
    out[7] = tmp14
    out[5] = tmp15
    out[3] = tmp16_
    out[1] = tmp17
    return out

def bin_dct2(block):
    rows = np.zeros((8, 8), dtype=np.int32)
    for i in range(8):
        rows[i] = bin_dct_1d(block[i])
    out = np.zeros((8, 8), dtype=np.int32)
    for j in range(8):
        col = bin_dct_1d(rows[:, j])
        out[:, j] = col >> 3
    return out



#test với random ma trận 8x8
block = np.random.randint(0, 256, (8, 8))
print("random block: \n", block)
print("\n======================================\n")
dct_block = bin_dct2(block)
print("Bin DCT 2 block:\n", dct_block)
