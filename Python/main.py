from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
import time
import sys
import os
from Option import *
from user_create import Ui_user_create
from user_delete import Ui_user_delete
from user_face import Ui_user_face
from sign_in import Ui_user_sign_in
from DB.filelist import *
from DB.user_list import user_list
import DB.appfilesave as App
from datetime import timedelta, datetime


week_list, day_list = [], []
first = ATDATE
curr = datetime.now()
user_list(HOST, PORT, USER, PWD)

for i in range(0, 5):
    second = first + timedelta(weeks = i)
    week_list.append(second)
    day_list.append(second.date())
try:
    currlimit = week_list[day_list.index(curr.date())]
except ValueError as e:
    currlimit = None
    print('main except', str(datetime.now()), e)
    
        
class Photo_data_recv(QtCore.QThread): 
    '''Measure the similarity of pictures received from the app'''
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent = None):
        super(Photo_data_recv, self).__init__(parent)

    def run(self):
        while True:
            file_list, new_list, delete_list = [], [], []
            filelist()
            for (root, directories, files) in os.walk(TEMP_PATH):
                for file in files:
                    if ".jpg" in file:
                        file_list.append(str(file[0:8]))
            if not file_list is []:
                for id in file_list:
                    if id not in new_list:            
                        new_list.append(id)
                print("new_list : "+ str(new_list)) 
                       
                for new_id in new_list:
                    App.app_verify(new_id)
                user_list()
                
            delete_list = delete_userlist()
            print("delete_list:", delete_list)
            for del_id in delete_list:
                delete_pickle(del_id)
            user_list()
            time.sleep(10)
            

class Ui_MainWindow(object):
    def Late(self):
        global day_list, week_list
        day_list.clear()
        week_list.clear()
        for i in range(0, 5):
            now = datetime.now()
            ymdh = datetime(first.year, first.month, first.day, (now.hour-1))
            second = ymdh + timedelta(weeks=i)
            week_list.append(second)
            day_list.append(second.date())
        try:
            currlimit = week_list[day_list.index(curr.date())]
            self.Present_Time.setText("수업 시간 : "+ str(currlimit))
        except:
            self.Present_Time.setText("수업 시간 : None")
            
    def Absent(self):
        global day_list, week_list
        day_list.clear()
        week_list.clear()
        for i in range(0,5):
            now = datetime.now()
            ymdh = datetime(first.year, first.month, first.day, (now.hour-4))
            second = ymdh + timedelta(weeks=i)
            week_list.append(second)
            day_list.append(second.date())
        try:
            currlimit = week_list[day_list.index(curr.date())]
            self.Present_Time.setText("수업 시간 : "+ str(currlimit))
        except:
            self.Present_Time.setText("수업 시간 : None")
            
    def Attend(self):
        global day_list, week_list
        day_list.clear()
        week_list.clear()
        for i in range(0, 5):
            now = datetime.now()
            ymdh = datetime(first.year, first.month, first.day, (now.hour+1))
            second = ymdh + timedelta(weeks=i)
            week_list.append(second)
            day_list.append(second.date())
        try:
            currlimit = week_list[day_list.index(curr.date())]
            self.Present_Time.setText("수업 시간 : "+ str(currlimit))
        except:
            self.Present_Time.setText("수업 시간 : None")
            
    def sign_in_window(self):   
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_sign_in()
        self.ui.setupUi(self.window)
        self.window.show()      # 창전환
        
    def sign_up_window(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_create()
        self.ui.setupUi(self.window)
        self.window.show()      # 창전환
        
    def delete_user_window(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_delete()
        self.ui.setupUi(self.window)
        self.window.show()      # 창전환
        
    def face_matching_window(self):
        global day_list, week_list
        lines = []      # 학번 이름이 저장된 리스트
        with open(r"Python\DB\User_List.txt") as f: 
            lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        print("Name :",lines)
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_face(day_list, week_list)
        self.ui.setupUi(self.window)
        self.window.show()      # 창전환
        
    def setupUi(self, MainWindow):          
        MainWindow.setObjectName("메인")
        MainWindow.resize(1920, 1080)
        self.File_path = None
        self.Photo_data_R = Photo_data_recv()
        self.Photo_data_R.start()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Late_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.Late_Btn.setGeometry(QtCore.QRect(1670, 100, 211, 45))
        self.Late_Btn.setObjectName("Late_Btn")
        self.Absent_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.Absent_Btn.setGeometry(QtCore.QRect(1670, 150, 211, 45))
        self.Absent_Btn.setObjectName("Absent_Btn")
        self.Attend_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.Attend_Btn.setGeometry(QtCore.QRect(1670, 50, 211, 45))
        self.Attend_Btn.setObjectName("Attend_Btn")
        self.User_del = QtWidgets.QPushButton(self.centralwidget)
        self.User_del.setGeometry(QtCore.QRect(1430, 890, 211, 91))
        self.User_del.setObjectName("User_del")
        self.Logo = QtWidgets.QLabel(self.centralwidget)
        self.Logo.setGeometry(QtCore.QRect(10, 920, 218, 60))
        self.Logo.setText("")
        self.Logo.setObjectName("Logo")
        self.User_create = QtWidgets.QPushButton(self.centralwidget)
        self.User_create.setGeometry(QtCore.QRect(1190, 890, 211, 91))
        self.User_create.setObjectName("User_create")
        self.User_face = QtWidgets.QPushButton(self.centralwidget)
        self.User_face.setGeometry(QtCore.QRect(950, 890, 211, 91))
        self.User_face.setObjectName("User_face")
        self.User_login = QtWidgets.QPushButton(self.centralwidget)
        self.User_login.setGeometry(QtCore.QRect(1670, 890, 211, 91))
        self.User_login.setObjectName("User_login")
        self.Present_Time = QtWidgets.QLabel(self.centralwidget)
        self.Present_Time.setGeometry(QtCore.QRect(1670, 10, 211, 30))
        self.Present_Time.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "메인"))
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.User_del.setText(_translate("MainWindow", "사용자 삭제"))  
        self.User_create.setText(_translate("MainWindow", "사용자 등록"))
        self.User_face.setText(_translate("MainWindow", "출석하기"))
        self.User_login.setText(_translate("MainWindow", "관리자 모드"))
        self.Late_Btn.setText(_translate("MainWindow", "지각"))
        self.Absent_Btn.setText(_translate("MainWindow", "결석"))
        self.Attend_Btn.setText(_translate("MainWindow", "출석"))
        self.Present_Time.setText(_translate("MainWindow", "수업 시간 : "+str(currlimit)))
        self.User_create.clicked.connect(lambda: self.sign_up_window())
        self.User_del.clicked.connect(lambda : self.delete_user_window())
        self.User_face.clicked.connect(lambda : self.face_matching_window())
        self.User_login.clicked.connect(lambda : self.sign_in_window())
        self.Attend_Btn.clicked.connect(lambda : self.Attend())
        self.Late_Btn.clicked.connect(lambda : self.Late())
        self.Absent_Btn.clicked.connect(lambda : self.Absent())
        Logo =QPixmap('./Logo/Logo.png')
        self.Logo.setPixmap(Logo)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    File = open(r".\Python\Ui\Devsion.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())