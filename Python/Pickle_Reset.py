import __default__  as default
from Face_detection import *
import os
import time

def reset():
    with open(default.PKL_Mask_Path,"wb") as a:
        pass
    with open(default.PKL_NoMask_Path,"wb") as b:
        pass

    a = [default.Mask_DB_Path, default.NoMask_DB_Path]
    for i in a:
        pkl_file = os.path.join(i,default.pkl)
        open_pkl = open(pkl_file,'ab')
        for (root, directories, files) in os.walk(i):
            for file in files:
                if '.jpg' in file:
                    path = (os.path.join(root, file))
                    path = path.replace("\\", '/')
                    embedding = ArcFace(path)
                    pickle.dump([path,embedding], open_pkl)
        open_pkl.close()
    
a = input("reset? (y or n)")
if a == "y":
    start =time.time()
    print(start)
    reset()
    print(time.time()-start)