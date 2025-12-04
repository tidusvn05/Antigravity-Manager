# -*- coding: utf-8 -*-
import os
import time
import platform
import subprocess
import psutil

# Use relative imports
from utils import info, error, warning, get_antigravity_executable_path, open_uri

def is_process_running(process_name=None):
    """Kiểm tra xem tiến trình Antigravity có đang chạy không
    
    Sử dụng phương pháp phát hiện đa nền tảng:
    - macOS: Kiểm tra đường dẫn chứa Antigravity.app
    - Windows: Kiểm tra tên tiến trình hoặc đường dẫn chứa antigravity
    - Linux: Kiểm tra tên tiến trình hoặc đường dẫn chứa antigravity
    """
    system = platform.system()
    
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_name_lower = proc.info['name'].lower() if proc.info['name'] else ""
            exe_path = proc.info.get('exe', '').lower() if proc.info.get('exe') else ""
            
            # Phát hiện đa nền tảng
            is_antigravity = False
            
            if system == "Darwin":
                # macOS: Kiểm tra đường dẫn chứa Antigravity.app
                is_antigravity = 'antigravity.app' in exe_path
            elif system == "Windows":
                # Windows: Kiểm tra tên tiến trình hoặc đường dẫn chứa antigravity
                is_antigravity = (process_name_lower in ['antigravity.exe', 'antigravity'] or 
                                 'antigravity' in exe_path)
            else:
                # Linux: Kiểm tra tên tiến trình hoặc đường dẫn chứa antigravity
                is_antigravity = (process_name_lower == 'antigravity' or 
                                 'antigravity' in exe_path)
            
            if is_antigravity:
                return True
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def close_antigravity(timeout=10, force_kill=True):
    """Đóng tất cả các tiến trình Antigravity một cách an toàn
    
    Chiến lược đóng (ba giai đoạn, đa nền tảng):
    1. Cách thoát an toàn cụ thể cho từng nền tảng
       - macOS: AppleScript
       - Windows: taskkill /IM (chấm dứt an toàn)
       - Linux: SIGTERM
    2. Chấm dứt nhẹ nhàng (SIGTERM/TerminateProcess) - Cho tiến trình cơ hội dọn dẹp
    3. Buộc giết (SIGKILL/taskkill /F) - Biện pháp cuối cùng
    """
    info("Đang cố gắng đóng Antigravity...")
    system = platform.system()
    
    # Kiểm tra nền tảng
    if system not in ["Darwin", "Windows", "Linux"]:
        warning(f"Nền tảng hệ thống không xác định: {system}, sẽ thử phương pháp chung")
    
    try:
        # Giai đoạn 1: Thoát an toàn cụ thể cho từng nền tảng
        if system == "Darwin":
            # macOS: Sử dụng AppleScript
            info("Đang cố gắng thoát Antigravity an toàn qua AppleScript...")
            try:
                result = subprocess.run(
                    ["osascript", "-e", 'tell application "Antigravity" to quit'],
                    capture_output=True,
                    timeout=3
                )
                if result.returncode == 0:
                    info("Đã gửi yêu cầu thoát, đang chờ ứng dụng phản hồi...")
                    time.sleep(2)
            except Exception as e:
                warning(f"Thoát qua AppleScript thất bại: {e}, sẽ sử dụng cách khác")
        
        elif system == "Windows":
            # Windows: Sử dụng taskkill chấm dứt an toàn (không có tham số /F)
            info("Đang cố gắng thoát Antigravity an toàn qua taskkill...")
            try:
                # CREATE_NO_WINDOW = 0x08000000
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                result = subprocess.run(
                    ["taskkill", "/IM", "Antigravity.exe", "/T"],
                    capture_output=True,
                    timeout=3,
                    creationflags=0x08000000
                )
                if result.returncode == 0:
                    info("Đã gửi yêu cầu thoát, đang chờ ứng dụng phản hồi...")
                    time.sleep(2)
            except Exception as e:
                warning(f"Thoát qua taskkill thất bại: {e}, sẽ sử dụng cách khác")
        
        # Linux không cần xử lý đặc biệt, sử dụng trực tiếp SIGTERM
        
        # Kiểm tra và thu thập các tiến trình vẫn đang chạy
        target_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                process_name_lower = proc.info['name'].lower() if proc.info['name'] else ""
                exe_path = proc.info.get('exe', '').lower() if proc.info.get('exe') else ""
                
                # Loại trừ tiến trình bản thân
                if proc.pid == os.getpid():
                    continue
                
                # Loại trừ tất cả các tiến trình trong thư mục ứng dụng hiện tại (tránh giết nhầm bản thân và tiến trình con)
                # Trong môi trường đóng gói PyInstaller, sys.executable trỏ đến file exe
                # Trong môi trường phát triển, nó trỏ đến python.exe
                try:
                    import sys
                    current_exe = sys.executable
                    current_dir = os.path.dirname(os.path.abspath(current_exe)).lower()
                    if exe_path and current_dir in exe_path:
                        # print(f"DEBUG: Skipping process in current dir: {proc.info['name']}")
                        continue
                except:
                    pass

                # Phát hiện đa nền tảng: Kiểm tra tên tiến trình hoặc đường dẫn file thực thi
                is_antigravity = False
                
                if system == "Darwin":
                    # macOS: Kiểm tra đường dẫn chứa Antigravity.app
                    is_antigravity = 'antigravity.app' in exe_path
                elif system == "Windows":
                    # Windows: Khớp chính xác tên tiến trình antigravity.exe
                    # Hoặc đường dẫn chứa antigravity và tên tiến trình không phải là Antigravity Manager.exe
                    is_target_name = process_name_lower in ['antigravity.exe', 'antigravity']
                    is_in_path = 'antigravity' in exe_path
                    is_manager = 'manager' in process_name_lower
                    
                    is_antigravity = is_target_name or (is_in_path and not is_manager)
                else:
                    # Linux: Kiểm tra tên tiến trình hoặc đường dẫn chứa antigravity
                    is_antigravity = (process_name_lower == 'antigravity' or 
                                     'antigravity' in exe_path)
                
                if is_antigravity:
                    info(f"Phát hiện tiến trình mục tiêu: {proc.info['name']} ({proc.pid}) - {exe_path}")
                    target_processes.append(proc)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not target_processes:
            info("Tất cả các tiến trình Antigravity đã đóng bình thường")
            return True
        
        info(f"Phát hiện {len(target_processes)} tiến trình vẫn đang chạy")

        # Giai đoạn 2: Yêu cầu chấm dứt tiến trình nhẹ nhàng (SIGTERM)
        info("Gửi tín hiệu chấm dứt (SIGTERM)...")
        for proc in target_processes:
            try:
                if proc.is_running():
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                continue
            except Exception as e:
                continue

        # Chờ tiến trình tự kết thúc
        info(f"Đang chờ tiến trình thoát (tối đa {timeout} giây)...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            still_running = []
            for proc in target_processes:
                try:
                    if proc.is_running():
                        still_running.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not still_running:
                info("Tất cả các tiến trình Antigravity đã đóng bình thường")
                return True
                
            time.sleep(0.5)

        # Giai đoạn 3: Buộc chấm dứt tiến trình cứng đầu (SIGKILL)
        if still_running:
            still_running_names = ", ".join([f"{p.info['name']}({p.pid})" for p in still_running])
            warning(f"Vẫn còn {len(still_running)} tiến trình chưa thoát: {still_running_names}")
            
            if force_kill:
                info("Gửi tín hiệu buộc chấm dứt (SIGKILL)...")
                for proc in still_running:
                    try:
                        if proc.is_running():
                            proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                # Kiểm tra lần cuối
                time.sleep(1)
                final_check = []
                for proc in still_running:
                    try:
                        if proc.is_running():
                            final_check.append(proc)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if not final_check:
                    info("Tất cả các tiến trình Antigravity đã bị chấm dứt")
                    return True
                else:
                    final_list = ", ".join([f"{p.info['name']}({p.pid})" for p in final_check])
                    error(f"Các tiến trình không thể chấm dứt: {final_list}")
                    return False
            else:
                error("Một số tiến trình không thể đóng, vui lòng đóng thủ công và thử lại")
                return False
                
        return True

    except Exception as e:
        error(f"Lỗi xảy ra khi đóng tiến trình Antigravity: {str(e)}")
        return False

def start_antigravity(use_uri=True):
    """Khởi động Antigravity
    
    Args:
        use_uri: Có sử dụng giao thức URI để khởi động hay không (mặc định True)
                 Giao thức URI đáng tin cậy hơn, không cần tìm đường dẫn file thực thi
    """
    info("Đang khởi động Antigravity...")
    system = platform.system()
    
    try:
        # Ưu tiên sử dụng giao thức URI để khởi động (đa nền tảng)
        if use_uri:
            info("Sử dụng giao thức URI để khởi động...")
            uri = "antigravity://oauth-success"
            
            if open_uri(uri):
                info("Lệnh khởi động URI Antigravity đã được gửi")
                return True
            else:
                warning("Khởi động URI thất bại, thử sử dụng đường dẫn file thực thi...")
                # Tiếp tục thực hiện phương án dự phòng bên dưới
        
        # Phương án dự phòng: Sử dụng đường dẫn file thực thi để khởi động
        info("Sử dụng đường dẫn file thực thi để khởi động...")
        if system == "Darwin":
            subprocess.Popen(["open", "-a", "Antigravity"])
        elif system == "Windows":
            path = get_antigravity_executable_path()
            if path and path.exists():
                # CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen([str(path)], creationflags=0x08000000)
            else:
                error("Không tìm thấy file thực thi Antigravity")
                warning("Gợi ý: Có thể thử sử dụng giao thức URI để khởi động (use_uri=True)")
                return False
        elif system == "Linux":
            subprocess.Popen(["antigravity"])
        
        info("Lệnh khởi động Antigravity đã được gửi")
        return True
    except Exception as e:
        error(f"Lỗi khi khởi động tiến trình: {e}")
        # Nếu khởi động URI thất bại, thử sử dụng đường dẫn file thực thi
        if use_uri:
            warning("Khởi động URI thất bại, thử sử dụng đường dẫn file thực thi...")
            return start_antigravity(use_uri=False)
        return False
