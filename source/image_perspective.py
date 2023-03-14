import cv2
import os

if __name__ == "__main__":
    print ('Running demo image_perspective')
    absolute_path = os.path.join(os.getcwd(), 'haw.jpg')
    img = cv2.imread('haw.jpg')
    rows,cols,ch = img.shape
    print(f'rows {rows},  cols {cols}, ch {ch}')
    cv2.imshow('test',img)
    input('hi')
