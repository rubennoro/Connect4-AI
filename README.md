Connect4 Game AI 
---------------------------------------------
Introduction
---------------------------------------------
This program uses python to implement a Minimax algorithm with alpha beta pruning for Connect4. MiniMax uses a customizable heuristic evaluation function that provides the logic behind the quality of different moves within the game.  

The game allows the user to go first or second and changes whether the AI is to minimize or maximize its score accordingly.  

MiniMax
---------------------------------------------
The MiniMax function operates by recursively searching through all possible moves following each move up to a certain depth. The goal of the "True" player is to maximize the score, and the "False" player is looking to minimize the score. Alpha Beta pruning is implemented, where alpha serves as the lowest possible score, set as -99999, and beta is set as the highest, 99999. This improves the efficiency of the program as it no longer has to search through certain parts of the possible game tree. The heuristic evaluation is important for MiniMax to quantify the score of a certain set of moves that does not result in either a win, loss, or draw, as the algorithm is depth limited. I have set depth to 5 in this function. 

Heuristic Evlaluation
---------------------------------------------
The heuristic evaluation function, titled count_score, is used in the MiniMax since the MiniMax is depth-limited due to longer run times. 

For scenarios where there are 4 consecutive player or AI pieces, the score will increase by the greatest amount, followed by 3 or 2 consecutive pieces at decreasing values. There is also score priority given to placing pieces in the bottom middle of the board. This function takes these scenarios for both the AI and the player, and returns the difference of both, which is used in the MiniMax.  

Test Function
---------------------------------------------
I also used a test function to check the validity of the heuristic function. This was done by comparing the AI against itself at different depths, and calculating the number of wins for each depth, and the number of draws. This data can be saved into an excel file. 
