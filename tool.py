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
FIXED_PASSWORD = "password" # Change this if needed

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
        "search_log_label": "Search Log:",
        "find_button": "Find",
        "all_button": "All",
        "export_button": "Export",
        "quit_dialog_title": "Quit",
        "quit_dialog_message": "Do you want to quit Ultimat-Unlock Tool?",
        "dependency_check_title": "Dependency Check",
        "adb_not_found_message": "ADB (Android Debug Bridge) not found or not working. Some features will be unavailable. Please install/configure ADB and add it to your system PATH.",
        "fastboot_not_found_message": "Fastboot not found or not working. Some features will be unavailable. Please install/configure Fastboot and add it to your system PATH.",
        "fatal_error_title": "Fatal Error",
        "fatal_error_message_prefix": "A critical error occurred:",
        "btn_get_detailed_info": "Get Detailed Device Info (ADB)",
        "btn_pull_file": "Pull File from Device",
        "btn_push_file": "Push File to Device",
        "btn_install_apk": "Install APK",
        "btn_uninstall_app": "Uninstall App",
        "btn_honor_info": "Read Serial & Software Info",
        "honor_frp_key_label": "Honor FRP Key:",
        "btn_honor_frp": "Remove FRP (Honor Code)",
        "btn_honor_reboot_bl": "Reboot Bootloader (Honor)",
        "btn_honor_reboot_edl": "Reboot EDL (Honor)",
        "btn_honor_wipe_data_cache": "Wipe Data/Cache (Honor)",
        "btn_xiaomi_adb_info": "Read Info (ADB)",
        "btn_xiaomi_enable_diag_root": "Enable Diag (ROOT)",
        "btn_xiaomi_reset_frp_adb": "Reset FRP (ADB)", # Placeholder, actual Xiaomi FRP is complex
        "btn_xiaomi_bypass_mi_account": "Bypass Mi Account (ADB)", # Placeholder
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
        "frp_reset_warning_message": "This will attempt a series of common ADB commands to reset FRP. These commands are not guaranteed to work on all devices or Android versions and may require specific device states or permissions (like USB Debugging already enabled and authorized).\n\nProceed with caution. No responsibility is taken for any issues that may arise.",
        "context_cut": "Cut",
        "context_copy": "Copy",
        "context_paste": "Paste",
        "context_select_all": "Select All"
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
        "export_button": "تصدير",
        "quit_dialog_title": "خروج",
        "quit_dialog_message": "هل تريد الخروج من أداة Ultimat-Unlock؟",
        "dependency_check_title": "فحص الاعتماديات",
        "adb_not_found_message": "ADB (Android Debug Bridge) غير موجود أو لا يعمل. بعض الميزات لن تكون متاحة. الرجاء تثبيت/تكوين ADB وإضافته إلى مسار النظام.",
        "fastboot_not_found_message": "Fastboot غير موجود أو لا يعمل. بعض الميزات لن تكون متاحة. الرجاء تثبيت/تكوين Fastboot وإضافته إلى مسار النظام.",
        "fatal_error_title": "خطأ فادح",
        "fatal_error_message_prefix": "حدث خطأ حرج:",
        "btn_get_detailed_info": "الحصول على معلومات مفصلة (ADB)",
        "btn_pull_file": "سحب ملف من الجهاز",
        "btn_push_file": "رفع ملف إلى الجهاز",
        "btn_install_apk": "تثبيت APK",
        "btn_uninstall_app": "حذف تطبيق",
        "btn_honor_info": "قراءة معلومات وسيريال هونور",
        "honor_frp_key_label": "رمز FRP لهونور:",
        "btn_honor_frp": "إزالة FRP (رمز هونور)",
        "btn_honor_reboot_bl": "إعادة تشغيل للبوتلودر (هونور)",
        "btn_honor_reboot_edl": "إعادة تشغيل لوضع EDL (هونور)",
        "btn_honor_wipe_data_cache": "مسح الداتا والكاش (هونور)",
        "btn_xiaomi_adb_info": "قراءة المعلومات (ADB)",
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
        "arabize_confirm_message": "سيحاول هذا الإجراء تغيير لغة الجهاز إلى العربية (ar-AE).\nقد يتطلب هذا أذونات معينة وقد لا يعمل على جميع الأجهزة.\nهل تريد المتابعة؟",
        "arabize_note": "ملاحظة: قد يتطلب التعريب إذن WRITE_SECURE_SETTINGS أو صلاحيات الروت على بعض الأجهزة.",
        "open_browser_title": "فتح رابط في متصفح الجهاز",
        "open_browser_prompt": "أدخل الرابط الكامل للفتح (مثال: https://ultimat-unlock.com/):",
        "frp_reset_warning_title": "محاولة إزالة FRP",
        "frp_reset_warning_message": "سيقوم هذا الإجراء بمحاولة تنفيذ سلسلة من أوامر ADB الشائعة لإزالة قفل FRP. هذه الأوامر ليست مضمونة للعمل على جميع الأجهزة أو إصدارات أندرويد وقد تتطلب حالات معينة للجهاز أو أذونات خاصة (مثل تفعيل تصحيح USB ومصادقته مسبقًا).\n\nيرجى المتابعة بحذر. لا نتحمل أي مسؤولية عن أي مشاكل قد تنشأ.",
        "context_cut": "قص",
        "context_copy": "نسخ",
        "context_paste": "لصق",
        "context_select_all": "تحديد الكل"
    }
}
log_to_file_debug_globally("LABELS defined.")

