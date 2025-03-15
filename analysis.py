import matplotlib.pyplot as plt
import os
import pandas as pd

#import stats file
stats = pd.read_json('team_stats.json', orient='index')

# Select a column to visualize
stats_names = stats.columns
stat_to_plot = ""
while True:
    for i in range(len(stats_names)):
        print(f"{i}: {stats_names[i]}")
    stat_to_plot = input("Enter a number of data to visualize: ")
    try:
        stat_to_plot = int(stat_to_plot)
    except:
        continue

    if stat_to_plot >= 0 and stat_to_plot < len(stats_names):
        stat_to_plot = stats_names[stat_to_plot]
        break
    

if "Common" not in stat_to_plot:
    # Plot bar chart
    plt.figure(figsize=(10, 5))
    stats[stat_to_plot].plot(kind="bar")

    # Labeling
    plt.xlabel("Teams")
    plt.ylabel(stat_to_plot)
    plt.title(f"{stat_to_plot} for Each Team")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
else:
    for i in stats[stat_to_plot].index:
        print(f"{i}:", stats[stat_to_plot].loc[i])

    
plt.show()
