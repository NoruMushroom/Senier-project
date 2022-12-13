from tkinter import Frame
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import re
import numpy as np
import os
from sqlalchemy import false
from Face_detection import *
from __default__ import NoMask_DB_Path
from retinaface import RetinaFace
embedding_list = []

class FrameGrabber(QtCore.QThread):
    signal = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self, parent=None):
        super(FrameGrabber, self).__init__(parent)
        self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.frame = None
        self.save_file = None
        self.score = 0.1
        self.face = None
    def run(self):
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        while True:
            self.success, self.frame = self.cap.read()
            if self.success:
                self.save_file = self.frame
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                faces = RetinaFace.detect_faces(self.frame)
                if type(faces) == dict:
                    self.face = faces['face_1']
                    self.box, landmarks, self.score = (self.face['facial_area'],
                                                       self.face['landmarks'],
                                                       self.face['score'])
                    cv2.rectangle(self.frame, (self.box[0], self.box[1]), (self.box[2], self.box[3]), color=(255, 0, 0), thickness=2)
                else:
                    self.box, landmarks, self.score = None, None, 0
            try:
                
                image = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
                self.signal.emit(image)
            except:
                continue
                
    def stop(self):
        self.cap.release()
class Ui_user_photo(object):
    def __init__(self,message):
        self.name = message
    def setupUi(self, Dialog):
        Dialog.setObjectName("사진 촬영")
        Dialog.resize(660, 550)
        self.count = 0
        self.grabber = FrameGrabber()
        self.grabber.signal.connect(self.updateFrame)
        self.grabber.start()
        self.Photo = QtWidgets.QPushButton(Dialog)
        self.Photo.setGeometry(QtCore.QRect(10, 500, 640, 40))
        self.Photo.setObjectName("Photo")
        self.Photo.clicked.connect(lambda : self.Take_photo(self.name, self.grabber.save_file, self.grabber.score, Dialog,self.grabber.face))
        #self.Back = QtWidgets.QPushButton(Dialog)
        #self.Back.setGeometry(QtCore.QRect(335, 500, 315, 40))
        #self.Back.setObjectName("Back")
        #self.Back.clicked.connect(lambda : self.close_video(Dialog, self.name))
        self.Video = QtWidgets.QLabel(Dialog)
        self.Video.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.Video.setText("")
        self.Video.setObjectName("Video")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        Dialog.setWindowTitle(_translate("Dialog", "사진 촬영"))
        self.Photo.setText(_translate("Dialog", "사진 촬영" + "("+ str(self.count) + "장" + ")"))
        #self.Back.setText(_translate("Dialog", "돌아가기"))

    def Take_photo(self, StudentID, frame, score, Dialog,face  ):
        file_path = ""
        global embedding_list    
        studentid_path = os.path.join(NoMask_DB_Path, str(StudentID))
        if score > 0.9:
            for (root, directories, files) in os.walk(studentid_path):
                for file in files:
                    if '.jpg' in file:
                        file_path = os.path.join(root, file)
                        
            if file_path == "":
                file_path = os.path.join(studentid_path, str(StudentID) + "_000.jpg")
                            
            number = os.path.basename(file_path)
            number = int(number[-7:-4]) + 1
            number = format(number, '03')
            savePath = os.path.join(os.path.dirname(file_path),
                                    os.path.basename(file_path)[0:8] + "_" +
                                    number + os.path.splitext(file_path)[1])
            
            savePath = savePath.replace("\\", "/")
            
            embedding_list.append(savePath)
            box, landmarks,= (face['facial_area'],face['landmarks'],)
            frame = postprocess.alignment_procedure(frame, landmarks['right_eye'],
                                                    landmarks['left_eye'],
                                                    landmarks['nose'])
            frame= frame[box[1]: box[3], box[0]:box[2]].copy()
            cv2.imwrite(savePath, frame)
            with open(r"Python\user_img\User_Register.txt", "a") as f:
                f.write(savePath+'\n')
            if self.count == 4:
                Dialog.close()
                self.close_video(Dialog, self.name)
                
            self.count = self.count + 1
            self.Photo.setText("사진 촬영" + "("+ str(self.count) + "장" + ")")    
    

    def updateFrame(self, image):
        self.Video.setPixmap(QtGui.QPixmap.fromImage(image))
    def close_video(self,Dialog,StudentID):
        if self.count == 4:
            exists_Pickle()
            global embedding_list
            for i in embedding_list: # 파일 피클 파일 생성
                embedding = ArcFace(i)
            with open(default.PKL_NoMask_Path ,"ab") as t:
                pickle.dump([i, embedding], t)
            save_masked_image(embedding_list)
            self.grabber.stop()
            embedding_list = []
            Dialog.close()
        self.count = self.count + 1
        self.Photo.setText("사진 촬영" + "("+ str(self.count) + "장" + ")")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_user_photo()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    
