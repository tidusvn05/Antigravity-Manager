import flet as ft

class ThemeColors:
    # Giao diện sáng
    LIGHT_BG_PAGE = "#FAFAFA"
    LIGHT_BG_CARD = "#FFFFFF"
    LIGHT_TEXT_MAIN = "#1A1A1A"
    LIGHT_TEXT_GREY = "#8E8E93"
    LIGHT_PRIMARY = "#4E75F6"
    LIGHT_BG_LIGHT_BLUE = "#F0F4FF"
    LIGHT_BG_LIGHT_RED = "#FFF0F0"
    LIGHT_BG_LIGHT_GREEN = "#F0FFF4"
    LIGHT_SHADOW = "#08000000"
    LIGHT_SIDEBAR_BG = "#F6F6F6"
    LIGHT_SIDEBAR_BORDER = "#E5E5E5"

    # Giao diện tối - Màu xám dịu hơn để thoải mái cho mắt
    DARK_BG_PAGE = "#121212"  # Xám đậm dịu thay vì đen tuyền
    DARK_BG_CARD = "#1E1E1E"  # Thẻ sáng hơn một chút
    DARK_TEXT_MAIN = "#E5E5E5"  # Trắng dịu
    DARK_TEXT_GREY = "#98989D"
    DARK_PRIMARY = "#6B93FF"  # Xanh lam sáng hơn cho chế độ tối
    DARK_BG_LIGHT_BLUE = "#1A2842"  # Tông xanh lam đậm hơn
    DARK_BG_LIGHT_RED = "#3D1F1F"  # Tông đỏ đậm hơn
    DARK_BG_LIGHT_GREEN = "#1F3D28"  # Tông xanh lục đậm hơn
    DARK_SHADOW = "#10000000"  # Bóng rất mờ
    DARK_SIDEBAR_BG = "#1A1A1A"  # Sidebar tối hơn trang một chút
    DARK_SIDEBAR_BORDER = "#2A2A2A"  # Viền mờ

class Palette:
    def __init__(self, is_dark):
        self.bg_page = ThemeColors.DARK_BG_PAGE if is_dark else ThemeColors.LIGHT_BG_PAGE
        self.bg_card = ThemeColors.DARK_BG_CARD if is_dark else ThemeColors.LIGHT_BG_CARD
        self.text_main = ThemeColors.DARK_TEXT_MAIN if is_dark else ThemeColors.LIGHT_TEXT_MAIN
        self.text_grey = ThemeColors.DARK_TEXT_GREY if is_dark else ThemeColors.LIGHT_TEXT_GREY
        self.primary = ThemeColors.DARK_PRIMARY if is_dark else ThemeColors.LIGHT_PRIMARY
        self.bg_light_blue = ThemeColors.DARK_BG_LIGHT_BLUE if is_dark else ThemeColors.LIGHT_BG_LIGHT_BLUE
        self.bg_light_red = ThemeColors.DARK_BG_LIGHT_RED if is_dark else ThemeColors.LIGHT_BG_LIGHT_RED
        self.bg_light_green = ThemeColors.DARK_BG_LIGHT_GREEN if is_dark else ThemeColors.LIGHT_BG_LIGHT_GREEN
        self.shadow = ThemeColors.DARK_SHADOW if is_dark else ThemeColors.LIGHT_SHADOW
        self.sidebar_bg = ThemeColors.DARK_SIDEBAR_BG if is_dark else ThemeColors.LIGHT_SIDEBAR_BG
        self.sidebar_border = ThemeColors.DARK_SIDEBAR_BORDER if is_dark else ThemeColors.LIGHT_SIDEBAR_BORDER

def get_palette(page: ft.Page):
    is_dark = page.platform_brightness == ft.Brightness.DARK
    return Palette(is_dark)
