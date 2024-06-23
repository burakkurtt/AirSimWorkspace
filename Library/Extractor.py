import cv2
from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform
from skimage.transform import EssentialMatrixTransform
import numpy as np


class Extractor():
    def __init__(self, K):
        self.orb = cv2.ORB_create()
        self.last = None
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        self.K = K
        self.Kinv = np.linalg.inv(self.K)

    def extractRt(self, E):
        W = np.mat([[0,-1,0],[1,0,0], [0,0,1]], dtype=float)
        U,d,Vt = np.linalg.svd(E)
        assert np.linalg.det(U) > 0
        if np.linalg.det(Vt) < 0:
            Vt *= -1.0
        R = np.dot(np.dot(U,W), Vt)
        if np.sum(R.diagonal()) < 0:
            R = np.dot(np.dot(U,W.T), Vt)

        t = U[:,2]

        Rt = np.concatenate([R,t.reshape(3,1)], axis=1)

        return Rt


    # Turn [[x,y]] > [[x,y,1]]
    def add_ones(self, x):
        return np.concatenate([x, np.ones((x.shape[0], 1))], axis=1)

    def normalize(self, pt):
        return np.dot(self.Kinv, self.add_ones(pt).T).T[:, 0:2]
    
    def denormalize(self, pt):
        # return int(round(pt[0] + self.H/2)), int(round(pt[1] + self.W/2))
        ret = np.dot(self.K, [pt[0], pt[1], 1.0])
        # print(ret)
        return int(round(ret[0])), int(round(ret[1]))

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
                if m.distance < 0.6*n.distance:
                    kp1 = kps[m.queryIdx].pt
                    kp2 = self.last['kps'][m.trainIdx].pt
                    ret.append((kp1, kp2))

        # Filter
        Rt = None
        if len(ret) > 0:
            ret = np.array(ret)
            # print(ret.shape)
             

            # Normalize coords
            ret[:, 0, :] = self.normalize(ret[:, 0, :])
            ret[:, 1, :] = self.normalize(ret[:, 1, :])

            model,  inliers = ransac((ret[:,0],ret[:,1]), 
                                      EssentialMatrixTransform,
                                    #   FundamentalMatrixTransform,
                                      min_samples=8, 
                                      residual_threshold=1, 
                                      max_trials=500)    
            # print(model.params)
            ret = ret[inliers]
            Rt = self.extractRt(model.params)

        # Return
        self.last = {'kps': kps, 'des': des}
        return ret, Rt