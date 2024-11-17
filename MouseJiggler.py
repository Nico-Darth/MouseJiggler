import sys
import threading
import time
import math
from PyQt5.QtWidgets import QApplication, QInputDialog, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer, Qt
from pynput.mouse import Controller
from pynput import keyboard
import random


class MouseJiggler:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mouse = Controller()
        self.jiggling = True
        self.paused = False  # New flag to track pause state
        self.duration = None
        self.motion_pattern = None
        self.pressed_keys = set()  # Track pressed keys

        self.show_credits_and_info()
        self.init_ui()
        self.start_keyboard_listener()

    def show_credits_and_info(self):
        self.info_window = QWidget()
        self.info_window.setWindowTitle("Mouse Jiggler")
        self.info_window.setGeometry(100, 100, 400, 300)
        self.info_window.setStyleSheet("background-color: #222; color: white; font-size: 14px; padding: 10px;")

        layout = QVBoxLayout()
        credits_label = QLabel("Mouse Jiggler\nCreated by: Niels Coert")
        credits_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        credits_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits_label)

        info_label = QLabel(
            "This program prevents your computer from sleeping or locking by simulating mouse movements.\n\n"
            "Controls:\n"
            "1. Choose a motion pattern.\n"
            "2. Enter the duration in seconds when prompted.\n"
            "3. The mouse will move based on the selected pattern.\n"
            "4. To stop the program immediately, press ALT+0.\n"
            "5. Press SPACEBAR to pause/resume the jiggling.\n\n"
            "Note: Use responsibly to avoid misuse."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding-top: 10px;")
        layout.addWidget(info_label)

        start_button = QPushButton("Start Program")
        start_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 8px;")
        start_button.clicked.connect(self.info_window.close)
        layout.addWidget(start_button)

        self.info_window.setLayout(layout)
        self.info_window.show()
        self.app.exec_()

    def init_ui(self):
        # Prompt user to select motion pattern
        self.motion_pattern, ok = QInputDialog.getItem(
            None, "Mouse Jiggler", "Choose a motion pattern:", 
            ["Circular", "Zigzag", "Random"], 0, False
        )
        if not ok:
            sys.exit()

        # Prompt user for duration
        self.duration, ok = QInputDialog.getInt(None, "Mouse Jiggler", "Enter time in seconds:", min=1)
        if not ok:
            sys.exit()

        # Create timer window
        self.timer_window = QWidget()
        self.timer_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.timer_window.setGeometry(10, 10, 150, 50)
        self.timer_window.setStyleSheet("background-color: black; color: white; font-size: 16px;")

        self.layout = QVBoxLayout()
        self.timer_label = QLabel("Time remaining: {}s".format(self.duration))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timer_label)
        self.timer_window.setLayout(self.layout)
        self.timer_window.show()

        # Start timer and jiggling
        self.start_timer()
        self.start_jiggling()

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        if not self.paused:  # Only update timer if not paused
            self.duration -= 1
            self.timer_label.setText(f"Time remaining: {self.duration}s")
            if self.duration <= 0:
                self.stop_program()

    def start_jiggling(self):
        if self.motion_pattern == "Circular":
            self.jiggle_circular()
        elif self.motion_pattern == "Zigzag":
            self.jiggle_zigzag()
        elif self.motion_pattern == "Random":
            self.jiggle_random()

    def jiggle_circular(self):
        def jiggle():
            angle = 0
            radius = 10
            center_x, center_y = self.mouse.position

            while self.jiggling:
                if not self.paused:  # Pause jiggling if paused
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    self.mouse.position = (x, y)
                    angle += 0.1
                    if angle >= 2 * math.pi:
                        angle -= 2 * math.pi
                    time.sleep(0.05)
                else:
                    time.sleep(0.1)  # Sleep to reduce CPU usage when paused

        threading.Thread(target=jiggle, daemon=True).start()

    def jiggle_zigzag(self):
        def jiggle():
            step = 10
            toggle = 1
            x, y = self.mouse.position

            while self.jiggling:
                if not self.paused:  # Pause jiggling if paused
                    x += step * toggle
                    toggle *= -1
                    self.mouse.position = (x, y)
                    time.sleep(0.1)
                else:
                    time.sleep(0.1)  # Sleep to reduce CPU usage when paused

        threading.Thread(target=jiggle, daemon=True).start()

    def jiggle_random(self):
        def jiggle():
            while self.jiggling:
                if not self.paused:  # Pause jiggling if paused
                    x_offset = random.randint(-10, 10)
                    y_offset = random.randint(-10, 10)
                    x, y = self.mouse.position
                    self.mouse.position = (x + x_offset, y + y_offset)
                    time.sleep(0.2)
                else:
                    time.sleep(0.1)  # Sleep to reduce CPU usage when paused

        threading.Thread(target=jiggle, daemon=True).start()

    def stop_program(self):
        self.jiggling = False
        self.timer.stop()
        self.timer_window.close()
        sys.exit()

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char:
                    self.pressed_keys.add(key.char)
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.pressed_keys.add('alt')

                if '0' in self.pressed_keys and 'alt' in self.pressed_keys:
                    self.stop_program()

                # Toggle pause when spacebar is pressed
                if key == keyboard.Key.space:
                    self.paused = not self.paused  # Toggle pause
                    if self.paused:
                        print("Jiggling paused.")
                    else:
                        print("Jiggling resumed.")

            except AttributeError:
                pass

        def on_release(key):
            try:
                if hasattr(key, 'char') and key.char:
                    self.pressed_keys.discard(key.char)
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.pressed_keys.discard('alt')
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    jiggler = MouseJiggler()
    jiggler.run()

