# Bin Directory

Thư mục này chứa các wrapper script cho phép gọi Antigravity Manager từ bất kỳ đâu trong terminal.

## Các file

### `agr`
Wrapper script cho CLI (Command Line Interface).

**Chức năng:**
- Tự động tìm đường dẫn đến thư mục project
- Sử dụng Python từ virtual environment (.venv)
- Gọi `main.py` với tất cả tham số được truyền vào

### `agr-ui`
Wrapper script cho GUI (Graphical User Interface).

**Chức năng:**
- Tự động tìm đường dẫn đến thư mục project
- Sử dụng Python từ virtual environment (.venv)
- Khởi động GUI bằng cách gọi `gui/main.py`

## Cách hoạt động

Các script này hoạt động theo cơ chế:

1. **Xác định đường dẫn**: Tự động phát hiện đường dẫn thư mục project dựa trên vị trí của script
2. **Kiểm tra môi trường**: Đảm bảo virtual environment và file Python cần thiết tồn tại
3. **Thực thi**: Chạy Python script với đường dẫn tuyệt đối

---

**Lưu ý**: Để biết cách cài đặt và sử dụng, vui lòng xem README.md ở thư mục gốc của project.
