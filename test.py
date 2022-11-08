import cv2
import numpy as np

def splitTextToTriplet(string):
    words = string.split()
    grouped_words = [' '.join(words[i: i + 7]) for i in range(0, len(words), 7)]
    return grouped_words

def convert_text_img(text_):
    len_txt = len(text_)
    print(len_txt)
    groupe_text = splitTextToTriplet(text_)
    print(len(groupe_text))
    img1 = np.zeros((24*len(groupe_text), 50*7, 3), dtype = np.uint8)
    y_start = 15
    y_increment = 20
    print(groupe_text)
    for i, line in enumerate(groupe_text):
        y = y_start + i*y_increment
        cv2.putText(img=img1, text=line, org=(0, y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(255,255,0), 
        thickness=1)
    
    #print(img1)
    cv2.imshow('image_text', img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

convert_text_img("Club scientifique de l'USTHB qui a pour but de promouvoir l'esprit de partage et la philosophie Open Source.")
    
