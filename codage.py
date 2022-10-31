import math
import cv2
import numpy as np

class Encode():
    def __init__(self, img, text= None):
        super(Encode, self).__init__()   
        self.img = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        self.text = text
        self.NB_BITS_8 = 8
        self.NB_BITS_16 = 16
    
    # Transform a text into a list of binary numbers
    def to_bin(self, n):
        return list(bin(n).replace("0b", ""))

    # Standarize the length of a binary number
    def standerdize_length_8(self, caracter):
        if len(caracter) < self.NB_BITS_8:
            return ['0']*(self.NB_BITS_8 - len(caracter)) + caracter
        return caracter
    
    def standerdize_length_16(self, caracter):
        if len(caracter) < self.NB_BITS_16:
            return ['0']*(self.NB_BITS_16 - len(caracter)) + caracter
        return caracter

    # change bits of the image to add text
    def change_bits(self, value, bit1, bit2):
        value = self.standerdize_length_8(self.to_bin(value))
        value[-5] = bit1
        value[-6] = bit2
        return int("".join(value),2)

    def to_int(self, binary):
        binary = [str(element) for element in binary]
        return int("".join(binary),2)
    
   
    
    def create_img_with_text(self, text):
    
        len_txt = len(text)
        # for each caracter in the text we need 4 pixels 
        img_shapes = int(((len_txt*4)**(1/2)))    
        img = np.zeros((img_shapes, img_shapes, 3), dtype = np.uint8)

        text_bit = []
        for char in text:
            text_bit += self.standerdize_length_8(self.to_bin(ord(char)))
        text_bit = np.array(text_bit + ['0']*self.NB_BITS_8)

        img_ravel = img.ravel()
        len_img_bit = len(img_ravel)
        len_text = len(text_bit)
        for i in range(len_img_bit):
            if i+1 == len_img_bit or i+1 == len_text:
                break
            img_ravel[i] = self.change_bits(img_ravel[i], text_bit[i], text_bit[i+1])

        shape = (img_shapes,img_shapes, 3)
        img = img_ravel.reshape(shape)
        
        return img
    
    def insert_img(self, value_A, value_B):
        value_A = self.standerdize_length_8(self.to_bin(value_A))
        value_A[7:] = value_B

        return int("".join(value_A),2)
    
    def get_dispatch(self, shape):
        #return int(math.log2((shape[1]**2 )- 1) - (shape[1]-1) + shape[0]) 
        return shape[1]
    
    def encodeImge(self):        
        imgA = self.img
        len_text = len(self.text)
        len_img = imgA.shape[0]*imgA.shape[1] *4
        if len_text> len_img: raise ValueError()
        else:
            if imgA.dtype == 'uint8':
                imgA=np.uint16(imgA)*255
            elif imgA.dtype != 'uint16':
                raise ValueError()
            imgB = self.create_img_with_text(self.text) 
            # COnvert last 4 bits of mgA ro 0111***********
            imgA_ravel = imgA.ravel()
            for i in range(len(imgA_ravel)):
                imgA_ravel_i= self.standerdize_length_8(self.to_bin(imgA_ravel[i]))
                imgA_ravel_i[-4:] = ['0','1','1','1']
                imgA_ravel[i] = int("".join(imgA_ravel_i),2)
            imgA = imgA_ravel.reshape(imgA.shape)

            dispatch = abs(self.get_dispatch(imgA.shape))

            # Use only cr cb ********************
            img_cr = imgA[:, :, 1]
            img_cb = imgA[:, :, 2]
            imgB_ravel = imgB.ravel()

            img_cr_ravel = img_cr.ravel()
            img_cb_ravel = img_cb.ravel()
            imgB_ravel_1 = imgB_ravel[:len(imgB_ravel)//2]
            imgB_ravel_2 = imgB_ravel[len(imgB_ravel)//2:]
            
            #on enregistre la taille 
            img_cr_ravel[0] = self.insert_img(img_cr_ravel[0], self.standerdize_length_8(self.to_bin(len(imgB_ravel))))
            print("la taille de l'image b est : ",img_cr_ravel[0])

            for i in range(len(imgB_ravel_2)):
                if i > len(imgB_ravel_1)-1:
                    break
                imgB_i_bit_1 = self.standerdize_length_8(self.to_bin(imgB_ravel_1[i]))
                print(imgB_i_bit_1)
                imgB_i_bit_2 = self.standerdize_length_8(self.to_bin(imgB_ravel_2[i]))
                print(imgB_i_bit_2)
                img_cr_ravel[(i+1)*dispatch] = self.insert_img(img_cr_ravel[(i+1)*dispatch], imgB_i_bit_1)
                img_cb_ravel[i*dispatch] = self.insert_img(img_cb_ravel[i*dispatch], imgB_i_bit_2)

        img_cr = img_cr_ravel.reshape(img_cr.shape)
        img_cb = img_cb_ravel.reshape(img_cb.shape)

        imgA[:, :, 1] = img_cr
        imgA[:, :, 2] = img_cb
        imgA = cv2.cvtColor(imgA, cv2.COLOR_YCrCb2RGB)
        cv2.imwrite("weshHBIBI.png", imgA)
        return imgA
    
    def get_text_from_img(self, val):
        print(val)
        val = self.standerdize_length_8(self.to_bin(val))
        text = val [-7:]
        print(val)
        text_ = [text[-5], text[-6]]
        return text_
    def getTaille(self, val):
        val = self.standerdize_length_8(self.to_bin(val))
        print(val [-7:])
        taille = int(self.decode(val [-7:]))
        return taille


    def BinaryToDecimal(self, binary): 
        binary = ''.join(i for i in binary)  
        decimal, i
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return (decimal)
    
    def decode(self, bin_data):
        for i in range(0, len(bin_data), 7):
            temp_data = int(bin_data[i:i + 7])
        decimal_data = self.BinaryToDecimal(temp_data)
        str_data = str_data + chr(decimal_data)
        return str_data
    

    def decodageImge(self):
        imgA = self.img
        text=""
        position = abs(self.get_dispatch(imgA.shape))
        img_cr = imgA[:, :, 1]
        img_cb = imgA[:, :, 2]
        img_cr_ravel = img_cr.ravel()
        img_cb_ravel = img_cb.ravel()
        taille = self.getTaille(img_cr_ravel[0])
        print(taille)
        print(position)
        imgB_ravel_1 = [] #img_cr
        imgB_ravel_2 = [] #img_cb

        for i in range(taille//2) :
            imgB_ravel_1 +=self.get_text_from_img(img_cr_ravel[(i+1)*position])
            imgB_ravel_2 +=self.get_text_from_img(img_cb_ravel[(i)*position])

        text = imgB_ravel_1+imgB_ravel_2
        print(text)
        text = self.decode(text)    

        return text



"""img = cv2.imread('test.jpg', cv2.COLOR_BGR2RGB)
img =  Encode(img, 'hollo je suis mario').encodeImge()"""

img = cv2.imread('weshHBIBI.png', cv2.COLOR_BGR2RGB)
text = Encode(img).decodageImge()

print("Le text secret est : ", text)

"""cv2.imshow('the IMAGE', img)
cv2.waitKey(0)
cv2.destroyAllWindows()"""


"""word = "hello"
binary = []
for char in word : 
    binary = binary + list(bin(ord(char)).replace("0b", ""))
str = ''.join(i for i in binary) 

def BinaryToDecimal(binary):  
    decimal, i
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return (decimal)

str_data =' '
bin_data =str
print("bin data : ", bin_data)
for i in range(0, len(bin_data), 7):
    temp_data = int(bin_data[i:i + 7])
    decimal_data = BinaryToDecimal(temp_data)
    str_data = str_data + chr(decimal_data)

print("The Binary value after string conversion is:",
       str_data)"""