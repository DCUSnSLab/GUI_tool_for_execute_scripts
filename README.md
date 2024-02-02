# GUI tool for Pothole Detection

## Requirements
This project requires the following development environment:
- Ubuntu 20.04 LTS
- Python 3.8.10
- PyQt5 5.14.1
- OpenCV2 4.9.0

## Guide
- `GUI.py` : Main Script for GUI. 
- `scripts/segnet-camera-excel.py` : Python Script to detect pothole and save data file. DO NOT RUN WITHOUT SETTING DEPENDENCY.
- `test/file_down_test.py` : Example Script for testing scenario. If you run `GUI.py`, this script will also be executed.
- `test/from_path/` : Directory for test (Data Save Path).
- `test/to_path/` : Directory fro test (Data Copy Path).

## Run
Run these commands in bash shell (Ubuntu 20.04) :
```
$ pip install pyqt5
$ pip install opencv-python
$ python3 GUI.py
```
