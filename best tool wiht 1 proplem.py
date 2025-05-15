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
import queue
import traceback

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
        "quit_dialog_message": "Do you want to quit? This will erase all user data.",
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
        "adb_not_found_message": "ADB غير موجود أو لا يعمل. بعض الميزات لن تكون متوفرة. يرجى تثبيت ADB وإضافته إلى متغير PATH في النظام.",
        "fastboot_not_found_message": "Fastboot غير موجود أو لا يعمل. بعض الميزات لن تكون متوفرة. يرجى تثبيت Fastboot وإضافته إلى متغير PATH في النظام.",
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
        "BTN_BG": "#03A9F4", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#0277BD",
        "GROUP_BG": "#FFFFFF", "LOG_BG": "#CFD8DC",
        "LOG_FG_SUCCESS": "#4CAF50", "LOG_FG_INFO": "#2196F3", "LOG_FG_ERROR": "#F44336",
        "LOG_FG_FAIL": "#D32F2F", "LOG_FG_CMD": "#00796B", "LOG_FG_WARNING": "#FF9800",
        "STATUS_BAR_BG": "#B0BEC5", "STATUS_BAR_FG": "#263238",
        "NOTEBOOK_TAB_BG": "#B0BEC5", "NOTEBOOK_TAB_FG": "#37474F",
        "NOTEBOOK_TAB_SELECTED_BG": "#03A9F4", "NOTEBOOK_TAB_SELECTED_FG": "#FFFFFF",
        "NOTEBOOK_TAB_ACTIVE_BG": "#0288D1"
    },
    "dark": {  # Original Dark Theme
        "BG": "#263238", "FG": "#ECEFF1", "ACCENT": "#03A9F4", "ACCENT2": "#0288D1",
        "BTN_BG": "#03A9F4", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#03A9F4",
        "GROUP_BG": "#37474F", "LOG_BG": "#455A64",
        "LOG_FG_SUCCESS": "#81C784", "LOG_FG_INFO": "#64B5F6", "LOG_FG_ERROR": "#E57373",
        "LOG_FG_FAIL": "#EF5350", "LOG_FG_CMD": "#4DB6AC", "LOG_FG_WARNING": "#FFB74D",
        "STATUS_BAR_BG": "#212121", "STATUS_BAR_FG": "#03A9F4",
        "NOTEBOOK_TAB_BG": "#37474F", "NOTEBOOK_TAB_FG": "#B0BEC5",
        "NOTEBOOK_TAB_SELECTED_BG": "#03A9F4", "NOTEBOOK_TAB_SELECTED_FG": "#FFFFFF",
        "NOTEBOOK_TAB_ACTIVE_BG": "#0288D1"
    },
    "professional_dark": {  # New Professional Dark Theme
        "BG": "#21252B", "FG": "#D1D9E0", "ACCENT": "#00AEEF", "ACCENT2": "#0095CC",  # Vibrant Blue
        "BTN_BG": "#00AEEF", "BTN_FG": "#FFFFFF", "BTN_BORDER": "#00AEEF",
        "GROUP_BG": "#2C313A", "LOG_BG": "#2C313A",  # Slightly lighter than main BG for contrast
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
TITLE_FONT = ("Segoe UI Semibold", 18)  # Increased size
LABEL_FONT = ("Segoe UI", 9, "bold")
BTN_FONT = ("Segoe UI", 10, "bold")
LOG_FONT = ("Consolas", 11)
log_to_file_debug_globally("FONTS defined.")


def get_labels(lang):
    return LABELS.get(lang, LABELS["en"])


def get_theme(theme_name):
    return THEMES.get(theme_name, THEMES["professional_dark"])  # Default to new theme


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
                    log_to_file_debug_globally(f"DBLogger: Failed to create DB at user path {dbfile_fallback}: {e_db_path2}", "ERROR")
                    dbfile = "operation_log.db"
                    log_to_file_debug_globally(f"DBLogger: Using local DB file (last resort): {dbfile}", "WARNING")
        self.dbfile = dbfile
        self.lock = threading.Lock()
        self._init()
        self.tk_root = tk_root
        log_to_file_debug_globally("DBLogger __init__ finished.")

    def _init(self):
        with self.lock:
            try:
                with sqlite3.connect(self.dbfile) as conn:
                    conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, tag TEXT, msg TEXT)")
                    conn.commit()
            except Exception as e:
                log_to_file_debug_globally(f"DBLogger: Failed to initialize database table: {e}", "CRITICAL")

    def add(self, msg, tag="info"):
        def _add_threaded():
            with self.lock:
                try:
                    with sqlite3.connect(self.dbfile) as conn:
                        conn.execute("INSERT INTO logs (ts, tag, msg) VALUES (?, ?, ?)",
                                     (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tag, msg))
                        conn.commit()
                except Exception as e:
                    log_to_file_debug_globally(f"DBLogger Error (add): {e}", "ERROR")

        if self.tk_root and threading.current_thread() is not threading.main_thread():
            self.tk_root.after(0, _add_threaded)
        else:
            _add_threaded()

    def search(self, term="", tag=None):
        with self.lock:
            try:
                with sqlite3.connect(self.dbfile) as conn:
                    q = "SELECT ts, tag, msg FROM logs WHERE msg LIKE ?"
                    params = [f"%{term}%"]
                    if tag:
                        q += " AND tag=?"
                        params.append(tag)
                    return conn.execute(q, params).fetchall()
            except Exception as e:
                log_to_file_debug_globally(f"DBLogger Error (search): {e}", "ERROR")
                return []

    def all(self, limit=100):
        with self.lock:
            try:
                with sqlite3.connect(self.dbfile) as conn:
                    return conn.execute(
                        "SELECT ts, tag, msg FROM logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
            except Exception as e:
                log_to_file_debug_globally(f"DBLogger Error (all): {e}", "ERROR")
                return []


class ProgressbarManager(tk.Frame):
    def __init__(self, master, theme):
        super().__init__(master, bg=theme["BG"])
        self.var = tk.IntVar(value=0)
        self.pb = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=220, mode='indeterminate', variable=self.var)
        self.pb.pack(fill=tk.X, padx=6, pady=(8, 12))
        self.pb["maximum"] = 100
        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            log_to_file_debug_globally("Clam theme not available for progress bar.", "WARNING")
        progress_bar_color = theme.get("ACCENT", "#00AEEF")
        self.style.configure("Custom.Horizontal.TProgressbar",
                             troughcolor=theme.get("GROUP_BG", theme["BG"]),
                             bordercolor=theme.get("ACCENT2", theme["ACCENT"]),
                             background=progress_bar_color,
                             lightcolor=progress_bar_color,
                             darkcolor=progress_bar_color,
                             thickness=10)
        self.pb.configure(style="Custom.Horizontal.TProgressbar")
        self.running = False

    def start(self):
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
        log_title_frame.pack(fill=tk.X, padx=6, pady=(8, 2))
        tk.Label(log_title_frame, text=labels["log"], font=LABEL_FONT, bg=theme["BG"],
                 fg=theme.get("FG", "#D1D9E0")).pack(side=tk.LEFT)

        self.text = tk.Text(self, height=25, font=LOG_FONT, state=tk.DISABLED,
                            bg=theme["LOG_BG"], fg=theme["LOG_FG_INFO"],
                            bd=1, relief="sunken", wrap=tk.WORD,
                            selectbackground=theme["ACCENT"], selectforeground=theme["BTN_FG"],
                            insertbackground=theme["FG"])
        self.text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        for tag_name, color_key in [("info", "LOG_FG_INFO"), ("success", "LOG_FG_SUCCESS"),
                                   ("error", "LOG_FG_ERROR"), ("fail", "LOG_FG_FAIL"),
                                   ("cmd", "LOG_FG_CMD"), ("warning", "LOG_FG_WARNING")]:
            font_config = (LOG_FONT[0], LOG_FONT[1], "bold") if tag_name in ["success", "error", "fail"] else LOG_FONT
            if tag_name == "fail":
                font_config = (*font_config, "underline")
            self.text.tag_configure(tag_name, foreground=theme[color_key], font=font_config)

        self.db_logger = db_logger
        self.progress_bar = ProgressbarManager(self, theme)
        self.progress_bar.pack(fill=tk.X, padx=6)

        search_frame = tk.Frame(self, bg=theme["BG"])
        search_frame.pack(fill=tk.X, padx=6, pady=(6, 10))

        tk.Label(search_frame, text=labels.get("search_log_label", "بحث في السجل:"), bg=theme["BG"],
                 fg=theme["FG"], font=FONT).pack(side=tk.LEFT, padx=(0, 4))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25, font=FONT,
                              bg=theme.get("GROUP_BG", "#2C313A"), fg=theme.get("FG", "#D1D9E0"),
                              insertbackground=theme["FG"], relief="flat", bd=2, highlightthickness=1,
                              highlightbackground=theme.get("ACCENT2", "#0095CC"),
                              highlightcolor=theme.get("ACCENT", "#00AEEF"))
        search_entry.pack(side=tk.LEFT, padx=4, ipady=2)

        ModernButton(search_frame, labels.get("find_button", "بحث"), self.show_search, theme, width=8, height=1,
                     icon="").pack(side=tk.LEFT, padx=(2, 2))
        ModernButton(search_frame, labels.get("all_button", "الكل"), self.show_all, theme, width=8, height=1,
                     icon="").pack(side=tk.LEFT, padx=(0, 2))
        ModernButton(search_frame, labels.get("export_button", "تصدير"), self.save_to_file, theme, width=10, height=1,
                     icon="").pack(side=tk.RIGHT, padx=(4, 0))

        if self.db_logger:
            self.show_all()

    def log(self, message, tag="info"):
        if not self.winfo_exists():
            return

        def __log_to_widget():
            if not self.text.winfo_exists():
                return
            self.text.config(state=tk.NORMAL)
            timestamp = f"[{datetime.now().strftime('%H:%M:%S')}]: "
            prefix_map = {"cmd": "[CMD]", "success": "[SUCCESS]", "error": "[ERROR]", "fail": "[FAIL]",
                          "warning": "[WARNING]", "info": "[INFO]"}
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
        prefix_map = {"cmd": "[CMD]", "success": "[SUCCESS]", "error": "[ERROR]", "fail": "[FAIL]",
                      "warning": "[WARNING]", "info": "[INFO]"}
        for ts, tag, msg in reversed(entries):
            log_line = f"{ts} {prefix_map.get(tag, '[LOG]')} {msg}\n"
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
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text', '.txt')],
                                               parent=self.tk_root)
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
        self.set_status(labels["adb_status_not_connected"], theme.get("LOG_FG_ERROR", "#F44336"))
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
                out = subprocess.check_output(["adb", "get-state"], stderr=subprocess.STDOUT, text=True, timeout=2,
                                            creationflags=flags)
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

        # Initialize command queue and start processing thread
        self.command_queue = queue.Queue()
        self.command_queue_processing_active = True
        self._command_thread_id = None
        self.after(100, self._process_command_queue)

        log_to_file_debug_globally("UltimateDeviceTool __init__ finished successfully.")

    def _apply_styles(self):
        log_to_file_debug_globally("Applying styles...")
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            log_to_file_debug_globally("Clam theme not available.", "WARNING")
            # تعديلات على style configure
            self.style.configure("TNotebook", background=self.theme["BG"], borderwidth=0, tabmargins=[2, 5, 2, 0])
            self.style.configure("TNotebook.Tab",
                                 background=self.theme.get("NOTEBOOK_TAB_BG", self.theme["GROUP_BG"]),
                                 foreground=self.theme.get("NOTEBOOK_TAB_FG", self.theme["FG"]),
                                 padding=[10, 5], font=("Segoe UI", 10, "bold"), borderwidth=6)
            self.style.map("TNotebook.Tab",
                           background=[("selected", self.theme.get("NOTEBOOK_TAB_SELECTED_BG", self.theme["ACCENT"])),
                                       ("active", self.theme.get("NOTEBOOK_TAB_ACTIVE_BG", self.theme["ACCENT2"]))],
                           foreground=[("selected", self.theme.get("NOTEBOOK_TAB_SELECTED_FG", self.theme["BTN_FG"]))])
            self.style.configure("TPanedWindow", background=self.theme["BG"])
        log_to_file_debug_globally("Styles applied.")

    def _build_ui(self):
        log_to_file_debug_globally("Building UI...")
        self.config(bg=self.theme["BG"])
        menubar = tk.Menu(self, bg=self.theme["BG"], fg=self.theme["FG"], relief=tk.FLAT, bd=0,
                          activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT,
                            activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
        theme_menu.add_command(label=self.labels["light"], command=lambda: self.set_theme("light"))
        theme_menu.add_command(label=self.labels["dark"], command=lambda: self.set_theme("dark"))
        theme_menu.add_command(label=self.labels["professional_dark"],
                              command=lambda: self.set_theme("professional_dark"))
        menubar.add_cascade(label=self.labels["theme"], menu=theme_menu)
        lang_menu = tk.Menu(menubar, tearoff=0, bg=self.theme["GROUP_BG"], fg=self.theme["FG"], relief=tk.FLAT,
                           activebackground=self.theme["ACCENT"], activeforeground=self.theme["BTN_FG"])
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
        title_frame.pack(fill=tk.X, pady=(15, 8), padx=(15, 0))
        tk.Label(title_frame, text=self.labels["title"], font=TITLE_FONT, bg=self.theme["BG"],
                 fg=self.theme.get("TITLE_FG", self.theme["ACCENT"])).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(title_frame, text=self.labels["edition"], font=LABEL_FONT, bg=self.theme["BG"],
                 fg=self.theme.get("EDITION_FG", self.theme["FG"])).pack(side=tk.LEFT, pady=(6, 0))

        self.notebook = ttk.Notebook(left_area_container, style="TNotebook")
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=15, pady=(0, 15))

        try:
            self.log_panel = LogPanel(right_area_container, self.theme, self.labels, db_logger=self.db_logger, tk_root=self)
            self.log_panel.pack(fill=tk.BOTH, expand=True, padx=(5, 15), pady=(15, 15))
            log_to_file_debug_globally("Log panel created.")
        except Exception as e_log_panel:
            log_to_file_debug_globally(f"Error creating LogPanel: {e_log_panel}", "CRITICAL")
            traceback.print_exc(file=open(_DEBUG_LOG_PATH, "a"))

        # Add Tabs
        self.notebook.add(SamsungTab(self.notebook, self), text=self.labels["tab_samsung"], padding=10)
        self.notebook.add(HonorTab(self.notebook, self), text=self.labels["tab_honor"], padding=10)
        self.notebook.add(XiaomiTab(self.notebook, self), text=self.labels["tab_xiaomi"], padding=10)
        self.notebook.add(FileAdvancedTab(self.notebook, self), text=self.labels["tab_file_advanced"], padding=10)

        log_to_file_debug_globally("UI Building finished.")

    def execute_command_async(self, command_list, operation_name="Operation", callback_on_finish=None):
        log_panel_available = hasattr(self, "_log_panel") and getattr(self, "_log_panel", None) is not None
        if log_panel_available:
            self.log_panel.progress_bar.start()
        else:
            log_to_file_debug_globally(f"LogPanel not available for command: {operation_name}", "WARNING")

        # Put command in queue
        self.command_queue.put({
            "command": command_list,
            "operation_name": operation_name,
            "callback": callback_on_finish
        })

    def _command_thread(self):
        while self.command_queue_processing_active:
            try:
                result = self.command_queue.get(timeout=1)
                command_list = result["command"]
                operation_name = result["operation_name"]

                process = subprocess.Popen(
                    command_list,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                stdout, stderr = process.communicate(timeout=120)
                return_code = process.returncode

                result_data = {
                    "stdout": stdout,
                    "stderr": stderr,
                    "return_code": return_code,
                    "operation_name": operation_name,
                    "command": command_list
                }

                if result.get("callback"):
                    if self.tk_root and threading.current_thread() is not threading.main_thread():
                        self.tk_root.after(0, lambda r=result_data: result["callback"](r))
                    else:
                        result["callback"](result_data)
            except queue.Empty:
                continue
            except subprocess.TimeoutExpired:
                self.command_queue.put({
                    "error": "TimeoutExpired",
                    "operation_name": operation_name,
                    "command": command_list,
                    "callback": callback_on_finish
                })
            except Exception as e:
                self.command_queue.put({
                    "error": str(e),
                    "operation_name": operation_name,
                    "command": command_list,
                    "callback": callback_on_finish
                })

    def _process_command_queue(self):
        log_to_file_debug_globally("Processing command queue...")
        try:
            while True:
                try:
                    result = self.command_queue.get_nowait()
                    log_panel_available = hasattr(self, "_log_panel") and getattr(self, "_log_panel", None) is not None

                    if log_panel_available:
                        self.log_panel.progress_bar.stop()
                    operation_name = result.get("operation_name", "Unknown Operation")
                    command_executed = result.get("command", ["N/A"])
                    log_msg_prefix = f"Operation: {operation_name} (Command: {' '.join(command_executed)})"

                    if log_panel_available:
                        self.log_panel.log(log_msg_prefix, "cmd")
                    else:
                        log_to_file_debug_globally(log_msg_prefix, "CMD_LOG")

                    if "error" in result:
                        error_type = result["error"]
                        error_reason = ""
                        if error_type == "TimeoutExpired":
                            error_reason = "Operation timed out after 120 seconds."
                        elif error_type == "FileNotFound":
                            error_reason = f"Command '{result.get('command_name', command_executed[0])}' not found. Ensure it's installed and in system PATH."
                        else:
                            error_reason = str(error_type)

                        if log_panel_available:
                            self.log_panel.log(f"Status: FAILED", "fail")
                            self.log_panel.log(f"Reason: {error_reason}", "error")
                        else:
                            log_to_file_debug_globally(f"Status: FAILED for {operation_name}", "FAIL_LOG")
                            log_to_file_debug_globally(f"Reason: {error_reason} for {operation_name}", "ERROR_LOG")
                    else:
                        stdout = result.get("stdout", "").strip()
                        stderr = result.get("stderr", "").strip()
                        if log_panel_available:
                            if stdout:
                                self.log_panel.log(stdout, "stdout")
                            if stderr:
                                self.log_panel.log(stderr, "stderr")
                        else:
                            if stdout:
                                log_to_file_debug_globally(stdout, "STDOUT")
                            if stderr:
                                log_to_file_debug_globally(stderr, "STDERR")
                except queue.Empty:
                    break
        except Exception as e_process:
            log_to_file_debug_globally(f"Error in _process_command_queue: {e_process}", "ERROR")
        finally:
            self._command_thread_id = self.after(100, self._process_command_queue)

    def get_detailed_adb_info(self, callback_after_all_props=None):
        log_panel_available = hasattr(self, "_log_panel") and getattr(self, "_log_panel", None) is not None
        if log_panel_available:
            self.log_panel.log("Initiating: Get Detailed Device Info (ADB)", "info")
        else:
            log_to_file_debug_globally("Initiating: Get Detailed Device Info (ADB)", "INFO_LOG")

        props_to_get = {"Model": "ro.product.model"}
        first_key = list(props_to_get.keys())[0]
        first_prop_name = props_to_get[first_key]
        command = ["adb", "shell", "getprop", first_prop_name]

        def _single_prop_callback(result):
            if callback_after_all_props:
                callback_after_all_props(result)

        self.execute_command_async(command, operation_name=f"Get {first_key}", callback_on_finish=_single_prop_callback)

    def set_language(self, lang):
        if self.lang == lang:
            return
        self.lang = lang
        self.labels = get_labels(self.lang)
        self.title(self.labels["title"])
        self.rebuild_ui()

    def set_theme(self, theme_mode):
        if self.theme_mode == theme_mode:
            return
        self.theme_mode = theme_mode
        self.theme = get_theme(self.theme_mode)
        self._apply_styles()
        self.rebuild_ui()

    def rebuild_ui(self):
        log_to_file_debug_globally("Rebuilding UI...")
        current_tab_index = 0
        try:
            current_tab_index = self.notebook.index(self.notebook.select())
        except tk.TclError:
            current_tab_index = 0

        for widget in self.winfo_children():
            widget.destroy()

        self._apply_styles()
        self._build_ui()

        # Restore tab selection if possible
        if hasattr(self, "_notebook") and self.notebook.winfo_exists():
            try:
                if self.notebook.tabs() and current_tab_index < len(self.notebook.tabs()):
                    self.notebook.select(current_tab_index)
            except tk.TclError:
                pass

        log_to_file_debug_globally("UI Rebuilt.")

    def _on_closing(self):
        log_to_file_debug_globally("Application closing attempt.")
        if messagebox.askokcancel(
            self.labels.get("quit_dialog_title", "Quit"),
            self.labels.get("quit_dialog_message", "Do you want to quit?"),
            parent=self
        ):
            if hasattr(self, "_status_bar") and self.status_bar.winfo_exists():
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
        self.configure(padding=(15, 15))

        button_frame = tk.Frame(self, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        button_frame.pack(pady=10, padx=10, fill=tk.X)

        col1_frame = tk.Frame(button_frame, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        col1_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), anchor=tk.N)

        ModernButton(col1_frame, text=self.labels.get("btn_get_detailed_info", "Get Detailed Info (ADB)"),
                     command=self.action_get_detailed_info,
                     theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_rec", "Reboot Recovery"),
                     command=self.action_reboot_recovery,
                     theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_dl", "Reboot Download"),
                     command=self.action_reboot_download,
                     theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col1_frame, text=self.labels.get("btn_reboot_bl", "Reboot Bootloader"),
                     command=self.action_reboot_bootloader,
                     theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

        col2_frame = tk.Frame(button_frame, bg=self.theme.get("GROUP_BG", self.theme["BG"]))
        col2_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), anchor=tk.N)

        ModernButton(col2_frame, text=self.labels.get("btn_remove_fr", "Remove FRP (ADB)"),
                     command=self.action_remove_fr_adb,
                     theme=self.theme, width=30).pack(pady=5, anchor=tk.W)
        ModernButton(col2_frame, text=self.labels.get("btn_factory_reset", "Factory Reset (ADB)"),
                     command=self.action_factory_reset_adb,
                     theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

        ModernButton(col2_frame, text=self.labels.get("btn_screenlock_reset", "Reset Screen Lock (ADB)"),
                     command=self.action_reset_screenlock_adb,
                     theme=self.theme, width=30).pack(pady=5, anchor=tk.W)

        log_to_file_debug_globally("SamsungTab __init__ finished.")

    def action_get_detailed_info(self):
        def after_info_callback(result):
            log_method = self.master_app.log_panel.log if hasattr(self.master_app, "log_panel") else log_to_file_debug_globally
            if result and result.get("return_code") == 0:
                log_method("Detailed info fetch attempt finished.", "success")
            else:
                log_method("Detailed info fetch attempt encountered issues.", "warning")

        self.master_app.get_detailed_adb_info(callback_after_all_props=after_info_callback)

    def action_reboot_recovery(self):
        command = ["adb", "reboot", "recovery"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Recovery (ADB)")

    def action_reboot_download(self):
        command = ["adb", "reboot", "download"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Download Mode (ADB)")

    def action_reboot_bootloader(self):
        command = ["adb", "reboot", "bootloader"]
        self.master_app.execute_command_async(command, operation_name="Reboot to Bootloader (ADB)")

    def action_remove_fr(self):
        log_panel_available = hasattr(self.master_app, "_log_panel") and getattr(self.master_app, "_log_panel", None) is not None
        log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
        log_method("FRP Removal (ADB) is a complex operation. This is a placeholder for specific methods.", "warning")
        messagebox.showinfo("FRP Removal", "Generic ADB FRP removal is highly device/version specific and often requires specialized tools or commands. This button is a placeholder.", parent=self.master_app)

    def action_factory_reset(self):
        if messagebox.askyesno("Confirm Factory Reset", "Are you sure you want to factory reset the device via ADB? This will erase all user data.", parent=self.master_app):
            command = ["adb", "shell", "wipe", "data"]
            self.master_app.execute_command_async(command, operation_name="Factory Reset (ADB)")
        else:
            log_panel_available = hasattr(self.master_app, "_log_panel") and getattr(self.master_app, "_log_panel", None) is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Factory Reset (ADB) cancelled by user.", "info")

    def action_reset_screenlock(self):
        if messagebox.askyesno("Confirm Screen Lock Reset", "Attempt to reset screen lock via ADB? This may not work on all devices/Android versions and could require root. Continue?", parent=self.master_app):
            commands_to_try = [
                (["adb", "shell", "rm", "/data/system/gesture.key"], "Remove gesture.key"),
                (["adb", "shell", "rm", "/data/system/password.key"], "Remove password.key"),
            ]
            self.master_app.execute_command_async(commands_to_try[0][0], operation_name=f"Reset Screen Lock: {commands_to_try[0][1]}")
            self.master_app.execute_command_async(commands_to_try[1][0], operation_name=f"Reset Screen Lock: {commands_to_try[1][1]}")
        else:
            log_panel_available = hasattr(self.master_app, "_log_panel") and getattr(self.master_app, "_log_panel", None) is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Screen Lock Reset (ADB) cancelled by user.", "info")


class HonorTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app):
        log_to_file_debug_globally("HonorTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15, 15))

        group_honor = tk.LabelFrame(self, text=self.labels.get("group_honor", "Honor Fastboot Tools"),
                              font=("Segoe UI", 10, "bold"), bg=self.theme["GROUP_BG"],
                              fg=self.theme["FG"])
        group_honor.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ModernButton(group_honor, self.labels.get("btn_honor_info", "Read Serial & Software Info"),
                     self.action_honor_info, self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_honor, self.labels.get("btn_honor_reboot_bl", "Reboot Bootloader (Honor)"),
                     self.action_honor_reboot_bootloader, self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_honor, self.labels.get("btn_honor_reboot_edl", "Reboot EDL (Honor)"),
                     self.action_honor_reboot_edl, self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_honor, self.labels.get("btn_honor_wipe_data_cache", "Wipe Data/Cache (Honor)"),
                     self.action_honor_wipe_data_cache, self.theme, width=35).pack(pady=5, anchor=tk.W)

        frp_frame = tk.Frame(group_honor, bg=self.theme["GROUP_BG"])
        frp_frame.pack(fill=tk.X, pady=(10, 5))
        tk.Label(frp_frame, text=self.labels.get("honor_frp_key_label", "Honor FRP Key:"),
                 bg=self.theme["GROUP_BG"], fg=self.theme["FG"]).pack(side=tk.LEFT, padx=(0, 5))
        self.honor_frp_key_var = tk.StringVar()
        tk.Entry(frp_frame, textvariable=self.honor_frp_key_var, width=20, font=("Segoe UI", 10),
                  bg=self.theme["LOG_BG"], fg=self.theme["FG"],
                  insertbackground=self.theme["FG"], relief="flat", bd=2, highlightthickness=1,
                  highlightbackground=self.theme.get("ACCENT2", "#0095CC"),
                  highlightcolor=self.theme.get("ACCENT", "#00AEEF")).pack(side=tk.LEFT, padx=5, ipady=2)

        ModernButton(frp_frame, self.labels.get("btn_honor_frp", "Remove FRP (Honor Code)"),
                     self.action_honor_remove_frp, self.theme, width=25, height=1,
                     icon="").pack(side=tk.LEFT, padx=5)

        log_to_file_debug_globally("HonorTab __init__ finished.")

    def action_honor_info(self):
        command = ["fastboot", "getvar", "all"]
        self.master_app.execute_command_async(command, operation_name="Read Honor Device Info (Fastboot)")

    def action_honor_reboot_bootloader(self):
        command = ["fastboot", "reboot-bootloader"]
        self.master_app.execute_command_async(command, operation_name="Reboot Honor Bootloader (Fastboot)")

    def action_honor_reboot_edl(self):
        command = ["fastboot", "oem", "edl"]
        self.master_app.execute_command_async(command, operation_name="Reboot Honor to EDL (Fastboot)")

    def action_honor_wipe_data_cache(self):
        if messagebox.askyesno("Confirm Wipe", "Are you sure you want to wipe data and cache on this Honor device? This will erase all user data.", parent=self.master_app):
            self.master_app.execute_command_async(["fastboot", "erase", "cache"], operation_name="Honor Wipe Cache (Fastboot)")
            self.master_app.execute_command_async(["fastboot", "erase", "userdata"], operation_name="Honor Wipe Userdata (Fastboot)")
        else:
            log_panel_available = hasattr(self.master_app, "_log_panel") and getattr(self.master_app, "_log_panel", None) is not None
            log_method = self.master_app.log_panel.log if log_panel_available else log_to_file_debug_globally
            log_method("Honor Wipe Data/Cache cancelled by user.", "info")

    def action_honor_remove_frp(self):
        frp_key = self.honor_frp_key_var.get()
        if not frp_key:
            messagebox.showerror("Input Error", self.labels.get("honor_frp_code_title", "Enter Honor FRP Key"),
                               parent=self.master_app)
            return

        # The actual command for Honor FRP removal with a key is device-specific and might be like `fastboot oem frp-unlock <key>` or similar.
        # This is a placeholder for the actual command structure.
        command = ["fastboot", "oem", "frp-unlock", frp_key]  # Example command, might need adjustment
        self.master_app.execute_command_async(command, operation_name=f"Honor Remove FRP with Key (Fastboot)")


class XiaomiTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app):
        log_to_file_debug_globally("XiaomiTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15, 15))

        # ADB Mode Section
        group_adb = tk.LabelFrame(self, text=self.labels["group_xiaomi_adb"],
                                font=("Segoe UI", 10, "bold"), bg=self.theme["GROUP_BG"],
                                fg=self.theme["FG"])
        group_adb.pack(padx=10, pady=10, fill=tk.BOTH)

        ModernButton(group_adb, self.labels.get("btn_xiaomi_adb_info", "Read Info (ADB)"),
                     self.action_xiaomi_adb_info,
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_adb, "Reboot Recovery (ADB)",
                     lambda: self.master_app.execute_command_async(["adb", "reboot", "recovery"],
                                                                 operation_name="Xiaomi Reboot Recovery (ADB)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_adb, "Reboot Download (ADB)",
                     lambda: self.master_app.execute_command_async(["adb", "reboot", "download"],
                                                                 operation_name="Xiaomi Reboot Download Mode (ADB)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_adb, "Reboot EDL (ADB)",
                     lambda: self.master_app.execute_command_async(["adb", "reboot", "edl"],
                                                                 operation_name="Xiaomi Reboot EDL (ADB)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)

        # Placeholders for more complex ADB features
        ModernButton(group_adb, self.labels.get("btn_xiaomi_enable_diag_root", "Enable Diag (ROOT)") + " *",
                     lambda: messagebox.showinfo("Info", "Enable Diag (ROOT) is a placeholder.", parent=self.master_app),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)

        # Fastboot Mode Section
        group_fastboot = tk.LabelFrame(self, text=self.labels["group_xiaomi_fastboot"],
                                     font=("Segoe UI", 10, "bold"), bg=self.theme["GROUP_BG"],
                                     fg=self.theme["FG"])
        group_fastboot.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ModernButton(group_fastboot, "Read Info (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "getvar", "all"],
                                                                 operation_name="Read Xiaomi Info (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_fastboot, "Read Security (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "oem", "read-security"],
                                                                 operation_name="Read Xiaomi Security (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_fastboot, "Unlock Bootloader (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "flashing", "unlock"],
                                                                 operation_name="Unlock Xiaomi Bootloader (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_fastboot, "Lock Bootloader (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "flashing", "lock"],
                                                                 operation_name="Lock Xiaomi Bootloader (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_fastboot, "Reboot System (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "reboot"],
                                                                 operation_name="Reboot Xiaomi to System (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_fastboot, "Reboot Fastboot (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "reboot-fastboot"],
                                                                 operation_name="Reboot Xiaomi to Fastboot (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_fastboot, "Reboot EDL (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "oem", "edl"],
                                                                 operation_name="Reboot Xiaomi to EDL (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)

        ModernButton(group_fastboot, "Wipe Cache (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "erase", "cache"],
                                                                 operation_name="Wipe Xiaomi Cache (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_fastboot, "Wipe Data (Fastboot)",
                     lambda: self.master_app.execute_command_async(["fastboot", "erase", "userdata"],
                                                                 operation_name="Wipe Xiaomi Userdata (Fastboot)"),
                     self.theme, width=35).pack(pady=5, anchor=tk.W)

        log_to_file_debug_globally("XiaomiTab __init__ finished.")

    def action_xiaomi_adb_info(self):
        self.master_app.get_detailed_adb_info()  # Uses the generic detailed info method


class FileAdvancedTab(ttk.Frame):
    def __init__(self, parent_notebook, master_app):
        log_to_file_debug_globally("FileAdvancedTab __init__ started.")
        super().__init__(parent_notebook, style="TFrame")
        self.master_app = master_app
        self.labels = master_app.labels
        self.theme = master_app.theme
        self.configure(padding=(15, 15))

        # File Management Section
        group_file = tk.LabelFrame(self, text=self.labels["group_file"],
                                font=("Segoe UI", 10, "bold"), bg=self.theme["GROUP_BG"],
                                fg=self.theme["FG"])
        group_file.pack(padx=10, pady=10, fill=tk.BOTH)

        ModernButton(group_file, self.labels.get("btn_pull_file", "Pull File from Device"),
                     self.action_pull_file,
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_file, self.labels.get("btn_push_file", "Push File to Device"),
                     self.action_push_file,
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_file, self.labels.get("btn_install_apk", "Install APK"),
                     self.action_install_apk,
                     self.theme, width=35).pack(pady=5, anchor=tk.W)
        ModernButton(group_file, self.labels.get("btn_uninstall_app", "Uninstall App"),
                     self.action_uninstall_app,
                     self.theme, width=35).pack(pady=5, anchor=tk.W)

        # Advanced Command Section
        group_adv = tk.LabelFrame(self, text=self.labels["group_advanced_cmd"],
                                 font=("Segoe UI", 10, "bold"), bg=self.theme["GROUP_BG"],
                                 fg=self.theme["FG"])
        group_adv.pack(padx=10, pady=10, fill=tk.BOTH)

        tk.Label(group_adv, text=self.labels["advanced_cmd_label"],
                 bg=self.theme["GROUP_BG"], fg=self.theme["FG"], font=FONT).pack(anchor=tk.W)
        self.adv_cmd_var = tk.StringVar()
        tk.Entry(group_adv, textvariable=self.adv_cmd_var, width=60, font=("Segoe UI", 10),
                  bg=self.theme["LOG_BG"], fg=self.theme["FG"],
                  insertbackground=self.theme["FG"], relief="flat", bd=2, highlightthickness=1,
                  highlightbackground=self.theme.get("ACCENT2", "#0095CC"),
                  highlightcolor=self.theme.get("ACCENT", "#00AEEF")).pack(pady=5)

        ModernButton(group_adv, self.labels.get("btn_run_advanced_cmd", "Run Command"),
                     self.action_run_advanced_cmd, self.theme, width=25, height=1,
                     icon="").pack(pady=5)

        log_to_file_debug_globally("FileAdvancedTab __init__ finished.")

    def action_pull_file(self):
        device_path = simpledialog.askstring(self.labels["pull_file_title"],
                                           self.labels["pull_file_device_path_msg"],
                                           parent=self.master_app)
        if not device_path:
            return

        local_path = filedialog.asksaveasfilename(parent=self.master_app)
        if not local_path:
            return

        self.master_app.execute_command_async(["adb", "pull", device_path, local_path],
                                          operation_name=f"Pull File: {os.path.basename(local_path)}")

    def action_push_file(self):
        local_path = filedialog.askopenfilename(parent=self.master_app)
        if not local_path:
            return

        device_path = simpledialog.askstring(self.labels["push_file_title"],
                                           self.labels["push_file_device_path_msg"],
                                           parent=self.master_app)
        if not device_path:
            return

        self.master_app.execute_command_async(["adb", "push", local_path, device_path],
                                          operation_name=f"Push File: {os.path.basename(local_path)}")

    def action_install_apk(self):
        apk_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")], parent=self.master_app)
        if not apk_path:
            return

        self.master_app.execute_command_async(["adb", "install", "-r", apk_path],
                                          operation_name=f"Install APK: {os.path.basename(apk_path)}")

    def action_uninstall_app(self):
        package_name = simpledialog.askstring(self.labels["uninstall_title"],
                                            self.labels["uninstall_msg"], parent=self.master_app)
        if not package_name:
            return

        self.master_app.execute_command_async(["adb", "uninstall", package_name],
                                          operation_name=f"Uninstall App: {package_name}")

    def action_run_advanced_cmd(self):
        cmd_string = self.adv_cmd_var.get().strip()
        if not cmd_string:
            messagebox.showwarning("Input Required", self.labels["advanced_cmd_label"],
                                  parent=self.master_app)
            return

        self.master_app.execute_command_async(cmd_string.split(), operation_name=f"Advanced Command: {cmd_string[:30]}...")


if __name__ == "__main__":
    log_to_file_debug_globally("Application __main__ started.")
    try:
        temp_root_for_warnings = tk.Tk()
        temp_root_for_warnings.withdraw()
        current_labels_for_warnings = get_labels("en")

        try:
            subprocess.run(["adb", "version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            log_to_file_debug_globally("ADB check successful.")
        except Exception as e_adb:
            log_to_file_debug_globally(f"ADB check failed: {e_adb}", "ERROR")
            messagebox.showwarning(
                current_labels_for_warnings.get("dependency_check_title"),
                current_labels_for_warnings.get("adb_not_found_message"),
                parent=temp_root_for_warnings
            )

        try:
            subprocess.run(["fastboot", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            log_to_file_debug_globally("Fastboot check successful.")
        except Exception as e_fastboot:
            log_to_file_debug_globally(f"Fastboot check failed: {e_fastboot}", "ERROR")
            messagebox.showwarning(
                current_labels_for_warnings.get("dependency_check_title"),
                current_labels_for_warnings.get("fastboot_not_found_message"),
                parent=temp_root_for_warnings
            )

        temp_root_for_warnings.destroy()

        app = UltimateDeviceTool()
        log_to_file_debug_globally("UltimateDeviceTool instance created.")
        app.mainloop()
        log_to_file_debug_globally("Application mainloop exited.")

    except Exception as e_main:
        log_to_file_debug_globally(f"Main application error: {e_main}", "CRITICAL")
        try:
            with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f_tb:
                traceback.print_exc(file=f_tb)
        except Exception as e_tb_log:
            log_to_file_debug_globally(f"Could not write to log file: {e_tb_log}", "ERROR")
            print(f"[CRITICAL] Could not write to log file: {e_tb_log}", file=sys.stderr)
        print(f"[CRITICAL] FATAL ERROR: {e_main}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        try:
            error_tk_root = tk.Tk()
            error_tk_root.withdraw()
            messagebox.showerror(
                current_labels_for_warnings.get("fatal_error_title"),
                f"{current_labels_for_warnings.get('fatal_error_message_prefix')} {e_main}\n\nPlease check '{_DEBUG_LOG_PATH}' for details.",
                parent=error_tk_root
            )
            error_tk_root.destroy()
        except Exception as e_msgbox:
            log_to_file_debug_globally(f"Could not show fatal error message: {e_msgbox}", "ERROR")
            print(f"[ERROR] Could not show fatal error message: {e_msgbox}", file=sys.stderr)

        sys.exit(1)