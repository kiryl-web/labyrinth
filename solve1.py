import argparse
from find_coordinates import getSurroundings, findEndCoordinates,findPlayerCoordinates
from read import getNormalizedCharMap
from original import gfx_stack as gfx

#Nach rechts, ansonsten geradeaus, ansonsten nach links, ansonsten zrück
def drawLabyrinth(normalizedMap: list[list[str]]):

    for row in range(len(normalizedMap)):  # Zeile
        for column in range(len(normalizedMap[row])):  # Spalte
            gfx.set_pixel((column, row), getColor(normalizedMap[row][column]))

    goal = findEndCoordinates(normalizedMap)
    player = findPlayerCoordinates(normalizedMap)

    width = len(normalizedMap[0])
    height = len(normalizedMap)

    x = player[0]
    y = player[1]

    orientation = normalizedMap[y][x]

    if orientation=="S": #Das heißt, es hat noch nicht gestarted
        normalizedMap[y][x] = "n"
        orientation = "n"

    if (x, y) == goal or goal == (-1, -1):
        return normalizedMap

    surroundings = getSurroundings(normalizedMap, x, y)
    normalizedMap[y][x] = "B"

    def north():
        if surroundings[0] != "#" and (y - 1) > 0:
            normalizedMap[y-1][x] = "n"
            return normalizedMap

    def west():
        if surroundings[1] != "#" and (x - 1) > 0:
            normalizedMap[y][x-1] = "w"
            return normalizedMap

    def south():
        if surroundings[2] != "#" and (y + 1) < height:
            normalizedMap[y+1][x] = "s"
            return normalizedMap

    def east():
        if surroundings[3] != "#" and (x + 1) < width:
            normalizedMap[y][x+1] = "e"
            return normalizedMap

    if orientation == "n":
        if east()  is not None: return normalizedMap
        if north() is not None: return normalizedMap
        if west()  is not None: return normalizedMap
        if south() is not None: return normalizedMap

    if orientation == "e":
        if south() is not None: return normalizedMap
        if east()  is not None: return normalizedMap
        if north() is not None: return normalizedMap
        if west()  is not None: return normalizedMap

    if orientation == "s":
        if west()  is not None: return normalizedMap
        if south() is not None: return normalizedMap
        if east()  is not None: return normalizedMap
        if north() is not None: return normalizedMap

    if orientation == "w":
        if north() is not None: return normalizedMap
        if west()  is not None: return normalizedMap
        if south() is not None: return normalizedMap
        if east()  is not None: return normalizedMap

    return normalizedMap

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
    parser = argparse.ArgumentParser(description="Labyrinth")
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
