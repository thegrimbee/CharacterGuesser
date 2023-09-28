import cv2
import random
import numpy as np

ORI_NAME = 'ori.jpg'
RES_NAME = 'res.jpg'

def img_variance(gray_image):
    mean_intensity = np.mean(gray_image)
    squared_diff = (gray_image - mean_intensity) ** 2
    variance = np.mean(squared_diff)
    
    return variance

path = "C:/Users/gabri/Downloads/CharacterGuesserBing/img/"

def blur_image():
    img = cv2.imread(path + RES_NAME)
    blurredImg = cv2.GaussianBlur(img, (13,13), 0)
    cv2.imwrite(path + RES_NAME, blurredImg)
    

difficulty_zooms = {'easy': 0.4, 'medium': 0.25, 'hard': 0.15}
difficulty_shuffles = {'easy': 4, 'medium': 7, 'hard': 11}

def create_zoomed_image(difficulty, modes):
    img = cv2.imread(path + ORI_NAME)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w,c = img.shape
    if 'shuffle' not in modes:
        var = 0
        tries = 0
        offset = 0
        while(var < 500 - offset):
            if tries % 50 == 0:
                offset += 100
            tries += 1
            x = random.randint(0,int((1-difficulty_zooms[difficulty])*w))
            y = random.randint(0,int((1-difficulty_zooms[difficulty])*h))
            grayZoomedImage = gray_img[y:int(y+difficulty_zooms[difficulty]*h), x:int(x+difficulty_zooms[difficulty]*w)]
            var = img_variance(grayZoomedImage)
            resImage = img[y:int(y+0.25*h), x:int(x+0.25*w)]
            print(var)
    else:
        shuffled_img = img.copy()
        pos_list = []
        dim = difficulty_shuffles[difficulty]
        for i in range(dim):
            for j in range(dim):
                pos_list.append([i*int(h/dim),j*int(w/dim)])
        random.shuffle(pos_list)
        for i in range(dim):
            for j in range(dim):
                shuffled_img[i*int(h/dim):(i+1)*int(h/dim),j*int(w/dim):(j+1)*int(w/dim)] = img[pos_list[i*dim+j][0]:pos_list[i*dim+j][0]+int(h/dim), pos_list[i*dim+j][1]:pos_list[i*dim+j][1]+int(w/dim)]
        resImage = shuffled_img
    if 'grayscale' in modes:
        resImage = cv2.cvtColor(resImage, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path + RES_NAME, resImage)
    if 'blur' in modes:
        blur_image()
    

    



