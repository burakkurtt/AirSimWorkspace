import cv2
from Library import Extractor
from Utils import utils

W = 256*2
H = 144*2

extractor = Extractor.Extractor()

def image_process(img):
    img = cv2.resize(img, (W, H))
    
    mathes = extractor.extract(img)

    print("%d mathes" %(len(mathes)))

    for pt1, pt2 in mathes:
        u1, v1 = map(lambda x: int(round(x)), pt1.pt)
        u2, v2 = map(lambda x: int(round(x)), pt2.pt)
        cv2.circle(img, (u1,v1), color=(0,255,0), radius=1)
        cv2.line(img, (u1,v1), (u2,v2), color=(255,0,0))

    utils.display(img)