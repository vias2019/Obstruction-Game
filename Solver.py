import math
from re import T
from random import randrange
import copy
from Board import Node, build_board


global file

# Print a winner to output
winner = ''

# Set up the size of the board
n = 6 # height
m = 6 # length

# Intermediate boards
gameGraph = []
gameBoard = []

# Check if game is over
is_game = True

# user input
turn = 0
algType = ''

# Assign unique ID to every node
id = 0

# List of Data - Data storage
record = []

# Mark boxes around selection 'o' or 'x'
def markAround (board,i, j): #x, y
    if (i - 1) >= 0: board[i - 1][j] = '/' #up
    if (j + 1) < len(board[0]): board[i][j + 1] = '/' #right
    if (i - 1) >= 0 and (j + 1) < len(board): board[i - 1][j + 1] = '/' #upper right
    if (j - 1) >= 0: board[i][j - 1] = '/' #left
    if ((j - 1) >= 0 and i - 1 >= 0 ): board[i - 1][j - 1] = '/' #upper left
    if (i + 1) < len(board): board[i + 1][j] = '/' #down
    if (i + 1) < len(board) and (j - 1) >= 0: board[i + 1][j - 1] = '/' #bottom left
    if (i + 1) < len(board) and (j + 1) < len(board): board[i + 1][j + 1] = '/' # bottom right
    
# Convert a graph to a string for printing    
def convertListToString (graph): # support for print_grid function
    res=  ''
    for i in range (0, len(graph)):
        for j in range (0, len(graph[i])):
           res = res + graph[i][j] 
    return res

# Print a board
def print_grid(board):
    list1=[' ']+[' '+item+' | ' for item in board]
    length=len(board)
    iter_=math.ceil(math.sqrt(length))

    temp = '  '
    for i in range (1, m + 1):
        temp = temp + '   ' + str(i) + ' '
    fallout=(iter_)**2-length
    if fallout:
        list1=list1+['   | ']*fallout
    t = 1
    print (temp)
    for i in range(0,length,iter_):
        print('  ' + '+----'*(iter_)+'+')
        pp=''.join(list1[i+1:i+iter_+1])
        print(str(t) + ' ' + '| '+ pp)
        t += 1
    print('  ' + '+----'*(iter_)+'+')
 

# Randomly select a child with the same utility value to make the game not repetative (Currently works only for MM algorithm)       
def randomPick(board):
    selection = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if (board[i][j] == '-'): selection.append([i,j])
    rand = randrange(0, len(selection) - 1)
    return selection[rand]

# Checks if board has empty boxes 
def check_is_game_over(board):
    for i in range (0, len(board)):
        for j in range (0, len(board[i])):
            if (board[i][j] == '-'): return False
    return True

# Create children for a parent board
def for_each_cell_create_board (board, parent):
    global id, next_level, record
    res = []
    for i in range (0, len(board)):
        for j in range (0, len(board[i])):
            if (board[i][j] == '-'):
                curr_board = copy.deepcopy(board)
                curr_board[i][j] = 'o'
                markAround(curr_board, i, j)
                new = Node(id, curr_board, parent, layer,[], [], [i+1,j+1])
                record.append(new)
                next_level.append(id)
                res.append(id)
                id += 1
        record[parent].children = res

# Calculates utility value for MIN
def pick_min(children):
    tempid = []
    tempUtility = []
    for i in range (0, len(children)):
        tempid.append(children[i])
        tempUtility.append(record[children[i]].utility[1])
    minValue = min(tempUtility)
    res = []
    for i in range (0, len(tempUtility)):
        if (tempUtility[i] == minValue): res.append(tempid[i])
    rand = randrange(0, len(res))
    return [res[rand], record[res[rand]].utility[1]]

# Calculates utility value for MAX
def pick_max(children):
    tempid = []
    tempUtility = []
    for i in range (0, len(children)):
        tempid.append(children[i])
        tempUtility.append(record[children[i]].utility[1])
    maxValue = max(tempUtility)
    res = []
    for i in range (0, len(tempUtility)):
        if (tempUtility[i] == maxValue): res.append(tempid[i])
    rand = randrange(0, len(res))
    return [res[rand], record[res[rand]].utility[1]]

# MM function
def mm(board):
    global record, gameBoard, id, layer
    build_graph(board)
    for i in reversed(record):
        if (i.children == -1): i.utility = -1 
        if (i.children == []): 
            if check_is_game_over(i.set):
                if(i.level % 2 == 0):
                    i.utility = [-1, -100]
                else: i.utility = [-1, 100]
            else: 
                i.utility = [-1, evaluation(i.set)] 
        else:
            if(i.level % 2 == 0):
                    i.utility = pick_max(i.children)
            else: i.utility = pick_min(i.children)        
    gameBoard = record[record[0].utility[0]].set

    print_graph()
    record = []
    id = 0
    layer = 0
       
curr_level = []
next_level = [] 
layer = 0
limit = 3

# Builds a graph
def build_graph(brd):
    global id, curr_level, next_level, layer
    board = copy.deepcopy(brd)
    newNode = Node(id, board, -1, layer)
    record.append(newNode)
    curr_level.append(id)
    id += 1
    layer += 1
    while (layer <= limit and curr_level):
        for i in range (0, len(curr_level)):
            for_each_cell_create_board(record[curr_level[i]].set, record[curr_level[i]].id)
        curr_level.pop(0)
        curr_level = next_level
        next_level = []
        layer += 1   
        
    else:
        curr_level = []
        return

