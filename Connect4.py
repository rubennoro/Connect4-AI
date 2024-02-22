import copy
import random

#Variables used to simplify functions
AI = 1
player = -1
empty = 0
ROW_NUM = 6
COL_NUM = 7

#Function prints board to user in 2D

def printboard(s):
    for nested_list in s:  # this will print the board
        print(' '.join(map(str, nested_list)))

#Function determining whose turn it is

def turn(s):
    x_times = 0
    #let X represent 1(AI)
    o_times = 0
    #let O represent -1(player)
    for row in range(len(s)):
        for val in range(len(s[row])):
            #for loops iterate through each row to check for filled in spaces
            if s[row][val] == AI:
                x_times +=1
            elif s[row][val] == player:
                o_times +=1
    if x_times > o_times:
        return player
    elif o_times > x_times:
        return AI
    elif x_times + o_times == 9:
        return None

#Array tranposed from [rows][cols] to [cols][rows] for more logical valid_moves searching
def transpose(s):
    return [[s[j][i] for j in range(len(s))] for i in range(len(s[0]))]

#Function checks each columns for the lowest empty space
def valid_moves(s):
        new_s = transpose(s)
        possible_moves = []
        for col in range(len(new_s)):
            for row in range(len(new_s[0])-1, -1, -1):
                if new_s[col][row] == 0:
                    possible_moves.append([col, row])
                    break
                # Once we find an empty space in this row, move to the next row
        switch_nested_values(possible_moves)
        print(possible_moves)
        return possible_moves
        #returns a list of nested lists with coordinates

#Function switches the values back from [col][row] to [row][col]
def switch_nested_values(nested_lists):
    for nested_list in nested_lists:
        nested_list[0], nested_list[1] = nested_list[1], nested_list[0]

#Function efficiently checks each column, row, and diagonal once to see if there is four consecutive pieces
def win_check(s):
        #Horizontal Checks
        for row in range(len(s)):
            for col in range(len(s[0]) - 3):
                if s[row][col] == s[row][col + 1] == s[row][col + 2] == s[row][col + 3] and s[row][col] != 0:
                    return s[row][col]
        #Vertical Checks
        for y in range(len(s) - 3):
            for z in range(len(s[0])):
                if s[y][z] == s[y + 1][z] == s[y + 2][z] == s[y + 3][z] and s[y][z] != 0:
                    return s[y][z]
        #Two sets of diagonal checks
        for a in range(len(s) - 3):
            for b in range(len(s[0]) - 3):
                if s[a][b] == s[a + 1][b + 1] == s[a + 2][b + 2] == s[a + 3][b + 3] and s[a][b] != 0:
                    return s[a][b]
                elif s[a][6 - b] == s[a + 1][5 - b] == s[a + 2][4 - b] == s[a + 3][3 - b] and s[a][b] != 0:
                    return s[a][b]
        return False
        #if there is no winner, function returns false

#Heuristic Evaluation function uses by Minimax Algorithm to give priority to certain moves
def count_score(s):
        player1Score = 0
        player2Score = 0
        # Check horizontally
        for row in range(len(s)):
            for col in range(len(s[0]) - 3):
                if s[row][col:col + 4].count([AI]) == 4:
                    player1Score += 100
                elif s[row][col:col + 4].count([AI]) == 3:
                    player1Score += 5
                elif s[row][col:col + 4].count([AI]) == 2:
                    player1Score += 2
                if s[row][col:col + 4].count([player]) == 4:
                    player2Score += 100
                elif s[row][col:col + 4].count([player]) == 3:
                    player2Score += 5
                elif s[row][col:col + 4].count([player]) == 2:
                    player2Score += 2
        # Check vertically
        for col in range(len(s[0])):
            for row in range(len(s) - 3):
                if [s[row + i][col] for i in range(4)].count([AI]) == 4:
                    player1Score += 100
                elif [s[row + i][col] for i in range(4)].count([AI]) == 3:
                    player1Score += 5
                elif [s[row + i][col] for i in range(4)].count([AI]) == 2:
                    player1Score += 2
                if [s[row + i][col] for i in range(4)].count([player]) == 4:
                    player2Score += 100
                elif [s[row + i][col] for i in range(4)].count([player]) == 3:
                    player2Score += 5
                elif [s[row + i][col] for i in range(4)].count([player]) == 2:
                    player2Score += 2

        # Check diagonally
        for row in range(len(s) - 3):
            for col in range(len(s[0]) - 3):
                if [s[row + i][col + i] for i in range(4)].count([AI]) == 4:
                    player1Score += 100
                elif [s[row + i][col + i] for i in range(4)].count([AI]) == 3:
                    player1Score += 5
                elif [s[row + i][col + i] for i in range(4)].count([AI]) == 2:
                    player1Score += 2
                if [s[row + i][col + i] for i in range(4)].count([player]) == 4:
                    player2Score += 100
                elif [s[row + i][col + i] for i in range(4)].count([player]) == 3:
                    player2Score += 5
                elif [s[row + i][col + i] for i in range(4)].count([player]) == 2:
                    player2Score += 2
                if [s[row + i][col + 3 - i] for i in range(4)].count([AI]) == 4:
                    player1Score += 100
                elif [s[row + i][col + 3 - i] for i in range(4)].count([AI]) == 3:
                    player1Score += 5
                elif [s[row + i][col + 3 - i] for i in range(4)].count([AI]) == 2:
                    player1Score += 2
                if [s[row + i][col + 3 - i] for i in range(4)].count([player]) == 4:
                    player2Score += 100
                elif [s[row + i][col + 3 - i] for i in range(4)].count([player]) == 3:
                    player2Score += 5
                elif [s[row + i][col + 3 - i] for i in range(4)].count([player]) == 2:
                    player2Score += 2

        for rows in range(3, 6):
            for cols in range(2, 5):
                if s[rows][cols]==player:
                    player2Score +=2
                elif s[rows][cols]==AI:
                    player1Score += 2

        return player1Score - player2Score

