import os
import cv2

image_names = os.listdir("../data/")
print(image_names)

def show_pics():
    for i in range(len(image_names)):
        path = "../data/"+image_names[i]
        print(path)
        img = cv2.imread(path)
        cv2.imshow("pencere",img)
        cv2.waitKey(0)

show_first_pics()


