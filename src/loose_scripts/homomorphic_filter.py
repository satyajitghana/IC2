import sys, os
import pydicom
import numpy as np
import skimage
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

    :param img:     the image
    :param resize:  defaults to False. otherwise a tuple consisting of new 
                    image size

    :return:        filtered image
    """

    if resize:
        img = skimage.transform.resize(img, resize, anti_aliasing=True)
    
    imgLog = np.log1p(img)
    Iout = high_pass_filter(imgLog, 10)
    return np.expm1(Iout)
    
def save_image(img, name):
    """
    saves the image to res/images/output

    :param img:     the image to be saved
    :param name:    the name of the image
    """

    cwd = os.getcwd()
    rootFolder = cwd[:cwd.rfind("/", 0, cwd.rfind("/"))]
    path = rootFolder+"/res/images/output/"+name

    plt.imsave(path, img, cmap=plt.cm.bone)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print("syntax: homomorphic_filter.py [file_name]")
        sys.exit(-1)

    dcm_data = load_dcm(sys.argv[1])
    Ihmf = homomorphic_filter(dcm_data.pixel_array, resize=(256,172))
    save_image(Ihmf, sys.argv[1].split(".")[0]+"OUT.jpg")