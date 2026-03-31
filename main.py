import time
import traceback

from keyboard import KeyboardDetector, format_keyboard_event
from mouse import MouseDetector, format_mouse_event
from focus import FocusDetector, format_focus_event


def main():
    mouse_detector = MouseDetector()
    keyboard_detector = KeyboardDetector()
    focus_detector = FocusDetector(check_interval=0.5)

    mouse_started = mouse_detector.start()
    keyboard_started = keyboard_detector.start()
    focus_started = focus_detector.start()

    try:
        while True:
            if mouse_started:
                for event in mouse_detector.get_events():
                    print(format_mouse_event(event))

            if keyboard_started:
                for event in keyboard_detector.get_events():
                    print(format_keyboard_event(event))

            if focus_started:
                for event in focus_detector.get_events():
                    print(format_focus_event(event))

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        traceback.print_exc()
    finally:
        mouse_detector.stop()
        keyboard_detector.stop()
        focus_detector.stop()


if __name__ == "__main__":
    main()
