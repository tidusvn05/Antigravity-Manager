# -*- coding: utf-8 -*-
import argparse
import sys
import os

# Thêm thư mục gui vào sys.path để các module nội bộ có thể import lẫn nhau (ví dụ: account_manager import utils)
sys.path.append(os.path.join(os.path.dirname(__file__), "gui"))

# Hỗ trợ chạy trực tiếp và import như một module
# Hỗ trợ chạy trực tiếp và import như một module
try:
    from gui.utils import info, error, warning
    from gui.account_manager import (
        list_accounts_data,
        add_account_snapshot,
        switch_account,
        delete_account
    )
    from gui.process_manager import start_antigravity, close_antigravity
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def show_menu():
    """Hiển thị menu chính"""
    print("\n" + "="*50)
    print("🚀 Công cụ quản lý tài khoản Antigravity")
    print("="*50)
    print("\nVui lòng chọn thao tác:")
    print("  1. 📋 Liệt kê tất cả bản sao lưu")
    print("  2. ➕ Thêm/Cập nhật bản sao lưu")
    print("  3. 🔄 Chuyển đổi/Khôi phục bản sao lưu")
    print("  4. 🗑️  Xóa bản sao lưu")
    print("  5. ▶️  Khởi động Antigravity")
    print("  6. ⏹️  Đóng Antigravity")
    print("  0. 🚪 Thoát")
    print("-"*50)

def list_accounts():
    """Liệt kê tất cả tài khoản"""
    accounts = list_accounts_data()
    if not accounts:
        info("Chưa có bản lưu trữ nào")
        return []
    else:
        print("\n" + "="*50)
        info(f"Có tổng cộng {len(accounts)} bản lưu trữ:")
        print("="*50)
        for idx, acc in enumerate(accounts, 1):
            print(f"\n{idx}. {acc['name']}")
            print(f"   📧 Email: {acc['email']}")
            print(f"   🆔 ID: {acc['id']}")
            print(f"   ⏰ Sử dụng lần cuối: {acc['last_used']}")
            print("-" * 50)
        return accounts

def add_account():
    """Thêm bản sao lưu tài khoản"""
    print("\n" + "="*50)
    print("➕ Thêm/Cập nhật bản sao lưu tài khoản")
    print("="*50)
    
    name = input("\nNhập tên tài khoản (để trống để tự động tạo): ").strip()
    email = input("Nhập email (để trống để tự động nhận diện): ").strip()
    
    name = name if name else None
    email = email if email else None
    
    print()
    if add_account_snapshot(name, email):
        info("✅ Thao tác thành công！")
    else:
        error("❌ Thao tác thất bại！")

def switch_account_interactive():
    """Chuyển đổi tài khoản tương tác"""
    accounts = list_accounts()
    if not accounts:
        return
    
    print("\n" + "="*50)
    print("🔄 Chuyển đổi/Khôi phục tài khoản")
    print("="*50)
    
    choice = input("\nNhập số thứ tự tài khoản cần chuyển đổi: ").strip()
    
    if not choice:
        warning("Đã hủy thao tác")
        return
    
    real_id = resolve_id(choice)
    if not real_id:
        error(f"❌ Số thứ tự không hợp lệ: {choice}")
        return
    
    print()
    if switch_account(real_id):
        info("✅ Chuyển đổi thành công！")
    else:
        error("❌ Chuyển đổi thất bại！")

def delete_account_interactive():
    """Xóa tài khoản tương tác"""
    accounts = list_accounts()
    if not accounts:
        return
    
    print("\n" + "="*50)
    print("🗑️  Xóa bản sao lưu tài khoản")
    print("="*50)
    
    choice = input("\nNhập số thứ tự tài khoản cần xóa: ").strip()
    
    if not choice:
        warning("Đã hủy thao tác")
        return
    
    real_id = resolve_id(choice)
    if not real_id:
        error(f"❌ Số thứ tự không hợp lệ: {choice}")
        return
    
    # Xác nhận xóa
    confirm = input(f"\n⚠️  Bạn có chắc chắn muốn xóa tài khoản này không? (y/N): ").strip().lower()
    if confirm != 'y':
        warning("Đã hủy xóa")
        return
    
    print()
    if delete_account(real_id):
        info("✅ Xóa thành công！")
    else:
        error("❌ Xóa thất bại！")

