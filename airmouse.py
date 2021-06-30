import serial
import pyautogui
import time
#import win32api, win32con

from pymouse import PyMouse
from numpy import interp

ser = serial.Serial("COM7", 115200)
ser.timeout = 1

sCount = 0
sXArray = []
sYArray = []

m = PyMouse()

try:
    while True:
        ser.write(b'd;')
        recv = ser.readline().decode().replace(";", "").strip()
            
        array = recv.split(",")
        #print(array)

        # Find out the display resolution to center the cursor properly
        w,h = pyautogui.size()

        #print(array)

        x = float(array[0])
        y = float(array[2])

        xAngle = 0
        if x < 360 and x > 310:
            xAngle = (360-x)*-1
        if x > 0 and x < 50:
            xAngle = x
        
        if x < 180 and x > 130:
            xAngle = 180-x
        if x > 180 and x < 230:
            xAngle = 180-x
        xCoord = interp(xAngle*-1,[-50,50],[0,w])

        yAngle = 0
        if y < 0 and y > -50:
            yAngle = y
        if y > 0 and y < 50:
            yAngle = y
        yCoord = interp(yAngle,[-50,50],[0,h])

        #print(xAngle, yAngle)
        #print(xCoord, yCoord)

        sXArray.append(int(xCoord))
        sYArray.append(int(yCoord))

        if array[3] == "0":
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, int(xCoord), int(yCoord), 0, 0)
            m.press(int(xCoord), int(yCoord))
        else:
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, int(xCoord), int(yCoord), 0, 0)
            m.release(int(xCoord), int(yCoord))

        if sCount >= 10:

            avgX = int(sum(sXArray)/sCount)
            avgY = int(sum(sYArray)/sCount)
            
            sCount = 0
            sXArray = []
            sYArray = []
            sButtonArray = []
            
            #pyautogui.moveTo(int(xCoord), int(yCoord))
            #win32api.SetCursorPos((int(xCoord),int(yCoord)))
            m.move(int(xCoord), int(yCoord))
            
        else:
            sCount += 1
            
        
except Exception as e:
    print(e)
    print("Ok bye")

ser.close()
