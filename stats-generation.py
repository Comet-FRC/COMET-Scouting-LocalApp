import pandas as pd
import numpy as np
import os

# initialize the file to be compiled by the end
stats = pd.DataFrame()

# path to scouting team data
data_dir = "scouting-data"

for filename in os.listdir(data_dir):
    if not filename.endswith(".json"):
        continue  # Skip non-JSON files
    
    # read team data
    team_data = pd.read_json(f"{data_dir}/{filename}", orient="index")

    # select columns to average out of the team data
    i_columns_to_avg = [0, 1, 2, 3, 4, 5, 6, 12, 13, 14]
    columns_to_avg = team_data.iloc[:, i_columns_to_avg]

    # handle list values in columns 1-6 (inclusive) by converting list-types to their length 
    for col in columns_to_avg.columns:
        if columns_to_avg[col].apply(lambda x: isinstance(x, list)).any(): # checks if any element is a list in the column 
            columns_to_avg.loc[:, col] = columns_to_avg[col].apply(lambda x: len(x) if isinstance(x, list) else x) # if so, 

    # compute mean values for each column
    avg_values = columns_to_avg.mean().values.tolist()
    new_names = [f"Average {col}" for col in columns_to_avg.columns]
    # print(len(avg_values))
    # print(len(new_names))

    # getting two most common tags
    # small visual error that can be fixed
    new_names.append("Common Tags")
    twoCommonTags = team_data["Tags"].mode()[:2]
    avg_values.append(twoCommonTags)
    '''for x in avg_values:
        if isinstance(x, list):
            print("x")
        print(f"{x}, ", end="")'''

    # average end position
    new_names.append("Common End Position")
    end_pos = team_data["End Position"].mode()[0]
    avg_values.append(end_pos)
     
    # get l1, l2, l3, l4 data out of team_data since columns_to_avg contains transformed data
    coral_points = 0
    teleop_coral_p = 0
    for col in team_data.iloc[:, [0, 1, 2, 3]].columns:
        for i in range(len(team_data[col])):
            values = team_data[col].iloc[i]
            # based on timestamp and auton timestamp, determine which were scored during auton
            # due to this, higher prone to inaccuracy (competely depends on scout input of timestamp)
            for val in values:
                if val < team_data["Auton Ended"].iloc[i]:
                    # add up to point total (based on coral level)
                    if col == "L1":
                        coral_points += 3
                    elif col == "L2":
                        coral_points += 4
                    elif col == "L3":
                        coral_points += 6
                    elif col == "L4":
                        coral_points += 7
                else:
                    # add to teleop total
                    if col == "L1":
                        teleop_coral_p += 2
                    elif col == "L2":
                        teleop_coral_p += 3
                    elif col == "L3":
                        teleop_coral_p += 4
                    elif col == "L4":
                        teleop_coral_p += 5

    # add coral auton point total to names and avg_values
    new_names.append("Average Coral Auton Points")
    avg_values.append(coral_points)

    # add coral teleop point total
    new_names.append("Average Coral Teleop Points")
    avg_values.append(teleop_coral_p)

    teamData = pd.DataFrame([avg_values], index=[filename[:-5]], columns=new_names)

    # append to main stats DataFrame
    stats = pd.concat([stats, teamData], ignore_index=False)

# print resulting DataFrame
print(stats.head())
# print(stats["Average Processor"].head())

# save to JSON for further processing
stats.to_json("team_stats.json", orient="index", indent=2)