# ========== THEMES ==========
THEMES = {
    "light": {
        "BG": "#ECEFF1", "FG": "#263238", "ACCENT": "#03A9F4", "ACCENT2": "#0288D1",
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
        "BG": "#263238", "FG": "#ECEFF1", "ACCENT": "#03A9F4", "ACCENT2": "#0288D1",
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
        "BG": "#21252B", "FG": "#D1D9E0", "ACCENT": "#00AEEF", "ACCENT2": "#0095CC",
        "BTN_BG": "#00AEEF", "BTN_BG2": "#0095CC", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#00AEEF",
        "GROUP_BG": "#2C313A", "LOG_BG": "#2C313A",
        "LOG_FG_SUCCESS": "#2ECC71", "LOG_FG_INFO": "#3498DB", "LOG_FG_ERROR": "#E74C3C", # Red for errors
        "LOG_FG_FAIL": "#C0392B", "LOG_FG_CMD": "#1ABC9C", "LOG_FG_WARNING": "#F39C12", # Darker red for fail
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
LOG_FONT = ("Consolas", 11) # Monospaced for logs
log_to_file_debug_globally("FONTS defined.")

def get_labels(lang):
    return LABELS.get(lang, LABELS["en"])

def get_theme(theme_name):
    return THEMES.get(theme_name, THEMES["professional_dark"])

class ModernButton(tk.Button):
    def __init__(self, master, text, command, theme, width=25, height=2, icon=None, **kwargs):
        display_text = f"{icon} {text}" if icon else text
        super().__init__(
            master, text=display_text, command=command, font=BTN_FONT,
            bg=theme["BTN_BG"], fg=theme["BTN_FG"],
            activebackground=theme["BTN_BG2"], activeforeground=theme["BTN_FG"],
            bd=0, relief="flat", cursor="hand2", height=height, width=width,
            padx=10, pady=5, **kwargs)
        self.theme = theme
        self.default_bg = theme["BTN_BG"]
        self.hover_bg = theme["BTN_BG2"]
        self.config(highlightbackground=theme.get("BTN_BORDER", theme["ACCENT"]), highlightthickness=1)
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))

class DBLogger:
    def __init__(self, dbfile=None, tk_root=None):
        log_to_file_debug_globally("DBLogger __init__ started.")
        if dbfile is None:
            try:
                base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                dbfile = os.path.join(base_dir, "operation_log.db")
                os.makedirs(os.path.dirname(dbfile), exist_ok=True)
                with open(dbfile, "a") as f_db_check:
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
                    dbfile = ":memory:"
                    log_to_file_debug_globally("DBLogger: Using in-memory database as last resort.")
        
        self.dbfile = dbfile
        self.tk_root = tk_root
        self.conn = None
        self.cursor = None
        
        try:
            self.conn = sqlite3.connect(self.dbfile)
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
            self.conn = None
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

    def search(self, term):
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

    def all(self, limit=1000):
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
    """
    Creates a right-click context menu for Text and Entry widgets.
    """
    def __init__(self, widget, tk_root, labels):
        self.widget = widget
        self.tk_root = tk_root  # Main Tk instance for clipboard operations
        self.labels = labels    # For localized menu item names
        self.menu = tk.Menu(widget, tearoff=0)

        self.menu.add_command(label=self.labels.get("context_cut", "Cut"), command=self.cut)
        self.menu.add_command(label=self.labels.get("context_copy", "Copy"), command=self.copy)
        self.menu.add_command(label=self.labels.get("context_paste", "Paste"), command=self.paste)
        self.menu.add_separator()
        self.menu.add_command(label=self.labels.get("context_select_all", "Select All"), command=self.select_all)

        widget.bind("<Button-3>", self.show_menu) # Button-3 is usually right-click

    def show_menu(self, event):
        # Update state of menu items based on context
        has_selection = False
        try:
            if self.widget.selection_get():
                has_selection = True
        except tk.TclError:
            has_selection = False

        self.menu.entryconfig(self.labels.get("context_cut", "Cut"), state=tk.NORMAL if has_selection and isinstance(self.widget, (tk.Entry, tk.Text)) and self.widget.cget('state') == tk.NORMAL else tk.DISABLED)
        self.menu.entryconfig(self.labels.get("context_copy", "Copy"), state=tk.NORMAL if has_selection else tk.DISABLED)
        
        can_paste = False
        try:
            if self.tk_root.clipboard_get() and isinstance(self.widget, (tk.Entry, tk.Text)) and self.widget.cget('state') == tk.NORMAL :
                can_paste = True
        except tk.TclError:
            can_paste = False
        self.menu.entryconfig(self.labels.get("context_paste", "Paste"), state=tk.NORMAL if can_paste else tk.DISABLED)
        
        has_text = False
        if isinstance(self.widget, tk.Text):
            if self.widget.get("1.0", tk.END).strip():
                has_text = True
        elif isinstance(self.widget, tk.Entry):
            if self.widget.get().strip():
                has_text = True
        
        self.menu.entryconfig(self.labels.get("context_select_all", "Select All"), state=tk.NORMAL if has_text else tk.DISABLED)

        self.menu.tk_popup(event.x_root, event.y_root)

    def cut(self):
        try:
            if self.widget.selection_get() and self.widget.cget('state') == tk.NORMAL:
                self.widget.event_generate("<<Cut>>")
        except tk.TclError:
            pass # No selection or widget not editable

    def copy(self):
        try:
            if self.widget.selection_get():
                self.widget.event_generate("<<Copy>>")
        except tk.TclError:
            pass # No selection

    def paste(self):
        try:
            if self.widget.cget('state') == tk.NORMAL:
                 self.widget.event_generate("<<Paste>>")
        except tk.TclError:
            pass # Widget not editable

    def select_all(self):
        if isinstance(self.widget, tk.Text):
            self.widget.tag_add(tk.SEL, "1.0", tk.END)
            self.widget.mark_set(tk.INSERT, "1.0") # Move cursor to beginning
            self.widget.see(tk.INSERT)
        elif isinstance(self.widget, tk.Entry):
            self.widget.select_range(0, tk.END)
            self.widget.icursor(tk.END) # Move cursor to end
        return "break" # To prevent default binding propagation


class ProgressBarManager(tk.Frame):
    def __init__(self, master, theme):
        super().__init__(master, bg=theme["BG"])
        self.var = tk.IntVar(value=0)
        progress_bar_color = theme.get("ACCENT", "#00AEEF")
        lightcolor = progress_bar_color
        darkcolor = theme.get("ACCENT2", "#0095CC")
        troughcolor = theme.get("BG", "#21252B")
        bordercolor = theme.get("ACCENT", "#00AEEF")
        thickness = 12

        self.pb = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="indeterminate", # Start as indeterminate
            variable=self.var,
            style="Custom.Horizontal.TProgressbar"
        )
        self.running = False # Tracks if indeterminate is running

        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=troughcolor,
            bordercolor=bordercolor,
            background=progress_bar_color,
            lightcolor=lightcolor,
            darkcolor=darkcolor,
            thickness=thickness
        )
        self.pb.pack(fill=tk.X, padx=10, pady=(2,5)) # Added some vertical padding

    def start(self): # For indeterminate progress
        if not self.winfo_exists(): return
        if not self.running:
            self.pb.config(mode="indeterminate")
            self.pb.start(10)
            self.running = True

    def stop(self): # Stops current activity (indeterminate or determinate), resets to 0 determinate
        if not self.winfo_exists(): return
        if self.running:
            self.pb.stop()
            self.running = False
        self.pb.config(mode="determinate")
        self.var.set(0)
        self.pb.update_idletasks()

    def set_value(self, percent): # For determinate progress
        if not self.winfo_exists(): return
        if self.running: # If it was indeterminate, stop it
            self.pb.stop()
            self.running = False
        self.pb.config(mode="determinate")
        self.var.set(max(0, min(100, int(percent))))
        self.pb.update_idletasks()


