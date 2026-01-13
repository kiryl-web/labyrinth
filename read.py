import argparse

import find_coordinates

def loadCharMapFromFile(filePath: str) -> list[list[str]]:
    lines = []

    with open(filePath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    #Überprüfung Rechteck
    for i in range(len(lines)):
        if len(lines[i]) != len(lines[0]):
            raise Exception("Labyrinth has lines of differing length. It is therefore not a rectangle.")

    charMap = []

    for line in lines:
        row = []
        for ch in line:
            row.append(ch)
        charMap.append(row)

    return charMap

def getNormalizedCharMap(filePath: str) -> list[list[str]]:
    """

    :rtype: object
    """
    charMap = loadCharMapFromFile(filePath)

    wayChar, wallChar= ".", "W"

    for row in charMap:
        for ch in row:
            if ch == "X":
                wayChar, wallChar= "W", "X"

    normalizedMap = []

    for y in range(len(charMap)):
        row = []
        for x in range(len(charMap[y])):
            char = charMap[y][x]

            if char == wallChar:
                row.append("#")
            if char == wayChar:
                row.append("0")
            if char == "S":
                row.append("S")
            if char == "Z":
                row.append("G")
            if char.isdigit():
                row.append(char)

        normalizedMap.append(row)

    return normalizedMap

def printLabyrinth(labyrinthMap: list[list[str]]):
    for row in labyrinthMap:
        line = ""
        for cellValue in row:
            line += str(cellValue)
        print(line)

def main() -> None:
    parser = argparse.ArgumentParser(description="Labyrinth")
    parser.add_argument("-f", "--file", help="Path to labyrinth text file")
    args = parser.parse_args()

    if not args.file:
        raise Exception("Provide --file PATH")

    normalizedMap = getNormalizedCharMap(args.file)
    printLabyrinth(normalizedMap)
    find_coordinates.findStartCoordinates(normalizedMap)
    find_coordinates.findEndCoordinates(normalizedMap)


if __name__ == "__main__":
    main()
