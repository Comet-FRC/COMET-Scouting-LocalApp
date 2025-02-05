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


# store the initial game data
scout_initals = qr_data[0:3]
match_num = decodeNumber(qr_data[3])
team_num = decodeNumber(qr_data[4:7])


# decode the inital scout, match, and team data
decoded += "Scout Initals:\t" + qr_data[0:3]
decoded += "Match Number:\t" + str(match_num) + "\n"
decoded += "Team Number:\t" + str(decodeNumber(qr_data[4:7])) + "\n"
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

match_data = [[]]

for i in range(8) :
    match_data.append([])


# create a variable to store the location of the next non game data
location = 0

for i in range(7, len(qr_data), 3) : 
    # if the next thing isn't an event store the location and break
    if not (qr_data[i] in events):
        location = i
        # print(location)
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
            case 't':
                match_data[8] = time

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

# convert match data into pandas Series
import pandas as pd

match_data = pd.Series(match_data, index = ["L1", "L2", "L3", "L4", "Processor", "Net", "End Position", "Tags", "Auton Ended"], name = ("Match " + str(match_num))) 

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




# print(team_data)

# check if the file exists, if it does then 

# add new data to it

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


print(calculateScore())



# load connection to database
# import mysql.connector

# create connection object
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "COM3T-5cou7!ng-2025"
# )

# print the connection object
# print(mydb)

# create a cursor to execute SQL statements
# cursor = mydb.cursor()

# try to create a team data database
# try:
#     cursor.execute("CREATE DATABASE team_data;")
# except mysql.connector.errors.DatabaseError: 
#     print("database team_data already exists");

# make sure that we're using it
# cursor.execute("USE team_data;")

team_data_metrics = {
    "Team Num": "INTEGER",
    "OPR": "INTEGER",
    "Points Per Game": "FLOAT",
    "Matches": "IDK"
}

# try to create a table for that team's data
# cursor.execute(f"CREATE TABLE IF NOT EXISTS {match_num} ")

    




# # open the file and work on it
# with open(data_file, mode='w', newline='') as csvfile:
#     # create a csv file writer
#     writer = csv.writer(csvfile)

#     # write data to the csv file
#     writer.writerows([["hello world"] * 8] * 2)

