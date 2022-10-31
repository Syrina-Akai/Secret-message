import cv2
import numpy as np

class Encode():
    def __init__(self, img, text):
        super(Encode, self).__init__()   
        self.img = img
        self.text = text
    
    def to_bin(self, n):
        return list(bin(n).replace("0b", ""))

    def to_int(self, binary):
        binary = [str(element) for element in binary]
        return int("".join(binary),2)
    
    def change_pixel(self, base):
        for i in range(base.shape[0]):
            pixel = base[i,5]
            pixel = self.to_bin(pixel) 
            pixel[-4:] = [0,1,1,1]
            #we're gonna add the value
            #***************************************
            pixel[-5] = 1 if pixel[-5] == 0 else 0
            pixel[-6] = 1 if pixel[-6] == 0 else 0
            #***************************************
            pixel = self.to_int(pixel)
            base[i,5] = pixel
        return base
    
    def adding_text(self, imgYCC):
        imgYCC[:, :, 1] = self.change_pixel(imgYCC[:, :, 1])
        imgYCC[:, :, 2] = self.change_pixel(imgYCC[:, :, 2])
        return imgYCC

    def encodeImge(self):
        cv2.imshow('original',self.img)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2YCR_CB)
        if self.img.dtype == 'uint8':
            print("type 8..")
            self.img=np.uint16(self.img)*255
        elif self.img.dtype != 'uint16':
            raise ValueError()

        self.img = self.adding_text(self.img)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_YCrCb2RGB)
        cv2.imshow('after adding values',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

img = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
encode = Encode(img, 'hillow')
encode.encodeImge()
