import cv2
import numpy as np

def decodeNumber(data) :
  # create a variable to store decoded data
  decoded = 0

  # loop backwards through the data
  for i in range(len(data) - 1, -1, -1) :
      # add the current character's value to the decoded number
      decoded += ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\\".index(data[i])) * 91 ** (len(data) - 1 - i)

  # return the decoded number
  return decoded

  

# initalize the camera and qrcode detector
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

# create a variable to store qr code data
qr_data = ""

# loop until a qr code is found
while True:
    # read the currect camera image
    ret, image = cap.read()

    #  check if frame was read successfully
    if ret:
        # display the current image
        cv2.imshow("QR Code Scanner", image)

        # wait for a millisecond and check if a key was pressed
        if cv2.waitKey(1) != -1:
            break

        # check the image for a qr code
        data, bbox, _ = detector.detectAndDecode(image)

        # if a qr code is found, print and store the data and stop searching
        if data:
            print(data)
            qr_data = data
            break
    else :
        break
    


# release the camera and close the window
cap.release()
cv2.destroyAllWindows()

# create a variable to store the decoded data
decoded = ""

match_num = decodeNumber(qr_data[0:1])

# decode the inital match and team data
decoded += "Match Number:\t" + str(match_num) + "\n"
decoded += "Team Number:\t" + str(decodeNumber(qr_data[1:4])) + "\n"
# decode the game event data
events = {
    "1": "L1 Scored",
    "2": "L2 Scored",
    "3": "L3 Scored",
    "4": "L4 Scored",

    "p": "Processor",
    "n": "Net Scored"
}

# create a temporary array for the coral scores

match_data = [[]]

for i in range(7) :
    match_data.append([])


# create a variable to store the location of the next non game data
location = 0

for i in range(4, len(qr_data), 3) : 
    # if the next thing isn't an event store the location and break
    if not (qr_data[i] in events):
        location = i
        print(location)
        break
    # otherwise decode the event and time 
    event_type = qr_data[i]
    time = decodeNumber(qr_data[i + 1:i + 3]) / 10.0

    # check if the event is a coral event
    if event_type in "1234" :
        match_data[int(event_type) - 1].append(time)
    else :
        match (event_type) :
            case 'p': 
                match_data[4].append(time)
            case 'n': 
                match_data[5].append(time)

    # add the data to the series
    
    decoded += events[event_type] + ": \t" + str(time) + " seconds\n"


# decode the endgame data
positions = {
    "x": "None",
    "d": "Deep Climb",
    "s": "Shallow Climb",
    "k": "Park"
}

end_pos = positions[qr_data[location]]

decoded += "End Position: \t" + end_pos + "\n"

match_data[6] = end_pos

# decare existing tags
tags = {
    1: "Fast Robot",
    2: "Good Auton",
    3: "Good Driving",
    4: "Good Defense",
    5: "Good Intake",
    6: "Efficient Scoring",

    65: "Slow Robot",
    66: "Bad Auton",
    67: "Bad Driving",
    68: "Bad Defense",
    69: "Bad Intake",
    70: "No Auton",
    71: "Bad Scoring",
}

decoded += "Tags:\n"

# decode the tags from the data
for i in range(location + 1, len(qr_data)) :
    tag_value = tags[decodeNumber(qr_data[i])]
    match_data[7].append(tag_value)
    decoded += tag_value + "\n"


# print the decoded data
# print(decoded)

# convert array into series of ndarrays



# TODO: add the data to a database or find a place to put it
import pandas as pd

#TODO: REMAINING STEPS
# read existing csv (columns - data types, rows - matches)
match_data = pd.Series(match_data, index = ["L1", "L2", "L3", "L4", "Processor", "Net", "End Position", "Tags"], name = ("Match " + str(match_num))) 
print(match_data)

# add new data to it

def calculateScore() :
    sum = 0
    auton = False

    

    auton_scoring = {
        "L1": 3,
        "L2": 4,
        "L3": 6,
        "L4": 7,
        "Processor": 6,
        "Net": 4,
    }

    teleop_scoring = {
        "L1": 2,
        "L2": 3,
        "L3": 4, 
        "L4": 5,
        "Processor": 6,
        "Net": 4
    }

    def compute(key) :
        if auton: 
            return len(match_data.get(key = key)) * auton_scoring[key] 
        else :
            return len(match_data.get(key = key)) * teleop_scoring[key]

    


    return sum


print(calculateScore())

# compile findings into database