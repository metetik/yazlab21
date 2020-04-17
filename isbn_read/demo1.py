import os
import cv2
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

def show_all_pics():
    image_names = os.listdir("../data/")
    for imname in image_names:
        path = "../data/"+imname
        print(path)
        img = cv2.imread(path)
        cv2.imshow("pencere",img)
        cv2.waitKey(0)

def image_to_string(img):
    img1 = Image.fromarray(img)#numpy array'i Image nesnesine dönüştürme
    text = pytesseract.image_to_string(img1)
    return text
    
def find_orientation(img):
    if len(img.shape) == 3:
        rows,cols,ch = img.shape
    else:
        rows,cols = img.shape
    
    for i in range(0,3):
        text = image_to_string(img)
        if "ISBN" in text:
            #cv2.imshow('rotation',img)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            return img
        M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
        img = cv2.warpAffine(img,M,(cols,rows))    
        
    return None

def threshold_show(img):
    #simple threshholding
    ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
    print(type(thresh1))
    titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in range(6):
        plt.subplot(2,3,i+1)
        plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([])
        plt.yticks([])
    plt.show()

    #adaptive threshholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(gray,5)
    ret,th1 = cv2.threshold(median,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(median,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(median,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
    titles = ['Original Image', 'Global Thresholding (v = 127)',
                'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]
    for i in range(4):
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

    # Otsu's Thresholding
    # global thresholding
    ret1,th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    # Otsu's thresholding
    ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # plot all the images and their histograms
    images = [gray, 0, th1,
            gray, 0, th2,
            blur, 0, th3]
    titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
            'Original Noisy Image','Histogram',"Otsu's Thresholding",
            'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
    for i in range(3):
        plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
        plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
        plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
        plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
    plt.show()

def th_demo():
    image_names = os.listdir("../data/")
    ths = [0,0,0,0,0,0,0,0,0,0,0]
    
    for imname in image_names:
        thresh = []
        path = "../data/"+imname
        img = cv2.imread(path)
        #cv2.imshow("pencere",img)
        #cv2.waitKey(0)
        #simple threshholding
        ret,th = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        thresh += [th]
        ret,th = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
        thresh += [th]
        ret,th = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
        thresh += [th]
        ret,th = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
        thresh += [th]
        ret,th = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
        thresh += [th]
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        median = cv2.medianBlur(gray,5)
        ret,th = cv2.threshold(median,127,255,cv2.THRESH_BINARY)
        thresh += [th]
        th = cv2.adaptiveThreshold(median,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                    cv2.THRESH_BINARY,11,2)
        thresh += [th]
        th = cv2.adaptiveThreshold(median,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)
        thresh += [th]
        # Otsu's Thresholding
        # global thresholding
        ret1,th = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        thresh += [th]
        # Otsu's thresholding
        ret2,th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh += [th]
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret3,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh += [th]
        
        for i in range(11):
            if type(find_orientation(thresh[i])) != type(None):
                ths[i] += 1
        
    print(ths)
    #[14, 13, 14, 14, 8, 12, 3, 8, 15, 17, 15] --> Otsu's thresholding is the best

def isbn_read(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret2,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_oriented = find_orientation(thresh)
    if type(img_oriented) != type(None):
        text = image_to_string(img_oriented)
        return text
    else:
        return "None"
    
image_names = os.listdir("../data/")

for imname in image_names:
    path = "../data/"+imname
    print(path)
    img = cv2.imread(path)
    text = isbn_row(img)
    print(text)
    print(30*"#"+"\n"+30*"#")
    #img = find_orientation(img)
    #print(type(img))"""
