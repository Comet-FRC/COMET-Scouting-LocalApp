OpenCV
Matplotlib
NumPy
Pandas

Steps:
- Read a QR Code and decode the scouting information
- Sort the information into a CSV file (columns - types of data, rows - matches)
- Manipulate the data to form valuable metrics (e.g. average points / match)
- Compile metrics into readable reports and graphs

QR Code data format:

pregame info:

first 3 digits    - Scout initials, plaintext uppercase
next 1 digit      - Match number, base 91 number
next 3 digits     - Team number, base 91 number
next 1 digit      - Auton leave status, y = true; n = false
next 1 digit      - Team color, r = red; b = blue

game events:
next ? * 3 digits - events, stored in the following format : [1 digit letter / number event id][2 digit base 91 representation of timer value] 

endgame info: 

next 1 digit      - endgame position, x = none; d = deep hang; s = shallow hang; p = park

last ? digits     - tags, stored with their tag id base 91


example:
JRHKAU%nb4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2CadB&

[JRH]KAU%nb4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2CadB&
 ^
scout initials

JRH[K]AU%nb4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2CadB&
    ^
match number, base 91

JRHK[AU%]nb4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2CadB&
      ^
  team number, base 91

JRHKAU%[n]b4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2CadB&
        ^
  auton leave status (false in this case)

JRHKAU%n[b]4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2CadB&
         ^
     team color (blue in this case)

JRHKAU%nb [[4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2Ca]] dB&
              ^       ^       ^       ^       ^   
              all game events

JRHKAU%nb[4AZ]3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2CadB&
           ^
    single game event (l4 score at time [AZ] converted from base 91)


JRHKAU%nb4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2Ca[d]B&
                                              ^
                                     game end position (deep hang)
                                    
JRHKAU%nb4AZ3Ad2Ai1AmtB81B[1B_1B}2CC4CQ3CV2Cad[B&]
                                                ^
                                              tag ids (fast robot and bad auton)