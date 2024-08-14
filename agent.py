  #!/usr/bin/python3
  #  agent_smart.py
  #  Nine-Board Tic-Tac-Toe Agent starter code
  #  COMP3411/9814 Artificial Intelligence
  #  CSE, UNSW
  # Code Brief Answer:
  # Briefly describe how your program works, including any algorithms and data structures employed,
  # and explain any design decisions you made along the way.
  # Our program works by looking at the current state of the boarding and performing a minimax alpha beta pruning search
      # on future states of the game to a specific depth defined by a depth interval step function, in order to calculate
      # the best move to make at a given state
      # The main datastrucutre employed is the use of a StateNode to store specific possible moves in the Minimax search
      # this StateNode function also has a Transposition table class which is used to Cachce different results of the Alpha
      # beta pruning search. This helps avoid needing to recaculate different future states for a potential serach that have already been
      # Calculated
      # One of the main design decisions was to use an extra state to keep track of the search in a transposition table
      # Additionaly using a step function to define the depth that would be searched to was another essential design decision.
      # as it allowed us to manually finetune the search to use a low depth at the begining and a higher depth at the end of the                                                
      # search.
import socket
import math
import sys
import cProfile
import concurrent.futures
import time
# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here
# the boards are of size 10 because index 0 isn't used
boardArray = [[0] * 10 for i in range(10)]
s = [".", "X", "O"]
moveCount = 1
playerIndex = 1
prevMove = 0
# Current choice of board / board to play on
currChoice = 0
winConditions = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7],
]
# Debug print statement,
DEBUG = False
def debug_print(inputStr):
    if DEBUG:
        print(inputStr)
def minimax(currStateNode, is_maximizing_player, alpha, beta, depth):
    minimax.counter += 1
    current_state = currStateNode.currentState()
    # Check transposition table
    key = currStateNode.getHash()
    tt_entry = transposition_table.lookup(key)
    if tt_entry is not None and tt_entry[1] >= depth:
        return tt_entry[0]
    if current_state > 0 or depth == 0:
        score = currStateNode.evaluateCurrBoard()
        transposition_table.store(key, score, depth)
        return score
    value = float("-inf") if is_maximizing_player else float("inf")
    update = max if is_maximizing_player else min
    # Move ordering
    moves = []
    for move in range(1, 10):
        new_node = currStateNode.createNode(move)
        if new_node is None:
            continue
        moves.append((move, new_node))
    moves.sort(key=lambda x: x[1].evaluateCurrBoard(), reverse=is_maximizing_player)
    for _, new_node in moves:
        curr = minimax(new_node, not is_maximizing_player, alpha, beta, depth - 1)
        value = update(value, curr)
        if is_maximizing_player:
            alpha = update(alpha, value)
        else:
            beta = update(beta, value)
        if alpha >= beta:
            break
    transposition_table.store(key, value, depth)
    return value
def findMove():
    start_time = time.time()
    MOVE_DEPTH_PAIRS = [
        # Move num | DEPTH
        (5, 4),
        (10, 6),
        (12, 6),
        (20, 7),
        # (20, 9),
        (26, 8),
        (28, 11),
        (34, 25),
        (40, 30),
        (45, 40),
        (50, 50)
    ]
    # Calculate the depth based on the number of moves
    depth = 24
    for moves, depth_level in MOVE_DEPTH_PAIRS:
        if moveCount <= moves:
            depth = depth_level
            break
    debug_print(f"\nMoves: {moveCount} depth: {depth}")
    def evaluate_move(index):
        start_time = time.time()
        if boardArray[currChoice][index] == 0:

            tempBoard = [[0] * 10]
            for num in range(1, 10):
                tempBoard.append(boardArray[num][:])

            tempBoard[currChoice][index] = 1
            currStateNode = StateNode(tempBoard, currChoice, index, 1)
            minimax.counter = 0
            value = minimax(currStateNode, False, -math.inf, math.inf, depth - 1)
            end_time = time.time()
            return index, value, end_time - start_time
        return None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(evaluate_move, index) for index in range(1, 10)]
        concurrent.futures.wait(futures)
        moves = []
        thread_times = {}
        for future in futures:
            result = future.result()
            if result is not None:
                index, value, thread_time = result
                thread_times[index] = thread_time
                moves.append((index, value))
    debug_print(moves)
    bestMove = max(moves, key=lambda x: x[1])[1]
    best_choices = [index for index, value in moves if value == bestMove]
    end_time = time.time()
    total_time = end_time - start_time
    debug_print(f"\nThread execution times:")
    for index, thread_time in thread_times.items():
        debug_print(f"Thread {index}: Time taken = {thread_time:.5f} seconds")
    debug_print(f"\nTotal move time: {total_time:.5f} seconds")
    debug_print(f"Longest thread time: {max(thread_times.values()):.5f} seconds")
    debug_print(f"Number of threads used: {len(futures)}")
    findMove.prev_move_time = total_time
    findMove.prev_depth = depth
    return best_choices[0]
