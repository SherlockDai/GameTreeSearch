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




# define minimax function here
def minimax(state, input):
    # OPEN OUTPUT FILE
    output = open("output.txt", "wb")
    rootState = maxValue(state, input, float('-inf'), float('inf'), output)
    line = "%s, %s, %s" % (rootState['nextMove']['1'][-1],
                           state['nextMove']['assignment'][state['nextMove']['1'][-1]],
                           state['nextMove']['v'])
    output.write(line)
# define the function to find all possible next moves and check depth
def terminalTest(state, input, player):
    # check the depth
    possibleMoves = []
    if state['depth'] == int(input['maxDepthOfTree']):
        return []
    else:
        toBeExplored = []
        # join all neighbors
        for city in state['explored']:
            neighbors = input['connections'][city]
            toBeExplored = list(set(toBeExplored + neighbors))
        # remove explored cities
        for city in state['explored']:
            toBeExplored.remove(city)
        # sort cities to be explored
        toBeExplored = sortByAlphabet(toBeExplored)
        for city in toBeExplored:
            for color in input['colors']:
                neighbors = input['connections'][city]
                for neighbor in neighbors:
                    if state['assignment'][neighbor] == color:
                        #skip this color and checck the next one
                        break
                if state['assignment'][neighbor] == color:
                    continue
                else:
                    newState = {}
                    # copy v
                    newState['v'] = state['v']
                    #copy nextMove
                    newState['nextMove'] = dict(state['nextMove'])
                    # update the depth of the next possible state
                    newState['depth'] = state['depth'] + 1
                    newState['explored'] = list(state['explored'])
                    newState['explored'].append(city)
                    newState['1'] = list(state['1'])
                    newState['2'] = list(state['2'])
                    newState[player].append(city)
                    # update the color assignment
                    newState['assignment'] = dict(state['assignment'])
                    newState['assignment'][city] = color
                    # update the score of the player
                    newState['playersScore'] = dict(state['playersScore'])
                    newState['playersScore'][player] = \
                        newState['playersScore'][player] + \
                        int(input['scores'][player][color])
                    possibleMoves.append(newState)
        return possibleMoves

# define maxValue fuction here for player1
def maxValue(state, input, alpha, beta, output):
    moves = terminalTest(state, input, "1")
    if len(moves) == 0:
        #evaluate the state
        state['v'] = state['playersScore']['1'] - state['playersScore']['2']
        line = "%s, %s, %s, %s, %s, %s\n" % (state['2'][-1], state['assignment'][state['2'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
        output.write(line)
        return state
    else:
        state['v'] = float('-inf')
        line = "%s, %s, %s, %s, %s, %s\n" % (state['2'][-1], state['assignment'][state['2'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
        output.write(line)
        for move in moves:
            nextMove = minValue(move, input, alpha, beta, output)
            if state['v'] < nextMove['v']:
                state['nextMove'] = nextMove
            state['v'] = max(state['v'], nextMove['v'])
            if state['v'] >= beta:
                line = "%s, %s, %s, %s, %s, %s\n" % (state['2'][-1], state['assignment'][state['2'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
                output.write(line)
                return state
            else:
                alpha = max(alpha, state['v'])
                line = "%s, %s, %s, %s, %s, %s\n" % (state['2'][-1], state['assignment'][state['2'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
                output.write(line)
        return state

# define minValue function here for player2
def minValue(state, input, alpha, beta, output):
    moves = terminalTest(state, input, "2")
    if len(moves) == 0:
        #evaluate the state
        state['v'] = state['playersScore']['1'] - state['playersScore']['2']
        line = "%s, %s, %s, %s, %s, %s\n" % (state['1'][-1], state['assignment'][state['1'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
        output.write(line)
        return state
    else:
        state['v'] = float('inf')
        line = "%s, %s, %s, %s, %s, %s\n" % (state['1'][-1], state['assignment'][state['1'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
        output.write(line)
        for move in moves:
            nextMove = maxValue(move, input, alpha, beta, output)
            if state['v'] > nextMove['v']:
                state['nextMove'] = nextMove
            state['v'] = min(state['v'], nextMove['v'])
            if state['v'] <= alpha:
                line = "%s, %s, %s, %s, %s, %s\n" % (state['1'][-1], state['assignment'][state['1'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
                output.write(line)
                return state
            else:
                beta = min(beta, state['v'])
                line = "%s, %s, %s, %s, %s, %s\n" % (state['1'][-1], state['assignment'][state['1'][-1]],
                                            state['depth'], state['v'], str(alpha), str(beta))
                output.write(line)
        return state

# main()

input = readInput()
#define the state
rootNode = {'depth': 0, 'v': 0, 'nextMove': [], 'explored': [], 'assignment': {}, 'playersScore': {'1': 0, '2': 0},
            '1': [], '2':[]}
for city in input['connections']:
    rootNode['assignment'][city] = ""
#initiate the information of the rootNode
for firstMove in input["playersAndFirstMove"]:
    firstMoveInfo = firstMove.split("-")
    #store the player number
    player = firstMoveInfo[1]
    #extract city name and color assigned
    firstMoveInfo = firstMoveInfo[0].split(":")
    city = firstMoveInfo[0]
    color = firstMoveInfo[1]
    rootNode['explored'].append(city)
    #extract the score of the color based on the current player
    score = input['scores'][player][color]
    #update assignment in rootNode state
    rootNode['assignment'][city] = color
    rootNode[player].append(city)
    rootNode['playersScore'][player] = rootNode['playersScore'][player] + int(score)
minimax(rootNode, input)

