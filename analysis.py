import matplotlib.pyplot as plt
import os
import pandas as pd

#import stats file
stats = pd.read_json('team_stats.json', orient='index')

# Select a column to visualize
stat_to_plot = ""
while stat_to_plot == "" or not (stat_to_plot in stats.columns):
    print(f"'{stat_to_plot}'")
    stat_to_plot = input("Enter a column name to visualize: ")

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
    # implement string val plotting
    pass
plt.show()
