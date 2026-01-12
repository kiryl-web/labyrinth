import argparse
from time import sleep

from find_coordinates import getSurroundings, findPlayerCoordinates, giveClosestUsedSpot, findEndCoordinates
from read import getNormalizedCharMap
from original import gfx_stack as gfx

import math


#Dieses löst das Labyrinth so: je nach dem wo der
#Richtungsvektor von Spieler->Ziel zeigt,
#versucht es in eine Richtung zu gehen.
#Wenn es in eine Sackgasse kommt,
#teleportiert es sich auf ein Feld wo es schonmal war.
#Dieses Feld ist dabei das Nächste am Ziel.
#Es werden Felder, wo keine Bewegung möglich ist,
#z.B. 3 Wände und 1 bereits begangenes, wird als "W" gespeichert
#und somit eliminiert.

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

    if (x, y) == goal:
        return normalizedMap

    if goal == (-1, -1):
        return normalizedMap

    angle = (math.degrees(math.atan2(-(goal[1] - y), goal[0] - x)) + 360) % 360

    surroundings = getSurroundings(normalizedMap, x, y)

    normalizedMap[y][x] = "B"

    if deadEnd(surroundings):
        normalizedMap[y][x] = "W"

    def up():
        if surroundings[0] != "#" and surroundings[0] != "W" and surroundings[0] != "B" and (y - 1) > 0:
            normalizedMap[y-1][x] = "P"
            return normalizedMap

    def left():
        if surroundings[1] != "#" and surroundings[1] != "W" and surroundings[1] != "B" and (x - 1) > 0:
            normalizedMap[y][x-1] = "P"
            return normalizedMap

    def down():
        if surroundings[2] != "#" and surroundings[2] != "W" and surroundings[2] != "B" and (y + 1) < height:
            normalizedMap[y+1][x] = "P"
            return normalizedMap

    def right():
        if surroundings[3] != "#" and surroundings[3] != "W" and surroundings[3] != "B" and (x + 1) < width:
            normalizedMap[y][x+1] = "P"
            return normalizedMap

    if 0 <= angle < 45:
        if right() is not None: return normalizedMap
        if up() is not None: return normalizedMap
        if down() is not None: return normalizedMap
        if left() is not None: return normalizedMap

    elif 45 <= angle < 90:
        if up() is not None: return normalizedMap
        if right() is not None: return normalizedMap
        if left() is not None: return normalizedMap
        if down() is not None: return normalizedMap

    elif 90 <= angle < 135:
        if up() is not None: return normalizedMap
        if left() is not None: return normalizedMap
        if right() is not None: return normalizedMap
        if down() is not None: return normalizedMap

    elif 135 <= angle < 180:
        if left() is not None: return normalizedMap
        if up() is not None: return normalizedMap
        if down() is not None: return normalizedMap
        if right() is not None: return normalizedMap

    elif 180 <= angle < 225:
        if left() is not None: return normalizedMap
        if down() is not None: return normalizedMap
        if up() is not None: return normalizedMap
        if right() is not None: return normalizedMap

    elif 225 <= angle < 270:
        if down() is not None: return normalizedMap
        if left() is not None: return normalizedMap
        if right() is not None: return normalizedMap
        if up() is not None: return normalizedMap

    elif 270 <= angle < 315:
        if down() is not None: return normalizedMap
        if right() is not None: return normalizedMap
        if left() is not None: return normalizedMap
        if up() is not None: return normalizedMap

    elif 315 <= angle < 360:
        if down() is not None: return normalizedMap
        if right() is not None: return normalizedMap
        if left() is not None: return normalizedMap
        if up() is not None: return normalizedMap

    randomUsedSpot = giveClosestUsedSpot(normalizedMap)

    normalizedMap[randomUsedSpot[1]][randomUsedSpot[0]] = "P"

    return normalizedMap

def deadEnd(surroundings: list) -> bool:
    signsOfDecay = 0

    for i in surroundings:
        if i == "B" or i == "#" or i == "W":
            signsOfDecay+=1

    if signsOfDecay > 2:
        return True

def getColor(char: str):

    if char == "0": return "White"
    if char == "G": return "Green"
    if char == "S": return "Red"
    if char == "#": return "Black"
    if char == "B": return "Gray"
    if char == "P": return "Orange"
    if char == "W": return "Dark Gray"
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
