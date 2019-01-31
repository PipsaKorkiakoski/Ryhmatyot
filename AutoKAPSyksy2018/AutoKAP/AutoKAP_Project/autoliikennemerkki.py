import getopt
import cv2
import re
import os
from PIL import Image
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from io import StringIO, BytesIO
import time

SIFT = cv2.xfeatures2d.SIFT_create()
INDEX_PARAMS = None
SEARCH_PARAMS = None
FLANN = None
capture = None
ARGS = None
argdownscale = 2
argminkp = 5
argflann = 0.8
argmatches = 2
nopeus = 0

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
capture.set(cv2.CAP_PROP_FPS, 5)
car_cascade = cv2.CascadeClassifier('haarCascade.xml')

def read_paths(path):
    """Returns a list of files in given path"""
    images = [[] for _ in range(2)]
    for dirname, dirnames, _ in os.walk(path):
        for subdirname in dirnames:
            filepath = os.path.join(dirname, subdirname)
            for filename in os.listdir(filepath):
                try:
                    imgpath = str(os.path.join(filepath, filename))
                    images[0].append(imgpath)
                    limit = re.findall('[0-9]+', filename)
                    images[1].append(limit[0])
                except IOError as err:
                    print("I/O error")
                except:
                    print("I/O error 2")
                    raise
    return images

def load_images(imgpath):
    """Loads images in given path and returns
     a list containing image and keypoints"""
    images = read_paths(imgpath)
    imglist = [[], [], [], []]
    cur_img = 0
    SIFT = cv2.xfeatures2d.SIFT_create()
    for i in images[0]:
        img = cv2.imread(i, 0)
        imglist[0].append(img)
        imglist[1].append(images[1][cur_img])
        cur_img += 1
        keypoints, des = SIFT.detectAndCompute(img, None)
        imglist[2].append(keypoints)
        imglist[3].append(des)
    return imglist


def run_flann(img):
    """Run FLANN-detector for given image with given image list"""
    # Find the keypoint descriptors with SIFT
    _, des = SIFT.detectAndCompute(img, None)
    if des is None:
        return "Unknown", 0
    if len(des) < argminkp:
        return "Unknown", 0

    biggest_amnt = 0
    biggest_speed = 0
    cur_img = 0
    try:
        for _ in IMAGES[0]:
            des2 = IMAGES[3][cur_img]
            matches = FLANN.knnMatch(des2, des, k=2)
            matchamnt = 0
    # Find matches with Lowe's ratio test
            for _, (moo, noo) in enumerate(matches):
                if moo.distance < argflann*noo.distance:
                    matchamnt += 1
            if matchamnt > biggest_amnt:
                biggest_amnt = matchamnt
                biggest_speed = IMAGES[1][cur_img]
            cur_img += 1
        if biggest_amnt > argminkp:
            return biggest_speed, biggest_amnt
        else:
            return "Unknown", 0
    except getopt.GetoptError as e:
        return "Unknown", 0

IMAGES = load_images("data")

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        lastlimit = "00"
        lastdetect = "00"
        downscale = argdownscale
        matches = 2
        possiblematch = "00"
        timeInterval = 1
        lastTime = 0
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()

            while True:
                try:
                   #tästä poistettu koodi muistiossa
                    rc, img = capture.read()
                    origframe = img
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = cv2.resize(img, (128, 128))
                    comp = "Unknown"
                    comp, amnt = run_flann(img)

                    if comp != "Unknown":
                        if comp != lastlimit:
                            if comp == lastdetect:
                                possiblematch = comp
                                matches = matches + 1
                                if matches >= argmatches:
                                    lastlimit = possiblematch
                                    matches = 0
                            else:
                                possiblematch = "00"
                                matches = 0
                    else:
                        #print("Unknow speed limit")
                        comp = lastdetect

                    lastdetect = comp
                    cv2.putText(
                        origframe,
                        "Current speed limit: " + str(lastlimit) + " km/h.",
                        (5, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2
                    )

                    imgRGB = origframe
                    imgRGB = cv2.resize(imgRGB, (320, 240))
                    jpg = Image.fromarray(imgRGB)
                    tmpFile = BytesIO()
                    jpg.save(tmpFile, 'JPEG')
                    self.wfile.write("--jpgboundary".encode())
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(tmpFile.getbuffer().nbytes))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')


                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>'.encode())
            self.wfile.write('<img src="http://172.20.10.9:8080/cam.mjpg"/>'.encode())
            self.wfile.write('</body></html>'.encode())
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    try:
        server = ThreadedHTTPServer(('', 8080), CamHandler)
        print("Server started")
        server.serve_forever()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    INDEX_PARAMS = dict(algorithm=0, trees=5)
    SEARCH_PARAMS = dict(checks=50)  # or pass empty dictionary

    FLANN = cv2.FlannBasedMatcher(INDEX_PARAMS, SEARCH_PARAMS)
    main()
