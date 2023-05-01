
"live only"
# import cv2
# import image_processing as img_proc
# import common.midi_creation as mc
# import image_processing_ai as img_proc_ai
# from imageai.Detection import ObjectDetection
# import numpy as np 
# #
# cap = cv2.VideoCapture(0)
# #




# if __name__ == "__main__":


#     while(1):
        
        
#         ret, img = cap.read()
#         shapes = img_proc.get_contours_from_image(img)         
#         img_proc_ai.detect_shapes_with_contour(shapes, img)
#         img_proc_ai.detect_shapes_with_ai(img)

#         cv2.imshow("met detectie", img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break    


        




"alleen camera en foto laten zien"

import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import numpy as np
import image_processing_ai as img_proc_ai

cap = cv2.VideoCapture(0)
img_counter = 0



img_counter = 0
if __name__ == "__main__":

    while(1):
        _, imageFrame = cap.read()

        cv2.imshow("Result", imageFrame)
    
        if cv2.waitKey(1) & 0xFF == ord('w'):
            img_path = "opencv_fram_{}.png".format(img_counter)
            cv2.imwrite(img_path, imageFrame)
            print("screenshot taken")
            img_path = "opencv_fram_{}.png".format(img_counter)
            img = cv2.imread(img_path) 
            img_counter+=1 

            shapes = img_proc.get_contours_from_image(img)      
            print("shapes: ", len(shapes))

            
            # shapes = img_proc.get_contours_from_image(img)         
            # img_proc_ai.detect_shapes_with_contour(shapes, img)
            # img_proc_ai.detect_shapes_with_ai(img)


            if len(shapes) < 1:  
                cv2.imshow("ai", img_proc_ai.detect_shapes_with_ai(img))
            else: 
                image, list_of_shapes = img_proc_ai.detect_shapes_with_contour(shapes, img)
                # img_proc_ai.detect_shapes_with_ai(image)
                cv2.imshow("contour", image)
                


                # shapes = img_proc.get_contours_from_image(img)
                # img_proc_ai.detect_shapes_with_contour(shapes, img)   
                # img_proc_ai.detect_shapes_with_ai(img)
                # cv2.imshow("contour", img)

        elif    cv2.waitKey(1) & 0xFF == ord('q'):
            break  



"met image stack" 

# import cv2
# import image_processing as img_proc
# import common.midi_creation as midi_creation
# import numpy as np
# import image_processing_ai as img_proc_ai

# cap = cv2.VideoCapture(0)

# img_counter = 0
# L2Gradient =  True
# def empty(a):
#     pass

# cv2.namedWindow("Parameters")
# cv2.resizeWindow("Parameters",640,240)
# cv2.createTrackbar("Threshold1","Parameters",159,255,empty)
# cv2.createTrackbar("Threshold2","Parameters",53,255,empty)
# cv2.createTrackbar("Area","Parameters",1111,30000,empty)






# def stackImages(scale,imgArray):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range ( 0, rows):
#             for y in range(0, cols):
#                 if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
#                 else:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
#                 if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.uint8)
#         hor = [imageBlank]*rows
#         hor_con = [imageBlank]*rows
#         for x in range(0, rows):
#             hor[x] = np.hstack(imgArray[x])
#         ver = np.vstack(hor)
#     else:
#         for x in range(0, rows):
#             if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
#                 imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
#             else:
#                 imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
#             if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#         hor= np.hstack(imgArray)
#         ver = hor
#     return ver

# img_counter = 0
# if __name__ == "__main__":
#     img_path = 'files\image_processing\example_shapes.png'
#     img = cv2.imread(img_path)    

#     while(1):

#         _, imageFrame = cap.read()
#         hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
#         success, img = cap.read()
    
#         threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
#         threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")

#         imgContour = img.copy()
#         imgBlur = cv2.GaussianBlur(img,(3,3),0)
#         imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
#         imgCanny = cv2.Canny(imgGray,threshold1,threshold2, L2gradient = L2Gradient)

#         kernel = np.ones((5,5))
#         imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
        
#         imgStack = stackImages(0.8,([imgCanny],[imgContour]))
#         cv2.imshow("Result", imgStack)


#         if cv2.waitKey(1) & 0xFF == ord('w'):
#             img_path = "opencv_fram_{}.png".format(img_counter)
#             cv2.imwrite(img_path, imgStack)
#             print("screenshot taken")
#             img_path = "opencv_fram_{}.png".format(img_counter)
#             img = cv2.imread(img_path) 
#             img_counter+=1 

#             shapes = img_proc.get_contours_from_image(img)      
#             print("shapes: ", len(shapes))
#             if len(shapes) < 1:  
#                 cv2.imshow("ai", img_proc_ai.detect_shapes_with_ai(img))
#             else: 
#                 image, list_of_shapes = img_proc_ai.detect_shapes_with_contour(shapes, img)
#                 cv2.imshow("contour", image)

#         elif    cv2.waitKey(1) & 0xFF == ord('q'):
#             break  



