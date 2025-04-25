import cv2
from pathlib import Path 
from PIL import Image

folder = Path ('./reals/')

tot = 500
for path in folder.glob('*.jpg') : 
    img = cv2.imread ('./reals/' + path.name)
    img = cv2.resize (img, (256, 256), interpolation=cv2.INTER_AREA)
    height, weight = img.shape[0], img.shape[1]
    if height != 256 or weight != 256 : 
        continue 
    objective = "./reals_regu/" + str(tot) + ".jpg"
    cv2.imwrite (objective, img)
    tot = tot - 1
    if tot == 0 : 
        break

