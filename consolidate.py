def decodeNumber(data) :
    # create a variable to store decoded data
        decoded = 0

        # loop backwards through the data
        for i in range(len(data) - 1, -1, -1) :
            # add the current character's value to the decoded number
            decoded += ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\\".index(data[i])) * 91 ** (len(data) - 1 - i)

        # return the decoded number
        return decoded

# get the data from the json file
import json

file_name = "aws-data.json"

with open(file_name, 'r') as json_file :
  aws_data = json.load(json_file)

# loo pthrough the qr codes and

for aws_item in aws_data :
  qr_data = aws_item["code"]

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
      "Scout Initials": "",
      "Notes": aws_item["notes"]
  })

  # store the initial game data
  scout_initials = qr_data[0:3]
  match_num = decodeNumber(qr_data[3])
  team_num = decodeNumber(qr_data[4:7])
  auton_left = qr_data[7] == 'y'
  alliance_color = qr_data[8]


  # decoded += f"Scout Initials:\t{scout_initials}\n"
  # decoded += f"Match Number:\t{match_num}\n"
  # decoded += f"Team Number:\t{team_num}\n"
  # decoded += f"Auton Leave:\t{auton_left}\n"
  # decoded += f"Alliance Color:\t{colors[alliance_color]}\n"

  match_data["Scout Initials"] = scout_initials
  match_data["Auton Leave"] = auton_left
  match_data["Alliance Color"] = colors[alliance_color]
  match_data["Notes"] = aws_item["notes"]


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
      
      # decoded += events[event_type] + ": \t" + str(time) + " seconds\n"


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
      # decoded += tag_value + "\n"

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

  