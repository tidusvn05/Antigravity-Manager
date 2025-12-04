# 🚀 Antigravity Manager (Trình quản lý tài khoản Antigravity)

> **Công cụ quản lý đa tài khoản Antigravity hiện đại được thiết kế cho macOS & Windows**

Antigravity Manager là một công cụ hỗ trợ mạnh mẽ, được thiết kế để giải quyết vấn đề khó khăn khi client Antigravity không hỗ trợ chuyển đổi đa tài khoản một cách tự nhiên. Bằng cách tiếp quản trạng thái cấu hình của ứng dụng, nó cho phép người dùng chuyển đổi liền mạch giữa vô số tài khoản chỉ với một cú nhấp chuột, đồng thời cung cấp tính năng tự động sao lưu, bảo vệ tiến trình và giao diện quản lý trực quan.

---

## ✨ Tính năng cốt lõi

### 🛡️ Bảo mật và Quản lý tài khoản
*   **Snapshot tài khoản không giới hạn**: Tạo số lượng bản sao lưu tài khoản tùy ý, lưu giữ đầy đủ thông tin đăng nhập, cấu hình người dùng và trạng thái cục bộ.
*   **Nhận diện thông minh**: Tự động đọc email và ID của tài khoản đang đăng nhập từ cơ sở dữ liệu, không cần nhập thủ công.
*   **Cơ chế tự động sao lưu**:
    *   **Sao lưu khi khởi động**: Tự động sao lưu trạng thái hiện tại mỗi khi khởi động trình quản lý để tránh ghi đè ngẫu nhiên.
    *   **Sao lưu khi chuyển đổi**: Tự động lưu trạng thái mới nhất của tài khoản hiện tại trước khi chuyển sang tài khoản khác.
*   **Metadata chi tiết**: Ghi lại thời gian tạo, thời gian sử dụng cuối cùng, email và ID duy nhất cho mỗi bản lưu trữ.

### ⚡️ Trải nghiệm liền mạch
*   **Chuyển đổi một chạm**: Chỉ cần nhấp một lần để hoàn tất quy trình "Đóng ứng dụng -> Thay thế dữ liệu -> Khởi động lại ứng dụng".
*   **Bảo vệ tiến trình**:
    *   **Thoát an toàn**: Ưu tiên sử dụng AppleScript (macOS) hoặc taskkill (Windows) để thông báo cho ứng dụng thoát bình thường, bảo vệ tính toàn vẹn của dữ liệu.
    *   **Buộc dừng dự phòng**: Nếu ứng dụng bị treo, sẽ tự động nâng cấp lên chiến lược buộc dừng để đảm bảo chuyển đổi thành công.
*   **Hỗ trợ đa nền tảng**: Tương thích hoàn hảo với macOS (Intel/Apple Silicon) và Windows 10/11.

### 🎨 Giao diện hiện đại
*   **Flet Driver**: GUI hiệu suất cao dựa trên Flutter, phản hồi nhanh chóng.
*   **Tích hợp tự nhiên**: Tự động thích ứng với chế độ tối/sáng của hệ thống, mang lại trải nghiệm cửa sổ tự nhiên.
*   **Tương tác thân thiện**: Chế độ xem danh sách rõ ràng, các nút thao tác trực quan và cửa sổ bật lên xác nhận thân thiện.

---

## 🛠️ Bắt đầu nhanh

### Yêu cầu môi trường
*   **Hệ điều hành**: macOS 10.15+ hoặc Windows 10+
*   **Python**: 3.10 hoặc cao hơn
*   **Antigravity**: Phải được cài đặt và chạy ít nhất một lần

### 1. Cài đặt phụ thuộc
Chạy lệnh sau trong thư mục gốc của dự án để cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

#### 🖥️ Chế độ giao diện đồ họa (GUI) - Khuyên dùng
Khởi động giao diện đồ họa để trải nghiệm đầy đủ các tính năng tương tác:

```bash
# macOS / Linux
python gui/main.py

# Windows
python gui\main.py
```

#### ⌨️ Chế độ dòng lệnh (CLI)
Phù hợp cho tích hợp script hoặc người dùng chuyên sâu.

**Menu tương tác**:
```bash
python main.py
```

**Các lệnh thường dùng**:
```bash
# Liệt kê tất cả các bản lưu trữ
agr list

# Sao lưu tài khoản hiện tại (tự động lấy tên)
agr add

# Sao lưu với tên chỉ định
agr add -n "Tài khoản công việc"

# Chuyển đổi tài khoản (sử dụng số thứ tự hoặc UUID)
agr switch 1

# Xóa bản sao lưu
agr delete 1
```

---

## 🔧 Cài đặt lệnh toàn cục (macOS)

Để có thể gọi các lệnh `agr` và `agr-ui` từ bất kỳ đâu trong terminal mà không cần vào thư mục source, bạn có thể sử dụng script cài đặt tự động:

### Cài đặt

```bash
# 1. Cấp quyền thực thi cho script cài đặt
chmod +x install_macos.sh

# 2. Chạy script cài đặt (sẽ yêu cầu mật khẩu sudo)
./install_macos.sh
```

