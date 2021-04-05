import argparse
import logging
import os

import cv2
import numpy as np
import requests
from tqdm import tqdm

from plot_bbox import plot_bbox, box_resize

logfilepath = ""
if os.path.isfile(logfilepath):
    os.remove(logfilepath)
logging.basicConfig(filename=logfilepath, level=logging.INFO)

def RunHttpClientImage(input="sample.jpg", output="result.jpg", classfile="class.txt", size=(512, 512), thresh=0.5, save_image=True):

    try:
        class_names =np.genfromtxt(classfile,  dtype=str)
    except:
        raise FileExistsError

    if not os.path.exists(input):
        raise FileExistsError

    dir, filename = os.path.split(output)
    if not dir == '':
        os.makedirs(dir)

    ids = []
    scores = []
    boxes = []
    image = cv2.imread(input, flags=cv2.IMREAD_COLOR)
    theight, twidth, _ = image.shape
    # 서버  호출
    '''
    requests.post argument data: (optional) Dictionary, list of tuples, bytes, or file-like
    object to send in the body of the :class:`Request`.
    '''
    _, data = cv2.imencode('.jpg', image)
    respose = requests.post(URL, data=data.tobytes(order='C')).json()

    print(respose)
    # if respose["objects"] != None:
    #     for rb in respose["objects"]:
    #         ids.append([rb['object_id']])
    #         scores.append([rb['score']])
    #         boxes.append([rb['x'], rb['y'], rb['x'] + rb['w'], rb['y'] + rb['h']])
    #     boxes = box_resize(np.array(boxes), (size[0], size[1]), (twidth, theight))
    # else:
    #     print("Request failed")

    # plotted_image = plot_bbox(origin_image, boxes, scores=scores, ids=ids, thresh=thresh, class_names = class_names)
    # if save_image:
    #     cv2.imwrite(output, plotted_image)
    # cv2.imshow("image", plotted_image)
    # cv2.waitKey(1)

    cv2.destroyAllWindows()


def RunHttpClientVideo(input="sample.mp4", output="result.mp4", classfile="class.txt", size=(512, 512), thresh=0.5, save_video=True):

    try:
        class_names =np.genfromtxt(classfile,  dtype=str)
    except:
        raise FileExistsError

    if not os.path.exists(input):
        raise FileExistsError

    dir, filename = os.path.split(output)
    if not dir == '':
        os.makedirs(dir)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    cap = cv2.VideoCapture(input)
    nframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    twidth  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    theight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output, fourcc, fps, (twidth, theight))

    # while(cap.isOpened()):
    for _ in tqdm(range(0, nframe)):
        ret, image = cap.read()
        if ret:
            ids = []
            scores = []
            boxes = []
            origin_image = image.copy()
            #image = cv2.resize(image, (size[0], size[1]), interpolation=cv2.INTER_AREA)
            # 서버  호출
            '''
            requests.post argument data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
            '''
            _, data = cv2.imencode('.jpg', image)
            respose = requests.post(URL, headers={'camera_id': '0'}, data=data.tostring())
            #respose = requests.post(URL, headers={'camera_id': '0'}, data=data.tobytes(order='C')).json()
            if respose["objects"] != None:
                for rb in respose["objects"]:
                    ids.append([rb['object_id']])
                    scores.append([rb['score']])
                    boxes.append([rb['x'], rb['y'], rb['x'] + rb['w'], rb['y'] + rb['h']])
                boxes = box_resize(np.array(boxes), (size[0], size[1]), (twidth, theight))
            else:
                print("Request failed")

            plotted_image = plot_bbox(origin_image, boxes, scores=scores, ids=ids, thresh=thresh, class_names = class_names)
            if save_video:
                out.write(plotted_image)
            cv2.imshow("image", plotted_image)
            cv2.waitKey(1)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    # https://greeksharifa.github.io/references/2019/02/12/argparse-usage/
    parser = argparse.ArgumentParser(description='python http client')
    parser.add_argument('--address', type=str, help="address:port", default="10.40.111.194:8080")
    parser.add_argument('--image', type=str, help="input image", default="sample.jpg")
    parser.add_argument('--video', type=str, help="input video", default="sample.mp4")

    parser.add_argument('--outimage', type=str, help="output image", default="result.jpg")
    parser.add_argument('--outvideo', type=str, help="output video", default="result.mp4")
    parser.add_argument('--classfile', type=str, help="class file", default="class.txt")

    parser.add_argument('--size', type=int, nargs=2, help='width height', default=[512, 512])
    parser.add_argument('--thresh', type=float, help='visual threshold', default=0.1)

    parser.add_argument('--saveimage', type=bool, help="image save?", default=True)
    parser.add_argument('--savevideo', type=bool, help="video save?", default=True)
    args = parser.parse_args()

    URL = 'http://' + args.address + "/predictions/facedetector" # 이미지 분석 요청
    RunHttpClientImage(input=args.image, output=args.outimage, classfile = args.classfile, size=args.size, thresh=args.thresh, save_image=args.saveimage)
    #RunHttpClient(input=args.image, output=args.outvideo, classfile = args.classfile, size=args.size, thresh=args.thresh, save_video=args.savevideo)

