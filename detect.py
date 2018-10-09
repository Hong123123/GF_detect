import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import config

def LogoDetect(obj_path, scene_path):
    MIN_MATCH_COUNT = 10

    c_img1 = cv.imread(obj_path)  # queryImage
    img1 = cv.cvtColor(c_img1, cv.COLOR_BGR2GRAY)

    c_img2 = cv.imread(scene_path)  # trainImage
    img2 = cv.cvtColor(c_img2, cv.COLOR_BGR2GRAY)

    try:
        img1 = cv.GaussianBlur(img1, (3, 3), 0.5)
        img2 = cv.GaussianBlur(img2, (3, 3), 0.5)

        # Initiate ORB detector
        detector = cv.ORB_create(nfeatures=9999)
        # find the keypoints and descriptors with ORB
        kp1, des1 = detector.detectAndCompute(img1,None)
        kp2, des2 = detector.detectAndCompute(img2,None)

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        flann = cv.FlannBasedMatcher(index_params, search_params)

        # matches = flann.knnMatch(des1,des2,k=2)
        matches = cv.BFMatcher_create().knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance <= 0.7*n.distance:
                good.append(m)

        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()
            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv.perspectiveTransform(pts,M)
            c_img2 = cv.polylines(c_img2,[np.int32(dst)],True,(255, 0, 0),5, cv.LINE_AA)
        else:
            print( "Not enough matches to detect - {}/{}".format(len(good), MIN_MATCH_COUNT) )
            matchesMask = None

        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                           singlePointColor = None,
                           matchesMask = matchesMask, # draw only inliers
                           flags = 2)

        img3 = cv.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
        if config.SHOW_MATCHES:
            plt.imshow(img3, 'gray'),plt.show()

    except:
        print('fail to detect')

    finally:
        return c_img2


if __name__ == '__main__':
    plt.show(plt.imshow(LogoDetect(config.DETECT_OBJ, config.FRAMES_PATH_BASE.format(1))))