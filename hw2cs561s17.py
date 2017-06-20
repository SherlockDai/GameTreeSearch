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
    player1Scores = lines[3]
    player2Scores = lines[4]
    connections = {}
    for line in lines[5:]:
        # establish the connection between cities
        line = line.replace(" ", "")
        connectionInfo = line.split(":")
        city = connectionInfo[0]
        neighbors = connectionInfo[1].split(",")
        connections[city] = neighbors

    return {'colors': colors, 'playersAndFirstMove': playersAndFirstMove, 'maxDepthOfTree': maxDepthOfTree,
            'player1Scores': player1Scores, 'player2Scores': player2Scores, 'connections': connections}

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
    parent = None
    alpha = float("-inf")
    beta = float("inf")
    v = float("-inf")
    toBeExplored = []
    assignment = {}
    def __init__(self, connections):
        for city in connections:
            self.toBeExplored.append(city)
            self.assignment[city] = []
        self.toBeExplored = sortByAlphabet(self.toBeExplored)
# main()
input = readInput()
rootNode = state(input['connections'])
test = 0;