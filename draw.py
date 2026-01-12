import argparse

from original import gfx_stack as gfx
from read import getNormalizedCharMap

def drawLabyrinth(normalizedMap: list[list[str]]):
    for row in range(len(normalizedMap)): #Zeile
        for column in range(len(normalizedMap[row])): #Spalte
            gfx.set_pixel((column,row),getColor(normalizedMap[row][column]))

def getColor(char: str):

    if char == "0": return "White" #Way
    if char == "G": return "Green" #Goal
    if char == "S": return "Red" #Start
    if char == "#": return "Black" #Wall

    return "Blue" #Bonus

def main():
    parser = argparse.ArgumentParser(description="Labyrinth 3.1–3.3: read + normalize + print")
    parser.add_argument("-f", "--file", help="Path to labyrinth text file")
    args = parser.parse_args()

    if not args.file:
        raise Exception("Provide --file PATH")

    normalizedMap = getNormalizedCharMap(args.file)

    gfx.init_once(surface_resolution=(len(normalizedMap[0])*1,len(normalizedMap)*1),window_title="",screen_resolution=(600, 600/len(normalizedMap[0]) * len(normalizedMap)*1))

    while not gfx.stop_prog:
        drawLabyrinth(normalizedMap)
        gfx.event_loop()

if __name__ == "__main__":
    main()
