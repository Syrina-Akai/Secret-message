import cv2
import numpy as np

class Encode():
    def __init__(self, path=None, text= None):
        super(Encode, self).__init__()  
        if path is None : #cas de codage du texte
            self.img = None
        elif path is not None: #cas ou il y a l'imgA
            if text is not None : #cas ou on va coder l'imgA à partir de l'imgB
                self.img = cv2.imread(path, cv2.IMREAD_COLOR)
                if self.img.shape[0]>1080 and self.img.shape[1]>1080 :
                    self.img = cv2.resize(self.img,dsize=None,fx = 0.15, fy = 0.15)
            else : #cas de décodage de l'imgA
                self.img = cv2.imread(path, -1)

            self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2YCrCb)
        self.text = text
        self.NB_BITS_20 = 20
        self.NB_BITS_16 = 16
        self.NB_BITS_8 = 8
    



    def splitTextToTriplet(self, string):
        words = string.split()
        grouped_words = [' '.join(words[i: i + 7]) for i in range(0, len(words), 7)]
        return grouped_words
    
    def convert_text_img(self):
        print("dkhelna converti text")
        len_txt = len(self.text)
        print(len_txt)
        groupe_text = self.splitTextToTriplet(self.text)
        
        img1 = np.zeros((24*len(groupe_text), 60*7, 3), dtype = np.uint8)
        y_start = 15
        y_increment = 20
        print(groupe_text)
        for i, line in enumerate(groupe_text):
            y = y_start + i*y_increment
            cv2.putText(img=img1, text=line, org=(0, y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(255,255,0), 
            thickness=1)

        print("on a terminer le codage du text..........")
        
        return img1

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

    def standerdize_length_20(self, caracter):
        if len(caracter) < self.NB_BITS_20:
            return ['0']*(self.NB_BITS_20 - len(caracter)) + caracter
        return caracter

    # insert boolean value into the image
    def insert_bool(self, img_cr_ravel, bool):
        imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[0]))
        imgA_cr_i_bit[-6] = bool
        img_cr_ravel[0] =  int("".join(imgA_cr_i_bit),2)

        return img_cr_ravel
    
    def insert_taille(self, img_cr_ravel, taille):

        if taille <=2**16 :
            img_cr_ravel = self.insert_bool(img_cr_ravel, '0')
            taille_bit = self.standerdize_length_16(self.to_bin(taille))
            ranging = 8
        else :
            img_cr_ravel = self.insert_bool(img_cr_ravel, '1')
            taille_bit = self.standerdize_length_20(self.to_bin(taille))
            ranging = 10
        for i in range(ranging):
            imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[i+1]))
            imgA_cr_i_bit[-6] = taille_bit[i*2]
            imgA_cr_i_bit[-5] = taille_bit[2*i+1]
            img_cr_ravel[i+1] =  int("".join(imgA_cr_i_bit),2)

        return img_cr_ravel
    
    def insert_imgB(self, base, pixel_b, index):
    
        pixel_b_bit = self.standerdize_length_8(self.to_bin(pixel_b))

        for i in range(4):
            base_i_bit =  self.standerdize_length_16(self.to_bin(base[index]))
            base_i_bit[-6] = pixel_b_bit[i*2]
            base_i_bit[-5] = pixel_b_bit[2*i+1]
            base[index] =  int("".join(base_i_bit),2)
            index = index+i+1

        return base, index

    def insert_into_image(self, imgB):
        imgB_ravel = imgB.ravel()
        imgA = self.img
        if imgA.dtype == 'uint8':
            imgA=np.uint16(imgA)*255
        elif imgA.dtype != 'uint16':
            raise ValueError()
        #getting cr & cb
        img_cr = imgA[:, :, 1]
        img_cb = imgA[:, :, 2]
        img_cr_ravel = img_cr.ravel()
        img_cb_ravel = img_cb.ravel()

        #COnserver la taille de l'image B dans les pixel de cr*******************
        img_cr_ravel = self.insert_taille(img_cr_ravel, len(imgB_ravel))

        #on divise l'imgB en 2
        imgB_ravel_1 = imgB_ravel[:len(imgB_ravel)//2]
        imgB_ravel_2 = imgB_ravel[len(imgB_ravel)//2:]
        print("taille avant codage : ", len(imgB_ravel))
        i=0
        index = 5 if len(imgB_ravel) <= 255 else 9 
        while i < len(imgB_ravel_1):
            imgB_i_bit_1 = imgB_ravel_1[i]
            imgB_i_bit_2 = imgB_ravel_2[i]

            img_cr_ravel, index = self.insert_imgB(img_cr_ravel, imgB_i_bit_1, index)
            img_cb_ravel, _ = self.insert_imgB(img_cb_ravel, imgB_i_bit_2, i)

            i+=1
        if len(imgB_ravel_1) <len(imgB_ravel_2):
            img_cb_ravel, _ = self.insert_imgB(img_cb_ravel, imgB_i_bit_2, i)

        img_cr = img_cr_ravel.reshape(img_cr.shape)
        img_cb = img_cb_ravel.reshape(img_cb.shape)
        imgA[:, :, 1] = img_cr
        imgA[:, :, 2] = img_cb

        imgA_ravel = imgA.ravel()
        for i in range(len(imgA_ravel)):
            imgA_ravel_i= self.standerdize_length_16(self.to_bin(imgA_ravel[i]))
            imgA_ravel_i[-4:] = ['0','1','1','1']
            imgA_ravel[i] = int("".join(imgA_ravel_i),2)
        imgA = imgA_ravel.reshape(imgA.shape)
        imgA = cv2.cvtColor(imgA, cv2.COLOR_YCrCb2RGB)
        return imgA

    def getTaille(self, img_cr_ravel):
        
        imgA_cr_0_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[0]))
        if imgA_cr_0_bit[-6] == '0':
            taille_bit = ['0']*16
            ranging = 8
        elif imgA_cr_0_bit[-6] == '1':
            taille_bit = ['0']*20
            ranging = 10

        for i in range(ranging):
            imgA_cr_i_bit =  self.standerdize_length_16(self.to_bin(img_cr_ravel[i+1]))
            taille_bit[i*2] = imgA_cr_i_bit[-6]
            taille_bit[2*i+1]= imgA_cr_i_bit[-5]

        taille =  int("".join(taille_bit),2)
        print("taille avant codage : ", taille)
        return taille

    def get_pixel(self, base, index):
        ranging = 4
        pixel_bit = ['0']*8
        for i in range(ranging):
            base_i_bit =  self.standerdize_length_16(self.to_bin(base[index]))
            pixel_bit[i*2] = base_i_bit[-6] 
            pixel_bit[2*i+1] = base_i_bit[-5]
            index = index+i+1

        pixel = int("".join(pixel_bit),2)
        return pixel, index

    def get_from_img(self):
        imgA = self.img
        #getting cr & cb
        img_cr = imgA[:, :, 1]
        img_cb = imgA[:, :, 2]
        img_cr_ravel = img_cr.ravel()
        img_cb_ravel = img_cb.ravel()

        #getting size of imgB_ravel
        taille_imgB_ravel = self.getTaille(img_cr_ravel)
        index = 5 if taille_imgB_ravel <= 255 else 9 
        imgB_ravel_1 = []
        imgB_ravel_2 = []
        i = 0

        while(i<taille_imgB_ravel//2):

            imgB_bit_1, index = self.get_pixel(img_cr_ravel, index)
            imgB_bit_2, _ = self.get_pixel(img_cb_ravel, i)
            imgB_ravel_1.append(imgB_bit_1)
            imgB_ravel_2.append(imgB_bit_2)
            i+=1
        
        if len(imgB_ravel_1) <len(imgB_ravel_2):
            img_cb_ravel, _ = self.get_pixel(img_cb_ravel, i)

        imgB_ravel = imgB_ravel_1 + imgB_ravel_2
        shape = [int(taille_imgB_ravel/(60*7 *3)), int(60*7), 3]
        print(shape)
        imgB = np.asarray(imgB_ravel, dtype = np.uint8)
        imgB = imgB.reshape(shape)
        return imgB