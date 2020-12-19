# Wumpus project by Walter Alcazar (original idea is from Rensselaer Polytechnic Institute)

This project involves creating an 8x8 board that contains one of five objects: 
1. nothing, 
2. a bottomless pit, " \__/ "
3. a mythical creature named a wumpus that will eat you if you land on his square " >=^( "
4. a pot of gold " $$$$ "
5. the robot that you control " =^^= "

The game places you in a limited number of random locations facing one of four directions: N, E, S, W.
The goal is to move the robot to the pot of gold and return to the starting square.
If you land on a bottomless pit or a square with the wumpus, you will die.
The wumpus creatures will wake up and get angry after you get the pot of gold. They will chase you.
There are four basic operations that you can do with the robot:
1. "f" = move forward
2. "b" = move backward
3. "l" = turn left
4. "r" = turn right

the game progresses one cycle after you enter an acceptable command from the list above.