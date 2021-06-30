# AirMouse
A very crude demo on how to make WiFi airmouse with NodeMCU and BNO055.
The demo only works on certain direction, there's no reset for the orientation and
the firmware kept on crashing so now the connection is restarted after every sent message to prevent
the stack from filling up.

#### Python3 required libraries:
- pynput
- numpy
- pyautogui

Edit: Now it seems like this keeps crashing the windows' window manager if you do the gesture a couple of times in a row, so make sure if you want to try this to close everything important :D

#### Pinout:
| NodeMCU pin   | BNO055 |
| ------------- | ------------- |
| D1  | SCL (BNO) |
| D2  | SDA (BNO) |
| 3V3 | VCC (BNO) |
| GND | GND (BNO) |

| NodeMCU pin   | Li-ion battery |
| ------------- | ------------- |
| VIN | BAT+ |
| GND | BAT- |

| NodeMCU pin   | Button |
| ------------- | ------------- |
| GND | pin 1 |
| D4 | pin 2 |
