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

# Static debug log path and function, defined early for global use
_DEBUG_LOG_PATH = "application_debug_log.txt"

def log_to_file_debug_globally(message, level="INFO"):
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f_log:
            f_log.write(f"[{datetime.now()}] [{level}] {message}\n")
    except Exception as e:
        print(f"[CRITICAL_ERROR] Global static log failed: {e} for message: {message}", file=sys.stderr)
        # Avoid traceback here to prevent potential recursion if print itself is part of the problem

log_to_file_debug_globally("Script execution started. Global logger active.")

# ========== LABELS ==========
LABELS = {
    "en": {
        "title": "Ultimate Device Tool",
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
        "btn_localize_10": "Localize Android 10",
        "btn_localize_11": "Localize Android 11",
        "btn_localize_12": "Localize Android 12",
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
        "advanced_command_button": "Advanced Command",
        "quit_dialog_title": "Quit",
        "quit_dialog_message": "Do you want to quit Ultimate Device Tool?",
        "dependency_check_title": "Dependency Check",
        "adb_not_found_message": "ADB (Android Debug Bridge) not found or not working. Some features will be unavailable. Please install/configure ADB and add it to your system PATH.",
        "fastboot_not_found_message": "Fastboot not found or not working. Some features will be unavailable. Please install/configure Fastboot and add it to your system PATH.",
        "fatal_error_title": "Fatal Error",
        "fatal_error_message_prefix": "A critical error occurred:",
        "btn_get_detailed_info": "Get Detailed Device Info (ADB)"
    },
    "ar": {
        "title": "أداة الأجهزة الشاملة",
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
        "btn_localize_10": "تعريب أندرويد 10",
        "btn_localize_11": "تعريب أندرويد 11",
        "btn_localize_12": "تعريب أندرويد 12",
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
        "advanced_command_button": "أمر متقدم",
        "quit_dialog_title": "خروج",
        "quit_dialog_message": "هل تريد الخروج من أداة الأجهزة الشاملة؟",
        "dependency_check_title": "فحص الاعتماديات",
        "adb_not_found_message": "ADB (Android Debug Bridge) not found or not working. Some features will be unavailable. Please install/configure ADB and add it to your system PATH.",
        "fastboot_not_found_message": "Fastboot not found or not working. Some features will be unavailable. Please install/configure Fastboot and add it to your system PATH.",
        "fatal_error_title": "خطأ فادح",
        "fatal_error_message_prefix": "حدث خطأ حرج:",
        "btn_get_detailed_info": "الحصول على معلومات مفصلة (ADB)"
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
    "dark": { # Original Dark Theme
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
    "professional_dark": { # New Professional Dark Theme
        "BG": "#21252B", "FG": "#D1D9E0", "ACCENT": "#00AEEF", "ACCENT2": "#0095CC", # Vibrant Blue
        "BTN_BG": "#00AEEF", "BTN_BG2": "#0095CC", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#00AEEF",
        "GROUP_BG": "#2C313A", "LOG_BG": "#2C313A", # Slightly lighter than main BG for contrast
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
TITLE_FONT = ("Segoe UI Semibold", 18) # Increased size
LABEL_FONT = ("Segoe UI", 9, "bold")
BTN_FONT = ("Segoe UI", 10, "bold")
LOG_FONT = ("Consolas", 11)
log_to_file_debug_globally("FONTS defined.")

def get_labels(lang):
    return LABELS.get(lang, LABELS["en"])

def get_theme(theme_name):
    return THEMES.get(theme_name, THEMES["professional_dark"]) # Default to new theme

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
                    dbfile_fallback = os.path.join(user_dir, ".UltimateDeviceTool", "operation_log.db")
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

class ProgressBarManager(tk.Frame):
    def __init__(self, master, theme):
        super().__init__(master, bg=theme["BG"])
        self.var = tk.IntVar(value=0)
        progress_bar_color = theme.get("ACCENT", "#00AEEF")
        lightcolor = progress_bar_color
        darkcolor = theme.get("ACCENT2", "#0095CC")
        troughcolor = theme.get("BG", "#21252B")
        bordercolor = theme.get("ACCENT", "#00AEEF")
        background = progress_bar_color
        thickness = 12  # Increased height for better visibility
        
        self.pb = ttk.Progressbar(
            self, 
            orient="horizontal", 
            mode="indeterminate", 
            variable=self.var,
            style="Custom.Horizontal.TProgressbar"
        )
        self.pb.configure(style="Custom.Horizontal.TProgressbar")
        self.running = False
        
        # Configure style
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
        
        self.pb.pack(fill=tk.X, padx=10, pady=0)

    def start(self):
        if not self.winfo_exists(): 
            return
        if not self.running and self.winfo_exists(): 
            self.pb["mode"] = "indeterminate"
            self.pb.start(10)
            self.running = True

    def stop(self):
        if self.running and self.winfo_exists(): 
            self.pb.stop()
            self.pb["mode"] = "determinate"
            self.var.set(0)
            self.running = False

    def set(self, percent):
        if self.winfo_exists():
            self.pb["mode"] = "determinate"
            if self.running: 
                self.pb.stop()
                self.running = False
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
        
        for tag_name, color_key in [("info", "LOG_FG_INFO"), ("success", "LOG_FG_SUCCESS"), ("error", "LOG_FG_ERROR"), ("fail", "LOG_FG_FAIL"), ("cmd", "LOG_FG_CMD"), ("warning", "LOG_FG_WARNING")]:
            font_config = (LOG_FONT[0], LOG_FONT[1], "bold") if tag_name in ["success", "error", "fail"] else LOG_FONT
            if tag_name == "fail": 
                font_config = (LOG_FONT[0], LOG_FONT[1], "bold", "underline")
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
        
        ModernButton(search_frame, labels.get("find_button", "Find"), self.show_search, theme, width=8, height=1, icon="").pack(side=tk.LEFT, padx=(2,2))
        ModernButton(search_frame, labels.get("all_button", "All"), self.show_all, theme, width=8, height=1, icon="").pack(side=tk.LEFT, padx=(0,2))
        ModernButton(search_frame, labels.get("export_button", "Export"), self.save_to_file, theme, width=10, height=1, icon="").pack(side=tk.RIGHT, padx=(4,0))
        
        if self.db_logger: 
            self.show_all()

    def log(self, message, tag="info"):
        if not self.winfo_exists(): 
            return
        def __log_to_widget():
            if not self.text.winfo_exists(): 
                return
            self.text.config(state=tk.NORMAL)
            timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] "
            prefix_map = {"cmd": "[CMD]", "success": "[SUCCESS]", "error": "[ERROR]", "fail": "[FAIL]", "warning": "[WARNING]", "info": "[INFO]"}
            log_prefix = prefix_map.get(tag, "[LOG]")
            full_log_message = f"{timestamp}{log_prefix} {message}\n"
            idx = self.text.index(tk.END)
            self.text.insert(tk.END, full_log_message)
            self.text.tag_add(tag, idx, f"{idx} lineend") 
            self.text.see(tk.END)
            self.text.config(state=tk.DISABLED)
            if self.db_logger: 
                self.db_logger.add(message, tag)
        if self.tk_root and threading.current_thread() is not threading.main_thread(): 
            self.tk_root.after(0, __log_to_widget)
        else: 
            __log_to_widget()

    def _display_log_entries(self, entries):
        if not self.text.winfo_exists(): 
            return
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        prefix_map = {"cmd": "[CMD]", "success": "[SUCCESS]", "error": "[ERROR]", "fail": "[FAIL]", "warning": "[WARNING]", "info": "[INFO]"}
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
        if self.winfo_exists(): 
            self.config(text=text, fg=color)

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
            except Exception: 
                pass 
            
            if self.winfo_exists() and self.master.winfo_exists():
                 self.master.after(0, lambda s=stat, c=color: self.set_status(s, c))
            
            if self.winfo_exists():
                 self._check_adb_after_id = self.after(5000, self._check_adb)

        threading.Thread(target=check_thread_func, daemon=True).start()

    def cancel_adb_check(self):
        if self._check_adb_after_id:
            self.after_cancel(self._check_adb_after_id)
            self._check_adb_after_id = None

class UltimateDeviceTool(tk.Tk):
    def __init__(self):
        log_to_file_debug_globally("UltimateDeviceTool __init__ started.")
        super().__init__()
        log_to_file_debug_globally("super().__init__() called.")
        self.lang = "en"
        self.theme_mode = "professional_dark"
        self.labels = get_labels(self.lang)
        self.theme = get_theme(self.theme_mode)
        self.db_logger = DBLogger(tk_root=self)
        log_to_file_debug_globally("Instance variables (lang, theme, db_logger) initialized.")
        self.title(self.labels["title"])
        self.geometry("1280x800")
        self.wm_minsize(1024, 700) 
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        log_to_file_debug_globally("Window properties (title, geometry, minsize, protocol) set.")
        self._apply_styles()
        self._build_ui()
        self.command_queue = queue.Queue()
        self.after(100, self._process_command_queue)
        log_to_file_debug_globally("UltimateDeviceTool __init__ finished successfully.")

    def _apply_styles(self):
        log_to_file_debug_globally("Applying styles...")
        self.style = ttk.Style(self)
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
        log_to_file_debug_globally("Styles applied.")

    def _build_ui(self):
        log_to_file_debug_globally("Building UI...")
        self.config(bg=self.theme["BG"])
        menubar = tk.Menu(self, bg=self.theme["BG"], fg=self.theme["FG"], relief=tk.FLAT, bd=0, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu.add_command(label=self.labels["light"], command=lambda: self.set_theme("light"))
        theme_menu.add_command(label=self.labels["dark"], command=lambda: self.set_theme("dark"))
        theme_menu.add_command(label=self.labels["professional_dark"], command=lambda: self.set_theme("professional_dark"))
        menubar.add_cascade(label=self.labels["theme"], menu=theme_menu)
        lang_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT, activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        lang_menu.add_command(label=LABELS["en"]["english"], command=lambda: self.set_language("en"))
        lang_menu.add_command(label=LABELS["ar"]["arabic"], command=lambda: self.set_language("ar"))
        menubar.add_cascade(label=self.labels["lang"], menu=lang_menu)
        self.config(menu=menubar)
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
            self.log_panel = LogPanel(right_area_container, self.theme, self.labels, db_logger=self.db_logger, tk_root=self)
            self.log_panel.pack(fill=tk.BOTH, expand=True, padx=(5,15), pady=(15,15))
            log_to_file_debug_globally("Log panel created.")
        except Exception as e_log_panel:
            log_to_file_debug_globally(f"Error creating LogPanel: {e_log_panel}", "CRITICAL")
            traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
        
        # Add Tabs
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
                messagebox.showerror("UI Build Error", f"Failed to build {self.labels[label_key]} tab: {e_tab_creation}", parent=self)

        log_to_file_debug_globally("UI Building finished.")

    def execute_command_async(self, command_list, operation_name="Operation", callback_on_finish=None):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None
        if log_panel_available:
            self.log_panel.progress_bar.start()
        else:
            log_to_file_debug_globally(f"LogPanel not available for command: {operation_name}", "WARNING")
        
        def _command_thread():
            try:
                process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                stdout, stderr = process.communicate(timeout=120)
                return_code = process.returncode
                result_data = {"stdout": stdout, "stderr": stderr, "return_code": return_code, "operation_name": operation_name, "command": command_list, "callback": callback_on_finish}
                self.command_queue.put(result_data)
            except subprocess.TimeoutExpired:
                self.command_queue.put({"error": "TimeoutExpired", "operation_name": operation_name, "command": command_list, "callback": callback_on_finish})
            except FileNotFoundError:
                self.command_queue.put({"error": "FileNotFound", "command_name": command_list[0], "operation_name": operation_name, "command": command_list, "callback": callback_on_finish})
            except Exception as e:
                self.command_queue.put({"error": str(e), "operation_name": operation_name, "command": command_list, "callback": callback_on_finish})
        
        threading.Thread(target=_command_thread, daemon=True).start()

    def _process_command_queue(self):
        try:
            while not self.command_queue.empty():
                result = self.command_queue.get_nowait()
                self._handle_command_result(result)
        except Exception as e:
            log_to_file_debug_globally(f"Error in _process_command_queue: {e}", "ERROR")
        finally:
            self.after(100, self._process_command_queue)

    def _handle_command_result(self, result):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None
        log_method = self.log_panel.log if log_panel_available else log_to_file_debug_globally
        tag_suffix = "" if log_panel_available else "_LOG"
        
        operation_name = result.get("operation_name", "Unknown Operation")
        command = result.get("command", ["unknown"])
        command_str = " ".join(command) if isinstance(command, list) else str(command)
        
        if "error" in result:
            error_type = result["error"]
            if error_type == "TimeoutExpired":
                log_method(f"Operation timed out: {operation_name}{tag_suffix}", "error")
                log_method(f"Command: {command_str}{tag_suffix}", "cmd")
            elif error_type == "FileNotFound":
                command_name = result.get("command_name", "unknown")
                log_method(f"Command not found: {command_name}. Operation: {operation_name}{tag_suffix}", "error")
                log_method(f"Make sure {command_name} is installed and in your PATH{tag_suffix}", "error")
            else:
                log_method(f"Error executing {operation_name}: {error_type}{tag_suffix}", "error")
                log_method(f"Command: {command_str}{tag_suffix}", "cmd")
        else:
            stdout = result.get("stdout", "")
            stderr = result.get("stderr", "")
            return_code = result.get("return_code", -1)
            
            # Log the command that was executed
            log_method(f"Executed: {operation_name}{tag_suffix}", "cmd")
            log_method(f"Command: {command_str}{tag_suffix}", "cmd")
            
            # Determine success/failure based on return code
            if return_code == 0:
                log_method(f"{operation_name} completed successfully.{tag_suffix}", "success")
                if stdout.strip():
                    log_method(f"Output: {stdout.strip()}{tag_suffix}", "info")
                if stderr.strip():
                    log_method(f"Warnings: {stderr.strip()}{tag_suffix}", "warning")
            else:
                log_method(f"{operation_name} failed with code {return_code}.{tag_suffix}", "fail")
                if stderr.strip():
                    log_method(f"Error: {stderr.strip()}{tag_suffix}", "error")
                if stdout.strip():
                    log_method(f"Output: {stdout.strip()}{tag_suffix}", "info")
        
        # Stop progress bar if it was started
        if log_panel_available:
            self.log_panel.progress_bar.stop()
        
        # Execute callback if provided
        callback = result.get("callback")
        if callback and callable(callback):
            try:
                callback(result)
            except Exception as e_callback:
                log_to_file_debug_globally(f"Error in command callback: {e_callback}", "ERROR")

    def get_detailed_adb_info(self, callback_after_all_props=None):
        log_panel_available = hasattr(self, 'log_panel') and self.log_panel is not None
        log_method = self.log_panel.log if log_panel_available else log_to_file_debug_globally
        tag_suffix = "" if log_panel_available else "_LOG"
        
        log_method(f"Fetching detailed device information...{tag_suffix}", "info")
        
        # List of properties to fetch
        properties = [
            "ro.product.manufacturer", "ro.product.model", "ro.product.name",
            "ro.build.version.release", "ro.build.version.sdk", "ro.serialno",
            "ro.bootloader", "ro.build.fingerprint", "ro.build.description",
            "gsm.version.baseband", "ro.hardware", "ro.build.id"
        ]
        
        results = {}
        remaining_props = len(properties)
        
        def _after_prop_fetch(result):
            nonlocal remaining_props
            prop = result.get("command", ["", "", ""])[2] if len(result.get("command", [])) > 2 else "unknown"
            if result.get("return_code") == 0:
                stdout = result.get("stdout", "").strip()
                if stdout:
                    results[prop] = stdout
            remaining_props -= 1
            
            # If all properties have been fetched, format and display results
            if remaining_props <= 0:
                formatted_info = "\n".join([f"{prop}: {value}" for prop, value in results.items()])
                log_method(f"Device Information:{tag_suffix}", "info")
                log_method(f"{formatted_info}{tag_suffix}", "info")
                
                if callback_after_all_props:
                    callback_after_all_props({"return_code": 0, "results": results})
        
        # Fetch each property
        for prop in properties:
            self.execute_command_async(["adb", "shell", "getprop", prop], 
                                      operation_name=f"Get Property: {prop}",
                                      callback_on_finish=_after_prop_fetch)

    def set_language(self, lang):
        if lang in LABELS:
            self.lang = lang
            self.labels = get_labels(self.lang)
            self._rebuild_ui()
            log_to_file_debug_globally(f"Language changed to {lang}.")
        else:
            log_to_file_debug_globally(f"Language {lang} not supported.", "WARNING")

    def set_theme(self, theme_name):
        if theme_name in THEMES:
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
            except tk.TclError:
                pass
        
        # Save DB logger reference
        db_logger_ref = self.db_logger if hasattr(self, 'db_logger') else None
        
        # Destroy all widgets except the root window
        for widget in self.winfo_children():
            widget.destroy()
        
        self._apply_styles() 
        self._build_ui() 
        
        if hasattr(self, 'notebook') and self.notebook.winfo_exists():
            try:
                if self.notebook.tabs(): 
                    self.notebook.select(current_tab_index if current_tab_index < len(self.notebook.tabs()) else 0)
            except tk.TclError:
                pass 
        log_to_file_debug_globally("UI Rebuilt.")

    def _on_closing(self):
        log_to_file_debug_globally("Application closing attempt.")
        if messagebox.askokcancel(self.labels.get("quit_dialog_title", "Quit"), self.labels.get("quit_dialog_message", "Do you want to quit?"), parent=self):
            if hasattr(self, 'status_bar') and self.status_bar.winfo_exists():
                self.status_bar.cancel_adb_check()
            log_to_file_debug_globally("Application closed by user.")
            self.destroy()

class SamsungTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app):
        log_to_file_debug_globally("SamsungTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))
        
        button_frame = tk.Frame(self, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        button_frame.pack(pady=10, padx=10, fill=tk.X)

        col1_frame = tk.Frame(button_frame, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        col1_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N)

        ModernButton(col1_frame, text=self.labels.get("btn_get_detailed_info", "Get Detailed Info (ADB)"), 
                                   command=self.action_get_detailed_info, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_rec", "Reboot Recovery"), 
                                       command=self.action_reboot_recovery, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_dl", "Reboot Download"), 
                                       command=self.action_reboot_download, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_bl", "Reboot Bootloader"), 
                                       command=self.action_reboot_bootloader, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

        col2_frame = tk.Frame(button_frame, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        col2_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N)

        ModernButton(col2_frame, text=self.labels.get("btn_remove_frp", "Remove FRP (ADB)"), 
                                       command=self.action_remove_frp_adb, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col2_frame, text=self.labels.get("btn_factory_reset", "Factory Reset (ADB)"), 
                                       command=self.action_factory_reset_adb, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col2_frame, text=self.labels.get("btn_screenlock_reset", "Reset Screen Lock (ADB)"), 
                                       command=self.action_reset_screenlock_adb, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        log_to_file_debug_globally("SamsungTab __init__ finished.")

    def action_get_detailed_info(self):
        def _after_info_callback(result):
            log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            tag_suffix = "" if log_panel_available else "_LOG" 
            
            if result and result.get("return_code") == 0:
                log_method(f"Detailed info fetch attempt finished.{tag_suffix}", "info")
            else:
                log_method(f"Detailed info fetch attempt encountered issues.{tag_suffix}", "warning")
        self.master_app.get_detailed_adb_info(callback_after_all_props=_after_info_callback)

    def action_reboot_recovery(self):
        command = ["adb", "reboot", "recovery"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Recovery (ADB)")

    def action_reboot_download(self):
        command = ["adb", "reboot", "download"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Download Mode (ADB)")

    def action_reboot_bootloader(self):
        command = ["adb", "reboot", "bootloader"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Bootloader (ADB)")

    def action_remove_frp_adb(self):
        log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
        log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
        log_method("FRP Removal (ADB) is a complex operation. This is a placeholder for specific methods.", "warning")
        messagebox.showinfo("FRP Removal", "Generic ADB FRP removal is highly device/version specific and often requires specialized tools or commands. This button is a placeholder.", parent=self.master_app)

    def action_factory_reset_adb(self):
        if messagebox.askyesno("Confirm Factory Reset", "Are you sure you want to factory reset the device via ADB? This will erase all user data.", parent=self.master_app):
            command = ["adb", "shell", "wipe", "data"]
            self.master_app.execute_command_async(command, operation_name="Factory Reset (ADB)")
        else:
            log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Factory Reset (ADB) cancelled by user.", "info")

    def action_reset_screenlock_adb(self):
        if messagebox.askyesno("Confirm Screen Lock Reset", "Attempt to reset screen lock via ADB? This may not work on all devices/Android versions and could require root. Continue?", parent=self.master_app):
            commands_to_try = [
                (["adb", "shell", "rm", "/data/system/gesture.key"], "Remove gesture.key"),
                (["adb", "shell", "rm", "/data/system/password.key"], "Remove password.key"),
            ]
            self.master_app.execute_command_async(commands_to_try[0][0], operation_name=f"Reset Screen Lock: {commands_to_try[0][1]}")
            self.master_app.execute_command_async(commands_to_try[1][0], operation_name=f"Reset Screen Lock: {commands_to_try[1][1]}")
        else:
            log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Screen Lock Reset (ADB) cancelled by user.", "info")

class HonorTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app):
        log_to_file_debug_globally("HonorTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))

        group_honor = tk.LabelFrame(self, text=self.labels.get("group_honor", "Honor Fastboot Tools"), 
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
        frp_frame.pack(fill=tk.X, pady=(10,5))
        tk.Label(frp_frame, text=self.labels.get("honor_frp_key_label", "Honor FRP Key:"), 
                 font=FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                 fg=self.theme.get("FG", "#D1D9E0")).pack(side=tk.LEFT, padx=(0,5))
        self.honor_frp_key_var = tk.StringVar()
        honor_frp_entry = tk.Entry(frp_frame, textvariable=self.honor_frp_key_var, width=20, font=FONT,
                                   bg=self.theme.get("LOG_BG", "#2C313A"), fg=self.theme.get("FG", "#D1D9E0"),
                                   insertbackground=self.theme["FG"], relief="flat", bd=2, highlightthickness=1,
                                   highlightbackground=self.theme.get("ACCENT2", "#0095CC"), highlightcolor=self.theme.get("ACCENT", "#00AEEF"))
        honor_frp_entry.pack(side=tk.LEFT, padx=5, ipady=2)
        ModernButton(frp_frame, text=self.labels.get("btn_honor_frp", "Remove FRP (Honor Code)"), 
                                   command=self.action_honor_remove_frp, theme=self.theme, width=25, height=1).pack(side=tk.LEFT, padx=5)

        log_to_file_debug_globally("HonorTab __init__ finished.")

    def action_honor_info(self):
        command = ["fastboot", "getvar", "all"]
        self.master_app.execute_command_async(command, operation_name="Honor Get Info (Fastboot)")

    def action_honor_reboot_bootloader(self):
        command = ["fastboot", "reboot-bootloader"]
        self.master_app.execute_command_async(command, operation_name="Honor Reboot Bootloader (Fastboot)")

    def action_honor_reboot_edl(self):
        command = ["fastboot", "oem", "edl"]
        self.master_app.execute_command_async(command, operation_name="Honor Reboot EDL (Fastboot)")

    def action_honor_wipe_data_cache(self):
        if messagebox.askyesno("Confirm Wipe", "Are you sure you want to wipe data and cache on this Honor device? This will erase all user data.", parent=self.master_app):
            self.master_app.execute_command_async(["fastboot", "erase", "cache"], operation_name="Honor Wipe Cache (Fastboot)")
            self.master_app.execute_command_async(["fastboot", "erase", "userdata"], operation_name="Honor Wipe Userdata (Fastboot)")
        else:
            log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Honor Wipe Data/Cache cancelled by user.", "info")

    def action_honor_remove_frp(self):
        frp_key = self.honor_frp_key_var.get()
        if not frp_key:
            messagebox.showerror("Input Error", "Please enter the Honor FRP key.", parent=self.master_app)
            return
        # The actual command for Honor FRP removal with a key is specific and might be like `fastboot oem frp-unlock <key>` or similar.
        # This is a placeholder for the actual command structure.
        command = ["fastboot", "oem", "frp-unlock", frp_key] # Example command, might need adjustment
        self.master_app.execute_command_async(command, operation_name=f"Honor Remove FRP with Key (Fastboot)")

class XiaomiTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app):
        log_to_file_debug_globally("XiaomiTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))

        # ADB Mode Section
        group_adb = tk.LabelFrame(self, text=self.labels.get("group_xiaomi_adb", "Xiaomi ADB Mode"), 
                                  font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                  fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_adb.pack(pady=(0,10), padx=10, fill=tk.BOTH, expand=False)
        
        adb_col1 = tk.Frame(group_adb, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        adb_col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N)
        adb_col2 = tk.Frame(group_adb, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        adb_col2.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N)

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
        # Placeholders for more complex ADB features
        ModernButton(adb_col2, text=self.labels.get("btn_xiaomi_enable_diag_root", "Enable Diag (ROOT)") + " *", 
                                   command=lambda: messagebox.showinfo("Info", "Enable Diag (ROOT) is a placeholder.", parent=self.master_app), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

        # Fastboot Mode Section
        group_fastboot = tk.LabelFrame(self, text=self.labels.get("group_xiaomi_fastboot", "Xiaomi Fastboot Mode"), 
                                       font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                       fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_fastboot.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        fb_col1 = tk.Frame(group_fastboot, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        fb_col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N)
        fb_col2 = tk.Frame(group_fastboot, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        fb_col2.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N)

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
                                   command=lambda: self.master_app.execute_command_async(["fastboot", "reboot", "bootloader"], "Xiaomi Reboot Fastboot (Fastboot)"), theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
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
        if messagebox.askyesno("Confirm Unlock", "Are you sure you want to unlock the bootloader? This will erase all user data and may void warranty.", parent=self.master_app):
            self.master_app.execute_command_async(["fastboot", "oem", "unlock"], operation_name="Xiaomi Unlock Bootloader (Fastboot)")
        else:
            log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Xiaomi Unlock Bootloader cancelled by user.", "info")

    def action_xiaomi_fastboot_lock(self):
        if messagebox.askyesno("Confirm Lock", "Are you sure you want to lock the bootloader? This will erase all user data.", parent=self.master_app):
            self.master_app.execute_command_async(["fastboot", "oem", "lock"], operation_name="Xiaomi Lock Bootloader (Fastboot)")
        else:
            log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Xiaomi Lock Bootloader cancelled by user.", "info")

    def action_xiaomi_fastboot_wipe_data(self):
        if messagebox.askyesno("Confirm Wipe", "Are you sure you want to wipe all user data? This cannot be undone.", parent=self.master_app):
            self.master_app.execute_command_async(["fastboot", "erase", "userdata"], operation_name="Xiaomi Wipe Data (Fastboot)")
        else:
            log_panel_available = hasattr(self.master_app, 'log_panel') and self.master_app.log_panel is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Xiaomi Wipe Data cancelled by user.", "info")

class FileAdvancedTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app):
        log_to_file_debug_globally("FileAdvancedTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15,15))

        # File Management Section
        group_file = tk.LabelFrame(self, text=self.labels.get("group_file", "File & App Management"), 
                                   font=LABEL_FONT, bg=self.theme.get("GROUP_BG", self.theme["BG"]),
                                   fg=self.theme.get("FG", "#D1D9E0"), padx=10, pady=10, relief="groove", bd=2)
        group_file.pack(pady=(0,10), padx=10, fill=tk.BOTH, expand=False)
        
        file_col1 = tk.Frame(group_file, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        file_col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor=tk.N)
        file_col2 = tk.Frame(group_file, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        file_col2.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), anchor=tk.N)

        ModernButton(file_col1, text=self.labels.get("btn_pull_file", "Pull File from Device"), 
                                   command=self.action_pull_file, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col1, text=self.labels.get("btn_push_file", "Push File to Device"), 
                                   command=self.action_push_file, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        
        ModernButton(file_col2, text=self.labels.get("btn_install_apk", "Install APK"), 
                                   command=self.action_install_apk, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(file_col2, text=self.labels.get("btn_uninstall_app", "Uninstall App"), 
                                   command=self.action_uninstall_app, theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

        # Advanced Command Section
        group_advanced = tk.LabelFrame(self, text=self.labels.get("group_advanced_cmd", "Advanced Command Execution"), 
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
        
        ModernButton(group_advanced, text=self.labels.get("btn_run_advanced_cmd", "Run Command"), 
                                   command=self.action_run_advanced_cmd, theme=self.theme, width=20).pack(pady=5, anchor=tk.W)
        
        log_to_file_debug_globally("FileAdvancedTab __init__ finished.")

    def action_pull_file(self):
        device_path = simpledialog.askstring(self.labels.get("pull_file_title", "Pull File from Device"),
                                            self.labels.get("pull_file_device_path_msg", "Enter device source path:"),
                                            parent=self.master_app)
        if not device_path:
            return
        
        local_path = filedialog.asksaveasfilename(parent=self.master_app)
        if not local_path:
            return
        
        self.master_app.execute_command_async(["adb", "pull", device_path, local_path], 
                                             operation_name=f"Pull File: {device_path} to {local_path}")

    def action_push_file(self):
        local_path = filedialog.askopenfilename(parent=self.master_app)
        if not local_path:
            return
        
        device_path = simpledialog.askstring(self.labels.get("push_file_title", "Push File to Device"),
                                            self.labels.get("push_file_device_path_msg", "Enter device destination path:"),
                                            parent=self.master_app)
        if not device_path:
            return
        
        self.master_app.execute_command_async(["adb", "push", local_path, device_path], 
                                             operation_name=f"Push File: {local_path} to {device_path}")

    def action_install_apk(self):
        apk_path = filedialog.askopenfilename(title=self.labels.get("install_apk_title", "Select APK to Install"),
                                             filetypes=[("APK Files", "*.apk"), ("All Files", "*.*")],
                                             parent=self.master_app)
        if not apk_path:
            return
        
        self.master_app.execute_command_async(["adb", "install", "-r", apk_path], 
                                             operation_name=f"Install APK: {os.path.basename(apk_path)}")

    def action_uninstall_app(self):
        package_name = simpledialog.askstring(self.labels.get("uninstall_title", "Uninstall App"),
                                             self.labels.get("uninstall_msg", "Enter package name:"),
                                             parent=self.master_app)
        if not package_name:
            return
        
        self.master_app.execute_command_async(["adb", "uninstall", package_name], 
                                             operation_name=f"Uninstall App: {package_name}")

    def action_run_advanced_cmd(self):
        cmd_str = self.advanced_cmd_var.get().strip()
        if not cmd_str:
            return
        
        cmd_parts = cmd_str.split()
        if not cmd_parts:
            return
        
        self.master_app.execute_command_async(cmd_parts, operation_name=f"Advanced Command: {cmd_str}")

if __name__ == "__main__":
    try:
        app = UltimateDeviceTool()
        app.mainloop()
    except Exception as e:
        log_to_file_debug_globally(f"Fatal error in main: {e}", "CRITICAL")
        traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))
        try:
            import tkinter.messagebox
            tkinter.messagebox.showerror("Fatal Error", f"A critical error occurred: {e}\n\nPlease check '{_DEBUG_LOG_PATH}' for details.")
        except:
            pass
