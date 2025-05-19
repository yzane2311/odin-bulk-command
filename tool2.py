#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import subprocess
import threading
import sqlite3
from datetime import datetime
import queue # For passing results from thread to main
import traceback # For detailed error logging
import webbrowser # For opening URL
import csv 

# Static debug log path and function, defined early for global use
_DEBUG_LOG_PATH = "application_debug_log.txt"

def log_to_file_debug_globally(message, level="INFO"):
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f_log:
            f_log.write(f"[{datetime.now()}] [{level}] {message}\n")
    except Exception as e:
        print(f"[CRITICAL_ERROR] Global static log failed: {e} for message: {message}", file=sys.stderr)

log_to_file_debug_globally("Script execution started. Global logger active.")

# Fixed credentials for login
FIXED_USERNAME = "admin"
FIXED_PASSWORD = "password" 

# ========== LABELS ==========
LABELS = {
    "en": {
        "title": "Ultimat-Unlock Tool",
        "edition": "Samsung, Honor & Xiaomi",
        "tab_samsung": "Samsung (ADB)",
        "tab_honor": "Honor (Fastboot)",
        "tab_xiaomi": "Xiaomi (ADB + Fastboot)",
        "tab_file_advanced": "Files & Advanced",
        "log": "Operation Log",
        "group_samsung": "Samsung ADB Repair & Utilities",
        "group_file": "File & App Management",
        "group_honor": "Honor Fastboot Tools",
        "group_xiaomi_adb": "Xiaomi ADB Mode",
        "group_xiaomi_fastboot": "Xiaomi Fastboot Mode",
        "group_advanced_cmd": "Advanced Command Execution",
        "btn_connection": "Check Connection",
        "btn_info": "Device Info",
        "btn_reboot_dl": "Reboot Download",
        "btn_reboot_rec": "Reboot Recovery",
        "btn_reboot_bl": "Reboot Bootloader",
        "btn_remove_frp": "Remove FRP (ADB)",
        "btn_usb_debug": "Enable USB Debug",
        "btn_repair_network": "Repair Network (root)",
        "btn_fix_perms": "Fix System Permissions",
        "btn_reset_wifi": "Reset WiFi",
        "btn_factory_reset": "Factory Reset (ADB)",
        "btn_mount_rw": "Mount System RW (root)",
        "btn_wipe_cache": "Wipe Cache (root)",
        "btn_clear_dalvik": "Clear Dalvik (root)",
        "btn_screenlock_reset": "Reset Screen Lock (ADB)",
        "btn_arabize_device": "Arabize Device (ADB)",
        "btn_open_browser_adb": "Open Browser (ADB)",
        "pull_file_title": "Pull File from Device",
        "pull_file_device_path_msg": "Enter device source path (e.g., /sdcard/file.txt):",
        "push_file_title": "Push File to Device",
        "push_file_device_path_msg": "Enter device destination path (e.g., /sdcard/newfile.txt):",
        "install_apk_title": "Select APK to Install",
        "uninstall_title": "Uninstall App",
        "uninstall_msg": "Enter package name (e.g., com.example.app):",
        "honor_frp_code_title": "Enter Honor FRP Key",
        "honor_frp_code_msg": "Please enter the Honor FRP unlock key:",
        "advanced_cmd_label": "Enter ADB or Fastboot command:",
        "btn_run_advanced_cmd": "Run Command",
        "adb_status_connected": "ADB: Connected",
        "adb_status_not_connected": "ADB: Not Connected",
        "search_log_label": "Search Log:", # Kept for potential future use, but UI elements removed
        "find_button": "Find", # Kept for potential future use
        "all_button": "All", # Kept for potential future use
        "export_button": "Export to TXT", # Kept for potential future use
        "btn_export_csv": "Export to CSV", # Kept for potential future use
        "btn_cancel_operation": "Cancel Operation", 
        "quit_dialog_title": "Quit",
        "quit_dialog_message": "Do you want to quit Ultimat-Unlock Tool?",
        "dependency_check_title": "Dependency Check",
        "adb_not_found_message": "ADB (Android Debug Bridge) not found or not working. Some features will be unavailable. Please install/configure ADB and add it to your system PATH.",
        "fastboot_not_found_message": "Fastboot not found or not working. Some features will be unavailable. Please install/configure Fastboot and add it to your system PATH.",
        "fatal_error_title": "Fatal Error",
        "fatal_error_message_prefix": "A critical error occurred:",
        "btn_get_detailed_info": "Read Device Info (ADB)", # Changed label to reflect new log style
        "btn_pull_file": "Pull File from Device",
        "btn_push_file": "Push File to Device",
        "btn_install_apk": "Install APK",
        "btn_uninstall_app": "Uninstall App",
        "btn_backup_user_data_adb": "Backup User Data (ADB)", 
        "btn_restore_user_data_adb": "Restore User Data (ADB)", 
        "backup_user_data_title": "Select Backup File Location",
        "backup_user_data_msg": "Choose where to save the user data backup (.ab file):",
        "restore_user_data_title": "Select Backup File to Restore",
        "restore_user_data_msg": "Choose the user data backup file (.ab) to restore:",
        "btn_honor_info": "Read Serial & Software Info",
        "honor_frp_key_label": "Honor FRP Key:",
        "btn_honor_frp": "Remove FRP (Honor Code)",
        "btn_honor_reboot_bl": "Reboot Bootloader (Honor)",
        "btn_honor_reboot_edl": "Reboot EDL (Honor)",
        "btn_honor_wipe_data_cache": "Wipe Data/Cache (Honor)",
        "btn_xiaomi_adb_info": "Read Device Info (ADB)", # Changed label
        "btn_xiaomi_enable_diag_root": "Enable Diag (ROOT)",
        "btn_xiaomi_reset_frp_adb": "Reset FRP (ADB)", 
        "btn_xiaomi_bypass_mi_account": "Bypass Mi Account (ADB)", 
        "btn_xiaomi_reboot_normal_adb": "Reboot Normal (ADB)",
        "btn_xiaomi_reboot_fastboot_adb": "Reboot Fastboot (ADB)",
        "btn_xiaomi_reboot_recovery_adb": "Reboot Recovery (ADB)",
        "btn_xiaomi_reboot_edl_adb": "Reboot EDL (ADB)",
        "btn_xiaomi_fastboot_info": "Read Info (Fastboot)",
        "btn_xiaomi_fastboot_read_security": "Read Security (Fastboot)",
        "btn_xiaomi_fastboot_unlock": "Unlock Bootloader (Fastboot)",
        "btn_xiaomi_fastboot_lock": "Lock Bootloader (Fastboot)",
        "btn_xiaomi_fastboot_reboot_sys": "Reboot System (Fastboot)",
        "btn_xiaomi_fastboot_reboot_fast": "Reboot Fastboot (Fastboot)",
        "btn_xiaomi_fastboot_reboot_edl": "Reboot EDL (Fastboot)",
        "btn_xiaomi_fastboot_wipe_cache": "Wipe Cache (Fastboot)",
        "btn_xiaomi_fastboot_wipe_data": "Wipe Data (Fastboot)",
        "lang": "Language",
        "theme": "Theme",
        "light": "Light",
        "dark": "Dark",
        "professional_dark": "Professional Dark",
        "arabic": "Arabic",
        "english": "English",
        "login_title": "Login - Ultimat-Unlock Tool",
        "username_label": "Username:",
        "password_label": "Password:",
        "login_button": "Login",
        "login_failed_title": "Login Failed",
        "login_failed_message": "Invalid username or password.",
        "arabize_confirm_title": "Confirm Arabization",
        "arabize_confirm_message": "This will attempt to change the device language to Arabic (ar-AE).\nThis may require specific permissions and might not work on all devices.\nProceed?",
        "arabize_note": "Note: Arabization might require WRITE_SECURE_SETTINGS permission or root on some devices.",
        "open_browser_title": "Open URL in Device Browser",
        "open_browser_prompt": "Enter the full URL to open (e.g., https://ultimat-unlock.com/):",
        "frp_reset_warning_title": "FRP Reset Attempt",
        "frp_reset_warning_message": "This will attempt a series of common ADB commands to reset FRP. These commands are not guaranteed to work on all devices or Android versions and may require specific permissions or root. Proceed with caution.",
        "context_cut": "Cut",
        "context_copy": "Copy",
        "context_paste": "Paste",
        "context_select_all": "Select All",
        "log_connect_server_success": "Connect to server...successful",
        "log_operation_started": "Operation Started: ",
        "log_device_info_header": "Device Information:",
        "log_frp_reset_ok": "FRP Reset.... OK",
        "log_frp_reset_fail": "FRP Reset.... FAILED",
        "log_read_info_complete": "Read Info.... COMPLETE"
    },
    "ar": {
        "title": "أداة Ultimat-Unlock",
        "edition": "سامسونج، هونور، شاومي",
        "tab_samsung": "سامسونج (ADB)",
        "tab_honor": "هونور (Fastboot)",
        "tab_xiaomi": "شاومي (ADB + Fastboot)",
        "tab_file_advanced": "ملفات وأدوات متقدمة",
        "log": "سجل العمليات",
        "group_samsung": "إصلاح سامسونج وأدوات ADB",
        "group_file": "إدارة الملفات والتطبيقات",
        "group_honor": "أدوات هونور Fastboot",
        "group_xiaomi_adb": "شاومي وضع ADB",
        "group_xiaomi_fastboot": "شاومي وضع Fastboot",
        "group_advanced_cmd": "تنفيذ أوامر متقدمة",
        "btn_connection": "فحص الاتصال",
        "btn_info": "معلومات الجهاز",
        "btn_reboot_dl": "إعادة تشغيل لوضع الداونلود",
        "btn_reboot_rec": "إعادة تشغيل للريكفري",
        "btn_reboot_bl": "إعادة تشغيل للبوتلودر",
        "btn_remove_frp": "إزالة FRP (ADB)",
        "btn_usb_debug": "تفعيل تصحيح USB",
        "btn_repair_network": "إصلاح الشبكة (روت)",
        "btn_fix_perms": "إصلاح صلاحيات النظام",
        "btn_reset_wifi": "إعادة ضبط WiFi",
        "btn_factory_reset": "إعادة ضبط المصنع (ADB)",
        "btn_mount_rw": "جعل النظام قابل للكتابة (روت)",
        "btn_wipe_cache": "مسح الكاش (روت)",
        "btn_clear_dalvik": "مسح دالفك (روت)",
        "btn_screenlock_reset": "إزالة قفل الشاشة (ADB)",
        "btn_arabize_device": "تعريب الهاتف (ADB)",
        "btn_open_browser_adb": "فتح المتصفح (ADB)",
        "pull_file_title": "سحب ملف من الجهاز",
        "pull_file_device_path_msg": "أدخل مسار الملف المصدر بالجهاز (مثال: /sdcard/file.txt):",
        "push_file_title": "رفع ملف إلى الجهاز",
        "push_file_device_path_msg": "أدخل مسار الوجهة بالجهاز (مثال: /sdcard/newfile.txt):",
        "install_apk_title": "اختر ملف APK للتثبيت",
        "uninstall_title": "حذف تطبيق",
        "uninstall_msg": "أدخل اسم الحزمة (مثال: com.example.app):",
        "honor_frp_code_title": "إدخال رمز FRP لهونور",
        "honor_frp_code_msg": "الرجاء إدخال رمز فك قفل FRP الخاص بهونور:",
        "advanced_cmd_label": "أدخل أمر ADB أو Fastboot:",
        "btn_run_advanced_cmd": "تنفيذ الأمر",
        "adb_status_connected": "ADB: متصل",
        "adb_status_not_connected": "ADB: غير متصل",
        "search_log_label": "بحث في السجل:",
        "find_button": "بحث",
        "all_button": "الكل",
        "export_button": "تصدير إلى TXT",
        "btn_export_csv": "تصدير إلى CSV",
        "btn_cancel_operation": "إلغاء العملية",
        "quit_dialog_title": "خروج",
        "quit_dialog_message": "هل تريد الخروج من أداة Ultimat-Unlock؟",
        "dependency_check_title": "فحص الاعتماديات",
        "adb_not_found_message": "ADB (Android Debug Bridge) غير موجود أو لا يعمل. بعض الميزات لن تكون متاحة. الرجاء تثبيت/تكوين ADB وإضافته إلى مسار النظام.",
        "fastboot_not_found_message": "Fastboot غير موجود أو لا يعمل. بعض الميزات لن تكون متاحة. الرجاء تثبيت/تكوين Fastboot وإضافته إلى مسار النظام.",
        "fatal_error_title": "خطأ فادح",
        "fatal_error_message_prefix": "حدث خطأ حرج:",
        "btn_get_detailed_info": "قراءة معلومات الجهاز (ADB)", # Changed
        "btn_pull_file": "سحب ملف من الجهاز",
        "btn_push_file": "رفع ملف إلى الجهاز",
        "btn_install_apk": "تثبيت APK",
        "btn_uninstall_app": "حذف تطبيق",
        "btn_backup_user_data_adb": "نسخ احتياطي لبيانات المستخدم (ADB)", 
        "btn_restore_user_data_adb": "استعادة بيانات المستخدم (ADB)", 
        "backup_user_data_title": "اختر موقع ملف النسخ الاحتياطي",
        "backup_user_data_msg": "اختر مكان حفظ النسخ الاحتياطي لبيانات المستخدم (ملف .ab):",
        "restore_user_data_title": "اختر ملف النسخ الاحتياطي للاستعادة",
        "restore_user_data_msg": "اختر ملف النسخ الاحتياطي لبيانات المستخدم (.ab) للاستعادة:",
        "btn_honor_info": "قراءة معلومات وسيريال هونور",
        "honor_frp_key_label": "رمز FRP لهونور:",
        "btn_honor_frp": "إزالة FRP (رمز هونور)",
        "btn_honor_reboot_bl": "إعادة تشغيل للبوتلودر (هونور)",
        "btn_honor_reboot_edl": "إعادة تشغيل لوضع EDL (هونور)",
        "btn_honor_wipe_data_cache": "مسح الداتا والكاش (هونور)",
        "btn_xiaomi_adb_info": "قراءة معلومات الجهاز (ADB)", # Changed
        "btn_xiaomi_enable_diag_root": "تفعيل Diag (روت)",
        "btn_xiaomi_reset_frp_adb": "إعادة تعيين FRP (ADB)", 
        "btn_xiaomi_bypass_mi_account": "تجاوز حساب Mi (ADB)", 
        "btn_xiaomi_reboot_normal_adb": "إعادة تشغيل عادي (ADB)",
        "btn_xiaomi_reboot_fastboot_adb": "إعادة تشغيل فاستبوت (ADB)",
        "btn_xiaomi_reboot_recovery_adb": "إعادة تشغيل ريكفري (ADB)",
        "btn_xiaomi_reboot_edl_adb": "إعادة تشغيل EDL (ADB)",
        "btn_xiaomi_fastboot_info": "قراءة المعلومات (Fastboot)",
        "btn_xiaomi_fastboot_read_security": "قراءة الأمان (Fastboot)",
        "btn_xiaomi_fastboot_unlock": "فتح البوتلودر (Fastboot)",
        "btn_xiaomi_fastboot_lock": "قفل البوتلودر (Fastboot)",
        "btn_xiaomi_fastboot_reboot_sys": "إعادة تشغيل للنظام (Fastboot)",
        "btn_xiaomi_fastboot_reboot_fast": "إعادة تشغيل فاستبوت (Fastboot)",
        "btn_xiaomi_fastboot_reboot_edl": "إعادة تشغيل EDL (Fastboot)",
        "btn_xiaomi_fastboot_wipe_cache": "مسح الكاش (Fastboot)",
        "btn_xiaomi_fastboot_wipe_data": "مسح الداتا (Fastboot)",
        "lang": "اللغة",
        "theme": "الثيم",
        "light": "فاتح",
        "dark": "داكن",
        "professional_dark": "داكن احترافي",
        "arabic": "العربية",
        "english": "الإنجليزية",
        "login_title": "تسجيل الدخول - أداة Ultimat-Unlock",
        "username_label": "اسم المستخدم:",
        "password_label": "كلمة المرور:",
        "login_button": "تسجيل الدخول",
        "login_failed_title": "فشل تسجيل الدخول",
        "login_failed_message": "اسم المستخدم أو كلمة المرور غير صحيحة.",
        "arabize_confirm_title": "تأكيد التعريب",
        "arabize_confirm_message": "سيحاول هذا الإجراء تغيير لغة الجهاز إلى العربية (ar-AE).\nقد يتطلب هذا أذونات معينة وقد لا يعمل على جميع الأجهزة.\nمتابعة؟",
        "arabize_note": "ملاحظة: قد يتطلب التعريب إذن WRITE_SECURE_SETTINGS أو صلاحيات الروت على بعض الأجهزة.",
        "open_browser_title": "فتح رابط في متصفح الجهاز",
        "open_browser_prompt": "أدخل الرابط الكامل للفتح (مثال: https://ultimat-unlock.com/):",
        "frp_reset_warning_title": "محاولة إزالة FRP",
        "frp_reset_warning_message": "سيقوم هذا الإجراء بمحاولة تنفيذ سلسلة من أوامر ADB الشائعة لإزالة قفل FRP. هذه الأوامر ليست مضمونة للعمل على جميع الأجهزة أو إصدارات أندرويد وقد تتطلب أذونات معينة أو صلاحيات الروت. قم بالمتابعة بحذر.",
        "context_cut": "قص",
        "context_copy": "نسخ",
        "context_paste": "لصق",
        "context_select_all": "تحديد الكل",
        "log_connect_server_success": "الاتصال بالخادم... ناجح",
        "log_operation_started": "بدء العملية: ",
        "log_device_info_header": "معلومات الجهاز:",
        "log_frp_reset_ok": "إعادة تعيين FRP.... تم بنجاح",
        "log_frp_reset_fail": "إعادة تعيين FRP.... فشل",
        "log_read_info_complete": "قراءة المعلومات.... اكتمل"
    }
}
log_to_file_debug_globally("LABELS defined.")

