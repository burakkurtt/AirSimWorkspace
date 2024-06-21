import cv2

class Extractor():
    def __init__(self):
        self.orb = cv2.ORB_create()
        self.last = None
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    def extract(self, img):
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detection
        feats = cv2.goodFeaturesToTrack(grayImg, maxCorners=3000, qualityLevel=0.01, minDistance=3)
        
        # Extraction
        kps = []
        for f in feats:
            kp = cv2.KeyPoint(x=f[0][0], y=f[0][1], size=1)
            kps.append(kp)
        kps, des = self.orb.compute(img, kps)
        
        # Matching
        ret = []
        if self.last is not None:
            matches = self.bf.knnMatch(des, self.last['des'], k=2)
            for m,n in matches:
                if m.distance < 0.75*n.distance:
                    ret.append((kps[m.queryIdx], self.last['kps'][m.trainIdx]))
    
        self.last = {'kps': kps, 'des': des}
        
        return ret