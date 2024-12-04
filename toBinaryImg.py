import cv2 # khai bao sp thu vien open cv
from PIL import Image # Khai sp thu vien xu li anh Pillow
import numpy as np # Khai bao sp thu vien toan hoc
# khai bao duong dan file
fileanh = 'rgb1.jpg'
#doc anh mau dung thu vien open cv
img = cv2.imread(fileanh,cv2.IMREAD_COLOR)
imgPIL = Image.open(fileanh)
#tao anh co cung kich thuoc va mode voi anh imgpill
binary = Image.new(imgPIL.mode,imgPIL.size)
#Lay kich thuoc cua anh tu imgpill
width= binary.size[0]
height = binary.size[1]

#thiet lap mot gia tri nguong de tinh anh nhi phan
Nguong = 150

#doc cac gai tri diem anh bang vong lap for
for x in range(width):
    for y in range(height):
        #lay cac gia tri diem anh
        R,G,B = imgPIL.getpixel((x,y))
        #dung pp chuyen doi anh mau RGB sang mau xam Luminance
        gray = np.uint8(0.2126*R+0.7152*G+0.0722*B)
        if ( gray <Nguong):
            binary.putpixel((x,y),(0,0,0))
        else:
            binary.putpixel((x,y),(255,255,255))
#chuyen anh tu pill sang opencb
nhiphan = np.array(binary)
#Hien thi anh ra man hinh
cv2.imshow ('Hinh goc ',img)
cv2.imshow('Anh nhi phan Binary',nhiphan)
cv2.waitKey(0)
cv2.destroyAllWindows()
#Tien hanh run