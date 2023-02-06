from Option import *
import Face
import os
import time
import pickle
from tqdm import tqdm
def reset():
    with open(MASK_PKL,"wb") as a:
        pass
    with open(NOMASK_PKL,"wb") as b:
        pass

    a = [MASK_PATH, NOMASK_PATH]
    for i in a:
        pkl_file = os.path.join(i,PKL)
        open_pkl = open(pkl_file,'ab')
        for (root, directories, files) in os.walk(i):
            for file in tqdm(files):
                if '.jpg' in file:
                    path = (os.path.join(root, file))
                    path = path.replace("\\", '/')
                    embedding = Face.Face_detection.ArcFace(path)
                    pickle.dump([path,embedding], open_pkl)
        open_pkl.close()
    
a = input("reset? (y or n)")
if a == "y":
    start =time.time()
    print(start)
    reset()
    print(time.time()-start)