#!/usr/bin/env python3
"""
Ransomware Behaviour Detection Engine - Prototype
Institute : GLA University
Team Name : The Undefine Elite
"""

import os
import time
import psutil
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =========================
# CONFIGURATION (DEMO TUNED)
# =========================
MONITOR_PATH = "monitor_folder"

FILE_CHANGE_THRESHOLD = 2      # minimum events in TIME_WINDOW
TIME_WINDOW = 4                # seconds to look back for burst
COOLDOWN_TIME = 1.5            # min seconds between two alerts
MIN_RISK_ALERT = 4             # minimum score to raise alert

SENSITIVE_EXTENSIONS = [
    ".doc", ".docx", ".xls", ".xlsx", ".pdf",
    ".ppt", ".pptx", ".jpg", ".jpeg", ".png",
    ".txt"
]

LOG_FILE = "ransomware_alerts.log"

event_times = []
last_alert_time = 0
first_alert_shown = False      # banner hide control

CONTENT_WIDTH = 90

# ANSI colours
GREEN        = "\033[0;32m"
YELLOW       = "\033[1;33m"
RED          = "\033[1;31m"
CYAN         = "\033[0;36m"
MAGENTA      = "\033[0;35m"
BRIGHT_GREEN = "\033[1;32m"
RESET        = "\033[0m"

FRAME = CYAN   # box/frame colour ek hi rakha hai


