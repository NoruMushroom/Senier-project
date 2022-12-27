from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from socket import *
from choose_student_name import Ui_choose_student_name
from datetime import timedelta, datetime
from DB.attendance import atd_upload
from Temp_error import Ui_Temp_error
import time
from retinaface import RetinaFace
import numpy as np
from Option import *
import os
from Face import *
from deepface.commons import distance
import sys

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)    
    clientSocket.connect((HOST,PORT))
    Thread_Pause = True
    
except TimeoutError as e:
    print(e)
    Thread_Pause = False
except ConnectionRefusedError as e:
    print(e)
    Thread_Pause = False
    
objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')                  
save_img = cameraimg = None
Face_Area = distest = []
send_data = recv_data = StudentID = None
dddown = 9                     
curtime = [datetime.now().month,datetime.now().day]
    




class Temp_data_send(QtCore.QThread):
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent = None):
        super(Temp_data_send, self).__init__(parent)
        global Thread_Pause
    def run(self):
        global Face_Area
        while Thread_Pause:
            if len(Face_Area) == 4:
                #1 체온
                send_data = str(Face_Area)    
                print(str(Face_Area))
                clientSocket.send(send_data.encode())  
                print()
                print(clientSocket.send(send_data.encode()))            
                time.sleep(0.5)
class Temp_data_recv(QtCore.QThread):
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent = None):
        super(Temp_data_recv, self).__init__(parent)
        #2global Thread_Pause
    def run(self):
        while Thread_Pause:
            global recv_data
            #1 체온
            recv_data = clientSocket.recv(1024)                            
            recv_data = recv_data.decode("utf-8")                          
            time.sleep(1)
class Temp_Data(QtCore.QThread):
    def __init__(self, parent=None):
        super(Temp_Data, self).__init__(parent)
        global recv_data
    signal = QtCore.pyqtSignal(str)
    def run(self):
        while Thread_Pause:
            self.signal.emit(str(recv_data))
            time.sleep(1)
            
class Name_Data(QtCore.QThread):
    def __init__(self, parent=None):
        super(Name_Data, self).__init__(parent)
        global StudentID
    signal = QtCore.pyqtSignal(str)
    def run(self):
        while Thread_Pause:
            self.signal.emit(str(StudentID))
            time.sleep(0.5)
