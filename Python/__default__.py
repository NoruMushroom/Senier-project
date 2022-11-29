from datetime import datetime

Attendance_date = datetime(2022, 10, 30, 12, 30, 00, 0)            ######
Mask_DB_Path = 'D:/Mask_Project/user_img/Mask'
NoMask_DB_Path ='D:/Mask_Project/user_img/NoMask'
Photo_Path = "D:/Mask_Project/user_img/Temp"
PKL_Mask_Path = "D:/Mask_Project/user_img/Mask/representations_arcface.pkl"
PKL_NoMask_Path = "D:/Mask_Project/user_img/NoMask/representations_arcface.pkl"
pkl = "representations_arcface.pkl"

#database
host = "127.0.0.1"
port = 8000
user = "root"
password = "1234"
