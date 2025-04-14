import random

def main():

    holes = [4,5,4,3,4,3,4,5,4,4,4,3,5,4,5,3,4,4]
    numWins = {'Rory':0, 'Bryson':0, 'Conners':0, 'Reed':0, 'Aberg':0}
    numTrials = 1500

    for i in range(numTrials):
        leaderboard = {'Rory':-12, 'Bryson':-10, 'Conners':-2, 'Reed':-3, 'Aberg':-3}
        for hole in holes:
            for p in leaderboard:
                score = genScore(hole)
                leaderboard[p] += score
        print(leaderboard)
        winner = findWinner(leaderboard)
        numWins[winner] += 1

    for player in numWins:
        pct = round((numWins[player] / numTrials) * 100)
        print(f'{player} wins {pct}% of the time')

def findWinner(lb):
    best = 99
    for player in lb:
        if lb[player] < best:
            best = lb[player]
            winner = player
    return winner


def genScore(par):
    tap3 = 3.07
    tap4 = 4.04
    tap5 = 4.64

    n = random.random()
    if par == 3:
        if n < .93:
            return 0
        else:
            return 1
    elif par == 4:
        if n < .96:
            return 0
        else:
            return 1
    elif par == 5:
        if n < .36:
            return -1
        elif n < .64:
            return 0
        else:
            return 1

main()
