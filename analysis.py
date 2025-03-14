import pandas as pd
import numpy as np
import os

# recalculates all compiled statistics
stats = pd.DataFrame()
for filename in os.listdir("scouting-data"):
    team_data = pd.read_json(f"scouting-data/{filename}", orient="index")
    #print(team_data.head(5))

    # choose columns to average out
    i_columns_to_avg = [12, 13, 14] # 4, 5, 6 - more columns to add
    columns_to_avg = team_data.iloc[:, i_columns_to_avg]
    print(columns_to_avg.head(5))
    # print(type(columns_to_avg["Processor"]))

    # for each selected column, average the values across rows (matches)

    # TO DO - DOESN'T WORK FOR EMPTY PANDA SERIES CASES (e.g. if no values were inputted for processor)
    # NEED TO IMPLEMENT FOR COLUMNS 4,5,6
    avg_values = columns_to_avg.mean().values
    new_names = [f"Average {col}" for col in columns_to_avg.columns ]
    teamData = pd.DataFrame([avg_values], index=[filename[:-5]], columns=new_names)
    stats = pd.concat([stats, teamData], ignore_index = False)
    '''if len(stats) == 0:
        stats.columns = [f"Average {col}" for col in columns_to_avg.columns]'''

print(stats.head(5))

# TO BE IMPLEMENTED - put team data into stats json (rows - teams, stats - columns) 


