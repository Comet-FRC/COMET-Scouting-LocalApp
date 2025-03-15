import numpy as np
import pandas as pd

red_teams = []
blue_teams = []

for i in range(56) :
  red_teams.append([0] * 29)
  blue_teams.append([0] * 29)


teams = {
    339: 0,
    404: 1,
    449: 2,
    623: 3,
    888: 4,
    1111: 5,
    1727: 6,
    1811: 7,
    1885: 8,
    2106: 9,
    2199: 10,
    2377: 11,
    2421: 12,
    2537: 13,
    3714: 14,
    3748: 15,
    3793: 16,
    4464: 17,
    4541: 18,
    5587: 19,
    7770: 20,
    7886: 21,
    8622: 22,
    9403: 23,
    9684: 24,
    9709: 25,
    10224: 26,
    10449: 27,
    10679: 28
}

input_data = """
    7770 5587 2106 7886 10679 404
    3714 339 2421 2537 8622 1111
    1885 623 2377 10449 449 10224    
    3793 2199 1811 4464 1727 9403 
    4541 7886 888 3748 2537 9709   
    404 1111 10224 2106 7770 2421   
    1811 3714 10449 2199 5587 4464 
    4541 3748 339 1727 1885 3793   
    9709 888 623 10679 8622 2377     
    404 2537 449 9403 2421 2199     
    7886 5587 1111 3714 4541 1885 
    1811 4464 10679 623 3748 2106   
    9403 339 7770 2377 449 888       
    10449 8622 1727 10224 3793 9709 
    2199 2106 1885 2421 404 4541   
    2377 9403 10679 449 1111 1811   
    3793 888 2537 10224 10449 3748   
    4464 623 339 8622 7886 7770     
    5587 9709 2377 404 1727 3714   
    1811 10449 9403 1885 10679 3748 
    1111 2199 888 8622 10224 623    
    7886 7770 2421 3793 3714 5587 
    2537 4541 1727 2106 4464 449   
    339 10679 10224 9709 10449 404     
    888 9403 3714 1111 3793 623    
    2537 5587 8622 1727 2377 7770 
    7886 1811 3748 449 9709 339     
    2106 4541 2199 4464 1885 2421 
    7770 404 3793 623 2537 9403     
    8622 9709 3714 3748 888 5587   
    449 10224 1885 1727 2421 1811   
    4541 2377 4464 339 1111 10449   
    9709 10679 2199 2106 7886 3793 
    2421 3748 449 888 10224 7770     
    1111 3714 1727 623 404 1811     
    10679 4541 8622 2199 339 2537   
    1885 10449 5587 9403 7886 2106 
    9709 3793 4464 2377 2421 404   
    3714 449 10224 4541 623 10679     
    10449 2106 1727 5587 888 339    
    4464 2537 7886 8622 1811 9403 
    7770 1885 1111 3748 2199 2377 
    5587 623 449 339 2106 9709       
    888 404 4464 10679 3714 10449    
    1727 10224 2199 1111 2377 7886 
    3793 3748 8622 1811 7770 4541 
    2537 2421 10449 9403 1885 9709 
    623 2199 404 339 1727 7886       
    10679 1111 2106 449 3793 8622   
    10224 9403 4541 3748 4464 3714 
    7770 2377 2537 888 1811 1885   
    2421 9709 1111 5587 1727 10679 
    404 9403 3748 2199 449 7886     
    3714 7770 623 1885 2106 2537   
    2421 8622 888 10449 4464 4541   
    2377 339 3793 10224 1811 5587
    """

    # Split the input data into lines
lines = input_data.strip().split('\n')

    # Process each line
for line in lines:
        # Split the line into individual numbers
  numbers = list(map(int, line.split()))
        
  # register red team participation
  for i in range(3):
    print(f"{numbers[i]} ", end='')
    red_teams[lines.index(line)][teams[numbers[i]]] = 1
        
  # register blue team participation
  for i in range(3, 6) :
    print(f"{numbers[i]} ", end='')
    blue_teams[lines.index(line)][teams[numbers[i]]] = 1

  print()



blue_teams = pd.DataFrame(np.array(blue_teams), index=range(1, 57), columns=teams)
red_teams = pd.DataFrame(np.array(red_teams), index=range(1, 57), columns=teams)

data = pd.Series([blue_teams, red_teams], index=["Red Alliance Teams", "Blue Alliance Teams"])

print(data)

data.to_json("newschedule.json", orient='index', index=True, indent=2)
exit()


for i in range(56) :
  blue_teams.append(0 * 29)
  red_teams.append(0 * 29)

  input_row = input()

  first = 0
  index = 0
  for j in range(3) :
    while not input_row[index] == ' ' :
      index += 1
    
    index += 1
    print(int(input_row[first:index]))
    # red_teams[teams[int(input_row[first:index])]] = 1
    first = index + 1
    index = first

  for j in range(3) :
    while not input_row[index] == ' ':
      index += 1

    index += 1
    # blue_teams[teams[int(input_row[first:index])]] = 1
    first = index + 1
    index = first
      
  

# print(scheduledata)
  