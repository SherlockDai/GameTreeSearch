'''
Author Yue Dai
Email: daiyue@usc.edu
'''

import sys

# function reads content from input file
def readInput():
    # initiate lines list to store the content of input file
    lines = []
    with open(sys.argv[2]) as f:
        lines.extend(f.read().splitlines())
    # extract color info from the first line
    for idx, line in enumerate(lines[:5]):
        lines[idx] = line.replace(" ", "")
    colors = lines[0].split(',')
    colors = sortByAlphabet(colors)
    playersAndFirstMove = lines[1].split(',')
    maxDepthOfTree = lines[2]
    player1ScoresList = lines[3]
    player1ScoresList = player1ScoresList.split(",")
    player1Scores = {}
    for score in player1ScoresList:
        player1ScoreInfo = score.split(":")
        player1Scores[player1ScoreInfo[0]] = player1ScoreInfo[1]
    player2ScoresList = lines[4]
    player2ScoresList = player2ScoresList.split(",")
    player2Scores = {}
    for score in player2ScoresList:
        player2ScoreInfo = score.split(":")
        player2Scores[player2ScoreInfo[0]] = player2ScoreInfo[1]
    scores = {}
    scores['1'] = player1Scores
    scores['2'] = player2Scores
    connections = {}
    for line in lines[5:]:
        # establish the connection between cities
        line = line.replace(" ", "")
        connectionInfo = line.split(":")
        city = connectionInfo[0]
        neighbors = connectionInfo[1].split(",")
        connections[city] = neighbors

    return {'colors': colors, 'playersAndFirstMove': playersAndFirstMove, 'maxDepthOfTree': maxDepthOfTree,
            'scores': scores, 'connections': connections}

# define the function to sort list based on alphabet
def sortByAlphabet(list):
    less = []
    greater = []
    # euqal is not useful in this case but we still implement it for future use
    equal = []
    if len(list) > 1:
        pivot = list[0]
        for value in list:
            if value < pivot:
                less.append(value)
            if value == pivot:
                equal.append(value)
            if value > pivot:
                greater.append(value)
        return sortByAlphabet(less) + equal + sortByAlphabet(greater)
    else:
        return list


# define class state which store the state of game
class state:
    depth = 0
    parent = None
    alpha = float("-inf")
    beta = float("inf")
    nextMove = []
    toBeExplored = []
    assignment = {}
    playersScore = {'1': 0, '2': 0}
    playersCities = {'1': [], '2': []}
    def __init__(self, connections):
        for city in connections:
            self.toBeExplored.append(city)
            self.assignment[city] = ""
        self.toBeExplored = sortByAlphabet(self.toBeExplored)

# define minimax function here
def minimax(state, input):
    return maxValue(state, input)
# define the function to find all possible next moves and check depth
def terminalTest(state, input):
    # check the depth
    if state.depth == input['maxDepthOfTree']:
        return []
    else:
        for city in state.toBeExplored:
            for color in input['colors']:
                neighbors = input['connecitons'][city]
                for neighbor in neighbors:
                    if state.assignment[neighbor] == color:
                        #skip this color and checck the next one
                        break
                if state.assignment[neighbor] == color:
                    continue
                else:
                    

# define maxValue fuction here for player1
def maxValue(state, input):
    moves = terminalTest(state, input)
    if moves.length == 0:
        return state
    else:
        v = float('-inf')
        for move in moves:
            v = max(v, minValue(move))
            if v >= state.beta:
                return state
            else:
                state.alpha = max(state.alpha, v)
        return state

# define minValue function here for player2
def minValue(state, input):
    moves = terminalTest(state, input)
    if moves.length == 0:
        return state
    else:
        v = float('inf')
        for move in moves:
            state.v = min(v, maxValue(move))
            if v <= state.alpha:
                return state
            else:
                state.beta = min(state.beta, v)
        return state

# main()
input = readInput()
rootNode = state(input['connections'])
#initiate the information of the rootNode
for firstMove in input["playersAndFirstMove"]:
    firstMoveInfo = firstMove.split("-")
    #store the player number
    player = firstMoveInfo[1]
    #extract city name and color assigned
    firstMoveInfo = firstMoveInfo[0].split(":")
    city = firstMoveInfo[0]
    color = firstMoveInfo[1]
    if city in rootNode.toBeExplored:
        rootNode.toBeExplored.remove(city)
    #extract the score of the color based on the current player
    score = input['scores'][player][color]
    #update assignment in rootNode state
    rootNode.assignment[city] = color
    rootNode.playersCities[player].append(city)
    rootNode.playersScore[player] = rootNode.playersScore[player] + int(score)

    test = 0;