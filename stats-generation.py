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
    i_columns_to_avg = ["L1", "L2", "L3", "L4", "Processor", "Net", "Algae Removed", "Points Scored", "Auton Points", "Teleop Points"]
    columns_to_avg = team_data.loc[:, i_columns_to_avg]

    # handle list values in columns 1-6 (inclusive) by converting list-types to their length 
    for col in columns_to_avg.columns:
        if columns_to_avg[col].apply(lambda x: isinstance(x, list)).any(): # checks if any element is a list in the column 
            columns_to_avg.loc[:, col] = columns_to_avg[col].apply(lambda x: len(x) if isinstance(x, list) else x) # if so, convert to length of list

    # compute mean values for each column
    avg_values = columns_to_avg.mean().values.tolist()
    new_names = [f"Average {col}" for col in columns_to_avg.columns]
    # print(len(avg_values))
    # print(len(new_names))

    # get all tags applied 
    new_names.append("Tag Counts")
    tags_applied = team_data.loc[:, "Tags"]
    flattened = np.concatenate(tags_applied.values)

    # turn all tags into sorted list of each tag count
    counts = pd.Series(flattened).value_counts().sort_values()[::-1]
    avg_values.append(counts)

    # average end position
    new_names.append("Common End Position")
    end_pos = team_data["End Position"].mode()[0]
    avg_values.append(end_pos)

    teleop_values = {
        "L1": 2,
        "L2": 3,
        "L3": 4,
        "L4": 5
    }

    auton_values = {
        "L1": 3,
        "L2": 4,
        "L3": 6,
        "L4": 7
    }

    # get l1, l2, l3, l4 data out of team_data since columns_to_avg contains transformed data
    coral_points = 0
    teleop_coral_p = 0
    for col in team_data.loc[:, ["L1", "L2", "L3", "L4"]].columns:
        for i in range(len(team_data[col])):
            values = team_data[col].iloc[i]
            # based on timestamp and auton timestamp, determine which were scored during auton
            # due to this, higher prone to inaccuracy (competely depends on scout input of timestamp)
            for val in values:
                if val < team_data["Auton Ended"].iloc[i]:
                    # add up to point total (based on coral level)
                    coral_points += auton_values[col]
                else:
                    # add to teleop total
                    teleop_coral_p += teleop_values[col]

    # add coral auton point total to names and avg_values
    new_names.append("Average Coral Auton Points")
    avg_values.append(coral_points / len(team_data))

    # add coral teleop point total
    new_names.append("Average Coral Teleop Points")
    avg_values.append(teleop_coral_p / len(team_data))

    teamData = pd.DataFrame([avg_values], index=[filename[:-5]], columns=new_names)

    # append to main stats DataFrame
    stats = pd.concat([stats, teamData], ignore_index=False)

# print resulting DataFrame
print(stats.head())
# print(stats["Average Processor"].head())

# save to JSON for further processing
stats.to_json("team_stats.json", orient="index", indent=2)
