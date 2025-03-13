import numpy as np

teams = {
  141: 0,
  401: 1,
  449: 2,
  977: 3,
  1086: 4,
  1262: 5,
  1629: 6,
  1793: 7,
  1885: 8,
  3361: 9,
  3939: 10,
  4456: 11,
  4575: 12,
  4967: 13,
  5724: 14,
  5804: 15,
  5830: 16,
  6189: 17,
  6194: 18,
  6802: 19,
  8230: 20,
  9003: 21,
  9033: 22,
  9403: 23,
  9496: 24
}

matches = []
scores = []

for i in range(67) :
    matches.append([0] * 25)
    input()
    match_teams = input()

    temp = 0
    last = 0
    for j in range(len(match_teams)) :
        if (temp >= 3) :
            temp = 0
            break
        if (match_teams[j] == '\t') :
            matches[i][teams[int(match_teams[last:j])]] = 1
            temp += 1
            last = j + 1
    for j in range(last + 1, len(match_teams)) :
        if (temp >= 3) :
            temp = 0
            break
        if (match_teams[j] == '\t') :
            matches[i][teams[int(match_teams[last:j])]] = 1
            temp += 1
            last = j + 1

    for j in range(last + 1, len(match_teams)) :
        if (match_teams[j] == '\t') :
            scores.append(int(match_teams[last:j]))
            break
    

        

print(np.array(matches))
print(np.array(scores))

