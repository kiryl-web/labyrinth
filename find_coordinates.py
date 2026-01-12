import random

def findStartCoordinates(normalizedMap: list[list[str]]) -> (int,int):
    #Geht durch die Matrix, bis es ein Feld mit "S" fand.
    for row in range(len(normalizedMap)):
        for column in range(len(normalizedMap[row])):
            if normalizedMap[row][column] == "S":
                return column,row


def findEndCoordinates(normalizedMap: list[list[str]]) -> (int,int):
    #Geht durch die Matrix, bis es ein Feld mit "G" (Goal) fand.
    #Wenn der Spieler auf dem Goal-Feld ist, gibt es (-1,-1) zurück.
    for row in range(len(normalizedMap)): #Zeile
        for column in range(len(normalizedMap[row])): #Spalte
            if normalizedMap[row][column] == "G":
                return column,row
    return -1,-1

def giveClosestUsedSpot(normalizedMap: list[list[str]]) -> (int, int):
    #Relevant für Zusatz
    height = len(normalizedMap)
    width = len(normalizedMap[0])

    goal = findEndCoordinates(normalizedMap)
    if goal == (-1, -1):
        for row in range(1, height - 1):
            for column in range(1, width - 1):
                if normalizedMap[row][column] == "B":
                    return column, row
        return 1, 1

    gx = goal[0]
    gy = goal[1]

    nearest = None
    bestDist2 = None

    for row in range(1, height - 1):
        for column in range(1, width - 1):
            if normalizedMap[row][column] == "B":
                dx = column - gx
                dy = row - gy
                dist2 = dx * dx + dy * dy

                if bestDist2 is None or dist2 < bestDist2:
                    bestDist2 = dist2
                    nearest = (column, row)

    if nearest is None:
        return 1, 1

    return nearest

def findPlayerCoordinates(normalizedMap: list[list[str]]) -> (int,int):
    #Geht durch die Matrix, bis es ein Feld mit "P", "n", "s", ... fand.
    #Wenn es nichts findet, gibt es die Position des Startfeldes.
    for row in range(len(normalizedMap)): #Zeile
        for column in range(len(normalizedMap[row])): #Spalte
            if normalizedMap[row][column] == "P" or normalizedMap[row][column] == "n" or normalizedMap[row][column] == "s" or normalizedMap[row][column] == "e" or normalizedMap[row][column] == "w":
                print("Player at", column, " ", row)
                return column,row

    return findStartCoordinates(normalizedMap)

def getSurroundings(normalizedMap: list[list[str]], x: int, y: int) -> list[str]:
    #Gibt eine Liste aus oben, links, unten und rechts.
    #Wenn eines der Richtungen nicht existiert, wird es als "#" (Wand) verkauft.

    height = len(normalizedMap)
    width = len(normalizedMap[0])

    up, left, down, right = "#", "#", "#", "#"

    if y - 1 >= 0: up = normalizedMap[y - 1][x]
    if x - 1 >= 0: left = normalizedMap[y][x - 1]
    if y + 1 < height: down = normalizedMap[y + 1][x]
    if x + 1 < width: right = normalizedMap[y][x + 1]

    return [up, left, down, right]
