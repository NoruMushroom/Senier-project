from datetime import datetime
import os

ATDATE = datetime(2022, 10, 30, 12, 30, 00, 0)            ######
USER_PATH = "C:/Users/gikim/Desktop/user_image"
MASK_PATH = os.path.join(USER_PATH, 'Mask')
NOMASK_PATH = os.path.join(USER_PATH, 'NoMask')
TEMP_PATH =  os.path.join(USER_PATH, "Temp")
PKL = "representations_arcface.pkl"
MASK_PKL = os.path.join(MASK_PATH, PKL)
NOMASK_PKL = os.path.join(NOMASK_PATH, PKL)

#database
HOST = "127.0.0.1"
PORT = 8000
USER = "root"
PWD = "1234"
