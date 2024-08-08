from time import sleep

import cv2

# Function to Capture Picture of board
def CaptureBoard():

    # Creating camera object
    camera = cv2.VideoCapture(0)

    # if condition to check if camera open
    if not camera.isOpened():
        print("Cannot open Camera")

    else:

        # Delaying for 3 sec
        sleep(3)

        # taking picture    
        res, capture = camera.read()
        print("picture taken")

        if res:
            # saving picture to current directory
            cv2.imwrite('BoardCapture.jpg', capture)
        
            sleep(1)

def CropCapture(imgpath):

    #Loading the image in
    image = cv2.imread(imgpath)

    # Declaring the x and y coorednates of the board
    x, y, w, h = 100, 20, 325, 360

    # Cropping the image 
    cropped_image = image[y:y+h, x:x+w]

    cv2.imwrite('BoardCaptureCrop.jpg', cropped_image)


    