Script sẽ tự động:
- ✅ Kiểm tra và thiết lập Python virtual environment
- ✅ Cài đặt tất cả dependencies
- ✅ Tạo symlink tại `/usr/local/bin`

### Sử dụng

Sau khi cài đặt, bạn có thể sử dụng các lệnh sau từ **bất kỳ đâu** trong terminal:

```bash
# Khởi động GUI
agr-ui

# Liệt kê tất cả tài khoản
agr list

# Thêm tài khoản mới
agr add

# Thêm tài khoản với tên chỉ định
agr add -n "Tài khoản công việc"

# Chuyển đổi tài khoản
agr switch 1

# Xóa tài khoản
agr delete 1

# Xem tất cả lệnh có sẵn
agr --help
```
    
### Gỡ cài đặt

Nếu muốn gỡ bỏ các lệnh toàn cục:

```bash
# Cấp quyền và chạy script gỡ cài đặt
chmod +x uninstall_macos.sh
./uninstall_macos.sh
```

**Lưu ý**: Script gỡ cài đặt chỉ xóa symlink, không xóa virtual environment và dữ liệu tài khoản.

---

## 📦 Đóng gói và Triển khai

Dự án này tích hợp sẵn các script xây dựng tự động, có thể tạo ra các tệp thực thi độc lập không cần môi trường Python.

### 🍎 Đóng gói cho macOS
Xây dựng ứng dụng `.app` và gói cài đặt `.dmg`.

```bash
# 1. Cấp quyền thực thi cho script
chmod +x build_macos.sh

# 2. Chạy xây dựng
./build_macos.sh
```
*   **Đường dẫn sản phẩm**: `gui/build/macos/`
*   **Bao gồm**: `Antigravity Manager.app`, `Antigravity Manager.dmg`
*   **Kiến trúc**: Universal Binary (Hỗ trợ Intel & M1/M2/M3)

### 🪟 Đóng gói cho Windows
Xây dựng chương trình thực thi `.exe` đơn file.

```powershell
# Chạy trong PowerShell
./build_windows.ps1
```
*   **Đường dẫn sản phẩm**: `dist/`
*   **Bao gồm**: `Antigravity Manager.exe`
*   **Đặc điểm**: Không có cửa sổ console đen, chạy đơn file di động.

---

## 🧩 Kiến trúc kỹ thuật

### Cấu trúc thư mục
```
antigravity_manager/
├── assets/                 # Tài nguyên tĩnh (icon, v.v.)
├── gui/                    # Kho mã nguồn cốt lõi
│   ├── main.py             # Điểm nhập GUI
│   ├── account_manager.py  # Logic tài khoản (CRUD)
│   ├── process_manager.py  # Kiểm soát tiến trình (quản lý tiến trình đa nền tảng)
│   ├── db_manager.py       # Lưu trữ dữ liệu (thao tác tệp)
│   ├── views/              # Thành phần giao diện UI
│   └── utils.py            # Các lớp tiện ích chung
├── main.py                 # Điểm nhập CLI
├── build_macos.sh          # Script xây dựng macOS
├── build_windows.ps1       # Script xây dựng Windows
└── requirements.txt        # Phụ thuộc Python
```

### Lưu trữ dữ liệu
*   **Tệp cấu hình**: `~/.antigravity-agent/accounts.json` (lưu trữ chỉ mục danh sách tài khoản)
*   **Dữ liệu sao lưu**: `~/.antigravity-agent/backups/*.json` (snapshot dữ liệu tài khoản thực tế)
*   **Tệp nhật ký**: `~/.antigravity-agent/app.log`

---

## ❓ Câu hỏi thường gặp (FAQ)

**Q: Sau khi chuyển đổi tài khoản, Antigravity không tự động khởi động?**
A: Vui lòng đảm bảo Antigravity được cài đặt tại đường dẫn tiêu chuẩn (`/Applications` cho macOS, thư mục cài đặt mặc định cho Windows). Nếu sử dụng đường dẫn tùy chỉnh, chương trình sẽ cố gắng khởi động thông qua giao thức URI (`antigravity://`).

**Q: Tệp sao lưu được lưu ở đâu?**
A: Tất cả dữ liệu được lưu trong thư mục `.antigravity-agent` tại thư mục chính của người dùng. Bạn có thể sao lưu thủ công thư mục này bất cứ lúc nào.

**Q: Tại sao phần mềm diệt virus trên Windows báo cáo là virus?**
A: Các tệp exe đơn file được đóng gói bằng PyInstaller đôi khi bị báo cáo sai. Đây là vấn đề đã biết của PyInstaller. Vui lòng thêm ứng dụng vào danh sách trắng hoặc chạy trực tiếp bằng mã nguồn Python.

---

## 📄 Giấy phép

Dự án này sử dụng giấy phép MIT. Hoan nghênh gửi Issue và Pull Request.

Copyright (c) 2025 Ctrler. All rights reserved.
