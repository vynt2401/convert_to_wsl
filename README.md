# Lab 3: Nén ảnh JPEG

# Giới thiệu: 

Repository này chứa nguyên bộ tài liệu và code từ lab "Nén ảnh JPEG" (Bài 3). Bao gồm các tài liệu PDF về lý thuyết DCT và BinDCT, hướng dẫn thực hành (Lab 3.pdf), code demo JPEG nén/giải nén, và code cho bài tập (câu 1-4: DCT thủ công, BinDCT loại C, zigzag thủ công, tính PSNR so sánh).
Mục tiêu lab: Tìm hiểu quy trình nén ảnh JPEG, bao gồm chuyển màu RGB sang YCbCr, chia khối 8x8, DCT/BinDCT, lượng tử hóa, zigzag, và mã hóa Huffman. Bài tập tập trung vào triển khai thủ công các phần cốt lõi và so sánh hiệu suất.
Repository được thiết kế để chạy trên Windows/Linux (với convert_to_wsl nếu cần WSL), sử dụng Anaconda/Spyder và Python 3.9.18.
Cấu trúc Repository

PDFs/: Các tài liệu lý thuyết và hướng dẫn.
binDCT1.pdf: Paper "The BinDCT: Fast Multiplierless Approximation of the DCT" bởi Trac D. Tran (1999). Giới thiệu họ BinDCT (A, B, C) – xấp xỉ DCT nhanh chỉ dùng shift/add, coding gain gần DCT (8.77-8.82 dB), ứng dụng lossy/lossless image coding.
binDCT.pdf: Paper "Fast Multiplierless Approximations of the DCT With the Lifting Scheme" bởi Jie Liang và Trac D. Tran (IEEE 2001). Chi tiết design BinDCT từ factorization Chen/Loeffler, lifting scheme, scaled DCT, ứng dụng JPEG/H.263+/lossless.

# Lab 3.pdf: Tài liệu thực hành. Bao gồm:

# Bài tập: 1 (DCT manual)
# Bài tập 2: (BinDCT explain/code type C)
# Bài tập 3: (zigzag manual)
# Bài tập: 4 (PSNR table for qualities 95/80/50/20, compare DCT vs BinDCT).

## Bash Script Enviroment
# Create env
# Linux 

Kiểm tra Python đã cài đặt chưa

'''
python --version
'''

# Install packages
pip install numpy==1.23.5 pillow==9.2.0 scipy==1.9.1 bitstream==2.6.0.2 matplotlib

# Install Spyder nếu cần (trong conda)
conda install spyder -y

echo "Setup hoàn tất. Activate env: conda activate python3918"
echo "Chạy Spyder: spyder"

Chạy: chmod +x setup.sh rồi ./setup.sh.
Note: Điều chỉnh version Anaconda nếu cần (check anaconda.com/downloads). Nếu trên Windows, dùng Anaconda Navigator.

Cách chạy Demo

Config Spyder: Run > Configuration per file > Command line options: "img1.ppm out.jpeg 96" (input PPM, output JPEG, quality 0-100).
Run encoder.py để nén.
Run decoder.py để giải nén (nếu có).

Bài tập
Câu 1: DCT thủ công
Triển khai DCT 2D thủ công cho block 8x8 (không dùng fftpack).
Câu 2: BinDCT

Giải thích flowgraph BinDCT A/B/C từ binDCT1.pdf (Hình 4-6), và chung từ binDCT.pdf (Hình 5).
Code BinDCT loại C (integer shift/add).

Câu 3: Zigzag thủ công
Triển khai zigzag scan/inverse (không dùng hàm sẵn).
Câu 4: Tính PSNR
Simulate nén/giải nén (DCT/BinDCT + quant + zigzag), tính PSNR cho qualities 95/80/50/20, bảng so sánh.
Code bài tập ở test_code.py (ví dụ PSNR table với ảnh test).
Kết quả mẫu
Với ảnh test (e.g., Lena PPM grayscale):






























QualityPSNR DCT Thủ côngPSNR BinDCT C9542.5 dB42.3 dB8038.2 dB38.0 dB5032.1 dB31.8 dB2025.4 dB25.0 dB
Lưu ý

Code dùng Python 3.9, test trên Spyder.
Nếu chạy chậm (e.g., DCT loop), vectorize bằng NumPy.
Liên hệ nếu lỗi env/pip.
