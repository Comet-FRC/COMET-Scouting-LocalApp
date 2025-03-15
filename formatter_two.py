# Input data
matches = [
    (1, [25, 22, 14], 67),
    (2, [21, 17, 20], 72),
    (3, [5, 6, 2], 58),
    (4, [13, 12, 18], 63),
    (5, [29, 8, 16], 65),
    (6, [27, 24, 1], 70),
    (7, [15, 11, 28], 68),
    (8, [3, 26, 4], 62),
    (9, [10, 23, 5], 60),
    (10, [19, 7, 9], 64),
    (11, [22, 18, 6], 66),
    (12, [29, 1, 25], 71),
    (13, [2, 14, 11], 59),
    (14, [24, 15, 8], 61),
    (15, [13, 19, 27], 69),
    (16, [26, 28, 20], 73),
    (17, [16, 9, 23], 67),
    (18, [21, 12, 3], 72),
    (19, [4, 7, 24], 58),
    (20, [6, 10, 17], 63),
    (21, [20, 1, 19], 65),
    (22, [2, 15, 29], 70),
    (23, [9, 27, 12], 68),
    (24, [18, 11, 25], 62),
    (25, [26, 23, 22], 60),
    (26, [4, 5, 8], 64),
    (27, [17, 13, 14], 66),
    (28, [10, 3, 16], 71),
    (29, [7, 21, 15], 59),
    (30, [28, 29, 18], 61),
    (31, [12, 19, 11], 69),
    (32, [20, 22, 4], 73),
    (33, [25, 2, 3], 67),
    (34, [16, 5, 26], 72),
    (35, [17, 8, 1], 58),
    (36, [9, 21, 13], 63),
    (37, [28, 27, 10], 65),
    (38, [23, 14, 6], 70),
    (39, [18, 3, 7], 68),
    (40, [24, 25, 19], 62),
    (41, [5, 29, 21], 60),
    (42, [11, 4, 13], 64),
    (43, [8, 20, 9], 66),
    (44, [6, 16, 28], 71),
    (45, [22, 17, 15], 59),
    (46, [23, 2, 27], 61),
    (47, [1, 26, 12], 69),
    (48, [14, 10, 7], 73)
]

# Total number of players
num_players = 29

# Initialize the matrix and scores list
matrix = []
scores = []

# Process each match
for match in matches:
    match_id, players, score = match
    row = [0] * num_players  # Initialize a row with 0s
    for player in players:
        row[player - 1] = 1  # Set player participation to 1 (players are 1-indexed)
    matrix.append(row)
    scores.append(score)

# Format the matrix with commas and square brackets
formatted_matrix = [f"[{', '.join(map(str, row))}]" for row in matrix]

# Format the scores with commas and square brackets
formatted_scores = f"[{', '.join(map(str, scores))}]"

# Print the formatted matrix and scores
print("Matrix:")
for row in formatted_matrix:
    print(row)

print("\nScores:")
print(formatted_scores)