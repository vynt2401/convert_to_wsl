import numpy as np
import pandas as pd
from PIL import Image
import cau1_chuan
import cau2_chuan
import cau3_chuan


height, width = 512, 512


original = np.array(Image.open('img1.ppm').convert('L'))


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
            if dct_func == cau2_chuan.bin_dct2:
                block = block.astype(np.int32) - 128
            else:
                block = block.astype(float) - 128
            dct_block = dct_func(block)
            zig = cau3_chuan.zigzag_scan(dct_block)
            q_zig = np.round(zig / quant.flatten())
            dq_zig = q_zig * quant.flatten()
            dq_block = cau3_chuan.inverse_zigzag_scan(dq_zig)
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
    recon_dct = simulate_compress_decompress(original, cau1_chuan.dct2, cau1_chuan.idct2, q)
    psnr_dct = psnr(original, recon_dct)
    recon_bin = simulate_compress_decompress(original, cau2_chuan.bin_dct2, cau1_chuan.idct2, q)
    psnr_bin = psnr(original, recon_bin)
    results.append((q, round(psnr_dct, 2), round(psnr_bin, 2)))

print("\n=======================================\n")



df = pd.DataFrame(results, columns=['Quality', 'PSNR DCT Thủ công', 'PSNR BinDCT C'])
print(df)