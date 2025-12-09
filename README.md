# Lab 3: Nén ảnh JPEG

# Giới thiệu: 

Repository này chứa nguyên bộ tài liệu và code từ lab "Nén ảnh JPEG" (Bài 3). Bao gồm các tài liệu PDF về lý thuyết DCT và BinDCT, hướng dẫn thực hành (Lab 3.pdf), code demo JPEG nén/giải nén, và code cho bài tập (câu 1-4: DCT thủ công, BinDCT loại C, zigzag thủ công, tính PSNR so sánh).
Mục tiêu lab: Tìm hiểu quy trình nén ảnh JPEG, bao gồm chuyển màu RGB sang YCbCr, chia khối 8x8, DCT/BinDCT, lượng tử hóa, zigzag, và mã hóa Huffman. Bài tập tập trung vào triển khai thủ công các phần cốt lõi và so sánh hiệu suất.
Repository được thiết kế để chạy trên Windows/Linux (với convert_to_wsl nếu cần WSL), sử dụng Anaconda/Spyder và Python 3.9.18.
Cấu trúc Repository

PDFs/: Các tài liệu lý thuyết và hướng dẫn.
binDCT1.pdf: Paper "The BinDCT: Fast Multiplierless Approximation of the DCT" bởi Trac D. Tran (1999). Giới thiệu họ BinDCT (A, B, C) – xấp xỉ DCT nhanh chỉ dùng shift/add, coding gain gần DCT (8.77-8.82 dB), ứng dụng lossy/lossless image coding.
binDCT.pdf: Paper "Fast Multiplierless Approximations of the DCT With the Lifting Scheme" bởi Jie Liang và Trac D. Tran (IEEE 2001). Chi tiết design BinDCT từ factorization Chen/Loeffler, lifting scheme, scaled DCT, ứng dụng JPEG/H.263+/lossless.

## Lab 3.pdf: Tài liệu thực hành. Bao gồm:

### Bài tập: 1 (DCT manual)
### Bài tập 2: (BinDCT explain/code type C)
### Bài tập 3: (zigzag manual)
### Bài tập: 4 (PSNR table for qualities 95/80/50/20, compare DCT vs BinDCT).

### Có thể clone repos này về

```
git clone https://github.com/vynt2401/convert_to_wsl
```
--> sau đó trỏ đến thư mục chứa repos này

### Bash Script Enviroment
### Linux 

Kiểm tra Python đã cài đặt chưa

```
#Linux (ubuntu)
python --version
```

```
#Windows
python --version
```

Nếu chưa có, có thể cài đặt thông qua

```
#Linux (ubuntu)
sudo apt-get install python3
```

```
#Windows --> có thể tải tại đây
https://www.python.org/downloads/
```

Sau đó cài đặt Virtual Enviroment 
```
#Linux (ubuntu)
python3 -m pip install virtualenv 
```

Tạo Enviroment và kích hoạt Enviroment Python

```
#Linux (ubuntu)
virtualenv venv_name
source venv_name/bin/activate
```

```
#Windows
python -m venv venv_name
.\venv_name\Scripts\activate
```

Sau khi activate Enviroment --> tải các package cần thiết

```
#Windows
pip install -r .\requirement.txt

#Linux (ubuntu)
python -m pip install requirement.txt
```

Sau khi đã tải xong các package cần thiết --> chạy chương trình các câu 

```
#Windows
python .\cau1_chuan.py
python .\cau2_chuan.py
python .\cau3_chuan.py
python .\cau4_chuan.py


#Linux (ubuntu)

python3 cau1_chuan.py
python3 cau2_chuan.py
python3 cau3_chuan.py
python3 cau4_chuan.py
```

Bài tập
Câu 1: DCT thủ công
Triển khai DCT 2D thủ công cho block 8x8 (không dùng fftpack).

Câu 2: BinDCT
Giải thích flowgraph BinDCT A/B/C từ binDCT1.pdf (Hình 4-6), và chung từ binDCT.pdf (Hình 5).
Code BinDCT loại C (integer shift/add).

Câu 3: Zigzag thủ công
Triển khai zigzag scan/inverse (không dùng hàm sẵn).

Câu 4: Tính PSNR
Simulate nén/giải nén (DCT/BinDCT + quant + zigzag), tính PSNR cho qualities 95/80/50/20, tạo bảng so sánh.


Lưu ý

Code dùng Python 3.9.
Nếu chạy chậm (e.g., DCT loop), vectorize bằng NumPy.
Liên hệ thông qua Profile nếu lỗi env/pip.
