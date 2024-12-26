# Real-Time Eye Blink Detection System

This project is a real-time eye blink detection system using a webcam and the `cvzone` library. The system tracks eye movements, calculates the Eye Aspect Ratio (EAR), and counts blinks. Additionally, it plots the EAR values in real time.

## Features
- Real-time detection of eye landmarks using `cvzone` and OpenCV.
- Calculation of Eye Aspect Ratio (EAR) for both eyes.
- Blink counting based on EAR thresholds.
- Visual feedback for blinks and prolonged eye closure.
- Live plotting of EAR values for debugging and visualization.

## Prerequisites
Make sure you have Python 3.7 or higher installed on your system.

### Required Libraries
Install the following Python libraries:
- `opencv-python`
- `cvzone`
- `numpy`

To install these libraries, run:
```bash
pip install opencv-python cvzone numpy
