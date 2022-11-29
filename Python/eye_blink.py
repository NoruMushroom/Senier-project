from deepface import DeepFace
import cv2
import numpy as np
from retinaface import RetinaFace
import time
from PIL import Image
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import matplotlib.pyplot as plt
import os
from keras.models import load_model
cap = cv2.VideoCapture(0)
start = time.time()
def recognition(img):
    Rdict = DeepFace.find(img_path=img, 
                          db_path=r'D:\Mask_Project\Senier-project\Python\user_img\NoMask',
                          enforce_detection=False,
                          model_name ='ArcFace',
                          detector_backend='retinaface')
    if len(Rdict) != 0:
        studentID = os.path.basename(Rdict.iloc[0]['identity'])
        studentID = studentID[0:8]
        return studentID
    else:
        #print("None")
        return None
    
def plt_eye_analysis(x):
    x[0] = np.array(x[0], 'float32')
    x[0] = x[0].reshape([26, 34])
    plt.title("left")
    plt.gray()
    plt.imshow(x[0])
    plt.show()
    
    x[1] = np.array(x[1], 'float32')
    x[1] = x[1].reshape([26, 34])
    plt.title("right")
    plt.gray()
    plt.imshow(x[1])
    plt.show()
    
def eye_blink(img, box, landmarks):
    face = img[box[1]: box[3], box[0]:box[2]].copy()
    x,y = face.shape[0]//13, face.shape[1]//17
    eye_l = img[int(landmarks['left_eye'][1])-y:int(landmarks['left_eye'][1]+y),
                int(landmarks['left_eye'][0])-x:int(landmarks['left_eye'][0])+x]
    
    eye_r = img[int(landmarks['right_eye'][1])-y:int(landmarks['right_eye'][1]+y),
                int(landmarks['right_eye'][0])-x:int(landmarks['right_eye'][0])+x]
    eye_r = cv2.flip(eye_r, flipCode=1)
    
    
    eye_r=Image.fromarray(eye_r).convert("L")
    eye_l=Image.fromarray(eye_l).convert("L")
    eye_l = eye_l.resize((34, 26), Image.ANTIALIAS)
    eye_r = eye_r.resize((34, 26), Image.ANTIALIAS)
    
    x_r = img_to_array(eye_r)
    x_l = img_to_array(eye_l)
    
    x_l = np.expand_dims(x_l, axis = 0) 
    x_r = np.expand_dims(x_r, axis = 0) 
    
    x_r /= 255
    x_l /= 255

    eye_model = load_model(r'./model/eye_blink_model.h5')
    
    left = eye_model.predict(x_l)
    right = eye_model.predict(x_r)
    return left[0][0], right[0][0] ,[x_l,x_r]

mode = "recognition"
while True:
    
    end= time.time()-start
    ret, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if end > 3 and mode == "recognition":
        faces = RetinaFace.detect_faces(img)
        if type(faces) == dict:
            box, landmarks, score = (faces['face_1']['facial_area'],
                                    faces['face_1']['landmarks'],
                                    faces['face_1']['score'])
            start = time.time()
            mode = "Eye_blink"
            print("StudentID : " +str((recognition(img))))
            end= time.time()-start
            recognition_img = img
            
    if end > 3 and mode == "Eye_blink":        
        faces = RetinaFace.detect_faces(img)
        if type(faces) == dict:
            box, landmarks, score = (faces['face_1']['facial_area'],
                                    faces['face_1']['landmarks'],
                                    faces['face_1']['score'])
            left,right ,x= eye_blink(img,box,landmarks)
            print("left : " +str(left))
            print("right : " +str(right))
            start = time.time()
            mode = "recognition"       
            df = DeepFace.verify(img1_path=img, img2_path=recognition_img, enforce_detection=False,
                               model_name ='ArcFace',detector_backend='retinaface')
            print(df['verified'])
            
    cv2.putText(img, str(int(end))+" mode : "+mode ,(20, 40), 5, 1, (0, 0, 255), 1)
    cv2.imshow("", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows() 