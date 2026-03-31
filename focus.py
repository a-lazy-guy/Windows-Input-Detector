import time
import threading
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from threading import Event
import win32gui
import win32process
import psutil


@dataclass
class FocusEvent:
    window_title: str
    process_name: str
    process_id: int
    timestamp: float = field(default_factory=time.time)


class FocusDetector:
    def __init__(self, check_interval: float = 0.5):
        self.check_interval = check_interval
        self._last_focus_info = None
        self._running = False
        self._lock = threading.Lock()
        self._focus_events = []
        self._thread = None
        self._stop_event = Event()

    def _get_active_window_info(self) -> Optional[Dict]:
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None

            window_title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"

            return {
                "window_title": window_title,
                "process_name": process_name,
                "process_id": pid,
                "hwnd": hwnd
            }
        except Exception:
            return None

    def _detection_thread(self):
        while not self._stop_event.is_set():
            try:
                focus_info = self._get_active_window_info()
                if focus_info:
                    with self._lock:
                        if self._last_focus_info is None or \
                           self._last_focus_info.get("window_title") != focus_info.get("window_title") or \
                           self._last_focus_info.get("process_name") != focus_info.get("process_name"):

                            self._focus_events.append(FocusEvent(
                                window_title=focus_info["window_title"],
                                process_name=focus_info["process_name"],
                                process_id=focus_info["process_id"]
                            ))
                            self._last_focus_info = focus_info
            except Exception:
                pass

            self._stop_event.wait(self.check_interval)

    def start(self):
        try:
            self._running = True
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._detection_thread, daemon=True)
            self._thread.start()
            return True
        except Exception:
            return False

    def get_events(self) -> List[FocusEvent]:
        with self._lock:
            events = self._focus_events.copy()
            self._focus_events.clear()
        return events

    def stop(self):
        self._running = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        self._thread = None


def format_focus_event(event: FocusEvent) -> str:
    return f"[focus] Focus changed: '{event.window_title}' | {event.process_name} (PID: {event.process_id})"
