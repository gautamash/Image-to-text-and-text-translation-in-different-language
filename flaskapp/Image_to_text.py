from PIL import Image
import pytesseract
import cv2
import numpy as np
import imutils
import translate
#import translator
import codecs
from yandex import Translater
import locale
import sys
import grp
import pwd
import os
#print (sys.stdout.encoding)
from PIL import Image


def test():
    os.chmod("/home/ubuntu/flaskapp/Img1.png", 0777)
    uid = pwd.getpwnam("nobody").pw_uid
    gid = grp.getgrnam("nogroup").gr_gid	
    #os.chown("/home/ubuntu/flaskapp/static/Img1.png", uid, gid)
    im = Image.open("/home/ubuntu/flaskapp/Img1.png")
    im.save("/home/ubuntu/flaskapp/Img1.png", dpi=(300,300))	
    ref = cv2.imread("/home/ubuntu/flaskapp/Img1.png")
    height, width, channels = ref.shape
    max_height = 1000
    max_width = 700
    scaling_factor=1
    print(height, width) 
    # only shrink if img is bigger than required
    if max_height < height or max_width < width:
    # get scaling factor
       scaling_factor = max_height / float(height)
       if max_width/float(width) < scaling_factor:
          scaling_factor = max_width / float(width)
    # resize image
    ref = cv2.resize(ref, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    ref = cv2.resize(ref, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_AREA)
    morph= ref.copy()

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))	
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    gradient_image = cv2.morphologyEx(morph, cv2.MORPH_GRADIENT, kernel)

    image_channels = np.split(np.asarray(gradient_image), 3, axis=2)
    channel_height, channel_width, _ = image_channels[0].shape

    for i in range(0, 3):
        _, image_channels[i] = cv2.threshold(~image_channels[i], 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
        image_channels[i] = np.reshape(image_channels[i], newshape=(channel_height, channel_width, 1))

    image_channels = np.concatenate((image_channels[0], image_channels[1], image_channels[2]), axis=2)

    ref=   image_channels
				
    ref=cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    ref=cv2.equalizeHist(ref)
    # create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    ref = clahe.apply(ref)
    #cv2.imshow("Image", ref)
    os.environ["TESSDATA_PREFIX"] ="/usr/share/tesseract-ocr/tessdata/tesseract-ocr/tessdata"

    ref =Image.fromarray(ref)

    text= pytesseract.image_to_string(ref)

    print ('Orginal Text Extracted from Image:',text)
    
    if not text: 
    	text="No Text Available"
    tr = Translater()
    tr.set_key('trnsl.1.1.20180215T092213Z.aa1fc0e95288ebd7.dab36b649144ed25babf6247bcabd9885b5bb63f')
    tr.set_from_lang('en')
    tr.set_to_lang('hi')
    tr.set_text(text)
    TransText=tr.translate()
    #TransText="Not Available"
    print ('Translated Text',TransText)
    return text,TransText