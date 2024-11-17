# Mouse Jiggler

**Mouse Jiggler** is a simple Python-based application that prevents your computer from sleeping or locking by simulating mouse movements. The application moves the mouse in a circular motion, and you can set a specific duration for the jiggling.

## Features
- **Prevent Sleep or Lock:** Keeps your computer awake by simulating mouse movements.
- **Adjustable Duration:** Enter the time in seconds when prompted, and the program will run for that duration.
- **Keyboard Control:** Press `ALT+0` to stop the program immediately.
- **Circular Motion:** The mouse moves in a smooth circular pattern to simulate activity.

## Installation

### EXE Version
For the EXE version, no installation is required. Simply download the EXE file and double-click to run the program. Upon running, you will be prompted to enter a duration in seconds. The program will then start the jiggling motion and display a timer window showing the remaining time.

### Python (.py) Version

If you want to run the `.py` version, you need to install the required dependencies. Follow these steps:

1. Install Python (version 3.6 or later).
2. Install the required libraries using the following command:

   ```
   pip install PyQt5 pynput
   ```

3. Run the Python script with:

   ```
   python MouseJiggler.py
   ```

## Controls

- **Start:** The program starts automatically after entering the time duration.
- **Stop:** Press `ALT + 0` to stop the program immediately.

## Credits

**Created by:** Niels Coert

## Disclaimer

Use this software responsibly. It can prevent the computer from sleeping or locking, which may interfere with certain system processes. Please ensure that it is used appropriately.

