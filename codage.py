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

    # Standarize the length of a binary number into 8bits
    def standerdize_length_8(self, caracter):
        if len(caracter) < self.NB_BITS_8:
            return ['0']*(self.NB_BITS_8 - len(caracter)) + caracter
        return caracter
    
    # Standarize the length of a binary number into 16bits
    def standerdize_length_16(self, caracter):
        if len(caracter) < self.NB_BITS_16:
            return ['0']*(self.NB_BITS_16 - len(caracter)) + caracter
        return caracter

    # change bits of the image to add text
    def change_bits(self, value, bit1, bit2):
        value = self.standerdize_length_8(self.to_bin(value))
        value[-6] = bit1
        value[-5] = bit2
        return int("".join(value),2)

    # change from binary to decimal
    def to_int(self, binary):
        binary = [str(element) for element in binary]
        return int("".join(binary),2)
    
   
    # create an image from a text
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
            if i>=(len_text-1)/2 :
                break
            img_ravel[i] = self.change_bits(img_ravel[i], text_bit[i*2], text_bit[i*2+1])

        shape = (img_shapes,img_shapes, 3)
        img = img_ravel.reshape(shape)

        return img
    

    # insert an image into another image
    def insert_img(self, value_A, value_B):
        value_A = self.standerdize_length_16(self.to_bin(value_A))
        value_A[8:] = value_B
        return int("".join(value_A),2)
    
    # function de dispersion
    def get_dispatch(self, shape):
        #return int(math.log2((shape[1]**2 )- 1) - (shape[1]-1) + shape[0]) 
        return shape[1]
    
    # put the size of the imgB into pixels of imgA
    def insert_taille(self, img_cr_ravel, taille):
        if taille <= 255:
            taille_bit = self.standerdize_length_8(self.to_bin(taille))
            ranging = 4
        else:
            taille_bit = self.standerdize_length_16(self.to_bin(taille))
            ranging = 8

        for i in range(ranging):
            imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[i]))
            imgA_cr_i_bit[-6] = taille_bit[i*2]
            imgA_cr_i_bit[-5] = taille_bit[2*i+1]
            img_cr_ravel[i] =  int("".join(imgA_cr_i_bit),2)

        return img_cr_ravel
    

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
            #*********************************************************
            
            # Use only cr cb ********************
            img_cr = imgA[:, :, 1]
            img_cb = imgA[:, :, 2]
            imgB_ravel = imgB.ravel()

            img_cr_ravel = img_cr.ravel()
            img_cb_ravel = img_cb.ravel()
            imgB_ravel_1 = imgB_ravel[:len(imgB_ravel)//2]
            imgB_ravel_2 = imgB_ravel[len(imgB_ravel)//2:]
            #**********************************************

            #COnserver la taille de l'image B dans les pixel de cr*******************
            img_cr_ravel = self.insert_taille(img_cr_ravel, len(imgB_ravel))
            #******************************************************

            # dispersion of the text in the image*************************************************
            dispatch = abs(self.get_dispatch(imgA.shape))

            i=0
            while i < len(imgB_ravel_1):
                imgB_i_bit_1 = self.standerdize_length_8(self.to_bin(imgB_ravel_1[i]))
                imgB_i_bit_2 = self.standerdize_length_8(self.to_bin(imgB_ravel_2[i]))
   
                if len(imgB_ravel) <= 255:
                     img_cr_ravel[(i+4)*dispatch] = self.insert_img(img_cr_ravel[(i+4)*dispatch], imgB_i_bit_1)
                else:
                     img_cr_ravel[(i+8)*dispatch] = self.insert_img(img_cr_ravel[(i+8)*dispatch], imgB_i_bit_1)
                
                img_cb_ravel[i*dispatch] = self.insert_img(img_cb_ravel[i*dispatch], imgB_i_bit_2)
                i+=1

            if len(imgB_ravel_1) <len(imgB_ravel_2):
                img_cb_ravel[i*dispatch] = self.insert_img(img_cb_ravel[i*dispatch], imgB_i_bit_2)
            #**************************************************************************      
        img_cr = img_cr_ravel.reshape(img_cr.shape)
        img_cb = img_cb_ravel.reshape(img_cb.shape)

        #test **********************************************************************
        """    print(self.standerdize_length_16(self.to_bin(img_cr.ravel()[0])))
            something  = self.standerdize_length_16(self.to_bin(img_cr.ravel()[0]))
            print(int("".join(something),2))"""
        #********************************************************************

        imgA[:, :, 1] = img_cr
        imgA[:, :, 2] = img_cb
        imgA = cv2.cvtColor(imgA, cv2.COLOR_YCrCb2RGB)
        """    cv2.imshow("hbibi_hadak.png", imgA)
            cv2.imshow('the message', imgB)
            cv2.waitKey(0)
            cv2.destroyAllWindows()"""

        #test **********************************************************************
        imgA = cv2.cvtColor(imgA, cv2.COLOR_RGB2YCrCb)
        img_cr = imgA[:, :, 1]
        """    something  = self.standerdize_length_16(self.to_bin(img_cr.ravel()[0]))
            print(self.standerdize_length_16(self.to_bin(img_cr.ravel()[0])))
            print(int("".join(something),2))"""
        #***************************************************************************
        img_cr_ravel = img_cr.ravel()
        print(self.getTaille(img_cr_ravel))
        return imgA
    


    def get_text_from_img(self, val):
        #print(val)
        val = self.standerdize_length_8(self.to_bin(val))
        text = val [-7:]
        #print(val)
        text_ = [text[-5], text[-6]]
        return text_
    
    def getTaille(self, img_cr_ravel):
        
        """    if taille <= 255:
                taille_bit = self.standerdize_length_8(self.to_bin(taille))
                ranging = 4
            else:
                taille_bit = self.standerdize_length_16(self.to_bin(taille))
                ranging = 8"""

        taille_bit = ['0']*8
        for i in range(4):
            imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[i]))
            
            taille_bit[i*2] = imgA_cr_i_bit[-6]
            taille_bit[2*i+1]= imgA_cr_i_bit[-5]

        taille =  int("".join(taille_bit),2)

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
        position = abs(self.get_0(imgA.shape))
        img_cr = imgA[:, :, 1]
        img_cb = imgA[:, :, 2]
        img_cr_ravel = img_cr.ravel()
        img_cb_ravel = img_cb.ravel()
        #print(img_cr_ravel)
        taille = self.getTaille(img_cr_ravel[0])
        #print("aaaaaaaaaaaaaaaaaaaaaaaa",taille)
        #print(position)
        imgB_ravel_1 = [] #img_cr
        imgB_ravel_2 = [] #img_cb

        for i in range(taille//2) :
            imgB_ravel_1 +=self.get_text_from_img(img_cr_ravel[(i+1)*position])
            imgB_ravel_2 +=self.get_text_from_img(img_cb_ravel[(i)*position])

        text = imgB_ravel_1+imgB_ravel_2
        #print(text)
        text = self.decode(text)    

        return text



img = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
img =  Encode(img, 'hollo je suis mario').encodeImge()

"""    text = Encode(img).decodageImge()
    print(text)"""
#img = cv2.imread('weshHBIBI.png', cv2.IMREAD_COLOR)


#print("Le text secret est : ", text)




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