class LogPanel(tk.Frame):
    def __init__(self, master, theme, labels, db_logger=None, tk_root=None):
        super().__init__(master, bg=theme["BG"])
        self.labels = labels
        self.theme = theme
        self.tk_root = tk_root
        
        log_title_frame = tk.Frame(self, bg=theme["BG"])
        log_title_frame.pack(fill=tk.X, padx=6, pady=(8,2))
        tk.Label(log_title_frame, text=labels["log"], font=LABEL_FONT, bg=theme["BG"], fg=theme.get("FG", "#D1D9E0")).pack(side=tk.LEFT)

        self.text = tk.Text(self, height=25, font=LOG_FONT, state=tk.DISABLED,
                            bg=theme["LOG_BG"], fg=theme["LOG_FG_INFO"],
                            bd=1, relief="sunken", wrap=tk.WORD,
                            selectbackground=theme["ACCENT"], selectforeground=theme["BTN_FG"],
                            insertbackground=theme["FG"])
        self.text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0,6))
        TextContextMenu(self.text, self.tk_root, self.labels) # Add context menu to log text area

        for tag_name, color_key in [("info", "LOG_FG_INFO"), ("success", "LOG_FG_SUCCESS"), ("error", "LOG_FG_ERROR"), ("fail", "LOG_FG_FAIL"), ("cmd", "LOG_FG_CMD"), ("warning", "LOG_FG_WARNING")]:
            font_config = (LOG_FONT[0], LOG_FONT[1], "bold") if tag_name in ["success", "error", "fail"] else LOG_FONT
            if tag_name == "fail": font_config = (LOG_FONT[0], LOG_FONT[1], "bold", "underline")
            self.text.tag_configure(tag_name, foreground=theme[color_key], font=font_config)
        
        self.db_logger = db_logger
        self.progress_bar = ProgressBarManager(self, theme)
        self.progress_bar.pack(fill=tk.X, padx=6)
        
        search_frame = tk.Frame(self, bg=theme["BG"])
        search_frame.pack(fill=tk.X, padx=6, pady=(6,10))
        tk.Label(search_frame, text=labels.get("search_log_label", "Search Log:"), bg=theme["BG"], fg=theme["FG"], font=FONT).pack(side=tk.LEFT, padx=(0,4))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25, font=FONT,
                                bg=theme.get("GROUP_BG", "#2C313A"), fg=theme.get("FG", "#D1D9E0"),
                                insertbackground=theme["FG"], relief="flat", bd=2, highlightthickness=1,
                                highlightbackground=theme.get("ACCENT2", "#0095CC"), highlightcolor=theme.get("ACCENT", "#00AEEF"))
        search_entry.pack(side=tk.LEFT, padx=4, ipady=2)
        TextContextMenu(search_entry, self.tk_root, self.labels) # Add context menu
        
        ModernButton(search_frame, labels.get("find_button", "Find"), self.show_search, theme, width=8, height=1, icon="").pack(side=tk.LEFT, padx=(2,2))
        ModernButton(search_frame, labels.get("all_button", "All"), self.show_all, theme, width=8, height=1, icon="").pack(side=tk.LEFT, padx=(0,2))
        ModernButton(search_frame, labels.get("export_button", "Export"), self.save_to_file, theme, width=10, height=1, icon="").pack(side=tk.RIGHT, padx=(4,0))
        
        if self.db_logger: self.show_all()

    def log(self, message, tag="info"):
        if not self.winfo_exists(): return
        def __log_to_widget():
            if not self.text.winfo_exists(): return
            self.text.config(state=tk.NORMAL)
            timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] "
            prefix_map = {"cmd": "[CMD]", "success": "[OK]", "error": "[ERR]", "fail": "[FAIL]", "warning": "[WARN]", "info": "[INFO]"}
            log_prefix = prefix_map.get(tag, "[LOG]")
            
            full_log_message = f"{timestamp}{log_prefix} {message}\n"
            
            idx = self.text.index(tk.END)
            self.text.insert(tk.END, full_log_message)
            self.text.tag_add(tag, idx, f"{idx} lineend")
            self.text.see(tk.END)
            self.text.config(state=tk.DISABLED)
            if self.db_logger: self.db_logger.add(message, tag)
        
        if self.tk_root and threading.current_thread() is not threading.main_thread():
            self.tk_root.after(0, __log_to_widget)
        else:
            __log_to_widget()

    def _display_log_entries(self, entries):
        if not self.text.winfo_exists(): return
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        prefix_map = {"cmd": "[CMD]", "success": "[OK]", "error": "[ERR]", "fail": "[FAIL]", "warning": "[WARN]", "info": "[INFO]"}
        for ts, tag, msg in reversed(entries):
            log_prefix = prefix_map.get(tag, "[LOG]")
            log_line = f"{ts} {log_prefix} {msg}\n"
            idx = self.text.index(tk.END)
            self.text.insert(tk.END, log_line)
            self.text.tag_add(tag, idx, f"{idx} lineend")
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)

    def show_search(self):
        if self.db_logger:
            term = self.search_var.get()
            if term:
                entries = self.db_logger.search(term)
                self._display_log_entries(entries)
                self.log(f"Searched for: '{term}'", "info")
            else:
                self.show_all()

    def show_all(self):
        if self.db_logger:
            entries = self.db_logger.all()
            self._display_log_entries(entries)
            self.log("Displayed all log entries.", "info")

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text','.txt')], parent=self.tk_root)
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.text.get("1.0", tk.END))
                self.log(f"Log exported to {file_path}", "info")
            except Exception as e:
                self.log(f"Error exporting log: {e}", "error")
                messagebox.showerror("Error", f"Could not save log: {e}", parent=self.tk_root)

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
            except Exception: pass
            
            if self.winfo_exists() and self.master.winfo_exists():
                 self.master.after(0, lambda s=stat, c=color: self.set_status(s, c))
            
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

        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        if parent_width < 50 or parent_height < 50:
             parent_width = self.parent.winfo_screenwidth()
             parent_height = self.parent.winfo_screenheight()
             parent_x = 0
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
        TextContextMenu(self.username_entry, self, self.labels) # Context menu for username

        tk.Label(main_frame, text=self.labels.get("password_label", "Password:"), font=FONT, bg=self.theme["BG"], fg=self.theme["FG"]).pack(anchor=tk.W)
        self.password_entry = tk.Entry(main_frame, font=FONT, width=30, show="*", bg=self.theme.get("LOG_BG", "#455A64"), fg=self.theme["FG"], insertbackground=self.theme["FG"])
        self.password_entry.pack(pady=(0,20), ipady=3)
        self.password_entry.bind("<Return>", self._attempt_login)
        TextContextMenu(self.password_entry, self, self.labels) # Context menu for password

        ModernButton(main_frame, text=self.labels.get("login_button", "Login"), command=self._attempt_login, theme=self.theme, width=15, height=1).pack()
        
        self.grab_set()
        self.focus_set()
        self.username_entry.focus()

    def _attempt_login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == FIXED_USERNAME and password == FIXED_PASSWORD:
            log_to_file_debug_globally("Login successful.")
            self.destroy()
            self.app_controller.show_main_app()
        else:
            log_to_file_debug_globally("Login failed.")
            messagebox.showerror(self.labels.get("login_failed_title", "Login Failed"),
                                 self.labels.get("login_failed_message", "Invalid username or password."),
                                 parent=self)
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()

    def _on_closing_login(self):
        log_to_file_debug_globally("Login window closed by user. Exiting application.")
        self.parent.destroy()

