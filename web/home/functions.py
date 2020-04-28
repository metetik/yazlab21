import cv2
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

def image_to_string(img):
    img1 = Image.fromarray(img)#numpy array'i Image nesnesine dönüştürme
    text = pytesseract.image_to_string(img1)
    return text
    
def find_orientation(img):
    if len(img.shape) == 3:
        rows,cols,ch = img.shape
    else:
        rows,cols = img.shape
    
    for i in range(3):
        text = image_to_string(img)
        if "ISBN" in text:
            #cv2.imshow('rotation',img)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            return img
        M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
        img = cv2.warpAffine(img,M,(cols,rows))    
        
    return None

def resim_oku(imname):
    path = "../data/"+imname
    print(path)
    img = cv2.imread(path)
    #cv2.imshow("pencere",img)
    #cv2.waitKey(0)  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret2,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_oriented = find_orientation(thresh)
    if type(img_oriented) != type(None):
        text = image_to_string(img_oriented)
        lines = text.split("\n")
        isbn = ""
        for i in range(len(lines)):
            #print(str(i)+".satır : "+lines[i])
            if "ISBN" in lines[i]:
                #print(">>>>"+lines[i]+"<<<<")
                line = lines[i]
                break
        line = line.replace("i","1")
        line = line.replace("b","6")

        if line.find("ISBN-13") != -1:
            for i in range(line.find("ISBN-13")+6,len(line)):
                if line[i].isdigit():
                    isbn += line[i]
                #print(line[i],end="")
            #print("isbn : "+isbn)
        elif line.find("ISBN") != -1:
            for i in range(line.find("ISBN")+4,len(line)):
                if line[i].isdigit():
                    isbn += line[i]
                #print(line[i],end="")
            #print("isbn : "+isbn)
        
        if len(isbn) == 13:
            return isbn
        else:
            return isbn
    else:
        return "None"
