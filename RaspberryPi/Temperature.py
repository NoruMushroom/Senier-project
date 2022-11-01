import time,board,busio
import numpy as np
import adafruit_mlx90640
import datetime as dt
import cv2
from threading import Thread
from socket import *

host = "192.168.0.6"
port = 1128

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(5)
connectionSocket,addr = serverSocket.accept()
print("connection!!")
startX = 0
startY = 0
endX = 0
endY = 0
W_ratio = 24/640
H_ratio = 32/480
Temp = 0

frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures

def td_to_image(f):
	norm = np.uint8((f + 40)*6.4)
	norm.shape = (24,32)
	return norm

def Receive_Data():
    global startX,startY,endX,endY
    while True:
        try:
            recv_data = connectionSocket.recv(1024)
            data = eval(recv_data)
            startX = int(data[0] * W_ratio)
            startY = int(data[1] * H_ratio)
            endX = int(data[2] * W_ratio)
            endY = int(data[3] * H_ratio)
            time.sleep(0.5)
        except:
            continue
R_Data = Thread(target = Receive_Data)

def Temp_Data():
    global Temp
    while True:
        try:
            data = 0
            for x in range(startX,endX+1):
                for y in range(startY,endY+1):
                    index = (24 * x) + y
                    if data < frame[index]:
                        data = frame[index]
                Temp = round(data,2)
                Temp = Temp + 3.2
            print("Temp:",Temp)
            time.sleep(1)
        except:
            continue
T_Data = Thread(target = Temp_Data)

def Send_Data():
    while True:
        try:
            connectionSocket.send(str(Temp).encode("utf-8"))
            time.sleep(1)
        except:
            continue
S_Data = Thread(target = Send_Data)

R_Data.start()
T_Data.start()
S_Data.start()
t0 = time.time()

i2c = busio.I2C(board.SCL, board.SDA, frequency = 1200000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # set refresh rate
mlx_shape = (24,32)

try:
    while True:
            try:
                mlx.getFrame(frame) # read MLX temperatures into frame var
                img16 = (np.reshape(frame,mlx_shape)) # reshape to 24x32
                ta_img = td_to_image(img16)
                # Image processing
                img = cv2.applyColorMap(ta_img, cv2.COLORMAP_JET)
                img = cv2.resize(img, (24,32), interpolation = cv2.INTER_LINEAR)
                img = cv2.flip(img, 1)
                img = cv2.rectangle(img,(startX,startY),(endX,endY),(0,0,0))
                cv2.imshow('Output', img)
                key = cv2.waitKey(1) & 0xFF
                t0 = time.time()
            except KeyboardInterrupt:
                break
            except:
                continue
except KeyboardInterrupt:
        cv2.destroyAllWindows()
        serverSocket.close()
cv2.destroyAllWindows()
