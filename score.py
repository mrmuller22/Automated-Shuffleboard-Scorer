# File for calculating and updating score
import cv2
import numpy as np
import time
from PIL import Image, ImageDraw, ImageFont 
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306


# Variable Decleration
global redPucks
global blackPucks

# Variable Decleration
redPucks = []
blackPucks = []
player1Score = 0
player2Score = 0
scoreLines = [17, 107, 206] #px location of score lines


# Function to Detect Board Objects
def DetectPucks(imagePath):

    print("Detecting Pucks")

    # Opening the image 
    image = cv2.imread(imagePath)

    # Converting the image to a grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #applying a blur to the image 
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detecting the circles around the pucks
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.25, 35, param1=50,
                            param2=30, minRadius=15, maxRadius=50)

    # Looping through circles
    if circles is not None:

        # Variable Decleration
        avgRValue = 0

        # Converting coordinates of circle into ints
        circles = np.round(circles[0, :]).astype("int")

        for (x,y, r) in circles:

            # Detecting the color of the center circle
            color = cv2.mean(image[y-10:y+10, x-10:x+1])

            avgRValue += color[0]
        
        avgRValue = avgRValue/len(circles)
        avgRValue = avgRValue - 20

        # Looping through cirles 
        for (x, y, r) in circles:

            # Creating circles around each puck
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)

            
            # Detecting the color of the center circle
            color = cv2.mean(image[y-10:y+10, x-10:x+1])
            
            print(x,y,color)

            # Draw center circle
            cv2.circle(image, (x, y), 3, (255, 0, 0), 4)

            # If conditions to assign score value to puck
            if ((scoreLines[0] + r) < y):
                 points = 4

            if((scoreLines[1] - r) > y > (r + scoreLines[0])):
                points = 3
                
            elif((scoreLines[1] - r) > y > (r + scoreLines[2]) or (scoreLines[2] - r) > y > (scoreLines[1] - r)):
                points = 2

            elif(y > scoreLines[2]):
                points = 1

            # if color is closer to red than black 
            if (color[0] > avgRValue):
                # append puck position to red puck list
                redPucks.append([x, y, points])

            # if color is closer to black than red
            elif (color[0] < avgRValue):
                # append puck position to black puck list
                blackPucks.append([x, y, points])

    #For testing purposes
    # cv2.imshow("GameBoard" , image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows
  

# Function to calculate score
def CalculateScore(image):

    print("Calculating Score")

    global player1Score
    global player2Score

    print(blackPucks)
    print(redPucks)

    # Opening the image 
    image = cv2.imread(image)

    # Getting height of image
    height = image.shape[1]

    farthestBlackPuck = height
    farthestRedPuck = height

    if blackPucks is not None:
        #Finding Fathest Black Puck
        for bpuck in blackPucks:
        
            if(bpuck[1] < farthestBlackPuck):
                farthestBlackPuck = bpuck[1]

    if redPucks is not None:
        #Finding Farthest Red Puck
        for rpuck in redPucks:
            
            if(rpuck[1] < farthestRedPuck):
                farthestRedPuck = rpuck[1]

    if blackPucks is not None:        
        # If statement to calculate Player1 Score
        if((farthestBlackPuck < farthestRedPuck)):

            # Looping through puck list
            for puck in blackPucks:

                # If puck y position less than farthest red puck position
                if(puck[1] < farthestRedPuck):

                    # Add Puck Score to Player 1 score
                    player1Score += puck[2]

    if redPucks is not None:
        # If statement to calculate Player 2 Score
        if((farthestRedPuck < farthestBlackPuck)):

            # Looping though red pucks
            for puck in redPucks:

                # if puck y position less than farthest black puck
                if(puck[1] < farthestBlackPuck):

                    # Add puck score to player2 score
                    player2Score += puck[2]


#Function to Display Score       
def DisplayScore(p1s, p2s):

    print("Displaying Score")

    oledAddress = 0x3C

    display1 = i2c(port=1, address=0x3C)
    #display2 = i2c(port=2, address=0x3c)

    device1 = ssd1306(display1)
    #device2 = ssd1306(display2)

    device1.clear()
    #device2.clear()

    player1Score = str(p1s)
    player2Score = str(p2s)

    # Font Size 
    fontSize = (device1.height * .75)

    # Declaring font type 
    font = ImageFont.truetype("Sherman-Display.ttf", int(fontSize))

   # Drawing Score 
    with canvas(device1) as draw:
        draw.text((device1.width*.1, device1.height/7), player1Score, font=font, fill="white")
        draw.text((device1.width*.75, device1.height/7), player2Score, font=font, fill="white")

    # with canvas(device2) as draw:
    #     draw.text((device1.width/2, device1.height/7), player2Score, font=font, fill="white")



