import cv2
import numpy as np
from builtins import int


class Encode():
    def __init__(self, path, text= None):
        super(Encode, self).__init__()  
        if text is not None :
            self.img = cv2.imread(path, cv2.IMREAD_COLOR)
            if self.img.shape[0]>1080 and self.img.shape[1]>1080 :
                self.img = cv2.resize(self.img,dsize=None,fx = 0.15, fy = 0.15) 
        else:
            self.img = cv2.imread(path, -1)

        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2YCrCb)
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

        text_bit = np.array(text_bit)
        
        img_ravel = img.ravel()
        len_img_bit = len(img_ravel)
        len_text = len(text_bit)
        for i in range(len_img_bit):
            if i>=(len_text-1)/2 :
                break
            # i was making a mistake hnaya, kont j'ecrase i à chaque fois, douka fixed now
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
        return shape[1]
    
    # put the size of the imgB into pixels of imgA
    def insert_taille(self, img_cr_ravel, taille):
        if taille <= 255:
            img_cr_ravel = self.insert_bool(img_cr_ravel, '0')
            taille_bit = self.standerdize_length_8(self.to_bin(taille))
            ranging = 4
        else:
            img_cr_ravel = self.insert_bool(img_cr_ravel, '1')
            taille_bit = self.standerdize_length_16(self.to_bin(taille))
            ranging = 8

        for i in range(ranging):
            imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[i+1]))
            imgA_cr_i_bit[-6] = taille_bit[i*2]
            imgA_cr_i_bit[-5] = taille_bit[2*i+1]
            img_cr_ravel[i+1] =  int("".join(imgA_cr_i_bit),2)

        return img_cr_ravel
    
    # insert boolean value into the image
    def insert_bool(self, img_cr_ravel, bool):
        imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[0]))
        imgA_cr_i_bit[-6] = bool
        img_cr_ravel[0] =  int("".join(imgA_cr_i_bit),2)

        return img_cr_ravel
    
    def encodeImge(self):        
        imgA = self.img
        imgA_coded = imgA.copy()
        len_text = len(self.text)
        len_img = imgA.shape[0]*imgA.shape[1] *4
        if len_text> len_img: raise ValueError()
        else:
            if imgA.dtype == 'uint8':
                imgA=np.uint16(imgA)*255
            elif imgA.dtype != 'uint16':
                raise ValueError()
            imgB = self.create_img_with_text(self.text) 

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
            print("on va faire l'encodage avec imgB")
            while i < len(imgB_ravel_1):
                imgB_i_bit_1 = self.standerdize_length_8(self.to_bin(imgB_ravel_1[i]))
                imgB_i_bit_2 = self.standerdize_length_8(self.to_bin(imgB_ravel_2[i]))
   
                if len(imgB_ravel) <= 255:
                    print("img <=255") 
                    img_cr_ravel[(i+5)*dispatch] = self.insert_img(img_cr_ravel[(i+5)*dispatch], imgB_i_bit_1)
                else:
                    try:
                        print("dans le else")
                        img_cr_ravel[(i+9)*dispatch] = self.insert_img(img_cr_ravel[(i+9)*dispatch], imgB_i_bit_1)
                        img_cb_ravel[i*dispatch] = self.insert_img(img_cb_ravel[i*dispatch], imgB_i_bit_2)
                    except IndexError as e:
                        print("The image is too small to contain the text")
                        imgA_coded = None
                i+=1

            if len(imgB_ravel_1) <len(imgB_ravel_2):
                try:
                    img_cb_ravel[i*dispatch] = self.insert_img(img_cb_ravel[i*dispatch], imgB_i_bit_2)
                except IndexError as e:
                    print("The image is too small to contain the text")
                    imgA_coded = None
        print("done...")
            #**************************************************************************      

        img_cr = img_cr_ravel.reshape(img_cr.shape)
        img_cb = img_cb_ravel.reshape(img_cb.shape)
        imgA[:, :, 1] = img_cr
        imgA[:, :, 2] = img_cb
        
        # THE PROBLEM WERE SYMPLY HERE, AU LIEU DE 16 KOUNA DAYRIN AGAIN 8 XD
        # COnvert last 4 bits of mgA ro 0111***********
        imgA_ravel = imgA.ravel()

        for i in range(len(imgA_ravel)):
            imgA_ravel_i= self.standerdize_length_16(self.to_bin(imgA_ravel[i]))
            imgA_ravel_i[-4:] = ['0','1','1','1']
            imgA_ravel[i] = int("".join(imgA_ravel_i),2)
        imgA = imgA_ravel.reshape(imgA.shape)

        #***********************************************
        imgA = cv2.cvtColor(imgA, cv2.COLOR_YCrCb2RGB)

        
        if imgA_coded == None: return None
        print("we return")
        return imgA
        #*****************************************************
    
    def getTaille(self, img_cr_ravel):

        imgA_cr_0_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[0]))
        if imgA_cr_0_bit[-6] == '0':
            taille_bit = ['0']*8
            ranging = 4
        elif imgA_cr_0_bit[-6] == '1':
            taille_bit = ['0']*16
            ranging = 8

        for i in range(ranging):
            imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[i+1]))
            taille_bit[i*2] = imgA_cr_i_bit[-6]
            taille_bit[2*i+1]= imgA_cr_i_bit[-5]

        taille =  int("".join(taille_bit),2)

        return taille


    def BinaryToDecimal(self, binary):   
        decimal, i = 0,0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return (decimal)
    
    def decode(self, bin_data):
        str_data = ' '
        for i in range(0, len(bin_data), 7):
            temp_data = int(bin_data[i:i + 7])
            decimal_data = self.BinaryToDecimal(temp_data)
            str_data = str_data + chr(decimal_data)
        return str_data


    def decodageImge(self):
        imgA = self.img
        dispatch = abs(self.get_dispatch(imgA.shape))
        img_cr = imgA[:, :, 1]
        img_cb = imgA[:, :, 2]
        img_cr_ravel = img_cr.ravel()
        img_cb_ravel = img_cb.ravel()
        taille = self.getTaille(img_cr_ravel)
        
        index = 5 if taille<=255 else 9
        text_bit_1 = []
        text_bit_2 = []
        i=0
        while i < taille//2:
            imgA_1 = self.standerdize_length_16(self.to_bin(img_cr_ravel[(i+index)*dispatch]))
            text_bit_1+=[imgA_1[-6],imgA_1[-5]] 
            imgA_2 = self.standerdize_length_16(self.to_bin(img_cb_ravel[i*dispatch]))
            text_bit_2+=[imgA_2[-6],imgA_2[-5]] 
            i+=1

        if taille%2!=0:
            imgA_2 = self.standerdize_length_16(self.to_bin(img_cb_ravel[i*dispatch]))
            text_bit_2+=[imgA_2[-6],imgA_2[-5]] 
        
        text = text_bit_1 + text_bit_2

        return self.work_with_bits(text)


    def BinaryToDecimal(self, binary):  
        decimal, i=0,0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return (decimal)


    def work_with_bits(self, text_bits_liste):
        i=0
        text_complet=""
        str_data = ""
        while k < len(text_bits_liste):
            k=(i+1)*8
            text_bits = text_bits_liste[i*8:k]
            if text_bits!=[]:
                if text_bits[0] == '0':
                    text_bits = text_bits[1:]
                text_bits = ''.join(i for i in text_bits)
                for j in range(0, len(text_bits), 7):
                    temp_data = int(text_bits[j:j + 7])
                    decimal_data = self.BinaryToDecimal(temp_data)
                    str_data = str_data + chr(decimal_data)

            i=i+1
            
        text_complet +=str_data
        return text_complet
