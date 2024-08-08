import time
import pigpio
import capture
import score
import ldr_calibration_config as calibration                           # (1)

# Below imports are part of Circuit Python and Blinka
import main
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def main():

    # Variable Decleration
    end_game = False
    turnCount = 1
    lastTurn = 0
    p1GPIO = 20
    p2GPIO = 21
    triggered = False
    a2dAddress = 0x48
    score.player1Score = 0
    score.player2Score = 0

    # Creating instance of pigpio
    pi = pigpio.pi()

    # Setting Up LEDs
    pi.set_mode(p1GPIO, pigpio.OUTPUT)
    pi.set_mode(p2GPIO, pigpio.OUTPUT)

    # Running display to display current score
    score.DisplayScore(score.player1Score, score.player2Score)

    # Turning off LEDs
    pi.write(p1GPIO, 0)  
    pi.write(p2GPIO, 0)

    # Voltage readings from ADS1115 when
    # LDR is in the Dark and in the Light
    LIGHT_VOLTS = calibration.MAX_VOLTS                                   # (2)
    DARK_VOLTS = calibration.MIN_VOLTS

    # Votage reading (and buffer) where we set
    # global variable triggered = True or False
    TRIGGER_VOLTS = LIGHT_VOLTS - ((LIGHT_VOLTS - DARK_VOLTS) / 2)        # (3)
    TRIGGER_BUFFER = 0.07

    # Create the I2C bus & ADS object.
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c, address = a2dAddress)
    analog_channel = AnalogIn(ads, ADS.P0)  #ADS.P0 --> A0	    

    print("game in session")

    while(not end_game): 


        print("Turn Count: " + str(turnCount))
        volts = analog_channel.voltage

        # if laser beam broke increment turn count
        if not triggered and volts < TRIGGER_VOLTS - TRIGGER_BUFFER:
            triggered = True
            print("laser broken")
            lastTurn = turnCount
            turnCount += 1

        elif triggered and (volts > TRIGGER_VOLTS + TRIGGER_BUFFER):
            triggered = False
            print("laser not broken")

        #time.sleep(.05)

        # If condition so LED only change when turn changes
        if(lastTurn != turnCount):

            # If condition to change LED depending on player turn
            if((turnCount % 2) == 1):

                # Turn player 1 LED off
                pi.write(p1GPIO, 1)

                # Turn player 2 LED on
                pi.write(p2GPIO, 0)

            if((turnCount % 2) == 0):

                # Turn player 1 LED on
                pi.write(p1GPIO, 0)

                # Turn player 2 LED off
                pi.write(p2GPIO, 1)

            lastTurn = turnCount


        if(turnCount == 9):
            
            # Delaying Program for 3 seconds
            time.sleep(3)

            # Taking Picture of Board
            #capture.CaptureBoard()

            #cropping img
            #capture.CropCapture("BoardCap1.jpg")

            print("Back in main")
            
            # Tracking Pucks on board
            score.DetectPucks("BoardCap1.jpg")

            # Calculating Score
            score.CalculateScore("BoardCap1.jpg")

            print(score.player1Score)
            print(score.player2Score)

            # display score to seven seg
            score.DisplayScore(score.player1Score, score.player2Score)

            turnCount = 1



        # If condition to end game
        if((score.player1Score >= 15) or (score.player2Score >= 15)):
            end_game = True

    score.DisplayScore(score.player1Score, score.player2Score)
    
    # Turning off LEDs
    pi.write(p1GPIO, 1)  
    pi.write(p2GPIO, 1)

    
    

if __name__ == "__main__":
    main()