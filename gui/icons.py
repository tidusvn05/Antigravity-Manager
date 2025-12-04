"""
Hệ thống biểu tượng thích ứng nền tảng cho Antigravity Manager.
Tự động chọn bộ biểu tượng phù hợp dựa trên hệ điều hành.
"""
import flet as ft
import platform

class AppIcons:
    """
    Giao diện biểu tượng thống nhất thích ứng với nền tảng.
    - macOS: Sử dụng CupertinoIcons (giao diện gốc)
    - Windows/Linux: Sử dụng Material Icons
    """
    
    _is_macos = platform.system() == "Darwin"
    
    # Biểu tượng điều hướng
    dashboard = ft.CupertinoIcons.SQUARE_GRID_2X2 if _is_macos else ft.Icons.DASHBOARD
    settings = ft.CupertinoIcons.GEAR if _is_macos else ft.Icons.SETTINGS
    
    # Biểu tượng hành động
    add = ft.CupertinoIcons.ADD if _is_macos else ft.Icons.ADD
    delete = ft.CupertinoIcons.DELETE if _is_macos else ft.Icons.DELETE_OUTLINE
    refresh = ft.CupertinoIcons.REFRESH if _is_macos else ft.Icons.REFRESH
    
    # Biểu tượng trạng thái
    check_circle = ft.CupertinoIcons.CHECK_MARK_CIRCLED_SOLID if _is_macos else ft.Icons.CHECK_CIRCLE
    pause_circle = ft.CupertinoIcons.PAUSE_CIRCLE if _is_macos else ft.Icons.PAUSE_CIRCLE_FILLED
    info = ft.CupertinoIcons.INFO if _is_macos else ft.Icons.INFO
    
    # Biểu tượng tập tin & thư mục
    folder = ft.CupertinoIcons.FOLDER_SOLID if _is_macos else ft.Icons.FOLDER
    document = ft.CupertinoIcons.DOC_TEXT_SEARCH if _is_macos else ft.Icons.SEARCH
    
    # Biểu tượng menu & khác
    ellipsis = ft.CupertinoIcons.ELLIPSIS if _is_macos else ft.Icons.MORE_VERT
    swap = ft.Icons.SWAP_HORIZ  # Same on all platforms
    
    @classmethod
    def is_macos(cls):
        """Trả về True nếu đang chạy trên macOS"""
        return cls._is_macos
