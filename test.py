import cv2
import numpy as np

from builtins import int 

EXT = "hello world, it's me Mariò"
IMG_PATH = "tree.jpg"
NEW_PATH = "tree_new.png"
NB_BITS = 8

# Transform a text into a list of binary numbers
def to_bin(n):
    return list(bin(n).replace("0b", ""))

# Standarize the length of a binary number
def standerdize_length(caracter):
    if len(caracter) < NB_BITS:
        return ['0']*(NB_BITS - len(caracter)) + caracter
    return caracter


# change bits of the image to add text
def change_bits(value, bit1, bit2):
    value = standerdize_length(to_bin(value))
    value[-5] = bit1
    value[-6] = bit2
    return int("".join(value),2)

# Create a new image from a text
def create_img_with_text(text):

    len_txt = len(text)
    # for each caracter in the text we need 4 pixels 
    img_shapes = int(((len_txt*4)**(1/2)))    
    img = np.zeros((img_shapes, img_shapes, 3), dtype = np.uint8)

    text_bit = []
    for char in text:
        text_bit += standerdize_length(to_bin(ord(char)))
    text_bit = np.array(text_bit + ['0']*NB_BITS)

    img_ravel = img.ravel()
    len_img_bit = len(img_ravel)
    len_text = len(text_bit)
    for i in range(len_img_bit):
        if i+1 == len_img_bit or i+1 == len_text:
            break
        img_ravel[i] = change_bits(img_ravel[i], text_bit[i], text_bit[i+1])

    shape = (img_shapes,img_shapes, 3)
    img = img_ravel.reshape(shape)
    
    return img

def insert_img(value_A, value_B):
    value_A = standerdize_length(to_bin(value_A))
    value_A[7:] = value_B
    return int("".join(value_A),2)


"""    imgB = create_img_with_text("hello world, it's me Mariò")

    print(imgB.ravel())
    imgB=cv2.cvtColor(imgB, cv2.COLOR_RGB2YCrCb) 
    imgB_cr = imgB[:,:,1]
    print("iiiiii", imgB_cr.ravel())
    imgB=cv2.cvtColor(imgB, cv2.COLOR_YCrCb2RGB) 
    imgB=cv2.cvtColor(imgB, cv2.COLOR_RGB2YCrCb) 
    imgB_cr = imgB[:,:,1]
    print("aaaa", imgB_cr.ravel())
"""


liste = [1,5,8,9,7,8,7,8, 9]
liste_1 = liste[:len(liste)//2]
liste_2= liste[len(liste)//2:]
for i, j in zip(range(len(liste_1)), range(len(liste_2))):
    print(liste_1[i], liste_2[j])


def encodage(imgA_path, text):

    imgA = cv2.imread(imgA_path, cv2.COLOR_BGR2RGB)
    imgA = cv2.cvtColor(imgA, cv2.COLOR_RGB2YCrCb)
    len_text = len(text)
    len_img = imgA.shape[0]*imgA.shape[1] *4
    if len_text> len_img: raise ValueError()
    else:
        imgA=np.uint16(imgA)*255
        imgB = create_img_with_text(text)  
    
        # COnvert last 4 bits of mgA ro 0111***********
        imgA_ravel = imgA.ravel()
        for i in range(len(imgA_ravel)):
            imgA_ravel_i= standerdize_length(to_bin(imgA_ravel[i]))
            imgA_ravel_i[-4:] = ['0','1','1','1']
            imgA_ravel[i] = int("".join(imgA_ravel_i),2)
        imgA = imgA_ravel.reshape(imgA.shape)
        #*******************************

        # Use only cr cb ********************
        img_cr = imgA[:, :, 1]
        img_cb = imgA[:, :, 2]
        imgB_ravel = imgB.ravel()

        img_cr_ravel = img_cr.ravel()
        img_cb_ravel = img_cb.ravel()
        imgB_ravel_1 = imgB_ravel[:len(imgB_ravel)//2]
        imgB_ravel_2 = imgB_ravel[len(imgB_ravel)//2:]
      
        for i in range(len(imgB_ravel_2)):
            if i > len(imgB_ravel_1)-1:
                break
            imgB_i_bit_1 = standerdize_length(to_bin(imgB_ravel_1[i]))
            imgB_i_bit_2 = standerdize_length(to_bin(imgB_ravel_2[i]))
            img_cr_ravel[i*(len(imgB_ravel)+9)//2] = insert_img(img_cr_ravel[i], imgB_i_bit_1)
            img_cb_ravel[i*(len(imgB_ravel)+9)//2] = insert_img(img_cb_ravel[i], imgB_i_bit_2)

            """    img_cr_ravel[i] = insert_img(img_cr_ravel[i], imgB_i_bit_1)
                img_cb_ravel[i] = insert_img(img_cb_ravel[i], imgB_i_bit_2)"""

        img_cr = img_cr_ravel.reshape(img_cr.shape)
        img_cb = img_cb_ravel.reshape(img_cb.shape)

        imgA[:, :, 1] = img_cr
        imgA[:, :, 2] = img_cb

        print(imgA.shape)
        cv2.imwrite("weshHBIBI.png", imgA)

        return imgA
    
"""    img = encodage("test.jpg", "this is a security project why am i doing this, it's cool man!")

    img =  cv2.cvtColor(img, cv2.COLOR_YCrCb2RGB)
    img2 =  cv2.imread("test.jpg", cv2.IMREAD_COLOR)
    cv2.imshow('the IMAGE', img)
    cv2.imshow('the IMAGE_', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""



"""    cv2.imshow('the IMAGE', imgA)
    cv2.imshow('the message', imgB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""


""" liste_ = [1/4, 1/2, 3/4]
    for elm  in liste:
    imgA_zone_1 = imgA[:imgA.shape[0]/4, :imgA.shape[1]/4, :]
    imgA_zone_2 = imgA[imgA.shape[0]/4:imgA.shape[0]/2, imgA.shape[1]/4:imgA.shape[1]/2, :]
    imgA_zone_3 = imgA[imgA.shape[0]/2:3*imgA.shape[0]/4, imgA.shape[1]/2:3*imgA.shape[1]/4, :]
    imgA_zone_4 = imgA[3*imgA.shape[0]/4:, 3*imgA.shape[1]/4:, :]"""