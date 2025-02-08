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


# get the qr code from the camera

# initalize the camera and qrcode detector
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

# create a variable to store qr code data
qr_data = ""

# loop until a qr code is found
while True:
    # read the currect camera image
    ret, image = cap.read()

    # read the test image
    # ret = True
    # image = cv2.imread("testcode.png")

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


# get the data from the captured qr code

# create a string variable to temporarily store the decoded data
decoded = ""

# store the initial game data
scout_initals = qr_data[0:3]
match_num = decodeNumber(qr_data[3])
team_num = decodeNumber(qr_data[4:7])
alliance_color = qr_data[7]


colors = {
    "r": "Red",
    "b": "Blue"
}

# decode the inital scout, match, and team data
decoded += f"Scout Initals:\t{scout_initals}"
decoded += f"Match Number:\t{match_num}\n"
decoded += f"Team Number:\t{team_num}\n"
decoded += f"Alliance Color:\t{colors[alliance_color]}"
print(f"Alliance Color:\t{colors[alliance_color]}")

# decode the game event data
events = {
    "1": "L1 Scored",
    "2": "L2 Scored",
    "3": "L3 Scored",
    "4": "L4 Scored",

    "p": "Processor",
    "n": "Net Scored",
    "t": "Auton Ended"
}

# create an array to store the data collected during the match
match_data = [[] for _ in range(13)]

import pandas as pd

match_data = pd.Series({
    "L1": [],
    "L2": [],
    "L3": [],
    "L4": [],
    "Processor": [],
    "Net": [],
    "End Position": "",
    "Tags": [],
    "Auton Ended": 210,
    "Alliance Color": "",
    "Points Scored": 0,
    "Auton Points": 0,
    "Teleop Points": 0    
})

match_data["Alliance Color"] = colors[alliance_color]
# match_data[9] = colors[alliance_color]


# create a variable to store the location of the next non game data
location = 0

events = {
    "1": "L1",
    "2": "L2",
    "3": "L3",
    "4": "L4",
    "p": "Processor",
    "n": "Net",
    "t": "Auton Ended"
}

for i in range(8, len(qr_data), 3) : 
    # if the next thing isn't an event store the location and break
    if not (qr_data[i] in events):
        location = i
        break
    # otherwise decode the event and time 
    event_type = qr_data[i]
    time = decodeNumber(qr_data[i + 1:i + 3]) / 10.0

    # check if teh event is the auton time
    if event_type == 't' :
        match_data["Auton Ended"] = time
    else :
        match_data[events[event_type]].append(time)

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

match_data["End Position"] = end_pos

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
    match_data["Tags"].append(tag_value)
    decoded += tag_value + "\n"

print(match_data)

# calculate the points scored 
auton_points = 0
teleop_points = 0

# get when auton ended
try :
    auton_ended = int(match_data["Auton Ended"])
except TypeError :
    auton_ended = 100000000

# store point values
point_values = {
    "Auton L1": 3,
    "Auton L2": 4,
    "Auton L3": 6,
    "Auton L4": 7,

    "Teleop L1": 2,
    "Teleop L2": 3,
    "Teleop L3": 4,
    "Teleop L4": 5,

    "Processor": 6,
    "Net": 4,

    "None": 0,
    "Park": 2,
    "Shallow Climb": 6,
    "Deep Climb": 12
}

# coral points
for i in match_data.index[:4] :
    for j in match_data[i] :
        if j < auton_ended :
            auton_points += point_values[f"Auton {i}"]
        else :
            teleop_points += point_values[f"Teleop {i}"]

        
# processor points
for i in match_data.index[4:6] :
    for j in match_data[i] :
        if j < auton_ended :
            auton_points += point_values[i]
        else :
            teleop_points += point_values[i]
    
# end position

teleop_points += point_values[match_data[6]]

match_data["Auton Points"] = auton_points
match_data["Teleop Points"] = teleop_points
match_data["Points Scored"] = auton_points + teleop_points



# print the decoded data
# print(decoded)

# convert match data into pandas Series

print(match_data)

# create the file path
file_path = f"scouting-data/{team_num}.csv"

# check for existing csv
try:
    # get the data in the existing dataframe
    team_data = pd.read_csv(file_path, index_col="Match Number")

    # add the new value to the dataframe
    team_data.loc[match_num] = match_data

    # replace the csv file
    data_file = team_data.to_csv(file_path, index_label="Match Number")
except FileNotFoundError: 
    print("file does not exist, creating a new one")
    # create a new csv file for the given team with the current match data
    team_data = pd.DataFrame([match_data], index=[match_num])
    data_file = team_data.to_csv(file_path, index_label="Match Number")

def calculateScore() :
    sum = 0
    auton_time = match_data.iloc[8]
    

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

    # multiply the number of values of match_data less than the auton time by the auton score multiplier
    match_data.iloc[0:7]
        

    # do the same for the values greater than the auton time by the auton score multiplier


    # loop through the values of match_data
    


    def compute(key) :
        if auton_time > match_data.get(key = key): 
            return len(match_data.get(key = key)) * auton_scoring[key] 
        else :
            return len(match_data.get(key = key)) * teleop_scoring[key]



    return sum