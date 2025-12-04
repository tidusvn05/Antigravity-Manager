# -*- coding: utf-8 -*-
import os
import sys
import platform
from pathlib import Path
from datetime import datetime

# -------------------------------------------------------------------------
# Công cụ ghi log
# -------------------------------------------------------------------------

def get_log_file_path():
    """Lấy đường dẫn file log"""
    try:
        log_dir = get_app_data_dir()
        return log_dir / "app.log"
    except:
        return None

def _log_to_file(message):
    """Ghi log vào file"""
    try:
        log_file = get_log_file_path()
        if log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
    except:
        pass

def _print_with_color(color_code, symbol, message):
    """Hàm in có màu, đồng thời ghi vào file"""
    formatted_msg = f"{symbol} {message}"
    # Trong chế độ không có console, sys.stdout có thể là None, in trực tiếp sẽ báo lỗi
    if sys.stdout:
        try:
            print(f"\033[{color_code}m{formatted_msg}\033[0m")
        except:
            pass
    _log_to_file(formatted_msg)

def info(message):
    """In log thông tin (màu xanh lá)"""
    _print_with_color("32", "INFO", message)

def warning(message):
    """In log cảnh báo (màu vàng)"""
    _print_with_color("33", "WARN", message)

def error(message):
    """In log lỗi (màu đỏ)"""
    _print_with_color("31", "ERR ", message)

def debug(message):
    """In log debug (màu xám)"""
    # Chỉ in khi biến môi trường DEBUG được thiết lập
    if os.environ.get("DEBUG"):
        _print_with_color("90", "DBUG", message)
    else:
        # Trong ứng dụng đóng gói, chúng ta cũng muốn ghi thông tin debug vào file để tiện kiểm tra
        _log_to_file(f"DBUG {message}")

# -------------------------------------------------------------------------
# Công cụ đường dẫn
# -------------------------------------------------------------------------

def get_app_data_dir():
    """Lấy thư mục dữ liệu ứng dụng (~/.antigravity-agent)"""
    home = Path.home()
    config_dir = home / ".antigravity-agent"
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_accounts_file_path():
    """Lấy đường dẫn file lưu trữ tài khoản"""
    return get_app_data_dir() / "antigravity_accounts.json"

def get_antigravity_db_paths():
    """Lấy các đường dẫn có thể có của cơ sở dữ liệu Antigravity"""
    system = platform.system()
    paths = []
    home = Path.home()

    if system == "Darwin":  # macOS
        # Đường dẫn chuẩn: ~/Library/Application Support/Antigravity/User/globalStorage/state.vscdb
        paths.append(home / "Library/Application Support/Antigravity/User/globalStorage/state.vscdb")
        # Đường dẫn dự phòng (vị trí có thể ở phiên bản cũ)
        paths.append(home / "Library/Application Support/Antigravity/state.vscdb")
    elif system == "Windows":
        # Đường dẫn chuẩn: %APPDATA%/Antigravity/state.vscdb
        appdata = os.environ.get("APPDATA")
        if appdata:
            base_path = Path(appdata) / "Antigravity"
            # Tham khảo cấu trúc đường dẫn của cursor_reset.py
            paths.append(base_path / "User/globalStorage/state.vscdb")
            paths.append(base_path / "User/state.vscdb")
            paths.append(base_path / "state.vscdb")
    elif system == "Linux":
        # Đường dẫn chuẩn: ~/.config/Antigravity/state.vscdb
        paths.append(home / ".config/Antigravity/state.vscdb")
    
    return paths

def get_antigravity_executable_path():
    """Lấy đường dẫn file thực thi Antigravity"""
    system = platform.system()
    
    if system == "Darwin":
        return Path("/Applications/Antigravity.app/Contents/MacOS/Antigravity")
    elif system == "Windows":
        # Tham khảo logic tìm kiếm của cursor_reset.py
        local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
        program_files = Path(os.environ.get("ProgramFiles", "C:\\Program Files"))
        program_files_x86 = Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"))
        
        possible_paths = [
            local_app_data / "Programs/Antigravity/Antigravity.exe",
            program_files / "Antigravity/Antigravity.exe",
            program_files_x86 / "Antigravity/Antigravity.exe"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
                
        # Fallback to default if nothing found (though likely won't exist)
        return local_app_data / "Programs/Antigravity/Antigravity.exe"
        
    elif system == "Linux":
        return Path("/usr/share/antigravity/antigravity")
    
    return None

def open_uri(uri):
    """Mở giao thức URI đa nền tảng
    
    Args:
        uri: URI cần mở, ví dụ "antigravity://oauth-success"
        
    Returns:
        bool: Khởi động thành công hay không
    """
    import subprocess
    system = platform.system()
    
    try:
        if system == "Darwin":
            # macOS: Sử dụng lệnh open
            subprocess.Popen(["open", uri])
        elif system == "Windows":
            # Windows: Sử dụng lệnh start
            # CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(["cmd", "/c", "start", "", uri], shell=False, creationflags=0x08000000)
        elif system == "Linux":
            # Linux: Sử dụng xdg-open
            subprocess.Popen(["xdg-open", uri])
        else:
            error(f"Hệ điều hành không được hỗ trợ: {system}")
            return False
        
        return True
    except Exception as e:
        error(f"Mở URI thất bại: {e}")
        return False
