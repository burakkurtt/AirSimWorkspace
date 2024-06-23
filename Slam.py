import cv2
from Library import Extractor
from Utils import utils
import numpy as np

W = 256*2
H = 144*2

F = 160
K = np.array([[F,0,W//2],[0,F,H//2], [0,0,1]])

extractor = Extractor.Extractor(K)

def image_process(img):
    img = cv2.resize(img, (W, H))

    matches, pose = extractor.extract(img)

    if pose is None:
        return

    print("%d mathes" %(len(matches)))
    print(pose)

    for pt1, pt2 in matches:
        u1, v1 = extractor.denormalize(pt1)
        u2, v2 = extractor.denormalize(pt2)
        cv2.circle(img, (u2,v2), color=(0,255,0), radius=1)
        cv2.line(img, (u2,v2), (u1,v1), color=(255,0,0))

    utils.display(img)