# ========== THEMES ==========
THEMES = {
    "light": {
        "BG": "#ECEFF1", "FG": "#263238", "ACCENT": "#03A9F4", "ACCENT2": "#0288D1", "PROGRESS_BAR_BG": "#2ECC71",
        "BTN_BG": "#03A9F4", "BTN_BG2": "#0288D1", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#0277BD",
        "GROUP_BG": "#FFFFFF", "LOG_BG": "#CFD8DC",
        "LOG_FG_SUCCESS": "#4CAF50", "LOG_FG_INFO": "#2196F3", "LOG_FG_ERROR": "#F44336",
        "LOG_FG_FAIL": "#D32F2F", "LOG_FG_CMD": "#00796B", "LOG_FG_WARNING": "#FF9800",
        "STATUS_BAR_BG": "#B0BEC5", "STATUS_BAR_FG": "#263238",
        "NOTEBOOK_TAB_BG": "#B0BEC5", "NOTEBOOK_TAB_FG": "#37474F",
        "NOTEBOOK_TAB_SELECTED_BG": "#03A9F4", "NOTEBOOK_TAB_SELECTED_FG": "#FFFFFF",
        "NOTEBOOK_TAB_ACTIVE_BG": "#0288D1"
    },
    "dark": {
        "BG": "#263238", "FG": "#ECEFF1", "ACCENT": "#03A9F4", "ACCENT2": "#0288D1", "PROGRESS_BAR_BG": "#2ECC71",
        "BTN_BG": "#03A9F4", "BTN_BG2": "#0288D1", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#03A9F4",
        "GROUP_BG": "#37474F", "LOG_BG": "#455A64",
        "LOG_FG_SUCCESS": "#81C784", "LOG_FG_INFO": "#64B5F6", "LOG_FG_ERROR": "#E57373",
        "LOG_FG_FAIL": "#EF5350", "LOG_FG_CMD": "#4DB6AC", "LOG_FG_WARNING": "#FFB74D",
        "STATUS_BAR_BG": "#212121", "STATUS_BAR_FG": "#03A9F4",
        "NOTEBOOK_TAB_BG": "#37474F", "NOTEBOOK_TAB_FG": "#B0BEC5",
        "NOTEBOOK_TAB_SELECTED_BG": "#03A9F4", "NOTEBOOK_TAB_SELECTED_FG": "#FFFFFF",
        "NOTEBOOK_TAB_ACTIVE_BG": "#0288D1"
    },
    "professional_dark": {
        "BG": "#21252B", "FG": "#D1D9E0", "ACCENT": "#00AEEF", "ACCENT2": "#0095CC", "PROGRESS_BAR_BG": "#2ECC71", # Green progress bar
        "BTN_BG": "#00AEEF", "BTN_BG2": "#0095CC", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#00AEEF",
        "GROUP_BG": "#2C313A", "LOG_BG": "#2C313A",
        "LOG_FG_SUCCESS": "#2ECC71", "LOG_FG_INFO": "#3498DB", "LOG_FG_ERROR": "#E74C3C", 
        "LOG_FG_FAIL": "#C0392B", "LOG_FG_CMD": "#1ABC9C", "LOG_FG_WARNING": "#F39C12", 
        "STATUS_BAR_BG": "#1A1D21", "STATUS_BAR_FG": "#00AEEF",
        "NOTEBOOK_TAB_BG": "#2C313A", "NOTEBOOK_TAB_FG": "#AAB8C5",
        "NOTEBOOK_TAB_SELECTED_BG": "#00AEEF", "NOTEBOOK_TAB_SELECTED_FG": "#FFFFFF",
        "NOTEBOOK_TAB_ACTIVE_BG": "#0095CC",
        "TITLE_FG": "#FFFFFF", "EDITION_FG": "#AAB8C5"
    }
}
log_to_file_debug_globally("THEMES defined.")

FONT = ("Segoe UI", 10)
TITLE_FONT = ("Segoe UI Semibold", 18)
LABEL_FONT = ("Segoe UI", 9, "bold")
BTN_FONT = ("Segoe UI", 10, "bold")
LOG_FONT = ("Consolas", 11) 
log_to_file_debug_globally("FONTS defined.")

# Device properties to fetch for the info block
DEVICE_INFO_PROPERTIES = [
    ("Model", "ro.product.model"), 
    ("Device", "ro.product.device"), 
    ("Brand Name", "ro.product.brand"),
    ("Chipset", "ro.board.platform"), # often gives chipset name like msm8996, exynos...
    ("Hw Version", "ro.hardware"), # Sometimes gives board name
    ("Android Version", "ro.build.version.release"),
    ("Usb.config", "sys.usb.config"), # Current USB configuration
    ("Model ID", "ro.build.display.id"), # Often full build string
    ("PDA", "ro.build.id"), # PDA/Build ID
    ("Platform", "ro.product.cpu.abi"), # e.g. arm64-v8a
    ("language", "ro.product.locale"),
    ("Security Patch", "ro.build.version.security_patch"),
    ("Root State", "ro.secure"), # 0 for root, 1 for no root (can also check for 'su' binary)
    ("Encryption State", "ro.crypto.state"), # e.g. encrypted
    ("Bootloader State", "ro.bootloader"), # Bootloader version
    ("description", "ro.build.description")
]


def get_labels(lang):
    return LABELS.get(lang, LABELS["en"])

def get_theme(theme_name):
    return THEMES.get(theme_name, THEMES["professional_dark"])

class ModernButton(tk.Button):
    def __init__(self, master, text, command, theme, width=25, height=2, icon=None, state=tk.NORMAL, **kwargs): 
        display_text = f"{icon} {text}" if icon else text
        super().__init__(
            master, text=display_text, command=command, font=BTN_FONT,
            bg=theme["BTN_BG"], fg=theme["BTN_FG"],
            activebackground=theme["BTN_BG2"], activeforeground=theme["BTN_FG"],
            bd=0, relief="flat", cursor="hand2", height=height, width=width,
            padx=10, pady=5, state=state, **kwargs) 
        self.theme = theme
        self.default_bg = theme["BTN_BG"]
        self.hover_bg = theme["BTN_BG2"]
        self.config(highlightbackground=theme.get("BTN_BORDER", theme["ACCENT"]), highlightthickness=1)
        
        if state == tk.NORMAL:
            self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg) if self.cget('state') == tk.NORMAL else None)
            self.bind("<Leave>", lambda e: self.config(bg=self.default_bg) if self.cget('state') == tk.NORMAL else None)
        elif state == tk.DISABLED:
            self.config(bg=theme.get("GROUP_BG", "#2C313A"), fg=theme.get("NOTEBOOK_TAB_FG", "#AAB8C5"))


