# build_windows.ps1

Write-Host "🚀 Bắt đầu build Antigravity Manager (Windows)..." -ForegroundColor Cyan

# 1. Kiểm tra môi trường
if (-not (Get-Command "flet" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Không tìm thấy lệnh flet, đang cài đặt..." -ForegroundColor Yellow
    pip install flet
}
if (-not (Get-Command "pyinstaller" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Không tìm thấy lệnh pyinstaller, đang cài đặt..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Cài đặt các phụ thuộc của dự án
if (Test-Path "requirements.txt") {
    Write-Host "📦 Đang cài đặt/cập nhật các phụ thuộc của dự án..." -ForegroundColor Green
    pip install -r requirements.txt
}

# 2. Dọn dẹp bản build cũ
Write-Host "🧹 Dọn dẹp file build cũ..." -ForegroundColor Green
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }

# 3. Chuẩn bị tài nguyên
# Đảm bảo gui/assets tồn tại và mới nhất
Write-Host "📦 Đồng bộ file tài nguyên..." -ForegroundColor Green
if (-not (Test-Path "gui/assets")) { New-Item -ItemType Directory -Path "gui/assets" | Out-Null }
Copy-Item "assets/*" "gui/assets/" -Recurse -Force

# 4. Thực hiện build
Write-Host "🔨 Bắt đầu biên dịch..." -ForegroundColor Green

# Sử dụng flet pack để đóng gói
# build_windows.ps1

Write-Host "🚀 Bắt đầu build Antigravity Manager (Windows)..." -ForegroundColor Cyan

# 1. Kiểm tra môi trường
if (-not (Get-Command "flet" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Không tìm thấy lệnh flet, đang cài đặt..." -ForegroundColor Yellow
    pip install flet
}
if (-not (Get-Command "pyinstaller" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Không tìm thấy lệnh pyinstaller, đang cài đặt..." -ForegroundColor Yellow
    pip install pyinstaller
}

# 2. Dọn dẹp bản build cũ
Write-Host "🧹 Dọn dẹp file build cũ..." -ForegroundColor Green
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }

# 3. Chuẩn bị tài nguyên
# Đảm bảo gui/assets tồn tại và mới nhất
Write-Host "📦 Đồng bộ file tài nguyên..." -ForegroundColor Green
if (-not (Test-Path "gui/assets")) { New-Item -ItemType Directory -Path "gui/assets" | Out-Null }
Copy-Item "assets/*" "gui/assets/" -Recurse -Force

# 4. Thực hiện build
Write-Host "🔨 Bắt đầu biên dịch..." -ForegroundColor Green

# Sử dụng flet pack để đóng gói
# --icon: Chỉ định biểu tượng
# --add-data: Thêm file tài nguyên (định dạng: đường dẫn nguồn;đường dẫn đích)
# --name: Chỉ định tên file đầu ra
# --noconsole: Không hiển thị cửa sổ console (nếu cần debug, có thể bỏ tham số này)
# gui/main.py: File đầu vào

# 4. Thực hiện đóng gói bằng PyInstaller
Write-Host "📦 Đang đóng gói..." -ForegroundColor Yellow

# Sử dụng PyInstaller để đóng gói trực tiếp
# --onefile: Đóng gói thành một file duy nhất
# --windowed: Không có console (ứng dụng GUI)
# --add-data: Thêm file tài nguyên (định dạng: đường dẫn nguồn;đường dẫn đích)
# --hidden-import: Buộc nhập các module có thể bị bỏ sót
pyinstaller --noconfirm --onefile --windowed --clean `
    --name "Antigravity Manager" `
    --icon "assets/icon.ico" `
    --add-data "assets;assets" `
    --add-data "gui;gui" `
    --noconsole `
    --paths "gui" `
    --hidden-import "views" `
    --hidden-import "views.home_view" `
    --hidden-import "views.settings_view" `
    --hidden-import "account_manager" `
    --hidden-import "db_manager" `
    --hidden-import "process_manager" `
    --hidden-import "utils" `
    --hidden-import "theme" `
    --hidden-import "icons" `
    "gui/main.py"

# Kiểm tra kết quả
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Đóng gói thất bại!" -ForegroundColor Red
    exit 1
}

# 5. Kiểm tra kết quả
if (Test-Path "dist/Antigravity Manager.exe") {
    Write-Host "`n🎉 Build thành công!" -ForegroundColor Green
    Write-Host "Vị trí file: dist/Antigravity Manager.exe" -ForegroundColor Cyan
} else {
    Write-Host "❌ Không tìm thấy file exe đã tạo" -ForegroundColor Red
    exit 1
}
