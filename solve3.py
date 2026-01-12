import argparse
from time import sleep

from find_coordinates import getSurroundings, findEndCoordinates, findPlayerCoordinates, findStartCoordinates
from read import getNormalizedCharMap
from original import gfx_stack as gfx

def drawLabyrinth(normalizedMap: list[list[str]]):
    try:
        start = findStartCoordinates(normalizedMap)
        normalizedMap[start[1]][start[0]] = "B"
    except:
        pass

    b = []

    width = len(normalizedMap[0])
    height = len(normalizedMap)

    for row in range(len(normalizedMap)):
        for column in range(len(normalizedMap[row])):
            gfx.set_pixel((column, row), getColor(normalizedMap[row][column]))
            if normalizedMap[row][column] == "B":
                b.append([column,row])

    for i in range(len(b)):
        x = b[i][0]
        y = b[i][1]

        if normalizedMap[y][x] == "B":
            surroundings = getSurroundings(normalizedMap, x, y)

            if surroundings[0] != "#" and (y - 1) > 0:
                normalizedMap[y-1][x] = "B"
            if surroundings[1] != "#" and (x - 1) > 0:
                normalizedMap[y][x-1] = "B"
            if surroundings[2] != "#" and (y + 1) < height:
                normalizedMap[y+1][x] = "B"
            if surroundings[3] != "#" and (x + 1) < width:
                normalizedMap[y][x+1] = "B"

    for i in range(len(b)):
        x = b[i][0]
        y = b[i][1]
        if normalizedMap[y][x] == "B":
            surroundings = getSurroundings(normalizedMap, x, y)
            if deadEnd(surroundings):
                normalizedMap[y][x] = "#"

    return normalizedMap

def deadEnd(surroundings: list) -> bool:
    signsOfDecay = 0

    for i in surroundings:
        if i == "#":
            signsOfDecay+=1

    if signsOfDecay > 2:
        return True


def getColor(char: str):

    if char == "0": return "White"
    if char == "G": return "Green"
    if char == "S": return "Red"
    if char == "#": return "Black"

    if char == "B": return "Gray"

    if char == "n": return "North"
    if char == "w": return "West"
    if char == "s": return "South"
    if char == "e": return "East"

    return "Blue"


def main():
    parser = argparse.ArgumentParser(description="Labyrinth 3.1–3.3: read + normalize + print")
    parser.add_argument("-f", "--file", help="Path to labyrinth text file")
    args = parser.parse_args()

    if not args.file:
        raise Exception("Provide --file PATH")

    normalizedMap = getNormalizedCharMap(args.file)

    gfx.init_once(surface_resolution=(len(normalizedMap[0])*1,len(normalizedMap)*1),window_title="",screen_resolution=(600, 600/len(normalizedMap[0]) * len(normalizedMap)*1))

    while not gfx.stop_prog:
        normalizedMap = drawLabyrinth(normalizedMap)
        gfx.event_loop()

if __name__ == "__main__":
    main()
