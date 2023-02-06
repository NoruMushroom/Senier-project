# app 에서 사진 찍은 경우
# 피클 리스트 만들기
# 마스크 벗은 얼굴
import os
import mysql.connector
from deepface.commons import distance
import os
import cv2
import pickle
import Option
import shutil
from Face import *
from ..Option import *



# app 파일 매칭
def app_verify(Name):                               # 수정 5/23
    print("매칭 중 : " + str(Name))
    app_file_list = []
    for (root, directories, files) in os.walk(TEMP_PATH):
                                for file in files:
                                    if str(Name) in file:
                                        file_path = os.path.join(root, file)
                                        file_path = file_path.replace("\\", "/")
                                        app_file_list.append(file_path)
    one, two = 0,-1
    for_exit = False     
    for i in range(0,len(app_file_list)): 
        one = i
        for j in range(1,len(app_file_list)):
            two = j
            if i < j:                
                dis = distance.findCosineDistance(Face_detection.ArcFace(app_file_list[i],True), Face_detection.ArcFace(app_file_list[j],True))
                if dis > 0.68:               # 거리값 
                    for_exit = True
                    print("사진 안맞음")
                    break 
        if for_exit:
            break
        

    if for_exit == False and one == two:                                  #사진이 맞을때
        print("다 맞음")
        pickle_upload(app_file_list, Name)        # 사진 저장
        try:
            os.rmdir(TEMP_PATH +"/"+ Name)
        except OSError:
            print("디렉터리가 비어 있지 않습니다")    
        try:
            connection = mysql.connector.connect(host='39.124.26.132',
                                                database='student',
                                                user='root',
                                                password='123456')

            cursor = connection.cursor(prepared = True)
            sql = 'UPDATE user SET renewal = 3 WHERE userID = %s;'

            data = (str(Name), )
            cursor.execute(sql, data)
            connection.commit()
            print("업로드 완료")

        except mysql.connector.Error as error:
            print("업로드 실패 {}".format(error))

        else:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("접속 종료")      
    elif for_exit:                                   # 사진이 매칭 안될 때(삭제)
        print("매칭안된 파일\n" + app_file_list[one] +"\n" +app_file_list[two])
        for k in app_file_list:
            if os.path.isfile(k):
                os.remove(k)
        try:
            os.rmdir(Option.Photo_Path +"/"+ Name)
        except OSError:
            print("디렉터리가 비어 있지 않습니다")        
        print("delete :" + str(app_file_list))
        
        try:
            connection = mysql.connector.connect(host='39.124.26.132',
                                                database='student',
                                                user='root',
                                                password='123456')

            cursor = connection.cursor(prepared = True)
            sql = 'UPDATE user SET renewal = 2 WHERE userID = %s;'

            data = (str(Name), )
            cursor.execute(sql, data)
            connection.commit()
            print("업로드 완료")

        except mysql.connector.Error as error:
            print("업로드 실패 {}".format(error))

        else:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("접속 종료")
    


def pickle_upload(img_list, Name):
    '''
    Save Image to Pickle File
    Name : StudentID
    '''
    
    Save_Folder_Path = NOMASK_PATH + "/" + str(Name)         # 폴더 없으면 생성
    Save_MaFolder_Path = MASK_PATH + "/" + str(Name)
    
    try:
        if not os.path.exists(Save_Folder_Path):
            os.makedirs(Save_Folder_Path)
        if not os.path.exists(Save_MaFolder_Path):
            os.makedirs(Save_MaFolder_Path)    
    except OSError:
        print("Error: Failed to create the directory.")
        
    path = ""
    for (root, directories, files) in os.walk(Save_Folder_Path):
        for file in files:
            if str(Name) in file:
                path = os.path.join(root, file)
                                        
    if path == "":
       path = os.path.join(Save_Folder_Path, str(Name) + "_001.jpg")
       
    number = os.path.basename(path)
    number = int(number[-7:-4])
    save_path = os.path.join(os.path.dirname(path),
                                os.path.basename(path)[0:8] + "_" + 
                            format(number, '03') + os.path.splitext(path)[1])
    save_path = save_path.replace("\\", "/")
    
    b = []
    for k in img_list:
        shutil.move(k, save_path)
        cv2.imwrite(save_path,Face_detection.face_box(save_path))
        b.append(save_path)
        number += 1
        # dir , studentID + _ + number:int + extension
        savePath = os.path.join(os.path.dirname(save_path),
                                 os.path.basename(save_path)[0:8] + "_" + 
                                format(number, '03') + os.path.splitext(save_path)[1])
        savePath = savePath.replace("\\", "/")
            
    
    for i in b:
        embedding = Face_detection.ArcFace(i)
        with open(Option.PKL_NoMask_Path, "ab") as p:
            pickle.dump([i, embedding], p)
    Face_detection.save_masked_image(b)                      # mask 임베딩

    print("업로드 및 nomask 사진 이동 완료")

