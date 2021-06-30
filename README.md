# AirMouse
A very crude demo on how to make WiFi airmouse with NodeMCU and BNO055.
The demo only works on certain direction, there's no reset for the orientation and
the firmware kept on crashing so now the connection is restarted after every sent message to prevent
the stack from filling up.

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
