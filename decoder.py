import cv2
import numpy as np

def run(single_run: bool, first_run: bool, cap=cv2.VideoCapture(0), detector=cv2.QRCodeDetector()) :
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

    # initialize the camera and qrcode detector

    # create a variable to store qr code data
    qr_data = ""
    if not first_run :
        timer = 10
    else :
        timer = 0

    # loop until a qr code is found
    while True:
        # read the currect camera image
        ret, image = cap.read() 

        # read the test image
        # ret = True
        # image = cv2.imread("testcode.png")

        #  check if frame was read successfully
        if ret:

            if timer > 0 :
                timer -= 1

                org = (50, 50)
                fontFace = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                lineType = cv2.LINE_AA
                cv2.putText(image, "Code Scanned", org, fontFace, fontScale, color, thickness, lineType)  
            else :
                # check the image for a qr code
                data, bbox, _ = detector.detectAndDecode(image)

                # if a qr code is found, print and store the data and stop searching
                if data:
                    print(data)
                    qr_data = data
                    break



            # display the current image
            cv2.imshow("QR Code Scanner", image)

            # wait for a millisecond and check if a key was pressed
            if cv2.waitKey(1) != -1:
                exit()
                break
        else :
            break
        


    # release the camera and close the window
    if single_run:
        cap.release()
        cv2.destroyAllWindows()


    # get the data from the captured qr code

    # create a string variable to temporarily store the decoded data
    decoded = ""


    colors = {
        "r": "Red",
        "b": "Blue"
    }

    # decode the game event data
    events = {
        "1": "L1",
        "2": "L2",
        "3": "L3",
        "4": "L4",

        "p": "Processor",
        "n": "Net",
        "r": "Algae Removed",
        "t": "Auton Ended"
    }

    # create an array to store the data collected during the match
    match_data = [[] for _ in range(14)]

    import pandas as pd

    match_data = pd.Series({
        "L1": [],
        "L2": [],
        "L3": [],
        "L4": [],
        "Processor": [],
        "Net": [],
        "Algae Removed": [],
        "Auton Leave": False,
        "End Position": "",
        "Tags": [],
        "Auton Ended": 210,
        "Alliance Color": "",
        "Points Scored": 0,
        "Auton Points": 0,
        "Teleop Points": 0,
        "Scout Initials": ""
    })

    # store the initial game data
    scout_initials = qr_data[0:3]
    match_num = decodeNumber(qr_data[3])
    team_num = decodeNumber(qr_data[4:7])
    auton_left = qr_data[7] == 'y'
    alliance_color = qr_data[8]


    decoded += f"Scout Initials:\t{scout_initials}\n"
    decoded += f"Match Number:\t{match_num}\n"
    decoded += f"Team Number:\t{team_num}\n"
    decoded += f"Auton Leave:\t{auton_left}\n"
    decoded += f"Alliance Color:\t{colors[alliance_color]}\n"

    match_data["Scout Initials"] = scout_initials
    match_data["Auton Leave"] = auton_left
    match_data["Alliance Color"] = colors[alliance_color]


    # create a variable to store the location of the next non game data
    location = 0

    # events = {
    #     "1": "L1",
    #     "2": "L2",
    #     "3": "L3",
    #     "4": "L4",
    #     "p": "Processor",
    #     "n": "Net",
    #     "t": "Auton Ended"
    # }

    for i in range(9, len(qr_data), 3) : 
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


    # decode the tags from the data
    for i in range(location + 1, len(qr_data)) :
        tag_value = tags[decodeNumber(qr_data[i])]
        match_data["Tags"].append(tag_value)
        decoded += tag_value + "\n"

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
        "Algae Removed": 0,
        "Net": 4,

        "Auton Leave": 3,

        "None": 0,
        "Park": 2,
        "Shallow Climb": 6,
        "Deep Climb": 12
    }

    # auton leave
    if match_data["Auton Leave"] :
        auton_points += point_values["Auton Leave"]

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

    teleop_points += point_values[match_data["End Position"]]

    match_data["Auton Points"] = auton_points
    match_data["Teleop Points"] = teleop_points
    match_data["Points Scored"] = auton_points + teleop_points

    # print the decoded data
    print(match_data)


    # create the file path
    file_path = f"scouting-data/{team_num}.json"

    # check for existing json
    try:
        # get the data in the existing dataframe
        team_data = pd.read_json(file_path, orient='index')

        # add the new value to the dataframe
        team_data.loc[match_num] = match_data

        # replace the json file
        data_file = team_data.to_json(file_path, index=True, orient='index', indent=2)
    except FileNotFoundError: 
        print("file does not exist, creating a new one")
        # create a new json file for the given team with the current match data
        team_data = pd.DataFrame([match_data], [match_num])
        data_file = team_data.to_json(file_path, index=True, orient='index', indent=2)

    # add the team's score to the match match data JSON file

    return
    # exit()

    # store indexes of teams that we are getting data for
    teams = {
        339: 0,
        404: 0,
        449: 0,
        623: 0,
        888: 0,
        1111: 0,
        1727: 0,
        1811: 0,
        1885: 0,
        2106: 0,
        2199: 0,
        2377: 0,
        2421: 0,
        2537: 0,
        3714: 0,
        3748: 0,
        3793: 0,
        4464: 0,
        4541: 0,
        5587: 0,
        7770: 0,
        7886: 0,
        8622: 0,
        9403: 0,
        9684: 0,
        9709: 0,
        10224: 0,
        10449: 0,
        10679: 0
    }


    # turn the matches JSON to a dataframe
    try :
        matches = pd.read_json("matches.json", orient='columns')

        # check if the match data exists in the JSON file
        if match_num in matches.index :
            # add the team's participation to the JSON file
            matches.loc[match_num, f"{match_data["Alliance Color"]} Alliance Teams"][team_num] = 1

            # add the team's score to the JSON file
            matches.loc[match_num, f"{match_data["Alliance Color"]} Alliance Score"] += match_data["Points Scored"]
        else :
            # add the data to a new Series in the JSON file
            temp = pd.Series([teams, teams, 0, 0], ["Red Alliance Teams", "Blue Alliance Teams", "Red Alliance Score", "Blue Alliance Score"])

            # add score and participation of current team
            temp.loc[f"{match_data["Alliance Color"]} Alliance Teams"][team_num] = 1
            temp.loc[f"{match_data["Alliance Color"]} Alliance Score"] += match_data["Points Scored"]

            # add the Series to the JSON file
            matches.loc[match_num] = temp

        # replace the JSON file
        matches_file = matches.to_json("matches.json", orient='columns', indent=2)

    except FileNotFoundError:
        print("match data file does not exist, creating a new one")
        # create a new JSON file for match data

        # print(point_values)
        temp = pd.Series([teams, teams, 0, 0], ["Red Alliance Teams", "Blue Alliance Teams", "Red Alliance Score", "Blue Alliance Score"])

        # add participation of current team
        temp.loc[f"{match_data["Alliance Color"]} Alliance Teams"][team_num] = 1

        # add score of current team
        temp.loc[f"{match_data["Alliance Color"]} Alliance Score"] += match_data["Points Scored"]

        # create dataframe and JSON file
        matches = pd.DataFrame([temp], [match_num])
        matches_file = matches.to_json("matches.json", orient='columns', indent=2)

    
    exit()
    

    matches = pd.read_json("matches.json", orient='columns')

    # get data from the schedule file
    schedule = pd.read_json("schedule.json", orient='columns')

    # create array of validated matches
    validated_matches = []

    # create an array of validated scores
    validated_scores = []

    exit()

    # loop through matches file
    for i in matches.index :
        # check if all teams have been scouted
        if (i in schedule.index) :
            if (np.array(matches.loc[i, "Red Alliance Teams"]) == np.array(schedule.loc[i, "Red Alliance Teams"])).all() :
                # store validated match and score
                validated_matches.append(matches.loc[i, "Red Alliance Teams"])
                validated_scores.append(matches.loc[i, "Red Alliance Score"])

            if (np.array(matches.loc[i, "Blue Alliance Teams"]) == np.array(schedule.loc[i, "Blue Alliance Teams"])).all() :
                validated_matches.append(matches.loc[i, "Blue Alliance Teams"])
                validated_scores.append(matches.loc[i, "Blue Alliance Score"])


    validated_matches = np.array(validated_matches)
    validated_scores = np.array(validated_scores)

    transposed = validated_matches.T


    # print(validated_matches)
    # print(transposed)
    # print(validated_scores)

    # testMatches = np.array([[1, 1, 1, 0, 0, 0],
    #                         [1, 0, 1, 0, 1, 0],
    #                         [0, 1, 1, 1, 0, 0],
    #                         [1, 0, 0, 0, 1, 1],
    #                         [0, 1, 0, 1, 0, 1],
    #                         [0, 1, 1, 1, 0, 0],
    #                         [1, 0, 0, 0, 1, 1]])

    testScores = np.array([15, 19, 15, 15, 14, 15, 16])

    validated_matches = testMatches
    transposed = validated_matches.transpose()  
    validated_scores = testScores

    X = validated_matches
    y = testScores

    print(X)
    print(y)

    XT_X = np.dot(X.T, X)
    XT_y = np.dot(X.T, y)
    theta = np.linalg.inv(XT_X).dot(XT_y)

    print(theta)

    exit()

    print(validated_matches)
    print(transposed)


    print(transposed @ validated_matches)

    exit()

    print(transposed @ validated_scores)    

    # normal_equation = np.linalg.inv(transposed @ validated_matches) @ transposed @ validated_scores

    print(np.linalg.inv(transposed @ validated_matches))

    # print(matches)



# run()