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
            columns_to_avg[col] = columns_to_avg[col].apply(lambda x: len(x) if isinstance(x, list) else x) # if so, 

    # compute mean values for each column
    avg_values = columns_to_avg.mean().values
    new_names = [f"Average {col}" for col in columns_to_avg.columns]

    # getting two most common tags
    new_names.append("Average Tags")
    twoCommonTags = team_data["Tags"].mode()[:2]
    avg_values = np.append(avg_values, twoCommonTags)

    # average end position
    new_names.append("Average End Position")
    end_pos = team_data["End Position"].mode()[0]
    avg_values = np.append(avg_values, end_pos)
     
    # get l1, l2, l3, l4 data out of team_data since columns_to_avg contains transformed data
    coral_points = 0
    for col in team_data.iloc[:, [0, 1, 2, 3]].columns:
        for i in range(len(team_data[col])):
            values = team_data[col].iloc[i]
            print(values)
            # based on timestamp and auton timestamp, determine which were scored during auton
            for val in values:
                if val < team_data["Auton Ended"].iloc[i]:
                    # add up to point total (based on coral level)
                    if col == "L1":
                        coral_points += 3
                    elif col == "L2":
                        coral_points += 4
                    elif col == "L3":
                        coral_points += 6
                    else:
                        coral_points += 7

    # add coral auton point total to names and avg_values
    new_names.append("Average Coral Auton Points")
    avg_values = np.append(avg_values, coral_points)

    # create a DataFrame with the team's averaged stats
    teamData = pd.DataFrame([avg_values], index=[filename[:-5]], columns=new_names)

    # append to main stats DataFrame
    stats = pd.concat([stats, teamData], ignore_index=False)

# print resulting DataFrame
print(stats.head())
# print(stats["Average Processor"].head())

# save to JSON for further processing
stats.to_json("team_stats.json", orient="index", indent=2)

#TODO: Matplotlib analysis here
import matplotlib


