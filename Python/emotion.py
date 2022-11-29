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
cap = cv2.VideoCapture(0)
start = time.time()
def recognition(img):
    Rdict = DeepFace.find(img_path=img, 
                          db_path='D:/Mask_Project/user_img/NoMask',
                          enforce_detection=False,
                          model_name ='ArcFace',
                          detector_backend='retinaface')
    if len(Rdict) != 0:
        #print(os.path.basename(Rdict.iloc[0]['identity']))
        studentID = os.path.basename(Rdict.iloc[0]['identity'])
        studentID = studentID[0:8]
        return studentID
    else:
        #print("None")
        return "Unknown"
    
def plt_emotion_analysis(emotions,x):
    objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    y_pos = np.arange(len(objects))
    
    plt.bar(y_pos, emotions, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('percentage')
    plt.title('emotion')
    plt.show()
    
    x = np.array(x, 'float32')
    x = x.reshape([48, 48])

    plt.gray()
    plt.imshow(x)
    plt.show()
    
def emotion(img, box):
    img = img[box[1]: box[3], box[0]:box[2]].copy()
    img=Image.fromarray(img).convert("L")
    img = img.resize((48, 48), Image.ANTIALIAS)
    x = img_to_array(img)

    x = np.expand_dims(x, axis = 0) 
    x /= 255
    from deepface.extendedmodels import Emotion
    model = Emotion.loadModel()
    custom = model.predict(x)
    return custom,x

mode = "recognition"
while True:
    
    end= time.time()-start
    ret, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if end > 3 and mode == "recognition":
        faces = RetinaFace.detect_faces(img_path = img)
        if type(faces) == dict:
            box, landmarks, score = (faces['face_1']['facial_area'],
                                    faces['face_1']['landmarks'],
                                    faces['face_1']['score'])
            #cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color=(255, 0, 0), thickness=2)
            
            #plt_emotion_analysis(custom[0], x)

            start = time.time()
            mode = "emotion"
            print("StudentID : " +(recognition(img)))
            end= time.time()-start
            
            
    if end > 3 and mode == "emotion":        
        faces = RetinaFace.detect_faces(img_path = img)
        if type(faces) == dict:
            box, landmarks, score = (faces['face_1']['facial_area'],
                                    faces['face_1']['landmarks'],
                                    faces['face_1']['score'])
            #cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color=(255, 0, 0), thickness=2)
            custom ,x= emotion(img,box)
            emo = np.where(custom[0] == max(custom[0]))
            objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')    
            
            print("Emotion : " +objects[emo[0][0]])
            print(custom[0]) 
            start = time.time()
            mode = "recognition"       
         
            
    cv2.putText(img, str(int(end))+" mode : "+mode ,(20, 40), 5, 1, (0, 0, 255), 1)
    cv2.imshow("", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows() 