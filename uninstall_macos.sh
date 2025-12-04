#!/usr/bin/env bash

# Antigravity Manager - macOS Uninstallation Script
# Script gỡ cài đặt để xóa symlink

set -e  # Dừng script nếu có lỗi

# Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Antigravity Manager - macOS Uninstallation   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Xóa symlink
echo -e "${YELLOW}Đang gỡ cài đặt symlink...${NC}"

REMOVED=0

if [ -L "/usr/local/bin/agr" ]; then
    echo "  Đang xóa /usr/local/bin/agr..."
    sudo rm "/usr/local/bin/agr"
    echo -e "${GREEN}✓${NC} Đã xóa symlink 'agr'"
    REMOVED=$((REMOVED + 1))
else
    echo -e "${YELLOW}⚠️${NC}  Symlink 'agr' không tồn tại"
fi

if [ -L "/usr/local/bin/agr-ui" ]; then
    echo "  Đang xóa /usr/local/bin/agr-ui..."
    sudo rm "/usr/local/bin/agr-ui"
    echo -e "${GREEN}✓${NC} Đã xóa symlink 'agr-ui'"
    REMOVED=$((REMOVED + 1))
else
    echo -e "${YELLOW}⚠️${NC}  Symlink 'agr-ui' không tồn tại"
fi

echo ""
if [ $REMOVED -gt 0 ]; then
    echo -e "${GREEN}✓ Gỡ cài đặt hoàn tất!${NC}"
    echo ""
    echo -e "${BLUE}📝 Lưu ý:${NC}"
    echo "  - Virtual environment (.venv) vẫn được giữ lại"
    echo "  - Dữ liệu tài khoản (~/.antigravity-agent) vẫn được giữ lại"
    echo "  - Để xóa hoàn toàn, vui lòng xóa thủ công thư mục project"
else
    echo -e "${YELLOW}⚠️  Không có symlink nào cần gỡ cài đặt${NC}"
fi
echo ""
