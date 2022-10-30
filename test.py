import cv2
import numpy as np



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
    img_shapes = int(((len_txt*4)**(1/3))) +1
    img = np.zeros((img_shapes, img_shapes, img_shapes), dtype = np.uint8)

    text_bit = []
    for char in text:
        text_bit += standerdize_length(to_bin(ord(char)))
    text_bit = np.array(text_bit + ['0']*NB_BITS)

    img_ravel = img.ravel()
    len_img_bit = len(img_ravel)

    for i in range(len_img_bit):
        if i+1 == len_img_bit:
            break
        img_ravel[i] = change_bits(img_ravel[i], text_bit[i], text_bit[i+1])

    shape = (img_shapes,img_shapes, img_shapes)
    img = img_ravel.reshape(shape)
    img_RGB = cv2.imread("message_in_image.png", cv2.COLOR_RGB2BGR)
    print(img)
    #cv2.imwrite("message_in.jpg", img)
    cv2.imshow('i\'m the message1', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img

print(create_img_with_text("hello world"))