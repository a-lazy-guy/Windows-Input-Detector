import time
import threading
from dataclasses import dataclass, field
from typing import List
from pynput import keyboard


@dataclass
class KeyboardEvent:
    event_type: str
    key: str
    timestamp: float = field(default_factory=time.time)


class KeyboardDetector:
    def __init__(self):
        self._keyboard_listener = None
        self._keyboard_events = []
        self._lock = threading.Lock()
        self._running = False

    def _convert_key(self, key) -> str:
        key_str = str(key).replace("'", "")
        if hasattr(key, 'char') and key.char:
            return key.char
        elif hasattr(key, 'name'):
            return key.name

        numpad_map = {
            '<96>': 'Num0', '<97>': 'Num1', '<98>': 'Num2', '<99>': 'Num3', '<100>': 'Num4',
            '<101>': 'Num5', '<102>': 'Num6', '<103>': 'Num7', '<104>': 'Num8', '<105>': 'Num9'
        }
        if key_str in numpad_map:
            return numpad_map[key_str]

        return key_str

    def _on_press(self, key):
        with self._lock:
            try:
                key_str = self._convert_key(key)
                self._keyboard_events.append(KeyboardEvent(
                    event_type="KEY_PRESS",
                    key=key_str
                ))
            except Exception:
                pass

    def _on_release(self, key):
        with self._lock:
            try:
                key_str = self._convert_key(key)
                self._keyboard_events.append(KeyboardEvent(
                    event_type="KEY_RELEASE",
                    key=key_str
                ))
            except Exception:
                pass

    def start(self):
        try:
            self._running = True
            self._keyboard_listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            self._keyboard_listener.start()
            return True
        except Exception:
            return False

    def get_events(self) -> List[KeyboardEvent]:
        with self._lock:
            events = self._keyboard_events.copy()
            self._keyboard_events.clear()
        return events

    def stop(self):
        self._running = False
        if self._keyboard_listener:
            self._keyboard_listener.stop()
            self._keyboard_listener = None


def format_keyboard_event(event: KeyboardEvent) -> str:
    if event.event_type == "KEY_PRESS":
        return f"[keyboard] Pressed: {event.key}"
    elif event.event_type == "KEY_RELEASE":
        return f"[keyboard] Released: {event.key}"
    return f"[keyboard] {event.event_type}: {event.key}"