# Evaluation function for non-terminate nodes
def evaluation(board):
    count = 0
    for i in range (0, len(board)):
            for j in range (0, len(board[i])):
                if(board[i][j] != '-'):
                    count += 1
    return count

# Check user input for a correct selection - to make sure that a user didn't select the blocked box    
def check_input():
    global userInput

    legit = False
    while legit == False:
        if(gameBoard[int(userInput[0])-1][int(userInput[2])-1] != '-'):
            print ("This r/c is blocked. Please try agian.")
            userInput = input('\nr/c: ')
        else: legit = True
    
# Record user input     
def record_user_input(string):
    global gameBoard, is_game, winner, userInput
        
    row = int(string[0]) - 1
    column = int(string[2]) - 1
   
    gameBoard[row][column] = 'x'
    markAround(gameBoard, row, column)

alpha = -1000
beta = 1000  
ab_limit = 4

# Support for AB function
def abSupport(parentBoard, parentId, level):
    global alpha, beta, id
    #cut off
    if level == ab_limit or evaluation(parentBoard) == (n*m):
    #assign utility value to the leaf node
        if check_is_game_over(parentBoard):
                if(level % 2 == 0):
                    record[parentId].utility = [-1, -100]
                else: record[parentId].utility = [-1, 100]
        else: 
                record[parentId].utility = [-1, evaluation(parentBoard)]
        return
    
    for i in range(0, len(parentBoard)):
        for j in range (0, len(parentBoard[i])):
            if (parentBoard[i][j] == '-'):
                
                curr_board = copy.deepcopy(parentBoard)
                curr_board[i][j] = 'o'
                markAround(curr_board, i, j)
                new = Node(id, curr_board, parentId, level + 1, [], [],[i+1,j+1])
                record[parentId].children.append(id)
                record.append(new)
                id += 1
            
                abSupport(new.set, new.id, level + 1)
                if(level % 2 == 0):
                    leaf_alpha = record[-1].utility
                    if(leaf_alpha == []):leaf_alpha = [-1, 0]
                    if alpha < leaf_alpha[1]: alpha = leaf_alpha[1]
                    if record[parentId].utility == [] or record[parentId].utility[1] < leaf_alpha[1]:
                        record[parentId].utility = [record[new.id].id, leaf_alpha[1]] 
                else:
                    leaf_beta = record[-1].utility
                    if(leaf_beta == []):leaf_beta = [-1, 0]
                    if beta > leaf_beta[1]: beta = leaf_beta[1]
                    if record[parentId].utility == [] or record[parentId].utility[1] > leaf_beta[1]:
                        record[parentId].utility = [record[new.id].id, leaf_beta[1]]
                if alpha >= beta: break 

# AB function                         
def ab(brd):
    global id, gameBoard, alpha, beta, record, level
    board = copy.deepcopy(brd)
    newNode = Node(id, board, -1, 0)
    record.append(newNode)
    curr_level.append(id)
    id += 1
    abSupport(newNode.set, newNode.id, 0)
    
    gameBoard = record[record[0].utility[0]].set
    print('AI move: ' + str(record[record[0].utility[0]].step[0]) + '/'+ str(record[record[0].utility[0]].step[1]))
    print_graph()
    record = []
    id = 0
    alpha = -1000
    beta = 1000  

# Print a graph/all nodes
def print_graph():
    global file
    file.write("\n\nNumber of nodes expanded in " + algType + ' algorithm: ' + str(len(record)))
    if (algType == 'MM'):
        file.write("\nDepth level for look-ahead for " + algType + ' algorithm: ' + str(limit))
    if (algType == 'AB'):
        file.write("\nDepth level for look-ahead for " + algType + ' algorithm: ' + str(ab_limit))
    file.write("\nGraph built with " + algType + ' algorithm: ')
    for i in range (0, len(record)):
        file.write(str(record[i].id) + '-->' + str(record[i].children))
    file.write('')
     
# Run a game function
def run_the_program (turn, alg):
    global is_game, userInput, algType
    algType = alg
    build_board(n, m, gameBoard)
    if (int(turn) == 1):
        print('Player 1: AI')
        print('Player 2: Human\n')
        # if AI is the first player
        while is_game:
            if algType == 'MM': mm(gameBoard) 
            if algType == 'AB': ab(gameBoard)
            print_grid(convertListToString(gameBoard))
            if (check_is_game_over(gameBoard) == True):
                is_game = False
                winner = 'AI'
                break
            userInput = input('\nr/c: ')
            check_input()
            record_user_input(userInput)  
            print_grid(convertListToString(gameBoard))
            if (check_is_game_over(gameBoard) == True):
                is_game = False
                winner = 'User'
                break
        print ("Game Over: " + winner + ' is a winner!')        
    else:
        # if user is the first player
        print('Player 1: Human')
        print('Player 2: AI\n')
        while is_game:
            print_grid(convertListToString(gameBoard))
            userInput = input('\nr/c: ')
            check_input()
            record_user_input(userInput)  
            if (check_is_game_over(gameBoard) == True):
                is_game = False
                winner = 'User'
                break
            if algType == 'MM': mm(gameBoard) 
            if algType == 'AB': ab(gameBoard)
            if (check_is_game_over(gameBoard) == True):
                is_game = False
                winner = 'AI'
                break
        print_grid(convertListToString(gameBoard))
        print ("Game Over: " + winner + ' is a winner!') 
        
        




