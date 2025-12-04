#!/bin/bash

# Thiết lập thoát khi có lỗi
set -e

echo "🚀 Bắt đầu build Antigravity Manager (macOS)..."

# 1. Đồng bộ file tài nguyên
echo "📦 Đồng bộ file tài nguyên..."
# Đảm bảo thư mục gui/assets tồn tại
mkdir -p gui/assets
# Đồng bộ nội dung thư mục assets vào gui/assets
cp -R assets/* gui/assets/
# Đồng bộ requirements.txt
cp requirements.txt gui/requirements.txt

# 2. Dọn dẹp bản build cũ
echo "🧹 Dọn dẹp file build cũ..."
rm -rf gui/build/macos

# 3. Thực hiện build
echo "🔨 Bắt đầu biên dịch..."
source .venv/bin/activate
cd gui

# Tạm thời tắt set -e, vì flet build có thể ném ra traceback SystemExit: 0 nhưng thực tế build thành công
set +e

# Đảm bảo không vào chế độ tương tác
unset PYTHONINSPECT

# Sử dụng python -c gọi trực tiếp flet_cli, bỏ qua vấn đề điểm nhập có thể xảy ra, và chuyển hướng đầu vào
python -c "import sys; from flet.cli import main; main()" build macos \
    --product "Antigravity Manager" \
    --org "com.ctrler.antigravity" \
    --copyright "Copyright (c) 2025 Ctrler" \
    --build-version "1.0.0" \
    --desc "Công cụ quản lý tài khoản Antigravity" < /dev/null
EXIT_CODE=$?
set -e

# Quay lại thư mục gốc
cd ..

# 4. Kiểm tra sản phẩm build và đóng gói DMG
APP_NAME="Antigravity Manager"
APP_PATH="gui/build/macos/$APP_NAME.app"
DMG_NAME="$APP_NAME.dmg"
OUTPUT_DMG="gui/build/macos/$DMG_NAME"

if [ -d "$APP_PATH" ]; then
    echo "✅ Phát hiện gói ứng dụng, build thành công (bỏ qua trạng thái thoát của Flet CLI)"
else
    echo "❌ Build thất bại, không tìm thấy gói ứng dụng"
    exit $EXIT_CODE
fi

echo "📦 Đang tạo gói cài đặt DMG..."

# Tạo thư mục tạm để làm DMG
DMG_SOURCE="gui/build/macos/dmg_source"
rm -rf "$DMG_SOURCE"
mkdir -p "$DMG_SOURCE"

# Sao chép ứng dụng vào thư mục tạm
echo "📋 Sao chép ứng dụng vào thư mục tạm..."
cp -R "$APP_PATH" "$DMG_SOURCE/"

# Tạo liên kết mềm Applications
ln -s /Applications "$DMG_SOURCE/Applications"

# Sử dụng hdiutil tạo DMG
echo "💿 Tạo file DMG..."
rm -f "$OUTPUT_DMG"
TEMP_DMG="gui/build/macos/temp.dmg"
rm -f "$TEMP_DMG"

# Bước 1: Tạo DMG có thể đọc ghi
hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_SOURCE" -ov -format UDRW "$TEMP_DMG"

# Bước 2: Chuyển đổi sang DMG nén chỉ đọc
hdiutil convert "$TEMP_DMG" -format UDZO -o "$OUTPUT_DMG"

# Dọn dẹp
rm -f "$TEMP_DMG"
rm -rf "$DMG_SOURCE"

echo "🎉 Đóng gói hoàn tất!"
echo "📂 Vị trí ứng dụng: $APP_PATH"
echo "💿 File DMG: $OUTPUT_DMG"