def interactive_mode():
    """Chế độ menu tương tác"""
    while True:
        show_menu()
        choice = input("Nhập lựa chọn (0-6): ").strip()
        
        if choice == "1":
            list_accounts()
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == "2":
            add_account()
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == "3":
            switch_account_interactive()
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == "4":
            delete_account_interactive()
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == "5":
            print()
            start_antigravity()
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == "6":
            print()
            close_antigravity()
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == "0":
            print("\n👋 Tạm biệt！")
            sys.exit(0)
            
        else:
            error("❌ Lựa chọn không hợp lệ, vui lòng chọn lại")
            input("\nNhấn Enter để tiếp tục...")

def cli_mode():
    """Chế độ dòng lệnh"""
    parser = argparse.ArgumentParser(description="Công cụ quản lý tài khoản Antigravity (Phiên bản Python thuần)")
    subparsers = parser.add_subparsers(dest="command", help="Các lệnh khả dụng")

    # List
    subparsers.add_parser("list", help="Liệt kê tất cả bản lưu trữ")

    # Add
    add_parser = subparsers.add_parser("add", help="Lưu trạng thái hiện tại thành bản lưu trữ mới")
    add_parser.add_argument("--name", "-n", help="Tên bản lưu trữ (tùy chọn, mặc định tự động tạo)")
    add_parser.add_argument("--email", "-e", help="Email liên kết (tùy chọn, mặc định đọc từ cơ sở dữ liệu)")

    # Switch
    switch_parser = subparsers.add_parser("switch", help="Chuyển sang bản lưu trữ chỉ định")
    switch_parser.add_argument("--id", "-i", required=True, help="ID bản lưu trữ")

    # Delete
    del_parser = subparsers.add_parser("delete", help="Xóa bản lưu trữ")
    del_parser.add_argument("--id", "-i", required=True, help="ID bản lưu trữ")
    
    # Process Control
    subparsers.add_parser("start", help="Khởi động Antigravity")
    subparsers.add_parser("stop", help="Đóng Antigravity")

    args = parser.parse_args()

    if args.command == "list":
        list_accounts()

    elif args.command == "add":
        if add_account_snapshot(args.name, args.email):
            info("Thêm bản lưu trữ thành công")
        else:
            sys.exit(1)

    elif args.command == "switch":
        real_id = resolve_id(args.id)
        if not real_id:
            error(f"ID hoặc số thứ tự không hợp lệ: {args.id}")
            sys.exit(1)
            
        if switch_account(real_id):
            info("Chuyển đổi thành công")
        else:
            sys.exit(1)

    elif args.command == "delete":
        real_id = resolve_id(args.id)
        if not real_id:
            error(f"ID hoặc số thứ tự không hợp lệ: {args.id}")
            sys.exit(1)

        if delete_account(real_id):
            info("Xóa thành công")
        else:
            sys.exit(1)
            
    elif args.command == "start":
        start_antigravity()
        
    elif args.command == "stop":
        close_antigravity()

    else:
        # Khi không có tham số, vào chế độ tương tác
        interactive_mode()

def main():
    """Điểm nhập chính"""
    # Nếu không có tham số dòng lệnh, vào chế độ tương tác
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        cli_mode()

def resolve_id(input_id):
    """Phân giải ID, hỗ trợ UUID hoặc số thứ tự"""
    accounts = list_accounts_data()
    
    # 1. Cố gắng xử lý như số thứ tự
    if input_id.isdigit():
        idx = int(input_id)
        if 1 <= idx <= len(accounts):
            return accounts[idx-1]['id']
            
    # 2. Cố gắng khớp như UUID
    for acc in accounts:
        if acc['id'] == input_id:
            return input_id
            
    return None

if __name__ == "__main__":
    main()
