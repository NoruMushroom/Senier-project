from retinaface import RetinaFace
from deepface import DeepFace
import os
import pickle
import __default__ as default
import cv2

#------------------------
mask_file_patha = ""
embedding_list_No = []
file_list = []
count = 0
embedding_list = []
#------------------------
down = 0.35
up = 0.05
embedding_list_No = []
embedding_list_Ma = []
fail_count = 0                           
                            
def save_pickle():
    '''Add the latest face image'''
    print("파일 추가중입니다.")
    with open(default.PKL_NoMask_Path,"wb") as m:
        pkl_m= pickle.load(m)
    with open(default.PKL_NoMask_Path,"wb") as n:
        pkl_n= pickle.load(n)
    with open("NoMask.txt") as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    for i in lines:
        embedding = DeepFace.represent(img_path = i,
                                       model_name = 'ArcFace',
                                       detector_backend = 'retinaface')
        path_embedding = [i, embedding]
        pkl_n.append(path_embedding)
    with open(default.PKL_NoMask_Path,"ab") as train:
        pickle.dump(pkl_n, train)
    
    with open("Mask.txt") as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    for i in lines:
        embedding = DeepFace.represent(img_path = i, 
                                       model_name = 'ArcFace',
                                       detector_backend = 'retinaface')
        path_embedding = [i, embedding]
        pkl_m.append(path_embedding)
    with open(default.PKL_Mask_Path,"ab") as train:
        pickle.dump(pkl_m, train)    
            
    print("파일 추가 완료")
    with open('NoMask.txt','w',encoding='UTF-8') as f:
            pass
    with open('Mask.txt','w',encoding='UTF-8') as f:
            pass
        
def save_image(id, img, img_db):
    path = os.path.join(img_db,id)
    save_path = ""
    for (root, directories, files) in os.walk(path):
        for file in files:
            if '.jpg' in file:
                save_path = os.path.join(root, file)
    if save_path == "":
        save_path =  os.path.join(f"{path}/", str(id) + "_001.jpg" )
        

    number = os.path.basename(save_path)
    number = int(number[-7:-4]) + 1
    number = format(number, '03')
    # dir , studentID + _ + number + extension
    save_path = os.path.join(os.path.dirname(save_path),
                            os.path.basename(save_path)[0:8] + "_" + number + os.path.splitext(save_path)[1])
    save_path = save_path.replace("\\", "/")
    cv2.imwrite(save_path, img)                
    save_list(save_path)
    
    
        
def save_list(path:str):
    ''' Insert attendance completed face image '''
    if "NoMask" in path:
        with open('NoMask.txt','a',encoding='UTF-8') as f:
                f.write(path +'\n')
    else: 
        with open('Mask.txt','a',encoding='UTF-8') as ff:
                ff.write(path +'\n') 
             
def exists_Pickle(): 
    ''' Create a pickle file if it does not exist '''
    if not os.path.exists(default.PKL_Mask_Path):
        with open(default.PKL_Mask_Path,"wb") as a:
            pickle.dump([], a)
    if not os.path.exists(default.PKL_NoMask_Path):
        with open(default.PKL_NoMask_Path,"wb") as b:
            pickle.dump([], b)

            
def save_masked_image(path_list:list):
    '''
    Cover the underside of the nose from the face bounding box using a white box
    
    list = ```image path```
    '''
    with open(default.PKL_Mask_Path ,"rb") as r:
        pkl = pickle.load(r)
    
    for path in path_list:    
        maskedImagePath = ""
        studentID = os.path.basename(path)[0:8]
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = RetinaFace.detect_faces(img)
        if type(faces) == dict:
                box, landmarks, score = (faces['face_1']['facial_area'],
                                        faces['face_1']['landmarks'],
                                        faces['face_1']['score'])
        else:
            box, landmarks, score = [], [], 0        
            print("face not found")
            return
            
            
        b = box[3] + box[1]
        b = b / 100 * 50
        cv2.rectangle(img, (box[0], int(b)), (box[2], box[3]), color=(255, 255, 255), thickness=-1)
        for (root, directories, files) in os.walk(f"{default.Mask_DB_Path}/{studentID}"):
            for file in files:
                if '.jpg' in file:
                    maskedImagePath = os.path.join(root, file)
                    
        if maskedImagePath == "":
            maskedImagePath =  os.path.join(f"{default.Mask_DB_Path}/{studentID}",
                                            str(studentID) + "_001.jpg" )
        

        number = os.path.basename(maskedImagePath)
        number = int(number[-7:-4]) + 1
        number = format(number, '03')
        # dir , studentID + _ + number + extension
        savePath = os.path.join(os.path.dirname(maskedImagePath),
                                os.path.basename(maskedImagePath)[0:8] + "_" + number + os.path.splitext(maskedImagePath)[1])
        savePath = savePath.replace("\\", "/")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(savePath, img)
        embedding = DeepFace.represent(img_path = savePath,
                                    enforce_detection = False,
                                    model_name ='ArcFace', 
                                    detector_backend = 'retinaface')
        user_list = [savePath,embedding]
        pkl.append(user_list)
    with open(default.PKL_Mask_Path ,"wb") as w:
        pickle.dump(pkl, w)   
        
        
        
def recognition(img, box, img_db):
    Rdict = DeepFace.find(img_path=img, 
                          db_path=img_db,
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
        
        
        
        
        
        
        
        
                  
exists_Pickle()