#Minimax Algorithm with Alpha Beta Pruning
#Sets player to true or false value
def minimax(board, depth, alpha, beta, player_bool):
    '''

    :param board: takes in the desired board for the first call and recursion
    :param depth: can be changed by user depending on priority of accuracy vs time efficiency
    :param alpha: set as very low value, incorporated to improve algorithm efficiency
    :param beta: set as very high value, incorporated to improve algorithm efficiency
    :param player_bool: takes in a true or false depending on whose turn the program is simulating
    :return: returns the game score based on the heuristic evaluation, and the optimal coordinates corresponding to it
    '''
    possibles = valid_moves(board)
    #Base Case
    if depth == 0 or win_check(board):
        if win_check(board):
            if win_check(board) == AI:
                return (None, 99999)
            elif win_check(board) == player:
                return (None, -99999)
            else:
                return (None, count_score(board))
        else:
            #This is the situation where depth is reached before possible game ending
            print("Score:", count_score(board))
            return (None, count_score(board))

    if player_bool:
        #Let the AI be the true
        value = -99999
        best_position = random.choice(possibles)
        for possible in possibles:
            board_copy = copy.deepcopy(board)
            board_copy[possible[0]][possible[1]] = AI
            value = max(value, minimax(board_copy, depth - 1, alpha, beta,False)[1])
            alpha = max(alpha, value)
            if alpha >= beta:
                break
            print("AI Move:", possible, "Value:", value)
        return best_position, value
    else:
        #This is the player situation
        value = 99999
        best_position = random.choice(possibles)
        for possible in possibles:
            board_copy = copy.deepcopy(board)
            board_copy[possible[0]][possible[1]] = player
            value = min(value, minimax(board_copy, depth - 1, alpha, beta, True)[1])
            print("Player Move:", possible, "Value:", value)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_position, value

#Function that checks if the player's move is possible
def proper_player_moves(board, position):
    moves = valid_moves(board)
    for move in moves:
        if move == position:
            return True
    return False

if __name__ == '__main__':
    AI = 1
    player = -1
    boardmain = [[0 for number in range(7)] for num in range(6)]
    printboard(boardmain)

    order = int(input("Please type 1 if you would like to go first, and 2 if you would like to go second."))

    if order == 1:
        while valid_moves(boardmain):
            # player goes first
            player_row = int(input("Please provide the row you would like to put your piece: "))
            player_col = int(input("Please provide the col you would like to put your piece: "))
            player_puts = [player_row - 1, player_col - 1]

            while proper_player_moves(boardmain, player_puts) is False:
                # This loop asks user to re-input coordinates if they original choice is taken
                print("You must re-input valid row and column choices.")
                player_row = int(input("Please provide the row you would like to put your piece: "))
                player_col = int(input("Please provide the col you would like to put your piece: "))
                player_puts = [player_row - 1, player_col - 1]

            boardmain[player_row - 1][player_col - 1] = player
            # this sets the position on the board equal to the player's value
            printboard(boardmain)
            if win_check(boardmain) == player:
                print("Player Wins")
                break

            best_spot = minimax(boardmain, 5, -99999, 99999, False)[0]
            boardmain[best_spot[0]][best_spot[1]] = AI

            print('''
Next Turn:
                    ''')
            printboard(boardmain)

            if win_check(boardmain) == AI:
                print("AI Wins")
                break

    elif order == 2:
        while valid_moves(boardmain):
            # player goes second

            best_spot = minimax(boardmain, 5, -99999, 99999, True)[0]
            boardmain[best_spot[0]][best_spot[1]] = AI

            if win_check(boardmain) == AI:
                print("AI Wins")
                break

            print('''
Next Turn:
                                ''')
            printboard(boardmain)

            player_row = int(input("Please provide the row you would like to put your piece: "))
            player_col = int(input("Please provide the col you would like to put your piece: "))
            player_puts = [player_row - 1, player_col - 1]

            while proper_player_moves(boardmain, player_puts) is False:
                # This loop asks user to re-input coordinates if they original choice is taken
                print("You must re-input valid row and column choices.")
                player_row = int(input("Please provide the row you would like to put your piece: "))
                player_col = int(input("Please provide the col you would like to put your piece: "))
                player_puts = [player_row - 1, player_col - 1]

            boardmain[player_row - 1][player_col - 1] = player
            # this sets the position on the board equal to the player's value
            printboard(boardmain)
            if win_check(boardmain) == player:
                print("Player Wins")
                break


    if not valid_moves(boardmain):
        print("Draw")

















