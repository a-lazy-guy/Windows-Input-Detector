import time
import threading
from dataclasses import dataclass, field
from typing import List, Optional
from pynput import mouse


@dataclass
class MouseEvent:
    event_type: str
    x: int
    y: int
    button: Optional[str] = None
    dx: Optional[int] = None
    dy: Optional[int] = None
    pressed: Optional[bool] = None
    distance: Optional[float] = None
    timestamp: float = field(default_factory=time.time)


class MouseDetector:
    def __init__(self):
        self._mouse_listener = None
        self._mouse_events = []
        self._lock = threading.Lock()
        self._running = False
        self._last_pos = None

    def _on_move(self, x, y):
        with self._lock:
            distance = None
            if self._last_pos is not None:
                last_x, last_y = self._last_pos
                dx = x - last_x
                dy = y - last_y
                distance = (dx ** 2 + dy ** 2) ** 0.5
            self._last_pos = (x, y)

            self._mouse_events.append(MouseEvent(
                event_type="MOUSE_MOVE",
                x=x,
                y=y,
                distance=distance
            ))

    def _on_click(self, x, y, button, pressed):
        with self._lock:
            self._mouse_events.append(MouseEvent(
                event_type="MOUSE_CLICK",
                x=x,
                y=y,
                button=str(button).split('.')[-1],
                pressed=pressed
            ))

    def _on_scroll(self, x, y, dx, dy):
        with self._lock:
            self._mouse_events.append(MouseEvent(
                event_type="MOUSE_SCROLL",
                x=x,
                y=y,
                dx=dx,
                dy=dy
            ))

    def start(self):
        try:
            self._running = True
            self._mouse_listener = mouse.Listener(
                on_move=self._on_move,
                on_click=self._on_click,
                on_scroll=self._on_scroll
            )
            self._mouse_listener.start()
            return True
        except Exception:
            return False

    def get_events(self) -> List[MouseEvent]:
        with self._lock:
            events = self._mouse_events.copy()
            self._mouse_events.clear()
        return events

    def stop(self):
        self._running = False
        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None


def format_mouse_event(event: MouseEvent) -> str:
    if event.event_type == "MOUSE_MOVE":
        if event.distance is not None:
            return f"[mouse] Moved: ({event.x}, {event.y}) | Distance: {event.distance:.2f}px"
        return f"[mouse] Moved: ({event.x}, {event.y})"
    elif event.event_type == "MOUSE_CLICK":
        action = "Pressed" if event.pressed else "Released"
        return f"[mouse] Click: {event.button} button {action} at ({event.x}, {event.y})"
    elif event.event_type == "MOUSE_SCROLL":
        direction = ""
        if event.dx > 0:
            direction += f"Right{event.dx}"
        elif event.dx < 0:
            direction += f"Left{-event.dx}"
        if event.dy > 0:
            direction += f"Up{event.dy}"
        elif event.dy < 0:
            direction += f"Down{-event.dy}"
        return f"[mouse] Scroll: {direction} at ({event.x}, {event.y})"
    return f"[mouse] {event.event_type}: ({event.x}, {event.y})"
