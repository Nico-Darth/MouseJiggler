import sys
import threading
import time
import math
from PyQt5.QtWidgets import QApplication, QInputDialog, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer, Qt
from pynput.mouse import Controller
from pynput import keyboard

class MouseJiggler:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mouse = Controller()
        self.jiggling = True
        self.duration = None
        self.pressed_keys = set()  # Set to track currently pressed keys

        self.show_credits_and_info()
        self.init_ui()
        self.start_keyboard_listener()

    def show_credits_and_info(self):
        # Create a credits and info window
        self.info_window = QWidget()
        self.info_window.setWindowTitle("Mouse Jiggler")  # Set the title to "Mouse Jiggler"
        self.info_window.setGeometry(100, 100, 400, 300)
        self.info_window.setStyleSheet("background-color: #222; color: white; font-size: 14px; padding: 10px;")

        layout = QVBoxLayout()

        # Add credits
        credits_label = QLabel("Mouse Jiggler\nCreated by: Niels Coert")
        credits_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        credits_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits_label)

        # Add instructions
        info_label = QLabel(
            "This program prevents your computer from sleeping or locking by simulating mouse movements.\n\n"
            "Controls:\n"
            "1. Enter the duration in seconds when prompted.\n"
            "2. The mouse will move in a circular motion.\n"
            "3. To stop the program immediately, press ALT+0.\n\n"
            "Note: Use responsibly to avoid misuse."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding-top: 10px;")
        layout.addWidget(info_label)

        # Add start button
        start_button = QPushButton("Start Program")
        start_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 8px;")
        start_button.clicked.connect(self.info_window.close)
        layout.addWidget(start_button)

        self.info_window.setLayout(layout)
        self.info_window.show()

        # Block the execution until the info window is closed
        self.app.exec_()


    def init_ui(self):
        # Prompt user for time
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
        self.timer.start(1000)  # Update every second

    def update_timer(self):
        self.duration -= 1
        self.timer_label.setText(f"Time remaining: {self.duration}s")

        if self.duration <= 0:
            self.stop_program()

    def start_jiggling(self):
        def jiggle():
            angle = 0  # Initial angle in radians
            radius = 10  # Radius of the circular motion
            center_x, center_y = self.mouse.position  # Get current mouse position as center

            while self.jiggling:
                # Calculate new x and y using circular motion formulas
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.mouse.position = (x, y)

                # Increment the angle for smooth motion
                angle += 0.1  # Smaller values = slower motion
                if angle >= 2 * math.pi:  # Reset angle after a full circle
                    angle -= 2 * math.pi

                time.sleep(0.05)  # Controls the speed of the motion

        threading.Thread(target=jiggle, daemon=True).start()

    def stop_program(self):
        self.jiggling = False
        self.timer.stop()
        self.timer_window.close()
        sys.exit()

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char:  # Track normal keys
                    self.pressed_keys.add(key.char)
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:  # Track Alt keys
                    self.pressed_keys.add('alt')

                if '0' in self.pressed_keys and 'alt' in self.pressed_keys:
                    self.stop_program()
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
