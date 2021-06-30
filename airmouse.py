import socket
import pyautogui
import time

from pynput.mouse import Button, Controller
from numpy import interp

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.0.0.184', 8421))

sCount = 0
sXArray = []
sYArray = []

mouse = Controller()

try:
    while True:
        
        recv = ""
        try:
            s.send(b'd')
            recv = s.recv(1024).decode().strip().replace('\n', "")
            s.close()
        except Exception as e:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('10.0.0.184', 8421))

        if not recv:
            continue
            
        array = recv.split(",")

        # Find out the display resolution to center the cursor properly
        w,h = pyautogui.size()


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

        sXArray.append(int(xCoord))
        sYArray.append(int(yCoord))

        if array[3] == "0":
            mouse.press(Button.left)
        else:
            mouse.release(Button.left)

        if sCount >= 10:

            avgX = int(sum(sXArray)/sCount)
            avgY = int(sum(sYArray)/sCount)
            
            sCount = 0
            sXArray = []
            sYArray = []
            sButtonArray = []
            
            mouse.position = (int(xCoord),int(yCoord))
            
        else:
            sCount += 1
            
        
except Exception as e:
    print(e)
    print("Ok bye")

s.close()