class DBLogger:
    def __init__(self, dbfile=None, tk_root=None):
        log_to_file_debug_globally("DBLogger __init__ started.")
        if dbfile is None:
            try:
                base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                dbfile = os.path.join(base_dir, "operation_log.db")
                os.makedirs(os.path.dirname(dbfile), exist_ok=True)
                with open(dbfile, "a") as f_db_check: # Ensure file can be created/accessed
                    os.utime(dbfile, None)
                log_to_file_debug_globally(f"DBLogger: DB file path set to: {dbfile}")
            except Exception as e_db_path1:
                log_to_file_debug_globally(f"DBLogger: Failed to create DB at primary path {dbfile}: {e_db_path1}", "WARNING")
                try:
                    user_dir = os.path.expanduser("~")
                    dbfile_fallback = os.path.join(user_dir, ".UltimatUnlockTool", "operation_log.db")
                    os.makedirs(os.path.dirname(dbfile_fallback), exist_ok=True)
                    with open(dbfile_fallback, "a") as f_db_check_fb:
                         os.utime(dbfile_fallback, None)
                    dbfile = dbfile_fallback
                    log_to_file_debug_globally(f"DBLogger: DB file path set to fallback: {dbfile}")
                except Exception as e_db_path2:
                    log_to_file_debug_globally(f"DBLogger: Failed to create DB at fallback path {dbfile_fallback}: {e_db_path2}", "ERROR")
                    dbfile = ":memory:" # Fallback to in-memory if all else fails
                    log_to_file_debug_globally("DBLogger: Using in-memory database as last resort.")
        
        self.dbfile = dbfile
        self.tk_root = tk_root
        self.conn = None
        self.cursor = None
        
        try:
            self.conn = sqlite3.connect(self.dbfile, check_same_thread=False) 
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 timestamp TEXT,
                                 tag TEXT,
                                 message TEXT)''')
            self.conn.commit()
            log_to_file_debug_globally("DBLogger: Database initialized/checked.")
        except Exception as e_db_init:
            log_to_file_debug_globally(f"DBLogger: Database initialization error: {e_db_init}", "ERROR")
            if self.conn:
                self.conn.close()
            self.conn = None # Ensure conn and cursor are None if init fails
            self.cursor = None
        log_to_file_debug_globally("DBLogger __init__ finished.")

    def add(self, message, tag="info"):
        if not self.conn or not self.cursor:
            log_to_file_debug_globally(f"DBLogger: Cannot add log, database not initialized. Message: {message}", "WARNING")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO logs (timestamp, tag, message) VALUES (?, ?, ?)",
                               (timestamp, tag, message))
            self.conn.commit()
        except Exception as e_add:
            log_to_file_debug_globally(f"DBLogger: Error adding log: {e_add}. Message: {message}", "ERROR")

    def search(self, term): # Not used by UI anymore but kept for backend
        if not self.conn or not self.cursor:
            log_to_file_debug_globally(f"DBLogger: Cannot search, database not initialized. Term: {term}", "WARNING")
            return []
        
        try:
            self.cursor.execute("SELECT timestamp, tag, message FROM logs WHERE message LIKE ? ORDER BY id DESC LIMIT 1000",
                               (f"%{term}%",))
            return self.cursor.fetchall()
        except Exception as e_search:
            log_to_file_debug_globally(f"DBLogger: Error searching logs: {e_search}. Term: {term}", "ERROR")
            return []

    def all(self, limit=1000): # Not used by UI anymore but kept for backend
        if not self.conn or not self.cursor:
            log_to_file_debug_globally("DBLogger: Cannot fetch all, database not initialized.", "WARNING")
            return []
        
        try:
            self.cursor.execute("SELECT timestamp, tag, message FROM logs ORDER BY id DESC LIMIT ?", (limit,))
            return self.cursor.fetchall()
        except Exception as e_all:
            log_to_file_debug_globally(f"DBLogger: Error fetching all logs: {e_all}", "ERROR")
            return []

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                log_to_file_debug_globally("DBLogger: Database connection closed.")
            except Exception as e_close:
                log_to_file_debug_globally(f"DBLogger: Error closing database: {e_close}", "ERROR")

class TextContextMenu:
    def __init__(self, widget, tk_root, labels):
        self.widget = widget
        self.tk_root = tk_root 
        self.labels = labels    
        self.menu = tk.Menu(widget, tearoff=0)

        self.menu.add_command(label=self.labels.get("context_cut", "Cut"), command=self.cut)
        self.menu.add_command(label=self.labels.get("context_copy", "Copy"), command=self.copy)
        self.menu.add_command(label=self.labels.get("context_paste", "Paste"), command=self.paste)
        self.menu.add_separator()
        self.menu.add_command(label=self.labels.get("context_select_all", "Select All"), command=self.select_all)

        widget.bind("<Button-3>", self.show_menu) 

    def show_menu(self, event):
        has_selection = False
        try:
            if self.widget.selection_get():
                has_selection = True
        except tk.TclError:
            has_selection = False

        is_editable = isinstance(self.widget, (tk.Entry, tk.Text)) and self.widget.cget('state') == tk.NORMAL
        self.menu.entryconfig(self.labels.get("context_cut", "Cut"), state=tk.NORMAL if has_selection and is_editable else tk.DISABLED)
        self.menu.entryconfig(self.labels.get("context_copy", "Copy"), state=tk.NORMAL if has_selection else tk.DISABLED)
        
        can_paste = False
        try:
            # Check clipboard and if widget is editable
            if self.tk_root.clipboard_get() and is_editable :
                can_paste = True
        except tk.TclError: # Clipboard might be empty or contain non-string data
            can_paste = False
        self.menu.entryconfig(self.labels.get("context_paste", "Paste"), state=tk.NORMAL if can_paste else tk.DISABLED)
        
        has_text = False
        if isinstance(self.widget, tk.Text):
            if self.widget.get("1.0", tk.END).strip(): # Check if text area has content
                has_text = True
        elif isinstance(self.widget, tk.Entry):
            if self.widget.get().strip(): # Check if entry has content
                has_text = True
        
        self.menu.entryconfig(self.labels.get("context_select_all", "Select All"), state=tk.NORMAL if has_text else tk.DISABLED)

        self.menu.tk_popup(event.x_root, event.y_root)

    def cut(self):
        try:
            if self.widget.selection_get() and self.widget.cget('state') == tk.NORMAL:
                self.widget.event_generate("<<Cut>>")
        except tk.TclError:
            pass 

    def copy(self):
        try:
            if self.widget.selection_get():
                self.widget.event_generate("<<Copy>>")
        except tk.TclError:
            pass 

    def paste(self):
        try:
            if self.widget.cget('state') == tk.NORMAL: # Check if widget is editable
                 self.widget.event_generate("<<Paste>>")
        except tk.TclError:
            pass 

    def select_all(self):
        if isinstance(self.widget, tk.Text):
            self.widget.tag_add(tk.SEL, "1.0", tk.END)
            self.widget.mark_set(tk.INSERT, "1.0") 
            self.widget.see(tk.INSERT) # Ensure selection is visible
        elif isinstance(self.widget, tk.Entry):
            self.widget.select_range(0, tk.END)
            self.widget.icursor(tk.END) # Move cursor to end
        return "break" # To prevent default binding propagation


class ProgressBarManager(tk.Frame):
    def __init__(self, master, theme):
        super().__init__(master, bg=theme["BG"])
        self.var = tk.IntVar(value=0)
        # Use a specific green from the theme or a fallback green
        progress_bar_color = theme.get("PROGRESS_BAR_BG", "#2ECC71") # Default to a nice green
        
        lightcolor = progress_bar_color 
        darkcolor = theme.get("ACCENT2", "#0095CC") # This is for gradient, less important if flat
        troughcolor = theme.get("GROUP_BG", theme.get("BG", "#21252B")) # Background of the trough
        bordercolor = progress_bar_color # Border color same as bar

        thickness = 12

        self.pb = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="indeterminate", 
            variable=self.var,
            style="Green.Horizontal.TProgressbar" # Use a custom style name
        )
        self.running = False 

        style = ttk.Style()
        # Configure the custom style for the progress bar
        style.configure(
            "Green.Horizontal.TProgressbar",
            troughcolor=troughcolor,
            bordercolor=bordercolor,
            background=progress_bar_color, # This is the main bar color
            lightcolor=lightcolor, # For gradient effect (if supported by theme/OS)
            darkcolor=darkcolor,   # For gradient effect
            thickness=thickness
        )
        self.pb.pack(fill=tk.X, padx=10, pady=(2,5)) 

    def start(self): 
        if not self.winfo_exists(): return
        if not self.running:
            self.pb.config(mode="indeterminate")
            self.pb.start(10) # Speed of indeterminate animation
            self.running = True

    def stop(self): 
        if not self.winfo_exists(): return
        if self.running:
            self.pb.stop()
            self.running = False
        self.pb.config(mode="determinate") # Switch to determinate mode
        self.var.set(0) # Reset value
        self.pb.update_idletasks()

    def set_value(self, percent): 
        if not self.winfo_exists(): return
        if self.running: 
            self.pb.stop()
            self.running = False
        self.pb.config(mode="determinate")
        self.var.set(max(0, min(100, int(percent)))) # Ensure value is between 0-100
        self.pb.update_idletasks()


class LogPanel(tk.Frame):
    def __init__(self, master, theme, labels, db_logger=None, tk_root=None, app_controller=None): 
        super().__init__(master, bg=theme["BG"])
        self.labels = labels
        self.theme = theme
        self.tk_root = tk_root
        self.app_controller = app_controller 
        
        log_title_frame = tk.Frame(self, bg=theme["BG"])
        log_title_frame.pack(fill=tk.X, padx=6, pady=(8,2))
        tk.Label(log_title_frame, text=labels["log"], font=LABEL_FONT, bg=theme["BG"], fg=theme.get("FG", "#D1D9E0")).pack(side=tk.LEFT)

        self.text = tk.Text(self, height=25, font=LOG_FONT, state=tk.DISABLED,
                            bg=theme["LOG_BG"], fg=theme["LOG_FG_INFO"],
                            bd=1, relief="sunken", wrap=tk.WORD,
                            selectbackground=theme["ACCENT"], selectforeground=theme["BTN_FG"],
                            insertbackground=theme["FG"])
        self.text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0,6))
        TextContextMenu(self.text, self.tk_root, self.labels) 

        # Configure tags for different log message types
        for tag_name, color_key in [("info", "LOG_FG_INFO"), ("success", "LOG_FG_SUCCESS"), 
                                    ("error", "LOG_FG_ERROR"), ("fail", "LOG_FG_FAIL"), 
                                    ("cmd", "LOG_FG_CMD"), ("warning", "LOG_FG_WARNING"),
                                    ("device_info_label", "FG"), # For labels like "Model:"
                                    ("device_info_value", "ACCENT")]: # For values like "SM-J400F"
            
            font_config = LOG_FONT
            if tag_name in ["success", "error", "fail"]:
                font_config = (LOG_FONT[0], LOG_FONT[1], "bold")
            if tag_name == "fail":
                font_config = (LOG_FONT[0], LOG_FONT[1], "bold", "underline")
            if tag_name == "device_info_label":
                 font_config = (LOG_FONT[0], LOG_FONT[1], "bold")


            self.text.tag_configure(tag_name, foreground=theme[color_key], font=font_config)
        
        self.db_logger = db_logger # For background logging if needed, not for UI display
        self.progress_bar = ProgressBarManager(self, theme)
        self.progress_bar.pack(fill=tk.X, padx=6)
        
        # Frame for the cancel button
        controls_frame = tk.Frame(self, bg=theme["BG"])
        controls_frame.pack(fill=tk.X, padx=6, pady=(6,10))
        
        self.cancel_button = ModernButton(controls_frame, labels.get("btn_cancel_operation", "Cancel Operation"),
                                           command=self.app_controller.action_cancel_operation if self.app_controller else None, 
                                           theme=theme, width=20, height=1, icon="", state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 4)) # Pack to the left or center as desired
        if self.app_controller: 
            self.app_controller.set_cancel_button_reference(self.cancel_button)


    def log(self, message, tag="info", indent=0): # Added indent parameter
        if not self.winfo_exists(): return
        
        # Ensure logging happens on the main thread for UI updates
        def __log_to_widget():
            if not self.text.winfo_exists(): return
            self.text.config(state=tk.NORMAL)
            
            timestamp_str = f"[{datetime.now().strftime('%H:%M:%S')}] "
            
            # Standard prefixes for non-device info lines
            prefix_map = {"cmd": "[CMD]", "success": "[OK]", "error": "[ERR]", "fail": "[FAIL]", "warning": "[WARN]", "info": "[INFO]"}
            log_prefix = prefix_map.get(tag, "[LOG]") # Default prefix

            # Indentation for structured logging (like device info)
            indent_space = "  " * indent 

            # For device info, we might not want a prefix like [INFO] for each line
            if tag.startswith("device_info_"):
                full_log_message = f"{timestamp_str}{indent_space}{message}\n"
            else:
                full_log_message = f"{timestamp_str}{indent_space}{log_prefix} {message}\n"

            idx = self.text.index(tk.END + "-1c linestart") # Get start of the line where text will be inserted
            self.text.insert(tk.END, full_log_message)
            self.text.tag_add(tag, idx, f"{idx} + {len(full_log_message)-1}c") # Apply tag to the inserted line
            
            self.text.see(tk.END) # Scroll to the end
            self.text.config(state=tk.DISABLED)
            
            # Log to DB if available (original message without timestamp/prefix for cleaner DB storage)
            if self.db_logger: self.db_logger.add(message, tag)
        
        if self.tk_root and hasattr(self.tk_root, 'after') and self.tk_root.winfo_exists(): 
            if threading.current_thread() is not threading.main_thread():
                self.tk_root.after(0, __log_to_widget)
            else:
                __log_to_widget()
        else: 
             __log_to_widget()

    def log_device_info_block(self, device_info_dict):
        """Logs a block of device information as per the new format."""
        if not self.winfo_exists(): return

        self.log(self.labels.get("log_connect_server_success", "Connect to server...successful"), "info")
        # self.log(self.labels.get("log_device_info_header", "Device Information:"), "info")

        max_label_len = 0
        if device_info_dict:
            max_label_len = max(len(label) for label, prop_key in DEVICE_INFO_PROPERTIES if label in device_info_dict) +1 # For spacing
        
        for label, prop_key in DEVICE_INFO_PROPERTIES:
            value = device_info_dict.get(label, "N/A") # Get value by display label
            if label == "Root State": # Custom handling for root state
                value = "No Root!" if value == "1" else ("Rooted!" if value == "0" else "Unknown")

            # Log label and value on the same line, applying different tags
            # This is a bit more complex to do with current self.log, might need direct text insertion
            
            if not self.text.winfo_exists(): return
            self.text.config(state=tk.NORMAL)
            timestamp_str = f"[{datetime.now().strftime('%H:%M:%S')}] "
            
            # Format the line: Timestamp Label : Value
            # Pad the label part for alignment
            formatted_label = f"{label}:".ljust(max_label_len +1) # +1 for the colon
            line_content = f"{timestamp_str}  {formatted_label} {value}\n"
            
            # Insert the line
            insert_pos = self.text.index(tk.END + "-1c linestart")
            self.text.insert(tk.END, line_content)
            
            # Apply tags: one for the label part, one for the value part
            # This requires careful index calculation.
            # Simpler: apply a general "info" tag or specific device_info tag to the whole line.
            # For now, let's use a simpler approach:
            # self.log(f"{formatted_label} {value}", "device_info_value", indent=1)
            # This will use the log function's prefix.
            # To achieve the exact visual style from example, manual insertion and tagging is better.

            # Manual insertion and tagging for label : value on one line
            start_index_line = self.text.index(tk.END + f"-{len(line_content)}c linestart")
            
            # Tag for timestamp (optional, could be part of default log style)
            # Tag for indent (already handled by indent_space if using self.log)
            
            # Tag for Label
            label_start_index = self.text.index(f"{start_index_line} + {len(timestamp_str)}c + 2c") # After timestamp and indent
            label_end_index = self.text.index(f"{label_start_index} + {len(formatted_label)}c")
            self.text.tag_add("device_info_label", label_start_index, label_end_index)

            # Tag for Value
            value_start_index = self.text.index(f"{label_end_index} + 1c") # After the space
            value_end_index = self.text.index(f"{value_start_index} + {len(value)}c")
            self.text.tag_add("device_info_value", value_start_index, value_end_index)
            
            self.text.config(state=tk.DISABLED)
        
        if self.text.winfo_exists(): self.text.see(tk.END)


    # Methods like show_search, show_all, save_to_file, export_to_csv are removed as UI elements are gone.
    # They could be kept if there's a plan to re-add UI for them or use them programmatically.
    # For now, removing them to simplify LogPanel according to the request.


class StatusBar(tk.Label):
    def __init__(self, master, theme, labels):
        super().__init__(master, anchor="w", font=("Segoe UI", 10),
                         bg=theme.get("STATUS_BAR_BG", theme["BG"]),
                         fg=theme.get("STATUS_BAR_FG", theme["ACCENT"]),
                         padx=10, pady=4)
        self.theme = theme
        self.labels = labels
        self._check_adb_after_id = None
        self.set_status(self.labels["adb_status_not_connected"], theme.get("LOG_FG_ERROR", "#F44336"))
        self._check_adb()

    def set_status(self, text, color):
        if self.winfo_exists(): self.config(text=text, fg=color)

    def _check_adb(self):
        def check_thread_func():
            stat = self.labels["adb_status_not_connected"]
            color = self.theme.get("LOG_FG_ERROR", "#F44336")
            try:
                flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                out = subprocess.check_output(['adb', 'get-state'], stderr=subprocess.STDOUT, text=True, timeout=2, creationflags=flags)
                if "device" in out:
                    stat = self.labels["adb_status_connected"]
                    color = self.theme.get("LOG_FG_SUCCESS", "#4CAF50")
            except Exception: pass # Ignore errors, status remains not connected
            
            # Safely update UI from thread
            if self.winfo_exists() and self.master.winfo_exists(): # Check master too
                 self.master.after(0, lambda s=stat, c=color: self.set_status(s, c))
            
            # Reschedule if widget still exists
            if self.winfo_exists():
                 self._check_adb_after_id = self.after(5000, self._check_adb)

        threading.Thread(target=check_thread_func, daemon=True).start()

    def cancel_adb_check(self):
        if self._check_adb_after_id:
            self.after_cancel(self._check_adb_after_id)
            self._check_adb_after_id = None

class LoginWindow(tk.Toplevel):
    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.parent = parent
        self.app_controller = app_controller
        self.labels = app_controller.labels
        self.theme = app_controller.theme
        
        self.title(self.labels.get("login_title", "Login"))
        self.geometry("400x250")
        self.resizable(False, False)
        self.configure(bg=self.theme["BG"])
        self.protocol("WM_DELETE_WINDOW", self._on_closing_login)

        # Center window
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        if parent_width < 50 or parent_height < 50: # Parent might be withdrawn
             parent_width = self.parent.winfo_screenwidth()
             parent_height = self.parent.winfo_screenheight()
             parent_x = 0 # Assume screen origin
             parent_y = 0

        x = parent_x + (parent_width // 2) - (400 // 2)
        y = parent_y + (parent_height // 2) - (250 // 2)
        self.geometry(f"+{x}+{y}")

        main_frame = tk.Frame(self, bg=self.theme["BG"], padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(main_frame, text=self.labels.get("login_title", "Login"), font=TITLE_FONT, bg=self.theme["BG"], fg=self.theme.get("TITLE_FG", self.theme["ACCENT"])).pack(pady=(0, 20))

        tk.Label(main_frame, text=self.labels.get("username_label", "Username:"), font=FONT, bg=self.theme["BG"], fg=self.theme["FG"]).pack(anchor=tk.W)
        self.username_entry = tk.Entry(main_frame, font=FONT, width=30, bg=self.theme.get("LOG_BG", "#455A64"), fg=self.theme["FG"], insertbackground=self.theme["FG"])
        self.username_entry.pack(pady=(0,10), ipady=3)
        TextContextMenu(self.username_entry, self, self.labels) 

        tk.Label(main_frame, text=self.labels.get("password_label", "Password:"), font=FONT, bg=self.theme["BG"], fg=self.theme["FG"]).pack(anchor=tk.W)
        self.password_entry = tk.Entry(main_frame, font=FONT, width=30, show="*", bg=self.theme.get("LOG_BG", "#455A64"), fg=self.theme["FG"], insertbackground=self.theme["FG"])
        self.password_entry.pack(pady=(0,20), ipady=3)
        self.password_entry.bind("<Return>", self._attempt_login) # Bind Enter key
        TextContextMenu(self.password_entry, self, self.labels) 

        ModernButton(main_frame, text=self.labels.get("login_button", "Login"), command=self._attempt_login, theme=self.theme, width=15, height=1).pack()
        
        self.grab_set() # Make window modal
        self.focus_set() # Focus on this window
        self.username_entry.focus() # Focus on username entry

    def _attempt_login(self, event=None): # Added event=None for Enter key binding
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == FIXED_USERNAME and password == FIXED_PASSWORD:
            log_to_file_debug_globally("Login successful.")
            self.destroy() # Close login window
            self.app_controller.show_main_app() # Show main application
        else:
            log_to_file_debug_globally("Login failed.")
            messagebox.showerror(self.labels.get("login_failed_title", "Login Failed"),
                                 self.labels.get("login_failed_message", "Invalid username or password."),
                                 parent=self) # Set parent for messagebox
            self.password_entry.delete(0, tk.END) # Clear password field
            self.username_entry.focus() # Refocus username

    def _on_closing_login(self):
        log_to_file_debug_globally("Login window closed by user. Exiting application.")
        self.parent.destroy() # Exit the whole application if login is closed

class AppController:
    def __init__(self):
        log_to_file_debug_globally("AppController __init__ started.")
        self.root = tk.Tk()
        self.root.withdraw() # Hide root window initially

        self.lang = "en" # Default language
        self.theme_mode = "professional_dark" # Default theme
        self.labels = get_labels(self.lang)
        self.theme = get_theme(self.theme_mode)
        
        self.main_app_window = None 
        self.cancel_button_ref = None 

        # Attempt to open website (optional)
        try:
            webbrowser.open("https://ultimat-unlock.com/")
            log_to_file_debug_globally("Website opened successfully.")
        except Exception as e_web:
            log_to_file_debug_globally(f"Failed to open website: {e_web}", "WARNING")

        self.login_window = LoginWindow(self.root, self) # Create and show login window
        log_to_file_debug_globally("LoginWindow instantiated.")

    def start(self):
        log_to_file_debug_globally("AppController start, entering root.mainloop().")
        self.root.mainloop()

    def show_main_app(self):
        log_to_file_debug_globally("show_main_app called.")
        self.root.deiconify() # Show the main root window
        if self.main_app_window is None:
            self.main_app_window = UltimateDeviceTool(master_tk_instance=self.root, app_controller=self)
            log_to_file_debug_globally("UltimateDeviceTool instantiated as main_app_window.")
        else: # Should not happen if login is modal and main app created after login
            log_to_file_debug_globally("Main app window already exists, deiconifying.", "WARNING")
            if isinstance(self.main_app_window, UltimateDeviceTool) and self.main_app_window.winfo_exists():
                 self.main_app_window.master.deiconify() 
            else: # Recreate if something went wrong
                 self.main_app_window = UltimateDeviceTool(master_tk_instance=self.root, app_controller=self)
    
    def set_cancel_button_reference(self, button_widget):
        self.cancel_button_ref = button_widget

    def action_cancel_operation(self):
        if self.main_app_window: # Ensure main app window exists
            self.main_app_window.action_cancel_operation()
        else:
            log_to_file_debug_globally("Cancel action called but main_app_window not available.", "WARNING")


class UltimateDeviceTool(tk.Frame):
    def __init__(self, master_tk_instance, app_controller):
        log_to_file_debug_globally("UltimateDeviceTool __init__ started.")
        super().__init__(master_tk_instance)
        
        self.master = master_tk_instance
        self.app_controller = app_controller 

        self.lang = self.app_controller.lang
        self.theme_mode = self.app_controller.theme_mode
        self.labels = get_labels(self.lang)
        self.theme = get_theme(self.theme_mode)

        self.db_logger = DBLogger(tk_root=self.master) # Initialize DBLogger
        log_to_file_debug_globally("Instance variables (lang, theme, db_logger) initialized.")
        
        self.master.title(self.labels["title"])
        self.master.geometry("1280x800") # Initial size
        self.master.wm_minsize(1024, 700) # Minimum size
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing) # Handle window close
        log_to_file_debug_globally("Window properties (title, geometry, minsize, protocol) set on master.")
        
        self.pack(fill=tk.BOTH, expand=True) # Make frame fill the window

        self._apply_styles()
        self._build_ui()
        self.command_queue = queue.Queue() # Queue for command results
        self.current_popen_process = None # To hold the current running subprocess
        self.after_id_process_command_queue = self.after(100, self._process_command_queue) # Start processing queue
        log_to_file_debug_globally("UltimateDeviceTool __init__ finished successfully.")

    def _apply_styles(self):
        log_to_file_debug_globally("Applying styles...")
        self.style = ttk.Style(self.master)
        try:
            self.style.theme_use('clam') 
        except tk.TclError:
            log_to_file_debug_globally("Clam theme not available. Default theme will be used.", "WARNING")
        
        # Notebook styles
        self.style.configure("TNotebook", background=self.theme["BG"], borderwidth=0, tabmargins=[2, 5, 2, 0])
        self.style.configure("TNotebook.Tab", background=self.theme.get("NOTEBOOK_TAB_BG", self.theme["GROUP_BG"]),
                                            foreground=self.theme.get("NOTEBOOK_TAB_FG", self.theme["FG"]),
                                            padding=[10, 5], font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("TNotebook.Tab",
                       background=[("selected", self.theme.get("NOTEBOOK_TAB_SELECTED_BG", self.theme["ACCENT"])),
                                   ("active", self.theme.get("NOTEBOOK_TAB_ACTIVE_BG", self.theme["ACCENT2"]))],
                       foreground=[("selected", self.theme.get("NOTEBOOK_TAB_SELECTED_FG", self.theme["BTN_FG"]))])
        
        self.style.configure("TPanedwindow", background=self.theme["BG"])
        self.style.configure("TFrame", background=self.theme["BG"]) # Default for ttk.Frame
        log_to_file_debug_globally("Styles applied.")

    def _build_ui(self):
        log_to_file_debug_globally("Building UI...")
        self.config(bg=self.theme["BG"])

        # Menubar
        menubar = tk.Menu(self.master, bg=self.theme["BG"], fg=self.theme["FG"], relief=tk.FLAT, bd=0, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu.add_command(label=self.labels["light"], command=lambda: self.set_theme("light"))
        theme_menu.add_command(label=self.labels["dark"], command=lambda: self.set_theme("dark"))
        theme_menu.add_command(label=self.labels["professional_dark"], command=lambda: self.set_theme("professional_dark"))
        menubar.add_cascade(label=self.labels["theme"], menu=theme_menu)
        
        lang_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        lang_menu.add_command(label=LABELS["en"]["english"], command=lambda: self.set_language("en")) # Use global LABELS for menu items
        lang_menu.add_command(label=LABELS["ar"]["arabic"], command=lambda: self.set_language("ar"))
        menubar.add_cascade(label=self.labels["lang"], menu=lang_menu)
        self.master.config(menu=menubar)

        # Status Bar
        self.status_bar = StatusBar(self, self.theme, self.labels)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Main Paned Window (Left: Controls, Right: Log)
        body = ttk.PanedWindow(self, orient=tk.HORIZONTAL, style="TPanedwindow")
        body.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_area_container = tk.Frame(body, bg=self.theme["BG"])
        right_area_container = tk.Frame(body, bg=self.theme["BG"])
        body.add(left_area_container, weight=2) 
        body.add(right_area_container, weight=1) 

        # Title Area (in left container)
        title_frame = tk.Frame(left_area_container, bg=self.theme["BG"])
        title_frame.pack(fill=tk.X, pady=(15, 8), padx=(15,0))
        tk.Label(title_frame, text=self.labels["title"], font=TITLE_FONT, bg=self.theme["BG"], fg=self.theme.get("TITLE_FG", self.theme["ACCENT"]) ).pack(side=tk.LEFT, padx=(0,10))
        tk.Label(title_frame, text=self.labels["edition"], font=LABEL_FONT, bg=self.theme["BG"], fg=self.theme.get("EDITION_FG", self.theme["FG"]) ).pack(side=tk.LEFT, pady=(6,0))
        
        # Notebook for tabs (in left container)
        self.notebook = ttk.Notebook(left_area_container, style="TNotebook")
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=15, pady=(0,15))
        
        # Log Panel (in right container)
        try: 
            self.log_panel = LogPanel(right_area_container, self.theme, self.labels, db_logger=self.db_logger, tk_root=self.master, app_controller=self.app_controller)
            self.log_panel.pack(fill=tk.BOTH, expand=True, padx=(5,15), pady=(15,15))
            log_to_file_debug_globally("Log panel created.")
        except Exception as e_log_panel:
            log_to_file_debug_globally(f"Error creating LogPanel: {e_log_panel}", "CRITICAL")
            traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a")) # Log full traceback
        
        # Add Tabs to Notebook
        tabs_to_add = [
            (SamsungTab, "tab_samsung"),
            (HonorTab, "tab_honor"),
            (XiaomiTab, "tab_xiaomi"),
            (FileAdvancedTab, "tab_file_advanced")
        ]
        
        for TabClass, label_key in tabs_to_add:
            try:
                tab_instance = TabClass(self.notebook, self) 
                self.notebook.add(tab_instance, text=self.labels[label_key], padding=10)
                log_to_file_debug_globally(f"{TabClass.__name__} added to notebook.")
            except Exception as e_tab_creation:
                log_to_file_debug_globally(f"Error creating or adding {TabClass.__name__}: {e_tab_creation}", "ERROR")
                traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
                messagebox.showerror("UI Build Error", f"Failed to build {self.labels[label_key]} tab: {e_tab_creation}", parent=self.master)

        log_to_file_debug_globally("UI Building finished.")

    def _update_cancel_button_state(self, enable=False):
        if self.app_controller and self.app_controller.cancel_button_ref:
            button = self.app_controller.cancel_button_ref
            if button.winfo_exists(): # Check if button widget still exists
                 button.config(state=tk.NORMAL if enable else tk.DISABLED)
                 # Re-apply theme styles for disabled/enabled state
                 if not enable:
                     button.config(bg=self.theme.get("GROUP_BG", "#2C313A"), fg=self.theme.get("NOTEBOOK_TAB_FG", "#AAB8C5"))
                 else:
                     button.config(bg=self.theme["BTN_BG"], fg=self.theme["BTN_FG"])


    def execute_command_async(self, command_list, operation_name="Operation", callback_on_finish=None, is_part_of_sequence=False, is_info_gathering=False):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None and self.log_panel.winfo_exists()
        
        if log_panel_available and not is_part_of_sequence and not is_info_gathering: 
            self.log_panel.progress_bar.start()
            self._update_cancel_button_state(enable=True)
        
        command_str_for_debug = " ".join(map(str,command_list)) if isinstance(command_list, list) else str(command_list)
        # Avoid logging individual getprop for info gathering to debug log if too verbose, or use a specific tag
        if not is_info_gathering:
            log_to_file_debug_globally(f"Executing ASYNC ({operation_name}): {command_str_for_debug}", "DEBUG_CMD") 

        def _command_thread():
            process = None 
            try:
                # For Windows, hide the console window for subprocess
                startupinfo = None
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                           text=True, encoding='utf-8', errors='replace', 
                                           startupinfo=startupinfo, # For hiding console on Windows
                                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                self.current_popen_process = process
                stdout, stderr = process.communicate(timeout=120) 
                return_code = process.returncode
                result_data = {"stdout": stdout, "stderr": stderr, "return_code": return_code, 
                               "operation_name": operation_name, "command": command_list, 
                               "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence,
                               "is_info_gathering": is_info_gathering}
                self.command_queue.put(result_data)
            except subprocess.TimeoutExpired:
                if process: process.kill() 
                log_to_file_debug_globally(f"Timeout for {operation_name}: {command_str_for_debug}", "ERROR")
                self.command_queue.put({"error": "TimeoutExpired", "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence, "is_info_gathering": is_info_gathering})
            except FileNotFoundError:
                log_to_file_debug_globally(f"FileNotFound for {operation_name}: {command_list[0]}", "ERROR")
                self.command_queue.put({"error": "FileNotFound", "command_name": command_list[0], "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence, "is_info_gathering": is_info_gathering})
            except Exception as e: 
                if process and process.returncode is not None and process.returncode < 0 : 
                     self.command_queue.put({"error": "Cancelled", "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence, "is_info_gathering": is_info_gathering})
                else:
                     log_to_file_debug_globally(f"Exception for {operation_name} ({command_str_for_debug}): {e}", "ERROR")
                     traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
                     self.command_queue.put({"error": str(e), "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence, "is_info_gathering": is_info_gathering})
            finally:
                self.current_popen_process = None 
        
        threading.Thread(target=_command_thread, daemon=True).start()

    def _process_command_queue(self):
        try:
            while not self.command_queue.empty():
                result = self.command_queue.get_nowait()
                self._handle_command_result(result)
        except Exception as e: # Catch any error during queue processing
            log_to_file_debug_globally(f"Error in _process_command_queue: {e}", "ERROR")
            traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
        finally:
            if self.winfo_exists(): 
                self.after_id_process_command_queue = self.after(100, self._process_command_queue)


    def _handle_command_result(self, result):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None and self.log_panel.winfo_exists()
        log_method = self.log_panel.log if log_panel_available else log_to_file_debug_globally
        
        operation_name = result.get("operation_name", "Unknown Operation")
        is_part_of_sequence = result.get("is_part_of_sequence", False)
        is_info_gathering = result.get("is_info_gathering", False) # Check if it's an info gathering sub-command

        # For info gathering sub-commands (individual getprop), we don't log to UI via this handler.
        # The main calling function (e.g., action_get_detailed_info) will handle logging the block.
        if is_info_gathering and "error" not in result : # only skip if no error
            # If there's an error during info gathering, it might be useful to log it.
            # However, the main function will also report "Error fetching" for that property.
            # For now, let's allow errors from info_gathering to be logged.
            if result.get("return_code") == 0: # Successfully got a property, no UI log here.
                 pass # Callback will handle it
            # else: allow error logging below

        # Standard logging for other commands or errors during info gathering
        if not (is_info_gathering and result.get("return_code") == 0) : # Avoid double logging successful getprops
            if "error" in result:
                error_type = result["error"]
                error_message_summary = ""
                if error_type == "TimeoutExpired": error_message_summary = "Operation timed out"
                elif error_type == "FileNotFound": error_message_summary = f"Command '{result.get('command_name', 'N/A')}' not found"
                elif error_type == "Cancelled": error_message_summary = "Operation cancelled by user"
                else: error_message_summary = f"Error - {error_type}"
                log_method(f"{operation_name}: {error_message_summary}", "error")
            else: # Success or failure from command execution
                stdout = result.get("stdout", "")
                stderr = result.get("stderr", "")
                return_code = result.get("return_code", -1)
                
                # Don't log success for "Get Property" here as it's handled by block logging
                # This check is crucial to avoid verbose logging of each getprop.
                if not operation_name.startswith("Get Property"):
                    if return_code == 0:
                        log_method(f"{operation_name}: Completed successfully.", "success")
                        # Log relevant output, avoid generic success messages
                        if stdout.strip() and not any(kw in stdout.lower() for kw in ["success", "already", "performed", "daemon started successfully"]):
                            summary_stdout = stdout.strip().splitlines()[0]
                            if len(summary_stdout) > 100: summary_stdout = summary_stdout[:100] + "..."
                            log_method(f"  Detail: {summary_stdout}", "info", indent=1)
                        elif stderr.strip(): # Non-fatal warnings on stderr
                            summary_stderr = stderr.strip().splitlines()[0]
                            if len(summary_stderr) > 100: summary_stderr = summary_stderr[:100] + "..."
                            log_method(f"  Warning: {summary_stderr}", "warning", indent=1)
                    else: # Command failed
                        log_method(f"{operation_name}: Failed (Code: {return_code}).", "fail")
                        if stderr.strip():
                            summary_stderr = stderr.strip().splitlines()[0]
                            if len(summary_stderr) > 120: summary_stderr = summary_stderr[:120] + "..."
                            log_method(f"  Error: {summary_stderr}", "error", indent=1)
                        elif stdout.strip(): # If no stderr, stdout might contain the error
                            summary_stdout = stdout.strip().splitlines()[0]
                            if len(summary_stdout) > 120: summary_stdout = summary_stdout[:120] + "..."
                            log_method(f"  Output: {summary_stdout}", "info", indent=1)
        
        # Stop progress bar and disable cancel button if the operation (or sequence part) is finished
        # And it's not an info_gathering sub-step (handled by its parent)
        if log_panel_available and not is_part_of_sequence and not is_info_gathering:
            self.log_panel.progress_bar.stop()
            self._update_cancel_button_state(enable=False)
        
        # Execute callback if provided
        callback = result.get("callback")
        if callback and callable(callback):
            try:
                callback(result)
            except Exception as e_callback:
                log_to_file_debug_globally(f"Error in command callback for {operation_name}: {e_callback}", "ERROR")
                traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))


    def action_cancel_operation(self):
        if self.current_popen_process and self.current_popen_process.poll() is None: 
            try:
                self.current_popen_process.terminate() # SIGTERM
                # self.current_popen_process.kill() # SIGKILL if terminate isn't enough
                if hasattr(self, 'log_panel') and self.log_panel and self.log_panel.winfo_exists():
                    self.log_panel.log("Attempting to cancel current operation...", "warning")
                else:
                    log_to_file_debug_globally("Attempting to cancel current operation... (no log panel)", "WARNING")
            except Exception as e:
                log_msg = f"Error during cancellation: {e}"
                if hasattr(self, 'log_panel') and self.log_panel and self.log_panel.winfo_exists():
                    self.log_panel.log(log_msg, "error")
                else:
                    log_to_file_debug_globally(log_msg, "ERROR")
        else:
            log_msg = "No operation currently running to cancel."
            if hasattr(self, 'log_panel') and self.log_panel and self.log_panel.winfo_exists():
                self.log_panel.log(log_msg, "info")
            else:
                log_to_file_debug_globally(log_msg, "INFO")
            self._update_cancel_button_state(enable=False) 

    def fetch_and_log_device_info(self, operation_label_key_on_success, callback_after_info_and_op=None, next_operation_command=None, next_operation_name=""):
        """
        Fetches device info, logs it, then optionally runs another command and logs its status.
        """
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None and self.log_panel.winfo_exists()
        if log_panel_available:
            self.log_panel.progress_bar.start()
            self._update_cancel_button_state(enable=True)
        
        # This dictionary will store fetched properties with their display labels as keys
        collected_props_display_keys = {}
        remaining_props_count = len(DEVICE_INFO_PROPERTIES)
        
        # This callback is for the 'get_detailed_adb_info_props' sequence
        def _after_all_props_fetched_for_operation(final_props_dict_internal_keys):
            nonlocal collected_props_display_keys # Ensure we're modifying the outer scope dict

            # Map internal prop keys (ro.product.model) to display labels (Model)
            # This was incorrectly done before, let's fix it.
            # The final_props_dict_internal_keys is already { 'ro.product.model': 'SM-J400F', ... }
            # We need to map this to { 'Model': 'SM-J400F', ... } for log_device_info_block
            
            temp_display_dict = {}
            for display_label, internal_key in DEVICE_INFO_PROPERTIES:
                temp_display_dict[display_label] = final_props_dict_internal_keys.get(internal_key, "N/A")
            
            collected_props_display_keys = temp_display_dict # Now this is correct

            if log_panel_available:
                self.log_panel.log_device_info_block(collected_props_display_keys)

            if next_operation_command: # If there's a follow-up command (e.g., FRP reset)
                self.execute_command_async(
                    next_operation_command,
                    operation_name=next_operation_name,
                    callback_on_finish=_after_next_operation_completed,
                    is_part_of_sequence=False # This is now the main operation after info
                )
            else: # If it was just "Read Info"
                if log_panel_available:
                    self.log_panel.log(self.labels.get(operation_label_key_on_success, "Operation successful."), "success")
                    self.log_panel.progress_bar.stop()
                    self._update_cancel_button_state(enable=False)
                if callback_after_info_and_op:
                    callback_after_info_and_op({"return_code": 0, "device_info": collected_props_display_keys})
        
        def _after_next_operation_completed(result):
            # This callback is for the 'next_operation_command' (e.g. FRP command)
            if log_panel_available:
                if result.get("return_code") == 0:
                    self.log_panel.log(self.labels.get(operation_label_key_on_success, "Operation successful."), "success")
                # Error/Fail logging for next_operation is handled by _handle_command_result
                
                self.log_panel.progress_bar.stop()
                self._update_cancel_button_state(enable=False)

            if callback_after_info_and_op:
                callback_after_info_and_op({"return_code": result.get("return_code", -1), 
                                            "device_info": collected_props_display_keys, 
                                            "operation_result": result})

        # Start fetching all properties
        self.get_detailed_adb_info_props(callback_after_all_props=_after_all_props_fetched_for_operation)


    def get_detailed_adb_info_props(self, callback_after_all_props=None):
        """
        Fetches multiple ADB properties.
        Calls `callback_after_all_props` with a dictionary of {prop_key: value}.
        Individual getprop commands are marked as 'is_info_gathering=True'.
        """
        # This dictionary will store fetched properties {internal_key: value}
        collected_props_internal_keys = {} 
        remaining_props_count = len(DEVICE_INFO_PROPERTIES)

        def _after_single_prop_fetch(result_single_prop):
            nonlocal remaining_props_count 
            # The command is like ['adb', 'shell', 'getprop', 'ro.product.model']
            # The actual property key is at index 3.
            prop_key_fetched = "unknown_prop"
            if result_single_prop.get("command") and len(result_single_prop["command"]) > 3:
                prop_key_fetched = result_single_prop["command"][3]

            if result_single_prop.get("return_code") == 0:
                stdout_val = result_single_prop.get("stdout", "").strip()
                if stdout_val:
                    collected_props_internal_keys[prop_key_fetched] = stdout_val
                else: # Property exists but is empty
                    collected_props_internal_keys[prop_key_fetched] = "" 
            else: # Error fetching this specific property
                collected_props_internal_keys[prop_key_fetched] = "Error fetching"
            
            remaining_props_count -= 1
            
            if remaining_props_count <= 0:
                if callback_after_all_props and callable(callback_after_all_props):
                    # Pass the dictionary with internal keys
                    callback_after_all_props(collected_props_internal_keys)
        
        # Fetch each property
        for _, prop_to_fetch_key in DEVICE_INFO_PROPERTIES: # Use the internal key for getprop
            self.execute_command_async(
                ["adb", "shell", "getprop", prop_to_fetch_key],
                operation_name=f"Get Property ({prop_to_fetch_key})", 
                callback_on_finish=_after_single_prop_fetch,
                is_part_of_sequence=True, # It's part of the "get all info" sequence
                is_info_gathering=True # Mark as info gathering sub-command
            )


    def set_language(self, lang):
        if lang in LABELS:
            self.app_controller.lang = lang 
            self.lang = lang
            self.labels = get_labels(self.lang)
            self._rebuild_ui() # Rebuild UI to apply new labels
            log_to_file_debug_globally(f"Language changed to {lang}.")
        else:
            log_to_file_debug_globally(f"Language {lang} not supported.", "WARNING")

    def set_theme(self, theme_name):
        if theme_name in THEMES:
            self.app_controller.theme_mode = theme_name 
            self.theme_mode = theme_name
            self.theme = get_theme(theme_name)
            self._rebuild_ui() # Rebuild UI to apply new theme
            log_to_file_debug_globally(f"Theme changed to {theme_name}.")
        else:
            log_to_file_debug_globally(f"Theme {theme_name} not supported.", "WARNING")

    def _rebuild_ui(self):
        log_to_file_debug_globally("Rebuilding UI...")
        current_tab_index = 0
        if hasattr(self, 'notebook') and self.notebook.winfo_exists():
            try:
                current_tab_index = self.notebook.index(self.notebook.select())
            except tk.TclError: pass 
        
        children_to_destroy = list(self.winfo_children()) # Avoid modifying list during iteration
        for widget in children_to_destroy:
            if widget.winfo_exists(): 
                 widget.destroy()
        
        self._apply_styles() 
        self._build_ui()   
        
        if hasattr(self, 'notebook') and self.notebook.winfo_exists():
            try:
                if self.notebook.tabs(): 
                    self.notebook.select(current_tab_index if current_tab_index < len(self.notebook.tabs()) else 0)
            except tk.TclError: 
                log_to_file_debug_globally("Error selecting tab after UI rebuild, or no tabs exist.", "WARNING")
        log_to_file_debug_globally("UI Rebuilt.")

    def _on_closing(self):
        log_to_file_debug_globally("Application closing attempt.")
        if messagebox.askokcancel(self.labels.get("quit_dialog_title", "Quit"),
                                 self.labels.get("quit_dialog_message", "Do you want to quit?"),
                                 parent=self.master):
            if hasattr(self, 'status_bar') and self.status_bar.winfo_exists():
                self.status_bar.cancel_adb_check()
            if hasattr(self, 'db_logger') and self.db_logger:
                self.db_logger.close()
            
            if hasattr(self, 'after_id_process_command_queue') and self.after_id_process_command_queue:
                self.after_cancel(self.after_id_process_command_queue)
                self.after_id_process_command_queue = None


            log_to_file_debug_globally("Application closed by user.")
            self.master.destroy() # Destroy the main window

class SamsungTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app: UltimateDeviceTool): 
        log_to_file_debug_globally("SamsungTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))
        
        self.num_frp_steps = 0 
        self.current_frp_step = 0 

        container = tk.Frame(self, bg=self.theme.get("BG", "#21252B"))
        container.pack(fill=tk.BOTH, expand=True)

        group_samsung = tk.LabelFrame(container, text=self.labels.get("group_samsung", "Samsung ADB Repair & Utilities"),
                                    font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                    fg=self.theme.get("FG", "#D1D9E0"), padx=15, pady=15, relief="groove", bd=2)
        group_samsung.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        col1_frame = tk.Frame(group_samsung, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        col1_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N)

        ModernButton(col1_frame, text=self.labels.get("btn_get_detailed_info"), # Updated label
                                   command=self.action_read_device_info, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_rec", "Reboot Recovery"),
                                       command=self.action_reboot_recovery, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_dl", "Reboot Download"),
                                       command=self.action_reboot_download, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_bl", "Reboot Bootloader"),
                                       command=self.action_reboot_bootloader, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

        col2_frame = tk.Frame(group_samsung, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        col2_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N)

        ModernButton(col2_frame, text=self.labels.get("btn_remove_frp", "Remove FRP (ADB)"),
                                       command=self.action_remove_frp_adb, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col2_frame, text=self.labels.get("btn_factory_reset", "Factory Reset (ADB)"),
                                       command=self.action_factory_reset_adb, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col2_frame, text=self.labels.get("btn_screenlock_reset", "Reset Screen Lock (ADB)"),
                                       command=self.action_reset_screenlock_adb, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col2_frame, text=self.labels.get("btn_arabize_device", "Arabize Device (ADB)"),
                                       command=self.action_arabize_device, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col2_frame, text=self.labels.get("btn_open_browser_adb", "Open Browser (ADB)"),
                                       command=self.action_open_browser_adb, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        
        tk.Label(group_samsung, text=self.labels.get("arabize_note", "Note: Arabization might require..."),
                 font=("Segoe UI", 8), bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                 fg=self.theme.get("LOG_FG_WARNING", "#FF9800"), wraplength=350, justify=tk.LEFT
                 ).pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))
        log_to_file_debug_globally("SamsungTab __init__ finished.")

    def action_read_device_info(self):
        self.master_app.fetch_and_log_device_info(operation_label_key_on_success="log_read_info_complete")

    def action_reboot_recovery(self):
        command = ["adb", "reboot", "recovery"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Recovery")

    def action_reboot_download(self):
        command = ["adb", "reboot", "download"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Download Mode")

    def action_reboot_bootloader(self):
        command = ["adb", "reboot", "bootloader"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Bootloader")

    def action_remove_frp_adb(self):
        if not messagebox.askokcancel(
            self.labels.get("frp_reset_warning_title", "FRP Reset Attempt"),
            self.labels.get("frp_reset_warning_message", "This will attempt a series of ADB commands... Proceed with caution."),
            icon=messagebox.WARNING,
            parent=self.master_app.master):
            if self.master_app.log_panel: self.master_app.log_panel.log("FRP Reset (ADB) cancelled by user.", "info")
            return

        # This will first fetch and log device info, then proceed with FRP commands.
        # The FRP commands themselves are now a sequence handled by _execute_next_frp_step
        # So, we need a way to chain: fetch_info -> start_frp_sequence
        
        def _start_frp_sequence_after_info(info_result):
            # info_result contains device_info and return_code for info fetching
            if info_result.get("return_code") != 0:
                if self.master_app.log_panel:
                    self.master_app.log_panel.log("Could not get device info before FRP reset. Aborting FRP.", "error")
                    self.master_app.log_panel.progress_bar.stop()
                    self.master_app._update_cancel_button_state(enable=False)
                return

            # Now start the actual FRP sequence
            if self.master_app.log_panel: self.master_app.log_panel.log("Starting FRP Reset sequence (ADB)...", "info")
            # Note: _update_cancel_button_state is already true from fetch_and_log_device_info
            
            self.commands_frp_sequence = [
                (["adb", "shell", "settings", "put", "global", "setup_wizard_has_run", "1"], "Set setup_wizard_has_run to 1"),
                (["adb", "shell", "settings", "put", "secure", "user_setup_complete", "1"], "Set user_setup_complete (secure table)"),
                (["adb", "shell", "settings", "put", "global", "device_provisioned", "1"], "Set device_provisioned to 1"),
                (["adb", "shell", "content", "insert", "--uri", "content://settings/secure", "--bind", "name:s:user_setup_complete", "--bind", "value:s:1"], "Insert user_setup_complete via content provider"),
            ]
            self.num_frp_steps = len(self.commands_frp_sequence)
            self.current_frp_step = 0

            if self.master_app.log_panel and self.master_app.log_panel.winfo_exists():
                self.master_app.log_panel.progress_bar.set_value(0) 

            self._execute_next_frp_step()

        # This is the new way: fetch_and_log_device_info will handle the info part.
        # We pass None for next_operation_command because the actual FRP is a sequence.
        # The callback _start_frp_sequence_after_info will initiate the FRP steps.
        self.master_app.fetch_and_log_device_info(
            operation_label_key_on_success="log_frp_reset_ok", # This won't be used directly by fetch_and_log...
            callback_after_info_and_op=_start_frp_sequence_after_info, # This callback starts FRP
            next_operation_command=None, # FRP is a sequence, not a single command here
            next_operation_name="Remove FRP (ADB) - Initializing" # Placeholder name
        )


    def _execute_next_frp_step(self):
        # This method executes one step of the FRP sequence
        if self.current_frp_step < self.num_frp_steps:
            command, op_desc = self.commands_frp_sequence[self.current_frp_step]
            
            # Log the attempt of this specific step
            if self.master_app.log_panel: self.master_app.log_panel.log(f"Attempting FRP Step: {op_desc}", "info", indent=1)

            self.master_app.execute_command_async(
                command,
                operation_name=f"FRP Step: {op_desc}",
                callback_on_finish=self._frp_step_callback,
                is_part_of_sequence=True # Mark as part of FRP sequence
            )
        else: # All steps attempted
            if self.master_app.log_panel and self.master_app.log_panel.winfo_exists():
                # Final status of FRP (OK or FAIL) should be determined by success of steps
                # For now, let's assume if it reaches here, all commands were sent.
                # A more robust way would be to check the result of each step.
                self.master_app.log_panel.log(self.labels.get("log_frp_reset_ok", "FRP Reset.... OK"), "success")
                self.master_app.log_panel.progress_bar.set_value(100) 
                self.master_app.after(1000, lambda: self.master_app.log_panel.progress_bar.stop() if self.master_app.log_panel and self.master_app.log_panel.winfo_exists() else None)
                self.master_app._update_cancel_button_state(enable=False)


    def _frp_step_callback(self, result):
        # This callback is for each individual FRP command
        # Logging of success/failure of this step is handled by _handle_command_result

        self.current_frp_step += 1
        
        if self.master_app.log_panel and self.master_app.log_panel.winfo_exists():
            progress_percentage = int((self.current_frp_step / self.num_frp_steps) * 100)
            self.master_app.log_panel.progress_bar.set_value(progress_percentage)

        if result.get("error") == "Cancelled" or (self.master_app.current_popen_process is None and self.current_frp_step < self.num_frp_steps ) :
            if self.master_app.log_panel: self.master_app.log_panel.log("FRP sequence cancelled by user.", "warning")
            if self.master_app.log_panel and self.master_app.log_panel.winfo_exists():
                self.master_app.log_panel.progress_bar.stop()
                self.master_app._update_cancel_button_state(enable=False)
            return 

        # If a step fails, should we stop the sequence?
        if result.get("return_code", 0) != 0 and result.get("error") is None:
            if self.master_app.log_panel: self.master_app.log_panel.log(f"FRP step '{result.get('operation_name')}' failed. Subsequent steps might not work.", "warning", indent=1)
            # Optionally, stop the sequence here or let it continue. For now, let it continue.

        self._execute_next_frp_step() # Execute next step

    def action_factory_reset_adb(self):
        if messagebox.askyesno("Confirm Factory Reset", "Are you sure you want to factory reset the device via ADB? This will erase all user data.", parent=self.master_app.master):
            command = ["adb", "shell", "wipe", "data"] 
            self.master_app.execute_command_async(command, operation_name="Factory Reset (ADB)")
            if self.master_app.log_panel: self.master_app.log_panel.log("Note: Factory Reset via 'adb shell wipe data' typically requires recovery mode or root.", "warning")
        else:
            if self.master_app.log_panel: self.master_app.log_panel.log("Factory Reset (ADB) cancelled by user.", "info")

    def action_reset_screenlock_adb(self):
        if messagebox.askyesno("Confirm Screen Lock Reset", "Attempt to reset screen lock via ADB? This usually requires root and may not work on all devices/Android versions. Continue?", parent=self.master_app.master):
            # This operation doesn't fit the "fetch info first" model as neatly as FRP.
            # We can log a generic start message.
            if self.master_app.log_panel: self.master_app.log_panel.log(self.labels.get("log_operation_started") + "Reset Screen Lock (ADB)", "info")

            commands_to_try = [
                (["adb", "shell", "rm", "/data/system/gesture.key"], "Remove gesture.key (requires root)"),
                (["adb", "shell", "rm", "/data/system/password.key"], "Remove password.key (requires root)"),
            ]
            # For simplicity, execute them sequentially. Progress bar will spin for each.
            # A more complex sequence handler could be used if needed.
            for cmd, desc in commands_to_try:
                self.master_app.execute_command_async(cmd, operation_name=f"Reset SL: {desc}", is_part_of_sequence=True) # Mark as part of a logical sequence
            
            if self.master_app.log_panel: self.master_app.log_panel.log("Attempted screen lock reset. Reboot device to see effect.", "info")
        else:
            if self.master_app.log_panel: self.master_app.log_panel.log("Screen Lock Reset (ADB) cancelled by user.", "info")

    def action_arabize_device(self):
        if messagebox.askyesno(
            self.labels.get("arabize_confirm_title", "Confirm Arabization"),
            self.labels.get("arabize_confirm_message", "This will attempt to change the device language to Arabic (ar-AE)... Proceed?"),
            parent=self.master_app.master):
            if self.master_app.log_panel: self.master_app.log_panel.log(self.labels.get("log_operation_started") + "Arabize Device (ADB)", "info")
            
            locale_to_set = "ar-AE" 
            arabize_commands = [
                (["adb", "shell", "settings", "put", "system", "system_locales", locale_to_set], f"Set system_locales to {locale_to_set}"),
                (["adb", "shell", "setprop", "persist.sys.locale", locale_to_set], f"Set persist.sys.locale to {locale_to_set}"),
                (["adb", "shell", "am", "broadcast", "-a", "android.intent.action.LOCALE_CHANGED"], "Broadcast Locale Change")
            ]
            for cmd, desc in arabize_commands:
                 self.master_app.execute_command_async(cmd, operation_name=desc, is_part_of_sequence=True)

            if self.master_app.log_panel: self.master_app.log_panel.log("Arabization commands sent. Check device. A reboot might be needed.", "info")
        else:
            if self.master_app.log_panel: self.master_app.log_panel.log("Arabization cancelled by user.", "info")

    def action_open_browser_adb(self):
        url = simpledialog.askstring(
            self.labels.get("open_browser_title", "Open URL"),
            self.labels.get("open_browser_prompt", "Enter URL:"),
            parent=self.master_app.master
        )
        if url and url.strip():
            if not (url.startswith("http://") or url.startswith("https://")):
                messagebox.showwarning("Invalid URL", "Please enter a full URL including http:// or https://", parent=self.master_app.master)
                if self.master_app.log_panel: self.master_app.log_panel.log(f"Invalid URL for Open Browser: {url}", "warning")
                return

            command = ["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url.strip()]
            self.master_app.execute_command_async(command, operation_name=f"Open URL: {url.strip()}")
        elif url is not None: 
             messagebox.showwarning("Empty URL", "URL cannot be empty.", parent=self.master_app.master)
             if self.master_app.log_panel: self.master_app.log_panel.log("Open Browser: URL was empty.", "info")
        else: 
            if self.master_app.log_panel: self.master_app.log_panel.log("Open Browser action cancelled by user.", "info")


class HonorTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app: UltimateDeviceTool):
        log_to_file_debug_globally("HonorTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))

        container = tk.Frame(self, bg=self.theme.get("BG", "#21252B"))
        container.pack(fill=tk.BOTH, expand=True)

        group_honor = tk.LabelFrame(container, text=self.labels.get("group_honor", "Honor Fastboot Tools"),
                                    font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                    fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_honor.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        ModernButton(group_honor, text=self.labels.get("btn_honor_info", "Read Serial & Software Info"),
                                   command=self.action_honor_info, theme=self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_honor, text=self.labels.get("btn_honor_reboot_bl", "Reboot Bootloader (Honor)"),
                                       command=self.action_honor_reboot_bootloader, theme=self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_honor, text=self.labels.get("btn_honor_reboot_edl", "Reboot EDL (Honor)"),
                                       command=self.action_honor_reboot_edl, theme=self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_honor, text=self.labels.get("btn_honor_wipe_data_cache", "Wipe Data/Cache (Honor)"),
                                       command=self.action_honor_wipe_data_cache, theme=self.theme, width=35).pack(pady=5, anchor=tk.W)
        
        frp_frame = tk.Frame(group_honor, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        frp_frame.pack(fill=tk.X, pady=(10,5), anchor=tk.W)
        tk.Label(frp_frame, text=self.labels.get("honor_frp_key_label", "Honor FRP Key:"),
                 font=FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                 fg=self.theme.get("FG", "#D1D9E0")).pack(side=tk.LEFT, padx=(0,5))
        self.honor_frp_key_var = tk.StringVar()
        honor_frp_entry = tk.Entry(frp_frame, textvariable=self.honor_frp_key_var, width=20, font=FONT,
                                   bg=self.theme.get("LOG_BG", "#2C313A"), fg=self.theme.get("FG", "#D1D9E0"),
                                   insertbackground=self.theme["FG"], relief="flat", bd=2, highlightthickness=1,
                                   highlightbackground=self.theme.get("ACCENT2", "#0095CC"), highlightcolor=self.theme.get("ACCENT", "#00AEEF"))
        honor_frp_entry.pack(side=tk.LEFT, padx=5, ipady=2)
        TextContextMenu(honor_frp_entry, self.master_app.master, self.labels) 

        ModernButton(frp_frame, text=self.labels.get("btn_honor_frp", "Remove FRP (Honor Code)"),
                                   command=self.action_honor_remove_frp, theme=self.theme, width=25, height=1).pack(side=tk.LEFT, padx=5)
        log_to_file_debug_globally("HonorTab __init__ finished.")

    def action_honor_info(self):
        # Fastboot getvar all is typically a single command whose output is the info
        if self.master_app.log_panel: self.master_app.log_panel.log(self.labels.get("log_operation_started") + "Honor Get Info (Fastboot)", "info")
        command = ["fastboot", "getvar", "all"]
        # The output of this command will be logged by _handle_command_result
        self.master_app.execute_command_async(command, operation_name="Honor Get Info (Fastboot)")

    def action_honor_reboot_bootloader(self):
        command = ["fastboot", "reboot-bootloader"]
        self.master_app.execute_command_async(command, operation_name="Honor Reboot Bootloader")

    def action_honor_reboot_edl(self):
        command = ["fastboot", "oem", "edl"] 
        self.master_app.execute_command_async(command, operation_name="Honor Reboot EDL")

    def action_honor_wipe_data_cache(self):
        if messagebox.askyesno("Confirm Wipe", "Are you sure you want to wipe data and cache on this Honor device? This will erase all user data.", parent=self.master_app.master):
            if self.master_app.log_panel: self.master_app.log_panel.log(self.labels.get("log_operation_started") + "Honor Wipe Data/Cache", "info")
            self.master_app.execute_command_async(["fastboot", "erase", "cache"], operation_name="Honor Wipe Cache", is_part_of_sequence=True)
            self.master_app.execute_command_async(["fastboot", "erase", "userdata"], operation_name="Honor Wipe Userdata", is_part_of_sequence=True)
            if self.master_app.log_panel: self.master_app.log_panel.log("Honor Wipe Data/Cache commands sent. Device may need manual reboot.", "info")
        else:
            if self.master_app.log_panel: self.master_app.log_panel.log("Honor Wipe Data/Cache cancelled by user.", "info")

    def action_honor_remove_frp(self):
        frp_key = self.honor_frp_key_var.get()
        if not frp_key:
            messagebox.showerror("Input Error", "Please enter the Honor FRP key.", parent=self.master_app.master)
            return
        if self.master_app.log_panel: self.master_app.log_panel.log(self.labels.get("log_operation_started") + "Honor Remove FRP", "info")
        command = ["fastboot", "oem", "frp-unlock", frp_key] 
        self.master_app.execute_command_async(command, operation_name=f"Honor Remove FRP with Key")
        if self.master_app.log_panel: self.master_app.log_panel.log("Note: Honor FRP removal methods vary. This is a common command.", "warning")


class XiaomiTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app: UltimateDeviceTool):
        log_to_file_debug_globally("XiaomiTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))
        
        container = tk.Frame(self, bg=self.theme.get("BG", "#21252B"))
        container.pack(fill=tk.BOTH, expand=True)

        group_adb = tk.LabelFrame(container, text=self.labels.get("group_xiaomi_adb", "Xiaomi ADB Mode"),
                                  font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                  fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_adb.pack(pady=(0,10), padx=10, fill=tk.X, expand=False)
        
        adb_cols_container = tk.Frame(group_adb, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        adb_cols_container.pack(fill=tk.X)
        adb_col1 = tk.Frame(adb_cols_container, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        adb_col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N, expand=True)
        adb_col2 = tk.Frame(adb_cols_container, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        adb_col2.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N, expand=True)

        ModernButton(adb_col1, text=self.labels.get("btn_xiaomi_adb_info"), # Updated label
                                   command=self.action_xiaomi_adb_info, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(adb_col1, text=self.labels.get("btn_xiaomi_reboot_normal_adb", "Reboot Normal (ADB)"),
                                   command=lambda: self.master_app.execute_command_async(["adb", "reboot"], "Xiaomi Reboot Normal (ADB)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(adb_col1, text=self.labels.get("btn_xiaomi_reboot_recovery_adb", "Reboot Recovery (ADB)"),
                                   command=lambda: self.master_app.execute_command_async(["adb", "reboot", "recovery"], "Xiaomi Reboot Recovery (ADB)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        
        ModernButton(adb_col2, text=self.labels.get("btn_xiaomi_reboot_fastboot_adb", "Reboot Fastboot (ADB)"),
                                   command=lambda: self.master_app.execute_command_async(["adb", "reboot", "bootloader"], "Xiaomi Reboot Fastboot (ADB)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(adb_col2, text=self.labels.get("btn_xiaomi_reboot_edl_adb", "Reboot EDL (ADB)"),
                                   command=lambda: self.master_app.execute_command_async(["adb", "reboot", "edl"], "Xiaomi Reboot EDL (ADB)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(adb_col2, text=self.labels.get("btn_xiaomi_enable_diag_root", "Enable Diag (ROOT)") + " *",
                                   command=lambda: messagebox.showinfo("Info", "Enable Diag (ROOT) is a placeholder for specific Xiaomi Diag enabling commands, which usually require root and device-specific knowledge. This button is illustrative.", parent=self.master_app.master), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)


        group_fastboot = tk.LabelFrame(container, text=self.labels.get("group_xiaomi_fastboot", "Xiaomi Fastboot Mode"),
                                       font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                       fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_fastboot.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        fb_cols_container = tk.Frame(group_fastboot, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        fb_cols_container.pack(fill=tk.X)
        fb_col1 = tk.Frame(fb_cols_container, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        fb_col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N, expand=True)
        fb_col2 = tk.Frame(fb_cols_container, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        fb_col2.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N, expand=True)

        ModernButton(fb_col1, text=self.labels.get("btn_xiaomi_fastboot_info", "Read Info (Fastboot)"),
                                   command=lambda: self.master_app.execute_command_async(["fastboot", "getvar", "all"], "Xiaomi Read Info (Fastboot)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(fb_col1, text=self.labels.get("btn_xiaomi_fastboot_read_security", "Read Security (Fastboot)"),
                                   command=lambda: self.master_app.execute_command_async(["fastboot", "oem", "device-info"], "Xiaomi Read Security (Fastboot)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(fb_col1, text=self.labels.get("btn_xiaomi_fastboot_unlock", "Unlock Bootloader (Fastboot)"),
                                   command=self.action_xiaomi_fastboot_unlock, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(fb_col1, text=self.labels.get("btn_xiaomi_fastboot_lock", "Lock Bootloader (Fastboot)"),
                                   command=self.action_xiaomi_fastboot_lock, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        
        ModernButton(fb_col2, text=self.labels.get("btn_xiaomi_fastboot_reboot_sys", "Reboot System (Fastboot)"),
                                   command=lambda: self.master_app.execute_command_async(["fastboot", "reboot"], "Xiaomi Reboot System (Fastboot)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(fb_col2, text=self.labels.get("btn_xiaomi_fastboot_reboot_fast", "Reboot Fastboot (Fastboot)"),
                                   command=lambda: self.master_app.execute_command_async(["fastboot", "reboot-bootloader"], "Xiaomi Reboot Fastboot (Fastboot)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(fb_col2, text=self.labels.get("btn_xiaomi_fastboot_reboot_edl", "Reboot EDL (Fastboot)"),
                                   command=lambda: self.master_app.execute_command_async(["fastboot", "oem", "edl"], "Xiaomi Reboot EDL (Fastboot)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(fb_col2, text=self.labels.get("btn_xiaomi_fastboot_wipe_cache", "Wipe Cache (Fastboot)"),
                                   command=lambda: self.master_app.execute_command_async(["fastboot", "erase", "cache"], "Xiaomi Wipe Cache (Fastboot)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(fb_col2, text=self.labels.get("btn_xiaomi_fastboot_wipe_data", "Wipe Data (Fastboot)"),
                                   command=self.action_xiaomi_fastboot_wipe_data, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        log_to_file_debug_globally("XiaomiTab __init__ finished.")

    def action_xiaomi_adb_info(self):
        self.master_app.fetch_and_log_device_info(operation_label_key_on_success="log_read_info_complete")


    def action_xiaomi_fastboot_unlock(self):
        if messagebox.askyesno("Confirm Unlock", "Are you sure you want to unlock the bootloader? This will erase all user data and may void warranty. For Xiaomi, this often requires Mi Unlock Tool and an authorized account.", parent=self.master_app.master):
            self.master_app.execute_command_async(["fastboot", "oem", "unlock"], operation_name="Xiaomi Unlock Bootloader (Attempt)")
            if self.master_app.log_panel: self.master_app.log_panel.log("Note: Xiaomi bootloader unlock often requires official Mi Unlock Tool and account authorization. This command attempts the generic unlock.", "warning")
        else:
            if self.master_app.log_panel: self.master_app.log_panel.log("Xiaomi Unlock Bootloader cancelled by user.", "info")

    def action_xiaomi_fastboot_lock(self):
        if messagebox.askyesno("Confirm Lock", "Are you sure you want to lock the bootloader? This will erase all user data if the device is not already formatted for a locked state.", parent=self.master_app.master):
            self.master_app.execute_command_async(["fastboot", "oem", "lock"], operation_name="Xiaomi Lock Bootloader")
        else:
            if self.master_app.log_panel: self.master_app.log_panel.log("Xiaomi Lock Bootloader cancelled by user.", "info")

    def action_xiaomi_fastboot_wipe_data(self):
        if messagebox.askyesno("Confirm Wipe", "Are you sure you want to wipe all user data? This cannot be undone.", parent=self.master_app.master):
            self.master_app.execute_command_async(["fastboot", "erase", "userdata"], operation_name="Xiaomi Wipe Data (Fastboot)")
        else:
            if self.master_app.log_panel: self.master_app.log_panel.log("Xiaomi Wipe Data cancelled by user.", "info")

class FileAdvancedTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app: UltimateDeviceTool):
        log_to_file_debug_globally("FileAdvancedTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))

        container = tk.Frame(self, bg=self.theme.get("BG", "#21252B"))
        container.pack(fill=tk.BOTH, expand=True)

        group_file = tk.LabelFrame(container, text=self.labels.get("group_file", "File & App Management"),
                                   font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                   fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_file.pack(pady=(0,10), padx=10, fill=tk.X, expand=False)
        
        file_cols_container = tk.Frame(group_file, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        file_cols_container.pack(fill=tk.X)
        file_col1 = tk.Frame(file_cols_container, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        file_col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0,5), anchor=tk.N, expand=True) 
        file_col2 = tk.Frame(file_cols_container, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        file_col2.pack(side=tk.LEFT, fill=tk.Y, padx=(5,0), anchor=tk.N, expand=True) 

        ModernButton(file_col1, text=self.labels.get("btn_pull_file", "Pull File from Device"),
                                   command=self.action_pull_file, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col1, text=self.labels.get("btn_push_file", "Push File to Device"),
                                   command=self.action_push_file, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col1, text=self.labels.get("btn_backup_user_data_adb", "Backup User Data (ADB)"), 
                                   command=self.action_backup_user_data, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        
        ModernButton(file_col2, text=self.labels.get("btn_install_apk", "Install APK"),
                                   command=self.action_install_apk, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col2, text=self.labels.get("btn_uninstall_app", "Uninstall App"),
                                   command=self.action_uninstall_app, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col2, text=self.labels.get("btn_restore_user_data_adb", "Restore User Data (ADB)"), 
                                   command=self.action_restore_user_data, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)


        group_advanced = tk.LabelFrame(container, text=self.labels.get("group_advanced_cmd", "Advanced Command Execution"),
                                       font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                       fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_advanced.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        tk.Label(group_advanced, text=self.labels.get("advanced_cmd_label", "Enter ADB or Fastboot command:"),
                 font=FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                 fg=self.theme.get("FG", "#D1D9E0")).pack(anchor=tk.W, pady=(5,2))
        
        self.advanced_cmd_var = tk.StringVar()
        advanced_cmd_entry = tk.Entry(group_advanced, textvariable=self.advanced_cmd_var, width=60, font=FONT,
                                      bg=self.theme.get("LOG_BG", "#2C313A"), fg=self.theme.get("FG", "#D1D9E0"),
                                      insertbackground=self.theme["FG"], relief="flat", bd=2, highlightthickness=1,
                                      highlightbackground=self.theme.get("ACCENT2", "#0095CC"), highlightcolor=self.theme.get("ACCENT", "#00AEEF"))
        advanced_cmd_entry.pack(fill=tk.X, pady=(0,5), ipady=3)
        TextContextMenu(advanced_cmd_entry, self.master_app.master, self.labels) 

        ModernButton(group_advanced, text=self.labels.get("btn_run_advanced_cmd", "Run Command"),
                                   command=self.action_run_advanced_cmd, theme=self.theme, width=20).pack(pady=5, anchor=tk.W)
        log_to_file_debug_globally("FileAdvancedTab __init__ finished.")

    def action_pull_file(self):
        device_path = simpledialog.askstring(self.labels.get("pull_file_title", "Pull File from Device"),
                                            self.labels.get("pull_file_device_path_msg", "Enter device source path:"),
                                            parent=self.master_app.master)
        if not device_path or not device_path.strip(): 
            if self.master_app.log_panel: self.master_app.log_panel.log("Pull file: No device path entered.", "info")
            return
        
        local_path = filedialog.asksaveasfilename(parent=self.master_app.master, title="Save File As", initialfile=os.path.basename(device_path.strip()))
        if not local_path: 
            if self.master_app.log_panel: self.master_app.log_panel.log("Pull file: No local save path selected.", "info")
            return
        
        self.master_app.execute_command_async(["adb", "pull", device_path.strip(), local_path],
                                             operation_name=f"Pull File: {os.path.basename(device_path.strip())}")

    def action_push_file(self):
        local_path = filedialog.askopenfilename(parent=self.master_app.master, title="Select File to Push")
        if not local_path: 
            if self.master_app.log_panel: self.master_app.log_panel.log("Push file: No local file selected.", "info")
            return
        
        device_path = simpledialog.askstring(self.labels.get("push_file_title", "Push File to Device"),
                                            self.labels.get("push_file_device_path_msg", "Enter device destination path:"),
                                            parent=self.master_app.master, initialvalue=f"/sdcard/{os.path.basename(local_path)}")
        if not device_path or not device_path.strip(): 
            if self.master_app.log_panel: self.master_app.log_panel.log("Push file: No device path entered.", "info")
            return
        
        self.master_app.execute_command_async(["adb", "push", local_path, device_path.strip()],
                                             operation_name=f"Push File: {os.path.basename(local_path)}")

    def action_install_apk(self):
        apk_path = filedialog.askopenfilename(title=self.labels.get("install_apk_title", "Select APK to Install"),
                                             filetypes=[("APK Files", "*.apk"), ("All Files", "*.*")],
                                             parent=self.master_app.master)
        if not apk_path: 
            if self.master_app.log_panel: self.master_app.log_panel.log("Install APK: No APK file selected.", "info")
            return
        
        self.master_app.execute_command_async(["adb", "install", "-r", apk_path], # -r for reinstall
                                             operation_name=f"Install APK: {os.path.basename(apk_path)}")

    def action_uninstall_app(self):
        package_name = simpledialog.askstring(self.labels.get("uninstall_title", "Uninstall App"),
                                             self.labels.get("uninstall_msg", "Enter package name:"),
                                             parent=self.master_app.master)
        if not package_name or not package_name.strip(): 
            if self.master_app.log_panel: self.master_app.log_panel.log("Uninstall App: No package name entered.", "info")
            return
        
        self.master_app.execute_command_async(["adb", "uninstall", package_name.strip()],
                                             operation_name=f"Uninstall App: {package_name.strip()}")

    def action_backup_user_data(self):
        backup_file_path = filedialog.asksaveasfilename(
            title=self.labels.get("backup_user_data_title", "Save Backup As"),
            defaultextension=".ab",
            filetypes=[("ADB Backup Files", "*.ab"), ("All Files", "*.*")],
            parent=self.master_app.master
        )
        if not backup_file_path:
            if self.master_app.log_panel: self.master_app.log_panel.log("Backup User Data: Cancelled by user.", "info")
            return

        command = ["adb", "backup", "-f", backup_file_path, "-all"] # Backup all apps data
        operation_name = "Backup User Apps Data"

        if self.master_app.log_panel: 
            self.master_app.log_panel.log(f"Starting User Data Backup to {backup_file_path}. Confirm on device.", "info")
            self.master_app.log_panel.log("ADB Backup requires confirmation on the device. The operation will wait.", "warning")
        self.master_app.execute_command_async(command, operation_name=operation_name)


    def action_restore_user_data(self):
        backup_file_path = filedialog.askopenfilename(
            title=self.labels.get("restore_user_data_title", "Select Backup to Restore"),
            filetypes=[("ADB Backup Files", "*.ab"), ("All Files", "*.*")],
            parent=self.master_app.master
        )
        if not backup_file_path:
            if self.master_app.log_panel: self.master_app.log_panel.log("Restore User Data: Cancelled by user.", "info")
            return

        command = ["adb", "restore", backup_file_path]
        if self.master_app.log_panel: 
            self.master_app.log_panel.log(f"Starting User Data Restore from {backup_file_path}. Confirm on device.", "info")
            self.master_app.log_panel.log("ADB Restore requires confirmation on the device. The operation will wait.", "warning")

        self.master_app.execute_command_async(command, operation_name="Restore User Data")


    def action_run_advanced_cmd(self):
        cmd_str = self.advanced_cmd_var.get().strip()
        if not cmd_str: 
            if self.master_app.log_panel: self.master_app.log_panel.log("Advanced Command: No command entered.", "info")
            return
        
        cmd_parts = cmd_str.split() 
        if not cmd_parts: 
            if self.master_app.log_panel: self.master_app.log_panel.log("Advanced Command: Command is empty after parsing.", "info")
            return
        
        if self.master_app.log_panel: self.master_app.log_panel.log(f"Executing: {cmd_str}", "cmd")
        self.master_app.execute_command_async(cmd_parts, operation_name=f"Advanced CMD: {cmd_parts[0]}")

if __name__ == "__main__":
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f_log_check:
            f_log_check.write(f"[{datetime.now()}] [INFO] Main execution block started.\n")
    except Exception as e_log_main_check:
        print(f"[CRITICAL_ERROR] Cannot write to main debug log '{_DEBUG_LOG_PATH}': {e_log_main_check}", file=sys.stderr)
        _DEBUG_LOG_PATH = "application_debug_log_local.txt"
        try:
            with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f_log_fallback:
                f_log_fallback.write(f"[{datetime.now()}] [INFO] Using fallback debug log: '{_DEBUG_LOG_PATH}'.\n")
        except Exception as e_log_fallback_create:
            print(f"[CRITICAL_ERROR] Cannot write to fallback debug log '{_DEBUG_LOG_PATH}': {e_log_fallback_create}", file=sys.stderr)

    try:
        try:
            subprocess.check_output(["adb", "version"], stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            log_to_file_debug_globally("ADB found and working.")
        except Exception:
            log_to_file_debug_globally("ADB not found or not working. Some features might be unavailable.", "WARNING")
        
        try:
            subprocess.check_output(["fastboot", "--version"], stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            log_to_file_debug_globally("Fastboot found and working.")
        except Exception:
            log_to_file_debug_globally("Fastboot not found or not working. Some features might be unavailable.", "WARNING")

        controller = AppController()
        controller.start()

    except Exception as e:
        log_to_file_debug_globally(f"Fatal error in main execution: {e}", "CRITICAL")
        traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a")) 
        try:
            root_err = tk.Tk()
            root_err.withdraw() 
            messagebox.showerror("Fatal Error", f"A critical error occurred: {e}\n\nPlease check '{_DEBUG_LOG_PATH}' for details.", parent=None)
            root_err.destroy()
        except Exception as e_tk_fatal:
            print(f"A critical error occurred: {e}. Check '{_DEBUG_LOG_PATH}'. Tkinter error dialog also failed: {e_tk_fatal}", file=sys.stderr)
