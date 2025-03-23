import matplotlib.pyplot as plt
import os
import pandas as pd

#import stats file
stats = pd.read_json('team_stats.json', orient='index')

# Select a column to visualize
stats_names = stats.columns
stat_to_plot = ""

team_analysis = False
team_num = -1

def do_analysis(stat_to_plot, team_num = 0) :
    if team_analysis:
        print(f"Analyzing team number {team_num}")
        
        # Calculate each scoring type in comparision to other teams' scoring
        comp_stat_names = ["Average L1", "Average L2", "Average L3", "Average L4", "Average Processor", "Average Net"]
        proficiency_stats = dict(zip(comp_stat_names, (float(stats.loc[team_num, x]) for x in comp_stat_names)))


        # create function to remove zeroes
        a = lambda arr : arr[arr != 0]

        # get the averages and standard deviations of each stat
        overall_means = [float(a(stats.loc[:, x].values).mean()) for x in comp_stat_names]
        overall_std = [float(a(stats.loc[:, x].values).std()) for x in comp_stat_names]
        
        import numpy as np 

        # find the z-score for each value
        z_scores = (np.array(list(proficiency_stats.values())) - overall_means) / overall_std

        from scipy.stats import norm
        
        # find the probability of getting each value
        probs = [norm.cdf(x) * 100 for x in z_scores] 

        # put the values in a dictionary
        proficiency_scores = dict(zip(comp_stat_names, probs))

        # Compute angles for the radar chart
        angles = np.linspace(0, 2 * np.pi, len(comp_stat_names), endpoint=False).tolist()
        angles += angles[:1]  # Close the loop

        # Initialize the figure
        fig = plt.figure(figsize=(12, 6))

        # Radar Chart
        ax1 = fig.add_subplot(223, polar=True)
        values = list(proficiency_scores.values())
        values += values[:1]  # Close the loop
        ax1.plot(angles, values, 'o-', linewidth=2, label='Team Stats')
        ax1.fill(angles, values, alpha=0.25)
        ax1.set_ylim(0, 100)  # Set maximum value to 100
        ax1.set_rgrids(range(0, 101, 20))  # Set grid lines at intervals of 20
        ax1.set_thetagrids(np.degrees(angles[:-1]), [x.replace("Average ", "") for x in comp_stat_names])
        ax1.set_title('Proficiencies\n')

        # Bar Chart
        ax2 = fig.add_subplot(2, 2, (1, 2))
        score_categories = ["Average Points Scored", "Average Teleop Points", "Average Auton Points"]

        team_scores = [stats.loc[team_num, x] for x in score_categories]
        mean_scores = [float(stats.loc[:, x].values.mean()) for x in score_categories]
        labels = ['Overall Scoring', 'Teleop Scoring', 'Auton Scoring']
        x = np.arange(len(labels))
        width = 0.35
        ax2.bar(x - width/2, team_scores, width, label='Team')
        ax2.bar(x + width/2, mean_scores, width, label='Mean')
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels)
        ax2.set_title('Average Scoring')
        ax2.legend()

        team_tag_counts = stats.loc[team_num, "Tag Counts"]

        # Tag Histogram
        ax3 = fig.add_subplot(2, 2, 4)
        labels = team_tag_counts.keys()
        x = np.arange(len(labels))
        width = 0.35
        ax3.bar(x, team_tag_counts.values())
        ax3.set_xticks(x)
        ax3.set_xticklabels(labels)
        ax3.set_title("Common Tags")


        # Adjust layout
        plt.tight_layout()    
            
    elif "Common" not in stat_to_plot:
        print("Opening window...")
        # Plot bar chart
        plt.figure(figsize=(10, 5))
        stats[stat_to_plot].sort_values()[::-1].plot(kind="bar")

        # Labeling
        plt.xlabel("Teams")
        plt.ylabel(stat_to_plot)
        plt.title(f"{stat_to_plot} for Each Team")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    else:
        print("Displaying information in the console... though you should just view the .json files for this")
        for i in stats[stat_to_plot].index:
            print(f"{i}:", stats[stat_to_plot].loc[i] if stat_to_plot == "Common End Position" else stats[stat_to_plot].loc[i]['0'])

        
    plt.show()


while True:
    for i in range(len(stats_names)):
        print(f"{i}: {stats_names[i]}")
    print(f"{len(stats_names)}: Team Analysis")
    stat_to_plot = input("Enter a number of data to visualize: ")
    try:
        stat_to_plot = int(stat_to_plot)
    except:
        continue

    if stat_to_plot >= 0 and stat_to_plot < len(stats_names):
        stat_to_plot = stats_names[stat_to_plot]
        do_analysis(stat_to_plot)
    elif stat_to_plot == 14:
        while True: 
            team_num = input("Enter the team number to run analysis of: ")
            try: 
                team_num = int(team_num)
            except:
                continue

            if team_num in stats.index :
                team_analysis = True
                break
            elif team_num == -1 :
                exit()
            else :
                print("That's not a valid team number. Here are all the valid team numbers:")
                print(list(stats.index))
                print()
        do_analysis(stat_to_plot, team_num)
    elif stat_to_plot == -1:
        exit()

