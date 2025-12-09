import numpy as np
import pandas as pd
from PIL import Image


# Ảnh test simulate (512x512 grayscale gradient, thay bằng ảnh thầy: np.array(Image.open('anh_thay.ppm').convert('L')))
height, width = 512, 512
#original = (255 * (np.linspace(0, 1, height)[:, np.newaxis] + np.linspace(0, 1, width)) / 2).astype(np.uint8)

original = np.array(Image.open('img1.ppm').convert('L'))

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

def inverse_zigzag_scan(zig):
    inv_block = np.zeros((8,8))
    for k, pos in enumerate(zig_order):
        inv_block[pos[0], pos[1]] = zig[k]
    return inv_block

# Bảng lượng tử (giữ nguyên)
quant_luma = np.array([
    [16, 11, 10, 16, 124, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

def get_quant_table(quality):
    if quality < 50:
        s = 5000 / quality
    else:
        s = 200 - 2 * quality
    return np.floor((s * quant_luma + 50) / 100).clip(1, 255)

# Hàm simulate (giữ nguyên, nhưng nhanh hơn nhờ DCT vectorized)
def simulate_compress_decompress(image, dct_func, idct_func, quality):
    h, w = image.shape
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8
    padded_image = np.pad(image, ((0, pad_h), (0, pad_w)), mode='edge')
    h_p, w_p = padded_image.shape
    quant = get_quant_table(quality)
    recon_p = np.zeros_like(padded_image, dtype=float)
    for i in range(0, h_p, 8):
        for j in range(0, w_p, 8):
            block = padded_image[i:i+8, j:j+8]
            if dct_func == bin_dct2:
                block = block.astype(np.int32) - 128
            else:
                block = block.astype(float) - 128
            dct_block = dct_func(block)
            zig = zigzag_scan(dct_block)
            q_zig = np.round(zig / quant.flatten())
            dq_zig = q_zig * quant.flatten()
            dq_block = inverse_zigzag_scan(dq_zig)
            idct_block = idct_func(dq_block) + 128
            recon_p[i:i+8, j:j+8] = np.clip(idct_block, 0, 255)
    recon = recon_p[:h, :w].astype(np.uint8)
    return recon

def psnr(original, reconstructed):
    mse = np.mean((original - reconstructed) ** 2)
    if mse == 0:
        return float('inf')
    max_val = 255.0
    return 10 * np.log10(max_val**2 / mse)

qualities = [95, 80, 50, 20]
results = []
for q in qualities:
    recon_dct = simulate_compress_decompress(original, dct2, idct2, q)
    psnr_dct = psnr(original, recon_dct)
    recon_bin = simulate_compress_decompress(original, bin_dct2, idct2, q)
    psnr_bin = psnr(original, recon_bin)
    results.append((q, round(psnr_dct, 2), round(psnr_bin, 2)))

df = pd.DataFrame(results, columns=['Quality', 'PSNR DCT Thủ công', 'PSNR BinDCT C'])
print(df)