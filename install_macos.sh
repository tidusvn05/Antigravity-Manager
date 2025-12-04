#!/usr/bin/env bash

# Antigravity Manager - macOS Installation Script
# Script cài đặt để thiết lập bin cho macOS

set -e  # Dừng script nếu có lỗi

# Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Lấy đường dẫn thư mục hiện tại (thư mục gốc của project)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Antigravity Manager - macOS Installation    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Kiểm tra Python
echo -e "${YELLOW}[1/5]${NC} Kiểm tra Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Lỗi: Python 3 chưa được cài đặt${NC}"
    echo -e "${YELLOW}💡 Vui lòng cài đặt Python 3.10 hoặc cao hơn${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓${NC} Đã tìm thấy Python $PYTHON_VERSION"

# 2. Tạo virtual environment nếu chưa có
echo -e "\n${YELLOW}[2/5]${NC} Thiết lập virtual environment..."
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "  Đang tạo virtual environment..."
    python3 -m venv "$PROJECT_ROOT/.venv"
    echo -e "${GREEN}✓${NC} Đã tạo virtual environment"
else
    echo -e "${GREEN}✓${NC} Virtual environment đã tồn tại"
fi

# 3. Cài đặt dependencies
echo -e "\n${YELLOW}[3/5]${NC} Cài đặt dependencies..."
source "$PROJECT_ROOT/.venv/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "$PROJECT_ROOT/requirements.txt"
echo -e "${GREEN}✓${NC} Đã cài đặt dependencies"

# 4. Cấp quyền thực thi cho các script
echo -e "\n${YELLOW}[4/5]${NC} Cấp quyền thực thi..."
chmod +x "$PROJECT_ROOT/bin/agr"
chmod +x "$PROJECT_ROOT/bin/agr-ui"
echo -e "${GREEN}✓${NC} Đã cấp quyền thực thi cho bin/agr và bin/agr-ui"

# 5. Thiết lập symlink vào /usr/local/bin
echo -e "\n${YELLOW}[5/5]${NC} Thiết lập symlink..."

# Kiểm tra xem /usr/local/bin có tồn tại không
if [ ! -d "/usr/local/bin" ]; then
    echo -e "${YELLOW}⚠️  Thư mục /usr/local/bin không tồn tại, đang tạo...${NC}"
    sudo mkdir -p /usr/local/bin
fi

# Xóa symlink cũ nếu có
if [ -L "/usr/local/bin/agr" ]; then
    echo "  Đang xóa symlink cũ cho 'agr'..."
    sudo rm "/usr/local/bin/agr"
fi

if [ -L "/usr/local/bin/agr-ui" ]; then
    echo "  Đang xóa symlink cũ cho 'agr-ui'..."
    sudo rm "/usr/local/bin/agr-ui"
fi

# Tạo symlink mới
echo "  Đang tạo symlink (có thể yêu cầu mật khẩu sudo)..."
sudo ln -s "$PROJECT_ROOT/bin/agr" /usr/local/bin/agr
sudo ln -s "$PROJECT_ROOT/bin/agr-ui" /usr/local/bin/agr-ui

echo -e "${GREEN}✓${NC} Đã tạo symlink tại /usr/local/bin"

# Hoàn thành
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          ✓ Cài đặt hoàn tất thành công!       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📝 Bạn có thể sử dụng các lệnh sau từ bất kỳ đâu:${NC}"
echo ""
echo -e "  ${YELLOW}agr-ui${NC}              - Khởi động GUI"
echo -e "  ${YELLOW}agr list${NC}            - Liệt kê tất cả tài khoản"
echo -e "  ${YELLOW}agr add${NC}             - Thêm tài khoản mới"
echo -e "  ${YELLOW}agr add -n \"Tên\"${NC}   - Thêm tài khoản với tên chỉ định"
echo -e "  ${YELLOW}agr switch -i 1${NC}     - Chuyển đổi tài khoản"
echo -e "  ${YELLOW}agr delete -i 1${NC}     - Xóa tài khoản"
echo ""
echo -e "${BLUE}💡 Mẹo:${NC} Chạy ${YELLOW}agr --help${NC} để xem tất cả các lệnh có sẵn"
echo ""
