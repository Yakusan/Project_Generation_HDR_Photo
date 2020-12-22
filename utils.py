import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob

def load_images_from_folder(folder, imagesType):
    images = []
    for type in imagesType:
        filenames = glob.glob(folder + '/' + type)
        if(len(filenames) > 0):
            for filename in filenames:
                images.append(cv2.imread(filename).astype(np.uint8))

            break

    return images


def toLog(val):
    return np.array(np.log(val), dtype=np.float64)


def plot_ResponseCurves(ag):
    px = list(range(0,256))
    plt.figure(constrained_layout=False,figsize=(5,5))
    plt.title("Response curves for BGR", fontsize=20)
    plt.plot(px,np.exp(ag[2]),'r')
    plt.plot(px,np.exp(ag[1]),'g')
    plt.plot(px,np.exp(ag[0]),'b')
    plt.ylabel("log Exposure X", fontsize=20)
    plt.xlabel("Pixel value Z", fontsize=20)
    plt.show()