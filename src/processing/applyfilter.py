import matlab.engine as mb
import logging
import sys

logger = None
class Processor:
    def __init__(self):
        """
        creates matlab engine.
        """

        #TODO: class that handles creation of matlab engines. shares engines with processes if need be.
        self.eng = mb.start_matlab()
        self.eng.addpath("matlab-scripts")
        self.orig_img = None
        self.filtered_img = None
        logger.info("engine instantiated.")

    def load_dcm(self, name, resize=False):
        """
        loads dcm file.

        :param name:    name of the file
        :param resize:  tuple consisting of width and height,
                        if required.

        """

        self.orig_img = self.eng.load_dcm(name, resize)

    def apply_filters(self, sigma=10.0, se_type="disk", se_size=15.0):
        """
        applies filter to matlab image array.

        :param sigma:   the sigma value for high pass filter
        :param se_type: type of structuring element to use.
        :param se_size: size of the structuring element.
        """

        logger.debug("applying filters...")
        self.filtered_img = self.eng.apply_filters(self.orig_img)
        logger.debug("done.")

    def filtered_show(self):
        """
        displays image.

        :param img: image to be displayed.
        """
        logger.debug("displaying image...")
        self.eng.imshow(self.filtered_img)

def create_logger(verbose):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s", "%d-%m-%Y %H:%M:%S")
    if verbose:
        stream = logging.StreamHandler(sys.stdout)
        stream.setFormatter(fmt)
        logger.addHandler(stream)

    return logger


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("invalid number of arguments.")
        sys.exit(-1)
    
    if  (len(sys.argv) == 3 and sys.argv[2] == "-v") or (len(sys.argv) == 1):
        logger = create_logger(True)
    else:
        logger = create_logger(False)

    if len(sys.argv) == 1:
        name = "000000.dcm"
    else:
        name = sys.argv[1]
    resize = (256, 172)
    
    proc = Processor()
    proc.load_dcm(name, resize)
    proc.apply_filters()
    proc.filtered_show()
    
    

    