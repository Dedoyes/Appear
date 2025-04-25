import cv2 
import numpy as np 
from pathlib import Path 

folder = Path ('./reals/')

tot = 20
for path in folder.glob('*.jpg') : 
    img = cv2.imread ('./reals/' + path.name)
    img = cv2.resize (img, (512, 512), interpolation=cv2.INTER_AREA)
    height, weight = img.shape[0], img.shape[1]
    print (img.shape)
    objective = "./reals_regu/" + str(tot) + ".jpg"
    cv2.imwrite (objective, img)
    dx = cv2.Sobel (img, -1, dx=1, dy=0, ksize=3)
    dx = cv2.convertScaleAbs (dx)
    dy = cv2.Sobel (img, -1, dx=0, dy=1, ksize=3)
    dy = cv2.convertScaleAbs (dy)
    dst = cv2.add (dx, dy)
    grey = cv2.cvtColor (dst, cv2.COLOR_BGR2GRAY)
    final = np.zeros ((512, 512, 1), np.uint8)
    for i in range (512) : 
        for j in range (512) : 
            final[i, j] = 255 - grey[i, j]
            if final[i, j] < 128 : 
                final[i, j] = 0
            else : 
                final[i, j] = 255
    fileName = "./sketch/" + str (tot) + ".jpg"
    cv2.imwrite (fileName, final)
    tot = tot - 1
    if tot == 0 : 
        break