class FrameGrabber(QtCore.QThread):
    def __init__(self, parent=None):
        super(FrameGrabber, self).__init__(parent)
        self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.star = time.time()
        self.DB_Path =  MASK_PATH
        self.default_PKL = MASK_PKL
        self.score = 0
    signal = QtCore.pyqtSignal(QtGui.QImage)
    def run(self):
        global Face_Area, StudentID,embedding_list_No,embedding_list_Ma, save_img, cameraimg
        StudentID = None
        
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        
        while True:
            end = time.time() - self.star
            ret, img = self.cap.read()
            if ret:
                image = img
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if end > 5:
                    faces = RetinaFace.detect_faces(img)
                    if type(faces) == dict:
                        box, landmarks, self.score = (faces['face_1']['facial_area'],
                                                      faces['face_1']['landmarks'],
                                                      faces['face_1']['score'])
                        
                                            #cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color=(255, 0, 0), thickness=2)
                        
                        Face_Area = box[0], box[1], box[2], box[3]
    
                        pkl = os.path.join(self.DB_Path, PKL)
                        StudentID = Face_detection.recognition(image[box[1]: box[3], box[0]:box[2]],pkl ,dddown)
                        start1 = time.time()
                        if self.DB_Path == MASK_PATH:       # Mask
                            end1= time.time() - start1
                            print("StudentID :",StudentID)
                            while True and end1 < 3 and StudentID != None:
                                ret, img1 = self.cap.read()
                                img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                                faces = RetinaFace.detect_faces(img1)
                                if type(faces) == dict:
                                    box, landmarks, self.score = (faces['face_1']['facial_area'],
                                                                 faces['face_1']['landmarks'],
                                                                 faces['face_1']['score'])
                                    left,right ,x = Eye_blink.eye_blink(img1, box, landmarks)
                                    if left <= 0.5 and right <= 0.5:
                                        dis = distance.findCosineDistance(Face_detection.ArcFace(image,True)), Face_detection.ArcFace(img1,True)
                                        if dis < 0.68:
                                            print("학번은 : " + str(StudentID))
                                            Face_detection.save_image(StudentID, image[box[1]: box[3], box[0]:box[2]], self.DB_Path)
                                        
                        else:                               # NoMask
                            end1= time.time() - start1
                            while True and end1 < 3 and StudentID != None:
                                ret, img1 = self.cap.read()
                                img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                                faces = RetinaFace.detect_faces(img1)
                                if type(faces) == dict:
                                    box, landmarks, self.score = (faces['face_1']['facial_area'],
                                                                 faces['face_1']['landmarks'],
                                                                 faces['face_1']['score'])
                                    custom ,x= Emotion.emotion(img1,box)
                                    emo = np.where(custom[0] == max(custom[0]))
                                    print("Emotion : " +objects[emo[0][0]])
                                    print(custom[0]) 
                                    if 'neutral' != objects[emo[0][0]]:
                                        dis = distance.findCosineDistance(Face_detection.ArcFace(image,True)), Face_detection.ArcFace(img1,True)
                                        if dis < 0.68:
                                            print("학번은 : " + str(StudentID))
                                            Face_detection.save_image(StudentID, image[box[1]: box[3], box[0]:box[2]], self.DB_Path)
                                        
                        #print(cameraimg)
                        self.star = time.time()
                    else: 
                        box, landmarks, self.score = None, None, 0
                
            try:
                image = QtGui.QImage(img, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
                self.signal.emit(image)
            except:
                continue
           
    def stop(self):
        Face_detection.save_pickle()
        self.cap.release()
        cv2.destroyAllWindows()
class Face_Status(QtCore.QThread):
    def __init__(self, parent=None):
        super(Face_Status, self).__init__(parent)
    Face_value = QtCore.pyqtSignal(bool)
    def run(self):
        global StudentID
        while True:
            if StudentID in ("unknown","얼굴 인식 안됨", None ):
                self.Face_value.emit(False)
            else:
                self.Face_value.emit(True)
            time.sleep(1)
class Ui_user_face(object):
    def __init__(self, day, week):
        self.daylist = day
        self.weeklist = week
    def setupUi(self, Dialog):
        Dialog.setObjectName("출석")
        Dialog.resize(660, 600)
        Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.grabber = FrameGrabber()
        self.Temp_data_R = Temp_data_recv()
        self.Temp_data_S = Temp_data_send()
        self.temp = Temp_Data()
        self.name = Name_Data()
        self.Face_result = Face_Status()
        self.Face_result.Face_value.connect(self.Button_Status)
        self.temp.signal.connect(self.updateTemp)
        self.name.signal.connect(self.updateName)
        self.grabber.signal.connect(self.updateFrame)
        self.grabber.start()
        self.Temp_data_R.start()
        self.Temp_data_S.start()
        self.temp.start()
        self.name.start()
        self.Face_result.start()
        self.Video = QtWidgets.QLabel(Dialog)
        self.Video.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.Video.setText("")
        self.Video.setObjectName("Video")
        self.Temp = QtWidgets.QLabel(Dialog)
        self.Temp.setGeometry(QtCore.QRect(10, 500, 315, 40))
        self.Temp.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setWeight(75)
        self.Temp.setFont(font)
        self.Temp.setObjectName("Temp")
        self.Name = QtWidgets.QLabel(Dialog)
        self.Name.setGeometry(QtCore.QRect(335, 500, 315, 40))
        self.Name.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setWeight(75)
        self.Name.setFont(font)
        self.Name.setObjectName("Name")
        self.Attend = QtWidgets.QPushButton(Dialog)
        self.Attend.setGeometry(QtCore.QRect(10, 550, 205, 40))
        self.Attend.setObjectName("Attend")
        self.Attend.clicked.connect(lambda : self.choose())
        self.Back = QtWidgets.QPushButton(Dialog)
        self.Back.setGeometry(QtCore.QRect(440, 550, 205, 40))
        self.Back.setObjectName("Back")
        self.Back.clicked.connect(lambda: self.close_video(Dialog))
        self.Change = QtWidgets.QPushButton(Dialog)
        self.Change.setGeometry(QtCore.QRect(225, 550, 205, 40))
        self.Change.setObjectName("Change")
        self.Change.clicked.connect(lambda : self.swap())
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        global recv_data
        Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "출석"))
        self.Temp.setText(_translate("Dialog", "체온 :" + " " + str(recv_data)))
        self.Name.setText(_translate("Dialog", "학번 :"))
        self.Attend.setText(_translate("Dialog", "출석하기"))
        self.Back.setText(_translate("Dialog", "돌아가기"))
        self.Change.setText(_translate("Dialog", "2차 인증(마스크 O)"))
    def updateFrame(self, image):
        self.Video.setPixmap(QtGui.QPixmap.fromImage(image))
    def updateTemp(self, temp):
        self.Temp.setText("체온 :" + " " + temp + "℃")
    def updateName(self, name):
        #print(name)
        self.Name.setText("학번 :" + " " + name)
    def close_video(self,Dialog):#출석중 찍은 사진 피클파일 갱신
        self.grabber.stop() #비디오 멈춤
        Dialog.close()
    def choose(self):#출석중 사진 찍기
        #여기에 DB 출석 함수 넣기c
        global StudentID, save_img, cameraimg, recv_data
        weeklist = ["weekone", "weektwo", "weekthree", "weekfour", "weekfive"]
        curr = datetime.now()
        temp = float(recv_data)
        if int(temp) >= 30:
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Temp_error(recv_data)
            self.ui.setupUi(self.window)
            self.window.show()#창전환
        else:
            try:
                currlimit = self.weeklist[self.daylist.index(curr.date())] - curr
                if currlimit > timedelta(seconds= -1):
                    if currlimit  > timedelta(hours= 3):
                        print("너무 일찍 출석")
                    else:
                        print("출석")
                        print(self.daylist.index(curr.date())+1)
                        atd_upload(StudentID, weeklist[self.daylist.index(curr.date())], "출석")
                elif currlimit > timedelta(hours= -3):
                    print("지각")
                    print(self.daylist.index(curr.date())+1)
                    atd_upload(StudentID, weeklist[self.daylist.index(curr.date())], "지각")
                else:
                    print("결석")
                    print(self.daylist.index(curr.date())+1) 
                    atd_upload(StudentID, weeklist[self.daylist.index(curr.date())], "결석")
            except:
                print("기간아님")
            self.window = QtWidgets.QDialog()
            self.ui = Ui_choose_student_name(StudentID, cameraimg, save_img)
            self.ui.setupUi(self.window)
            self.window.show()#창전환
    def swap(self):
        global dddown
        if self.grabber.DB_Path == MASK_PATH:
            self.Change.setText("2차 인증(마스크 X)")
            self.grabber.DB_Path = NOMASK_PATH
            dddown = 0.45             
        else:
            self.grabber.DB_Path = MASK_PATH
            self.Change.setText("2차 인증(마스크 O)")
            dddown = 0.5            
        print(self.grabber.DB_Path)
    def Button_Status(self, status):
        if status:
            self.Attend.setEnabled(True)
        else:
            self.Attend.setEnabled(False)


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_user_face(curtime[0],curtime[1])
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())