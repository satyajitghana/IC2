import sys, os
import pydicom
import numpy as np
import cv2
import matplotlib.pyplot as plt

def load_dcm(name):
    """
    loads the dcm file
    :param path:    name of the image

    :return:        dcm data
    """

    cwd = os.getcwd()
    rootFolder = cwd[:cwd.rfind("/", 0, cwd.rfind("/"))]
    path = rootFolder+"/res/images/"+name

    try:
        return pydicom.dcmread(path)
    except FileNotFoundError:
        print("place the image in the res/images folder, and make sure that this script is running from src/loose_scripts folder.")
        sys.exit(-1)

def high_pass_filter(img, sigma):
    """
    applies gaussian high pass filter in frequency domain
    
    :param img:     the image
    :param sigma:   filter amount

    :return:        filtered image
    """ 

    rows = img.shape[0]
    cols = img.shape[1]

    M = 2*rows + 1
    N = 2*cols + 1
    (X, Y) = np.meshgrid(np.linspace(0, N-1, N), np.linspace(0, M-1, M))
    centerX = np.ceil(N/2)
    centerY = np.ceil(M/2)

    # gaussian low pass filter
    gaussianNumerator = (X - centerX)**2 + (Y - centerY)**2
    H = np.exp(-gaussianNumerator/(2*sigma*sigma))

    # high pass filter
    H = 1 - H

    # shift zero-frequency component to center (useful for visualizing a 
    # Fourier transform with the zero-frequency component in the middle of the spectrum.)
    # (in other words, shift the filter to the center)
    H = np.fft.fftshift(H)

    # applying filter
    If = np.fft.fft2(img, (M, N))
    Iout = np.real(np.fft.ifft2(If * H, (M, N)))

    # trimming extra padding
    Iout = Iout[0:rows, 0:cols]
    
    return Iout

def homomorphic_filter(img, resize=False):
    """
    applies homomorphic filtering on image.

    :param img:     the image (from dcm file data)
    :param resize:  defaults to False. otherwise a tuple consisting of new 
                    image size

    :return:        filtered image
    """

    if resize:
        # img = skimage.transform.resize(img, resize, anti_aliasing=True)
        img = cv2.resize(img, resize)
    
    img = im2double(img) 
    imgLog = np.log1p(img)
    Iout = high_pass_filter(imgLog, 10)
    return np.expm1(Iout)
    
def imtophat(img, se_type, se_size):
    """
    applies tophat transform on image.

    :param img:     the image
    :param se_type: the type of structuring element(from opencv)
    :param se_size: the size of the structuring element

    :return:        the transformed image
    """

    se = cv2.getStructuringElement(se_type, se_size)
    return cv2.morphologyEx(img, cv2.MORPH_TOPHAT, se)

def imbothat(img, se_type, se_size):
    """
    applies tophat transform on image.

    :param img:     the image
    :param se_type: the type of structuring element(from opencv)
    :param se_size: the size of the structuring element

    :return:        the transformed image
    """

    se = cv2.getStructuringElement(se_type, se_size)
    return cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, se)


def adapthisteq(img, clip_limit = 0.02, tile_grid_size = (8, 8)):
    """
    performs Constrast Limiting Adaptive Histogram Equalization on image.

    :param img:             the input image
    :param clip_limit:      the clip limit for CLAHE
    :param tile_grid_size:  the tile size for CLAHE

    :return:                the processed image
    """

    if img.dtype == np.dtype("float"):
        img = np.interp(img, (img.min(), img.max()), (0, 255)).astype('uint8')

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(img)

def save_image(img, name, cm=False):
    """
    saves the image to res/images/output

    :param img:     the image to be saved
    :param name:    the name of the image
    """

    cwd = os.getcwd()
    rootFolder = cwd[:cwd.rfind("/", 0, cwd.rfind("/"))]
    path = rootFolder+"/res/images/output/"+name

    if cm == True:
        plt.imsave(path, img, cmap="bone")
    elif cm != True and cm != False:
        plt.imsave(path, img, cmap=cm) 
    else:
        cv2.imwrite(path, img*255)

def im2double(img):
    """
    converts image to double values ranging from 0 to 1. if image is already of float type,
    returns the image as is.

    :param img: the image to convert.

    :return:    the converted image.
    """

    if img.dtype == np.dtype("float"):
        return img

    info = np.iinfo(img.dtype)
    return img.astype(np.float)/info.max



if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print("syntax: homomorphic_filter.py [file_name]")
        sys.exit(-1)

    dcm_data = load_dcm(sys.argv[1])
    Ihmf = homomorphic_filter(dcm_data.pixel_array, resize=(172, 256))
    save_image(Ihmf, sys.argv[1].split(".")[0]+"-HomomorphicFilter.jpg")
   
    tophat = imtophat(Ihmf, cv2.MORPH_ELLIPSE, (29, 29))
    save_image(tophat, sys.argv[1].split(".")[0]+"-tophat.jpg")
    
    bothat = imbothat(Ihmf, cv2.MORPH_ELLIPSE, (29, 29))
    save_image(bothat, sys.argv[1].split(".")[0]+"-bothat.jpg")

    processedImage = adapthisteq((Ihmf + tophat) - bothat)
    save_image(processedImage, sys.argv[1].split(".")[0]+"-CLAHE.jpg", cm="gray")