class AppController:
    def __init__(self):
        log_to_file_debug_globally("AppController __init__ started.")
        self.root = tk.Tk()
        self.root.withdraw()

        self.lang = "en"
        self.theme_mode = "professional_dark"
        self.labels = get_labels(self.lang)
        self.theme = get_theme(self.theme_mode)
        
        try:
            webbrowser.open("https://ultimat-unlock.com/")
            log_to_file_debug_globally("Website opened successfully.")
        except Exception as e_web:
            log_to_file_debug_globally(f"Failed to open website: {e_web}", "WARNING")

        self.login_window = LoginWindow(self.root, self)
        log_to_file_debug_globally("LoginWindow instantiated.")
        self.main_app_window = None

    def start(self):
        log_to_file_debug_globally("AppController start, entering root.mainloop().")
        self.root.mainloop()

    def show_main_app(self):
        log_to_file_debug_globally("show_main_app called.")
        self.root.deiconify()
        if self.main_app_window is None:
            self.main_app_window = UltimateDeviceTool(master_tk_instance=self.root, app_controller=self)
            log_to_file_debug_globally("UltimateDeviceTool instantiated as main_app_window.")
        else:
            log_to_file_debug_globally("Main app window already exists, deiconifying.", "WARNING")
            if isinstance(self.main_app_window, UltimateDeviceTool) and self.main_app_window.winfo_exists():
                 self.main_app_window.master.deiconify() # Ensure master (root) is deiconified
            else: # Recreate if something went wrong
                 self.main_app_window = UltimateDeviceTool(master_tk_instance=self.root, app_controller=self)


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

        self.db_logger = DBLogger(tk_root=self.master)
        log_to_file_debug_globally("Instance variables (lang, theme, db_logger) initialized.")
        
        self.master.title(self.labels["title"])
        self.master.geometry("1280x800")
        self.master.wm_minsize(1024, 700)
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        log_to_file_debug_globally("Window properties (title, geometry, minsize, protocol) set on master.")
        
        self.pack(fill=tk.BOTH, expand=True)

        self._apply_styles()
        self._build_ui()
        self.command_queue = queue.Queue()
        self.after(100, self._process_command_queue)
        log_to_file_debug_globally("UltimateDeviceTool __init__ finished successfully.")

    def _apply_styles(self):
        log_to_file_debug_globally("Applying styles...")
        self.style = ttk.Style(self.master)
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            log_to_file_debug_globally("Clam theme not available.", "WARNING")
        
        self.style.configure("TNotebook", background=self.theme["BG"], borderwidth=0, tabmargins=[2, 5, 2, 0])
        self.style.configure("TNotebook.Tab", background=self.theme.get("NOTEBOOK_TAB_BG", self.theme["GROUP_BG"]),
                                            foreground=self.theme.get("NOTEBOOK_TAB_FG", self.theme["FG"]),
                                            padding=[10, 5], font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("TNotebook.Tab",
                       background=[("selected", self.theme.get("NOTEBOOK_TAB_SELECTED_BG", self.theme["ACCENT"])),
                                   ("active", self.theme.get("NOTEBOOK_TAB_ACTIVE_BG", self.theme["ACCENT2"]))],
                       foreground=[("selected", self.theme.get("NOTEBOOK_TAB_SELECTED_FG", self.theme["BTN_FG"]))])
        
        self.style.configure("TPanedwindow", background=self.theme["BG"])
        self.style.configure("TFrame", background=self.theme["BG"]) # Default for ttk.Frame if used
        log_to_file_debug_globally("Styles applied.")

    def _build_ui(self):
        log_to_file_debug_globally("Building UI...")
        self.config(bg=self.theme["BG"])

        menubar = tk.Menu(self.master, bg=self.theme["BG"], fg=self.theme["FG"], relief=tk.FLAT, bd=0, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu.add_command(label=self.labels["light"], command=lambda: self.set_theme("light"))
        theme_menu.add_command(label=self.labels["dark"], command=lambda: self.set_theme("dark"))
        theme_menu.add_command(label=self.labels["professional_dark"], command=lambda: self.set_theme("professional_dark"))
        menubar.add_cascade(label=self.labels["theme"], menu=theme_menu)
        
        lang_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        lang_menu.add_command(label=LABELS["en"]["english"], command=lambda: self.set_language("en"))
        lang_menu.add_command(label=LABELS["ar"]["arabic"], command=lambda: self.set_language("ar"))
        menubar.add_cascade(label=self.labels["lang"], menu=lang_menu)
        self.master.config(menu=menubar)

        self.status_bar = StatusBar(self, self.theme, self.labels)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        body = ttk.PanedWindow(self, orient=tk.HORIZONTAL, style="TPanedwindow")
        body.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_area_container = tk.Frame(body, bg=self.theme["BG"])
        right_area_container = tk.Frame(body, bg=self.theme["BG"])
        body.add(left_area_container, weight=2)
        body.add(right_area_container, weight=1)

        title_frame = tk.Frame(left_area_container, bg=self.theme["BG"])
        title_frame.pack(fill=tk.X, pady=(15, 8), padx=(15,0))
        tk.Label(title_frame, text=self.labels["title"], font=TITLE_FONT, bg=self.theme["BG"], fg=self.theme.get("TITLE_FG", self.theme["ACCENT"]) ).pack(side=tk.LEFT, padx=(0,10))
        tk.Label(title_frame, text=self.labels["edition"], font=LABEL_FONT, bg=self.theme["BG"], fg=self.theme.get("EDITION_FG", self.theme["FG"]) ).pack(side=tk.LEFT, pady=(6,0))
        
        self.notebook = ttk.Notebook(left_area_container, style="TNotebook")
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=15, pady=(0,15))
        
        try:
            self.log_panel = LogPanel(right_area_container, self.theme, self.labels, db_logger=self.db_logger, tk_root=self.master)
            self.log_panel.pack(fill=tk.BOTH, expand=True, padx=(5,15), pady=(15,15))
            log_to_file_debug_globally("Log panel created.")
        except Exception as e_log_panel:
            log_to_file_debug_globally(f"Error creating LogPanel: {e_log_panel}", "CRITICAL")
            traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
        
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

    def execute_command_async(self, command_list, operation_name="Operation", callback_on_finish=None, is_part_of_sequence=False):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None
        if log_panel_available and not is_part_of_sequence: # Only start/stop for non-sequence or main sequence start
            self.log_panel.progress_bar.start()
        
        command_str_for_debug = " ".join(map(str,command_list)) if isinstance(command_list, list) else str(command_list)
        log_to_file_debug_globally(f"Executing ASYNC ({operation_name}): {command_str_for_debug}", "DEBUG_CMD") # More specific tag

        def _command_thread():
            try:
                process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                stdout, stderr = process.communicate(timeout=120)
                return_code = process.returncode
                result_data = {"stdout": stdout, "stderr": stderr, "return_code": return_code, "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence}
                self.command_queue.put(result_data)
            except subprocess.TimeoutExpired:
                log_to_file_debug_globally(f"Timeout for {operation_name}: {command_str_for_debug}", "ERROR")
                self.command_queue.put({"error": "TimeoutExpired", "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence})
            except FileNotFoundError:
                log_to_file_debug_globally(f"FileNotFound for {operation_name}: {command_list[0]}", "ERROR")
                self.command_queue.put({"error": "FileNotFound", "command_name": command_list[0], "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence})
            except Exception as e:
                log_to_file_debug_globally(f"Exception for {operation_name} ({command_str_for_debug}): {e}", "ERROR")
                traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
                self.command_queue.put({"error": str(e), "operation_name": operation_name, "command": command_list, "callback": callback_on_finish, "is_part_of_sequence": is_part_of_sequence})
        
        threading.Thread(target=_command_thread, daemon=True).start()

    def _process_command_queue(self):
        try:
            while not self.command_queue.empty():
                result = self.command_queue.get_nowait()
                self._handle_command_result(result)
        except Exception as e:
            log_to_file_debug_globally(f"Error in _process_command_queue: {e}", "ERROR")
            traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
        finally:
            self.after(100, self._process_command_queue)

    def _handle_command_result(self, result):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None
        log_method = self.log_panel.log if log_panel_available else log_to_file_debug_globally
        tag_suffix = "" if log_panel_available else "_NO_LOGPANEL"
        
        operation_name = result.get("operation_name", "Unknown Operation")
        command_list = result.get("command", [])
        command_str = " ".join(map(str,command_list)) if isinstance(command_list, list) else str(command_list)
        is_part_of_sequence = result.get("is_part_of_sequence", False)

        # Log full command details to debug log
        log_to_file_debug_globally(f"CMD_RESULT ({operation_name}): ReturnCode={result.get('return_code', 'N/A')}, Command='{command_str}'", "DEBUG_CMD_RESULT")
        if result.get("stdout", "").strip():
            log_to_file_debug_globally(f"  STDOUT: {result.get('stdout').strip()}", "DEBUG_CMD_RESULT")
        if result.get("stderr", "").strip():
            log_to_file_debug_globally(f"  STDERR: {result.get('stderr').strip()}", "DEBUG_CMD_RESULT")


        if "error" in result:
            error_type = result["error"]
            error_message_summary = ""
            if error_type == "TimeoutExpired":
                error_message_summary = "Operation timed out"
            elif error_type == "FileNotFound":
                command_name = result.get("command_name", "N/A")
                error_message_summary = f"Command '{command_name}' not found. Ensure it's installed and in PATH"
            else:
                error_message_summary = f"Error - {error_type}"
            log_method(f"{operation_name}: {error_message_summary}.{tag_suffix}", "error")
        else:
            stdout = result.get("stdout", "")
            stderr = result.get("stderr", "")
            return_code = result.get("return_code", -1)
            
            if return_code == 0:
                log_method(f"{operation_name}: Completed successfully.{tag_suffix}", "success")
                # Log brief, relevant output if any, avoid generic success messages from ADB/Fastboot
                if stdout.strip() and not any(kw in stdout.lower() for kw in ["success", "already", "performed", "daemon started successfully"]):
                    summary_stdout = stdout.strip().splitlines()[0]
                    if len(summary_stdout) > 100: summary_stdout = summary_stdout[:100] + "..."
                    log_method(f"  Detail: {summary_stdout}{tag_suffix}", "info")
                elif stderr.strip(): # Non-fatal warnings
                    summary_stderr = stderr.strip().splitlines()[0]
                    if len(summary_stderr) > 100: summary_stderr = summary_stderr[:100] + "..."
                    log_method(f"  Warning: {summary_stderr}{tag_suffix}", "warning")
            else:
                log_method(f"{operation_name}: Failed (Code: {return_code}).{tag_suffix}", "fail")
                # Prioritize stderr for error messages
                if stderr.strip():
                    summary_stderr = stderr.strip().splitlines()[0]
                    if len(summary_stderr) > 120: summary_stderr = summary_stderr[:120] + "..."
                    log_method(f"  Error: {summary_stderr}{tag_suffix}", "error")
                elif stdout.strip(): # If no stderr, stdout might contain the error
                    summary_stdout = stdout.strip().splitlines()[0]
                    if len(summary_stdout) > 120: summary_stdout = summary_stdout[:120] + "..."
                    log_method(f"  Output: {summary_stdout}{tag_suffix}", "info")
        
        if log_panel_available and not is_part_of_sequence:
            self.log_panel.progress_bar.stop()
        
        callback = result.get("callback")
        if callback and callable(callback):
            try:
                callback(result)
            except Exception as e_callback:
                log_to_file_debug_globally(f"Error in command callback for {operation_name}: {e_callback}", "ERROR")
                traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))

    def get_detailed_adb_info(self, callback_after_all_props=None):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None
        log_method = self.log_panel.log if log_panel_available else log_to_file_debug_globally
        tag_suffix = "" if log_panel_available else "_NO_LOGPANEL"
        
        log_method(f"Fetching detailed device information...{tag_suffix}", "info")
        if log_panel_available: self.log_panel.progress_bar.start() # Start progress for the whole operation

        properties = [
            "ro.product.manufacturer", "ro.product.model", "ro.product.name",
            "ro.build.version.release", "ro.build.version.sdk", "ro.serialno",
            "ro.bootloader", "ro.build.fingerprint",
            "gsm.version.baseband", "ro.hardware", "ro.build.id",
            "ro.build.type", "ro.build.tags", "ro.build.host",
            "ro.product.cpu.abi", "ro.product.board"
        ]
        
        results_dict = {}
        remaining_props_count = len(properties)
        
        def _after_single_prop_fetch(result_single_prop):
            nonlocal remaining_props_count
            prop_name_fetched = "unknown_prop"
            if result_single_prop.get("command") and len(result_single_prop["command"]) > 3:
                prop_name_fetched = result_single_prop["command"][3]

            if result_single_prop.get("return_code") == 0:
                stdout_val = result_single_prop.get("stdout", "").strip()
                if stdout_val: results_dict[prop_name_fetched] = stdout_val
            else:
                results_dict[prop_name_fetched] = "Error fetching"
                # log_method(f"Failed to get property: {prop_name_fetched}{tag_suffix}", "warning") # Already logged by _handle_command_result

            remaining_props_count -= 1
            
            if remaining_props_count <= 0:
                log_method(f"Detailed Device Information:{tag_suffix}", "info")
                for prop_key in sorted(results_dict.keys()):
                    log_method(f"  {prop_key}: {results_dict[prop_key]}{tag_suffix}", "info")
                
                if log_panel_available: self.log_panel.progress_bar.stop() # Stop progress for the whole operation
                if callback_after_all_props and callable(callback_after_all_props):
                    callback_after_all_props({"return_code": 0, "results": results_dict})
        
        for prop_to_fetch in properties:
            self.execute_command_async(["adb", "shell", "getprop", prop_to_fetch],
                                      operation_name=f"Get Property ({prop_to_fetch})", # More specific
                                      callback_on_finish=_after_single_prop_fetch,
                                      is_part_of_sequence=True) # Indicate it's part of a larger op

    def set_language(self, lang):
        if lang in LABELS:
            self.app_controller.lang = lang
            self.lang = lang
            self.labels = get_labels(self.lang)
            self._rebuild_ui()
            log_to_file_debug_globally(f"Language changed to {lang}.")
        else:
            log_to_file_debug_globally(f"Language {lang} not supported.", "WARNING")

    def set_theme(self, theme_name):
        if theme_name in THEMES:
            self.app_controller.theme_mode = theme_name
            self.theme_mode = theme_name
            self.theme = get_theme(theme_name)
            self._rebuild_ui()
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
        
        for widget in self.winfo_children():
            widget.destroy()
        
        self._apply_styles()
        self._build_ui()
        
        if hasattr(self, 'notebook') and self.notebook.winfo_exists():
            try:
                if self.notebook.tabs():
                    self.notebook.select(current_tab_index if current_tab_index < len(self.notebook.tabs()) else 0)
            except tk.TclError: pass
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
            log_to_file_debug_globally("Application closed by user.")
            self.master.destroy()

class SamsungTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app: UltimateDeviceTool):
        log_to_file_debug_globally("SamsungTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))
        
        self.num_frp_steps = 0 # For FRP progress
        self.current_frp_step = 0 # For FRP progress

        container = tk.Frame(self, bg=self.theme.get("BG", "#21252B"))
        container.pack(fill=tk.BOTH, expand=True)

        group_samsung = tk.LabelFrame(container, text=self.labels.get("group_samsung", "Samsung ADB Repair & Utilities"),
                                    font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                    fg=self.theme.get("FG", "#D1D9E0"), padx=15, pady=15, relief="groove", bd=2)
        group_samsung.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        col1_frame = tk.Frame(group_samsung, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        col1_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N)

        ModernButton(col1_frame, text=self.labels.get("btn_get_detailed_info", "Get Detailed Info (ADB)"),
                                   command=self.action_get_detailed_info, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
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

    def action_get_detailed_info(self):
        def _after_info_callback(result):
            # This callback is mostly for knowing when the sequence is done.
            # Individual property results are logged by get_detailed_adb_info itself.
            pass # Logging is handled within get_detailed_adb_info and _handle_command_result
        self.master_app.get_detailed_adb_info(callback_after_all_props=_after_info_callback)

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
            self.master_app.log_panel.log("FRP Reset (ADB) cancelled by user.", "info")
            return

        self.master_app.log_panel.log("Starting FRP Reset sequence (ADB)...", "info")
        
        # Sequence of commands to try for FRP reset
        self.commands_frp_sequence = [
            (["adb", "shell", "settings", "put", "global", "setup_wizard_has_run", "1"], "Set setup_wizard_has_run to 1"),
            (["adb", "shell", "settings", "put", "secure", "user_setup_complete", "1"], "Set user_setup_complete (secure table)"),
            (["adb", "shell", "settings", "put", "global", "device_provisioned", "1"], "Set device_provisioned to 1"),
            (["adb", "shell", "content", "insert", "--uri", "content://settings/secure", "--bind", "name:s:user_setup_complete", "--bind", "value:s:1"], "Insert user_setup_complete via content provider"),
            # The following are more aggressive and might require root or specific conditions.
            # (["adb", "shell", "pm", "clear", "com.google.android.gsf"], "Clear Google Services Framework data"),
            # (["adb", "shell", "pm", "clear", "com.google.android.gms"], "Clear Google Play Services data"),
            # (["adb", "shell", "reboot"], "Rebooting device after FRP attempts") # Optional last step
        ]
        self.num_frp_steps = len(self.commands_frp_sequence)
        self.current_frp_step = 0

        if self.master_app.log_panel:
            self.master_app.log_panel.progress_bar.set_value(0) # Reset to 0 for determinate sequence

        self._execute_next_frp_step()

    def _execute_next_frp_step(self):
        if self.current_frp_step < self.num_frp_steps:
            command, op_desc = self.commands_frp_sequence[self.current_frp_step]
            
            # Progress bar for the current individual command will be indeterminate
            # The overall progress is updated in the callback
            
            self.master_app.execute_command_async(
                command,
                operation_name=f"FRP: {op_desc}",
                callback_on_finish=self._frp_step_callback,
                is_part_of_sequence=True # Important for progress bar handling
            )
        else:
            self.master_app.log_panel.log("All FRP reset steps attempted. Please check the device.", "info")
            if self.master_app.log_panel:
                self.master_app.log_panel.progress_bar.set_value(100) # Mark as complete
                # Optionally, stop/reset after a delay or let it stay at 100
                self.master_app.after(2000, lambda: self.master_app.log_panel.progress_bar.stop() if self.master_app.log_panel else None)


    def _frp_step_callback(self, result):
        # This callback is mainly to advance the sequence and update overall progress.
        # Individual command success/failure is logged by _handle_command_result.
        
        self.current_frp_step += 1
        
        if self.master_app.log_panel:
            progress_percentage = int((self.current_frp_step / self.num_frp_steps) * 100)
            self.master_app.log_panel.progress_bar.set_value(progress_percentage)

        self._execute_next_frp_step() # Execute next step

    def action_factory_reset_adb(self):
        if messagebox.askyesno("Confirm Factory Reset", "Are you sure you want to factory reset the device via ADB? This will erase all user data.", parent=self.master_app.master):
            command = ["adb", "shell", "wipe", "data"]
            self.master_app.execute_command_async(command, operation_name="Factory Reset (ADB)")
        else:
            self.master_app.log_panel.log("Factory Reset (ADB) cancelled by user.", "info")

    def action_reset_screenlock_adb(self):
        if messagebox.askyesno("Confirm Screen Lock Reset", "Attempt to reset screen lock via ADB? This usually requires root and may not work on all devices/Android versions. Continue?", parent=self.master_app.master):
            commands_to_try = [
                (["adb", "shell", "rm", "/data/system/gesture.key"], "Remove gesture.key (requires root)"),
                (["adb", "shell", "rm", "/data/system/password.key"], "Remove password.key (requires root)"),
            ]
            self.master_app.execute_command_async(commands_to_try[0][0], operation_name=f"Reset SL: {commands_to_try[0][1]}")
            self.master_app.execute_command_async(commands_to_try[1][0], operation_name=f"Reset SL: {commands_to_try[1][1]}")
            self.master_app.log_panel.log("Attempted screen lock reset. Reboot device to see effect.", "info")
        else:
            self.master_app.log_panel.log("Screen Lock Reset (ADB) cancelled by user.", "info")

    def action_arabize_device(self):
        if messagebox.askyesno(
            self.labels.get("arabize_confirm_title", "Confirm Arabization"),
            self.labels.get("arabize_confirm_message", "This will attempt to change the device language to Arabic (ar-AE)... Proceed?"),
            parent=self.master_app.master):
            
            locale_to_set = "ar-AE"
            self.master_app.execute_command_async(
                ["adb", "shell", "settings", "put", "system", "system_locales", locale_to_set],
                operation_name=f"Set system_locales to {locale_to_set}"
            )
            self.master_app.execute_command_async(
                ["adb", "shell", "setprop", "persist.sys.locale", locale_to_set],
                operation_name=f"Set persist.sys.locale to {locale_to_set}"
            )
            self.master_app.execute_command_async(
                ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.LOCALE_CHANGED"],
                operation_name="Broadcast Locale Change"
            )
            self.master_app.log_panel.log("Arabization commands sent. Check device. A reboot might be needed.", "info")
        else:
            self.master_app.log_panel.log("Arabization cancelled by user.", "info")

    def action_open_browser_adb(self):
        url = simpledialog.askstring(
            self.labels.get("open_browser_title", "Open URL"),
            self.labels.get("open_browser_prompt", "Enter URL:"),
            parent=self.master_app.master
        )
        if url and url.strip():
            if not (url.startswith("http://") or url.startswith("https://")):
                messagebox.showwarning("Invalid URL", "Please enter a full URL including http:// or https://", parent=self.master_app.master)
                self.master_app.log_panel.log(f"Invalid URL for Open Browser: {url}", "warning")
                return

            command = ["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url.strip()]
            self.master_app.execute_command_async(command, operation_name=f"Open URL: {url.strip()}")
        elif url is not None:
             messagebox.showwarning("Empty URL", "URL cannot be empty.", parent=self.master_app.master)
             self.master_app.log_panel.log("Open Browser: URL was empty.", "info")
        else:
            self.master_app.log_panel.log("Open Browser action cancelled by user.", "info")


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
        TextContextMenu(honor_frp_entry, self.master_app.master, self.labels) # Add context menu

        ModernButton(frp_frame, text=self.labels.get("btn_honor_frp", "Remove FRP (Honor Code)"),
                                   command=self.action_honor_remove_frp, theme=self.theme, width=25, height=1).pack(side=tk.LEFT, padx=5)
        log_to_file_debug_globally("HonorTab __init__ finished.")

    def action_honor_info(self):
        command = ["fastboot", "getvar", "all"]
        self.master_app.execute_command_async(command, operation_name="Honor Get Info (Fastboot)")

    def action_honor_reboot_bootloader(self):
        command = ["fastboot", "reboot-bootloader"]
        self.master_app.execute_command_async(command, operation_name="Honor Reboot Bootloader")

    def action_honor_reboot_edl(self):
        command = ["fastboot", "oem", "edl"]
        self.master_app.execute_command_async(command, operation_name="Honor Reboot EDL")

    def action_honor_wipe_data_cache(self):
        if messagebox.askyesno("Confirm Wipe", "Are you sure you want to wipe data and cache on this Honor device? This will erase all user data.", parent=self.master_app.master):
            self.master_app.execute_command_async(["fastboot", "erase", "cache"], operation_name="Honor Wipe Cache")
            self.master_app.execute_command_async(["fastboot", "erase", "userdata"], operation_name="Honor Wipe Userdata")
        else:
            self.master_app.log_panel.log("Honor Wipe Data/Cache cancelled by user.", "info")

    def action_honor_remove_frp(self):
        frp_key = self.honor_frp_key_var.get()
        if not frp_key:
            messagebox.showerror("Input Error", "Please enter the Honor FRP key.", parent=self.master_app.master)
            return
        command = ["fastboot", "oem", "frp-unlock", frp_key]
        self.master_app.execute_command_async(command, operation_name=f"Honor Remove FRP with Key")

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

        ModernButton(adb_col1, text=self.labels.get("btn_xiaomi_adb_info", "Read Info (ADB)"),
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
                                   command=lambda: messagebox.showinfo("Info", "Enable Diag (ROOT) is a placeholder for specific Xiaomi Diag enabling commands, which usually require root and device-specific methods.", parent=self.master_app.master), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

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
        self.master_app.get_detailed_adb_info()

    def action_xiaomi_fastboot_unlock(self):
        if messagebox.askyesno("Confirm Unlock", "Are you sure you want to unlock the bootloader? This will erase all user data and may void warranty. For Xiaomi, this often requires Mi Unlock Tool and an authorized account.", parent=self.master_app.master):
            self.master_app.execute_command_async(["fastboot", "oem", "unlock"], operation_name="Xiaomi Unlock Bootloader")
            self.master_app.log_panel.log("Note: Xiaomi bootloader unlock often requires official Mi Unlock Tool.", "warning")
        else:
            self.master_app.log_panel.log("Xiaomi Unlock Bootloader cancelled by user.", "info")

    def action_xiaomi_fastboot_lock(self):
        if messagebox.askyesno("Confirm Lock", "Are you sure you want to lock the bootloader? This will erase all user data.", parent=self.master_app.master):
            self.master_app.execute_command_async(["fastboot", "oem", "lock"], operation_name="Xiaomi Lock Bootloader")
        else:
            self.master_app.log_panel.log("Xiaomi Lock Bootloader cancelled by user.", "info")

    def action_xiaomi_fastboot_wipe_data(self):
        if messagebox.askyesno("Confirm Wipe", "Are you sure you want to wipe all user data? This cannot be undone.", parent=self.master_app.master):
            self.master_app.execute_command_async(["fastboot", "erase", "userdata"], operation_name="Xiaomi Wipe Data (Fastboot)")
        else:
            self.master_app.log_panel.log("Xiaomi Wipe Data cancelled by user.", "info")

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
        file_col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N, expand=True)
        file_col2 = tk.Frame(file_cols_container, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        file_col2.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N, expand=True)

        ModernButton(file_col1, text=self.labels.get("btn_pull_file", "Pull File from Device"),
                                   command=self.action_pull_file, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col1, text=self.labels.get("btn_push_file", "Push File to Device"),
                                   command=self.action_push_file, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        
        ModernButton(file_col2, text=self.labels.get("btn_install_apk", "Install APK"),
                                   command=self.action_install_apk, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col2, text=self.labels.get("btn_uninstall_app", "Uninstall App"),
                                   command=self.action_uninstall_app, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

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
        TextContextMenu(advanced_cmd_entry, self.master_app.master, self.labels) # Add context menu

        ModernButton(group_advanced, text=self.labels.get("btn_run_advanced_cmd", "Run Command"),
                                   command=self.action_run_advanced_cmd, theme=self.theme, width=20).pack(pady=5, anchor=tk.W)
        log_to_file_debug_globally("FileAdvancedTab __init__ finished.")

    def action_pull_file(self):
        device_path = simpledialog.askstring(self.labels.get("pull_file_title", "Pull File from Device"),
                                            self.labels.get("pull_file_device_path_msg", "Enter device source path:"),
                                            parent=self.master_app.master)
        if not device_path: return
        
        local_path = filedialog.asksaveasfilename(parent=self.master_app.master)
        if not local_path: return
        
        self.master_app.execute_command_async(["adb", "pull", device_path, local_path],
                                             operation_name=f"Pull File: {os.path.basename(device_path)}")

    def action_push_file(self):
        local_path = filedialog.askopenfilename(parent=self.master_app.master)
        if not local_path: return
        
        device_path = simpledialog.askstring(self.labels.get("push_file_title", "Push File to Device"),
                                            self.labels.get("push_file_device_path_msg", "Enter device destination path:"),
                                            parent=self.master_app.master)
        if not device_path: return
        
        self.master_app.execute_command_async(["adb", "push", local_path, device_path],
                                             operation_name=f"Push File: {os.path.basename(local_path)}")

    def action_install_apk(self):
        apk_path = filedialog.askopenfilename(title=self.labels.get("install_apk_title", "Select APK to Install"),
                                             filetypes=[("APK Files", "*.apk"), ("All Files", "*.*")],
                                             parent=self.master_app.master)
        if not apk_path: return
        
        self.master_app.execute_command_async(["adb", "install", "-r", apk_path],
                                             operation_name=f"Install APK: {os.path.basename(apk_path)}")

    def action_uninstall_app(self):
        package_name = simpledialog.askstring(self.labels.get("uninstall_title", "Uninstall App"),
                                             self.labels.get("uninstall_msg", "Enter package name:"),
                                             parent=self.master_app.master)
        if not package_name: return
        
        self.master_app.execute_command_async(["adb", "uninstall", package_name],
                                             operation_name=f"Uninstall App: {package_name}")

    def action_run_advanced_cmd(self):
        cmd_str = self.advanced_cmd_var.get().strip()
        if not cmd_str: return
        
        cmd_parts = cmd_str.split()
        if not cmd_parts: return
        
        self.master_app.execute_command_async(cmd_parts, operation_name=f"Advanced Command: {cmd_parts[0]}") # Use first part as op name hint

if __name__ == "__main__":
    try:
        try:
            subprocess.check_output(["adb", "version"], stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            log_to_file_debug_globally("ADB found.")
        except Exception:
            log_to_file_debug_globally("ADB not found or not working.", "WARNING")

        controller = AppController()
        controller.start()

    except Exception as e:
        log_to_file_debug_globally(f"Fatal error in main: {e}", "CRITICAL")
        traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
        try:
            root_err = tk.Tk()
            root_err.withdraw()
            messagebox.showerror("Fatal Error", f"A critical error occurred: {e}\n\nPlease check '{_DEBUG_LOG_PATH}' for details.", parent=None)
            root_err.destroy()
        except Exception as e_tk_fatal:
            print(f"A critical error occurred: {e}. Check '{_DEBUG_LOG_PATH}'. Tkinter error dialog also failed: {e_tk_fatal}", file=sys.stderr)

