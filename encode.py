import cv2
import numpy as np
from numpy.core.fromnumeric import ravel


class Encode():
    
    def __init__(self, img, text):
        super(Encode, self).__init__(img, text)
        self.NB_BITS = 8

    def standerdize_length(self, caracter):
        if len(caracter) < self.NB_BITS:
            return ['0']*(self.NB_BITS - len(caracter)) + caracter
        return caracter

    def to_bin(n):
        return list(bin(n).replace("0b", ""))

    def change_last_bit(self, value, bit):
        value = self.to_bin(value)
        value[-1] = bit
        return int("".join(value),2)

    def text_to_image(self):
        h, w, _ = self.img.shape
        if len(self.text)+1 > h*w : 
            raise ValueError()
        else :
            imgRes = np.zeros(self.img.shape, dtype=np.uint8)
            text_bit = []
            for char in self.text:
                text_bit += self.standerdize_length(self.to_bin(ord(char)))

            text_bit = np.array(text_bit + ['0']*self.NB_BITS)

            img_flat = self.img.ravel()

            for i, p in enumerate(text_bit):
                img_flat[i] = self.change_last_bit(img_flat[i], p)

            self.img = img_flat
            
        

        

    def codage(self):
        pass
        