def printBoardRow(bd, a, b, c, i, j, k):
    print(
        " "
        + s[bd[a][i]]
        + " "
        + s[bd[a][j]]
        + " "
        + s[bd[a][k]]
        + " | "
        + s[bd[b][i]]
        + " "
        + s[bd[b][j]]
        + " "
        + s[bd[b][k]]
        + " | "
        + s[bd[c][i]]
        + " "
        + s[bd[c][j]]
        + " "
        + s[bd[c][k]]
    )
# Print the entire board
def printBoard(board):
    printBoardRow(board, 1, 2, 3, 1, 2, 3)
    printBoardRow(board, 1, 2, 3, 4, 5, 6)
    printBoardRow(board, 1, 2, 3, 7, 8, 9)
    print(" ------+-------+------")
    printBoardRow(board, 4, 5, 6, 1, 2, 3)
    printBoardRow(board, 4, 5, 6, 4, 5, 6)
    printBoardRow(board, 4, 5, 6, 7, 8, 9)
    print(" ------+-------+------")
    printBoardRow(board, 7, 8, 9, 1, 2, 3)
    printBoardRow(board, 7, 8, 9, 4, 5, 6)
    printBoardRow(board, 7, 8, 9, 7, 8, 9)
    print()
# choose a move to play
def play():
    n = findMove()
    debug_print(f"playing move: {n}, board {currChoice}")
    place(currChoice, n, 1)
    return n
# place a move in the global boards
def place(currBoard, move, playerIndex):
    global currChoice, moveCount, prevMove
    currChoice = move
    prevMove = currBoard
    boardArray[currBoard][move] = playerIndex
    moveCount += 1
    if DEBUG:
        printBoard(boardArray)
# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    # init tells us that a new game is about to begin.
    # start(x) or start(o) tell us whether we will be playing first (x)
    # or second (o); we might be able to ignore start if we internally
    # use 'X' for *our* moves and 'O' for *opponent* moves.
    global playerIndex

    # second_move(K,L) means that the (randomly generated)
    # first move was into square L of sub-board K,
    # and we are expected to return the second move.
    if command == "second_move":
        playerIndex = 2
        place(int(args[0]), int(args[1]), 2)
        return play()


    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        playerIndex = 1
        place(int(args[0]), int(args[1]), 1)
        place(currChoice, int(args[2]), 2)
        return play()


    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        place(currChoice, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0
# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2])
    s.connect(("localhost", port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())
class TranspositionTable:
    def __init__(self):
        self.table = {}
    def store(self, key, value, depth):
        self.table[key] = (value, depth)
    def lookup(self, key):
        if key in self.table:
            return self.table[key]
        return None
transposition_table = TranspositionTable()
# Our state node class
# which is used for keeping track of a current possible option that can be moved to by the board.
# State node keeps trac
class StateNode:
    def __init__(self, game, currentBoard, currMove, playerIndex):
        self.game = game
        self.board = currentBoard
        self.currMove = currMove
        self.playerIndex = playerIndex
    def copy(self, game):
        return list(map(lambda board: board.copy(), game))
    def getHash(self):
        return tuple(tuple(board) for board in self.game)
    def currentState(self):
        win = 0
        gameCur = self.game[self.board]
        for line in winConditions:
            if gameCur[line[0]] > 0:
                match_count = 0
                for pos in line:
                    if gameCur[pos] == gameCur[line[0]]:
                        match_count += 1
                if match_count == len(line):
                    return gameCur[line[0]]
        return win
    def evaluateCurrBoard(self):
        score = 0
        weights = [0, 1, 10, 100]  # Adjusted weights for faster evaluation
        for currBoard in self.game[1:]:
            possibleMoves = sum(1 for pos in range(1, 10) if currBoard[pos] == 0)
            for possibleWin in winConditions:
                currPlayers = [currBoard[pos] for pos in possibleWin]
                playerCount = currPlayers.count(1)
                opponentCount = currPlayers.count(2)
                score += (
                    weights[playerCount]
                    if playerCount > 0 and opponentCount == 0
                    else 0
                )
                score -= (
                    weights[opponentCount]
                    if opponentCount > 0 and playerCount == 0
                    else 0
                )
            score += possibleMoves
        return score
    def createNode(self, choice):
        if (self.game[self.currMove][choice] > 0):
            return None
        newPlayerNum = 2 if self.playerIndex == 1 else 1
        copynew = self.copy(self.game)
        copynew[self.currMove][choice] = newPlayerNum
        return StateNode(copynew, self.currMove, choice, newPlayerNum)
if __name__ == "__main__":
    main()