def get_left_pad() -> str:
    try:
        cols = shutil.get_terminal_size((120, 40)).columns
    except Exception:
        cols = 120
    pad = max((cols - CONTENT_WIDTH) // 2, 0)
    return " " * pad


def banner():
    os.system("cls" if os.name == "nt" else "clear")
    left_pad = get_left_pad()

    title = r"""
   ____                         _                                                 
  |  _ \ __ _ _ __  _ __   __ _| |__  _ __ ___   __ _ _ __ ___   ___  _   _ _ __  
  | |_) / _` | '_ \| '_ \ / _` | '_ \| '_ ` _ \ / _` | '_ ` _ \ / _ \| | | | '_ \ 
  |  _ < (_| | |_) | |_) | (_| | | | | | | | | | (_| | | | | | | (_) | |_| | | | |
  |_| \_\__,_| .__/| .__/ \__,_|_| |_|_| |_| |_|\__,_|_| |_| |_|\___/ \__,_|_| |_|
             |_|   |_|                                                             
    """.rstrip("\n")

    # ASCII logo bright green
    for line in title.splitlines():
        print(left_pad + BRIGHT_GREEN + line + RESET)

    # Title bar cyan
    bar = "═" * CONTENT_WIDTH
    print(left_pad + CYAN + bar + RESET)
    center_title = "RANSOMWARE BEHAVIOUR DETECTION ENGINE  (Prototype) 🛡️"
    print(left_pad + CYAN + center_title.center(CONTENT_WIDTH) + RESET)
    print(left_pad + CYAN + bar + RESET)

    # Info box
    box_width = CONTENT_WIDTH - 2
    print(left_pad + FRAME + "┌" + "─" * box_width + "┐" + RESET)

    def gline(text: str):
        print(left_pad + FRAME + text.ljust(box_width) + " │" + RESET)

    gline("│ Institute : GLA University")
    gline("│ Team Name : The Undefine Elite")
    gline("│ Team (3 | 2): Abhishek Raj  |  Anuj Kumar")
    gline("│               Shivangi Raj  |  Madhav Kumar")
    print(left_pad + FRAME + "├" + "─" * box_width + "┤" + RESET)

    left = "│ Mode      : "
    right = "Behaviour-based early warning 🔍"
    line = (FRAME + "│ " + RESET)  # start frame
    line = (YELLOW + left + RESET +
            CYAN + right.ljust(box_width - len(left)) +
            FRAME + "│" + RESET)
    print(left_pad + line)

    for txt in [
        "• Rapid file activity",
        "• Sensitive document focus",
        "• System resource anomalies",
    ]:
        inner = " " * 13 + txt
        line = (FRAME + "│ " + RESET +
                CYAN + inner.ljust(box_width - 1) +
                FRAME + "│" + RESET)
        print(left_pad + line)

    print(left_pad + FRAME + "├" + "─" * box_width + "┤" + RESET)

    def kv_line(label: str, value: str):
        left = f"│ {label:<13}: "
        val = value
        line = (YELLOW + left + RESET +
                GREEN + val.ljust(box_width - len(left)) +
                FRAME + " │")
        print(left_pad + line + RESET)

    kv_line("Monitoring path", os.path.abspath(MONITOR_PATH))
    kv_line("Threshold", f"{FILE_CHANGE_THRESHOLD} events / {TIME_WINDOW} sec")
    kv_line("Cooldown", f"{COOLDOWN_TIME} sec between alerts")

    print(left_pad + FRAME + "├" + "─" * box_width + "┤" + RESET)

    left = "│ Status          : "
    status_text = "RUNNING"
    tail = " (press Ctrl+C to stop) ✅"
    line = (YELLOW + left + RESET +
            YELLOW + status_text + RESET +
            GREEN + tail.ljust(box_width - len(left) - len(status_text)) +
            FRAME + "│")
    print(left_pad + line + RESET)

    print(left_pad + FRAME + "└" + "─" * box_width + "┘" + RESET)
    print("\n")


def ensure_monitor_path():
    if not os.path.exists(MONITOR_PATH):
        os.makedirs(MONITOR_PATH, exist_ok=True)


def log_alert(message: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")


def wrap_line(text: str, max_width: int):
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for w in words[1:]:
        if len(current) + 1 + len(w) <= max_width:
            current += " " + w
        else:
            lines.append(current)
            current = w
    lines.append(current)
    return lines


def get_entry_point_clues():
    clues = []
    try:
        monitor_abs = os.path.abspath(MONITOR_PATH).lower()
        keywords = ["ransomware", "monitor_folder", "encrypt", "python", "bash"]
        candidates = []

        for proc in psutil.process_iter(
            ["pid", "name", "username", "cpu_percent", "cmdline"]
        ):
            info = proc.info
            pid = info.get("pid")
            name = info.get("name") or "unknown"
            user = info.get("username") or "unknown"
            cpu = info.get("cpu_percent") or 0.0
            cmdline_list = info.get("cmdline") or []
            cmdline = " ".join(cmdline_list)
            lower_cmd = cmdline.lower()

            score = 0
            if monitor_abs and monitor_abs in lower_cmd:
                score += 3
            for kw in keywords:
                if kw in lower_cmd:
                    score += 1
            if cpu > 5:
                score += 1

            if score > 0:
                candidates.append((score, cpu, pid, name, user, cmdline))

        if not candidates:
            clues.append("No clear process clue (possible short-lived or external source).")
            return clues

        candidates.sort(reverse=True, key=lambda x: (x[0], x[1]))
        for idx, (score, cpu, pid, name, user, cmdline) in enumerate(candidates[:2]):
            msg = (
                f"{idx+1}) pid={pid}, proc={name}, user={user}, "
                f"cpu={cpu:.1f}%, score={score}, cmd='{cmdline}'"
            )
            clues.extend(wrap_line(msg, CONTENT_WIDTH - 8))

    except Exception as e:
        clues.append(f"Error collecting process clues: {e}")

    if not clues:
        clues.append("No clear process clue (possible short-lived or external source).")
    return clues


class RansomwareDetector(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.handle_event(event.src_path, "created")

    def on_modified(self, event):
        if not event.is_directory:
            self.handle_event(event.src_path, "modified")

    def handle_event(self, file_path: str, event_type: str):
        global last_alert_time, first_alert_shown

        now = time.time()
        if now - last_alert_time < COOLDOWN_TIME:
            return

        event_times.append(now)
        recent_events = [t for t in event_times if now - t <= TIME_WINDOW]
        event_times.clear()
        event_times.extend(recent_events)

        risk_score = 0
        reasons = []

        if len(recent_events) >= FILE_CHANGE_THRESHOLD:
            risk_score += 5
            reasons.append("Unusual burst of file changes")

        _, ext = os.path.splitext(file_path)
        if ext.lower() in SENSITIVE_EXTENSIONS:
            risk_score += 2
            reasons.append(f"Access to sensitive document type ({ext})")

        cpu = psutil.cpu_percent(interval=0.2)
        disk = psutil.disk_usage("/").percent

        if cpu > 10:
            risk_score += 2
            reasons.append(f"CPU spike detected ({cpu}%)")
        if disk > 10:
            risk_score += 1
            reasons.append(f"Disk activity observed ({disk}%)")

        if risk_score >= MIN_RISK_ALERT:
            last_alert_time = now
            event_times.clear()

            timestamp = datetime.now().strftime("%H:%M:%S")
            entry_clues = get_entry_point_clues()

            if not first_alert_shown:
                os.system("cls" if os.name == "nt" else "clear")
                first_alert_shown = True

            left_pad = get_left_pad()

            print(left_pad + YELLOW + "#" * CONTENT_WIDTH + RESET)
            header = f"#           🚨  POTENTIAL RANSOMWARE ACTIVITY DETECTED  |  {timestamp}"
            print(left_pad + YELLOW + header.ljust(CONTENT_WIDTH - 1) + "#" + RESET)
            print(left_pad + YELLOW + "#" * CONTENT_WIDTH + RESET)

            def print_field(label, value, colour=CYAN):
                base = f"#  {label:<17}: {value}"
                lines = wrap_line(base, CONTENT_WIDTH - 1)
                for i, line in enumerate(lines):
                    if i == 0:
                        print(left_pad + colour + line.ljust(CONTENT_WIDTH - 1) + "#" + RESET)
                    else:
                        cont = "#  " + line[3:]
                        print(left_pad + colour + cont.ljust(CONTENT_WIDTH - 1) + "#" + RESET)

            print_field("Event type", event_type)
            print_field("File path", file_path)
            print_field("Recent file events", f"{len(recent_events)} in last {TIME_WINDOW} sec")
            print_field("CPU usage", f"{cpu}%")
            print_field("Disk usage", f"{disk}%")
            print_field("Behaviour score", f"{risk_score} / 10", colour=RED)

            print(left_pad + MAGENTA + "#  Indicators:".ljust(CONTENT_WIDTH - 1) + "#" + RESET)
            for r in reasons:
                for line in wrap_line(r, CONTENT_WIDTH - 8):
                    print(left_pad + MAGENTA + f"#    • {line}".ljust(CONTENT_WIDTH - 1) + "#" + RESET)

            print(left_pad + CYAN + "#  Possible entry clues (process level):".ljust(CONTENT_WIDTH - 1) + "#" + RESET)
            for clue in entry_clues:
                for line in wrap_line(clue, CONTENT_WIDTH - 8):
                    print(left_pad + CYAN + f"#    • {line}".ljust(CONTENT_WIDTH - 1) + "#" + RESET)

            print(left_pad + GREEN + "#  Recommended steps:".ljust(CONTENT_WIDTH - 1) + "#" + RESET)
            steps = [
                "Investigate responsible process (see clues above)",
                "Temporarily isolate the host from network",
                "Secure latest backups of critical data",
            ]
            for s in steps:
                for line in wrap_line(s, CONTENT_WIDTH - 8):
                    print(left_pad + GREEN + f"#    • {line}".ljust(CONTENT_WIDTH - 1) + "#" + RESET)

            print(left_pad + YELLOW + "#" * CONTENT_WIDTH + RESET + "\n")

            log_alert(
                f"ALERT risk={risk_score} events={len(recent_events)} "
                f"cpu={cpu} disk={disk} file={file_path} clues={'; '.join(entry_clues)}"
            )


def main():
    ensure_monitor_path()
    banner()

    event_handler = RansomwareDetector()
    observer = Observer()
    observer.schedule(event_handler, path=MONITOR_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping observer...")

    observer.stop()
    observer.join()
    print("Engine stopped. 👋")


if __name__ == "__main__":
    main()
