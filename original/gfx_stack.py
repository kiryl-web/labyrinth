#!/usr/bin/env python3
# Grafik Utilities für das Software Engineering Grundlagen Praktikum WS2024/25

import pygame
import math

color_dict = {
    "Green": (100, 255, 100),
    "Yellow": (255, 255, 0),
    "Red": (255, 0, 0),
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Blue": (10,10,255),
    "Gray": (100,100,100),
    "Orange": (255, 200,0),
    "Dark Gray": (70,70,70),


    "North": (0,0,200),
    "South": (144,144,0),
    "West": (144,0,144),
    "East": (0,144,144),


    "1": (100,100,170),
    "2": (100,100,180),
    "3": (100,100,190),
    "4": (100,100,200),
    "5": (100,100,210),
    "6": (100,100,220),
    "7": (100,100,230),
    "8": (100,100,240),
    "9": (100,100,250),
}

stop_prog = False  # Flag: der Wert 'True' signalisiert den Wunsch des Anwenders zum Programmende
space_key = False  # Flag: die Leertaste wurde vom Anwender betätigt, muss vom Programmierer zurückgesetzt werden

# Modul-interne Vars, global für Debuggingzwecke
screen = None  # Fenster-Objekt in welches die Leinwand gezeichnet wird
surface = None  # Leinwand-Objekt zum Zeichnen
clock = None  # Timer-Objekt
screen_wxh = (0, 0)  # Debugging: angeforderte Größe des Fensters
surface_wxh = (0, 0)  # Debugging: angeforderte Größe der Leinwand


def init_once(surface_resolution=(120, 120),
              window_title="Software Engineering Grundlagen Praktikum 3, mögliche Eingaben: Leertaste und 'q'",
              screen_resolution=(640, 640)):
    """Wrapper initialisiere pygame und alles was sonst noch benötigt wird."""
    global stop_prog, screen, clock, surface, screen_wxh, surface_wxh
    stop_prog = False
    screen_wxh = screen_resolution
    surface_wxh = surface_resolution
    screen = pygame.display.set_mode(screen_wxh)
    surface = pygame.Surface(surface_wxh)
    pygame.display.set_caption(window_title)
    clock = pygame.time.Clock()
    pygame.init()


def quit_prog():
    """Wrapper aufräumen und vorbereiten für pygame Neustart."""
    pygame.display.quit()
    pygame.quit()


def set_pixel(pos, color):
    """Zeichne ein Pixel mit dem Farbnamen color an Position pos(x,y) in das Anwendungsfenster."""
    # eigentlich wird auf das Surface gezeichnet und dieses später auf das Fenster übertragen
    global surface
    color_val = color_dict[color]
    surface.set_at(pos, color_val)


def color_demo_paint_on_surface():
    """Zeichnet ein Testbild ins Fenster zur einfachen Funktionsüberprüfung."""
    color_it = iter(color_dict)
    for y in range(surface_wxh[1]):
        if y % math.ceil(surface_wxh[1] / 32) == 0:
            color_name = next(color_it)
        for x in range(surface_wxh[0]):
            set_pixel((x, y), color_name)


def event_loop():
    """Events behandeln, Leinwand auf Fensterzeichnen und blockieren für 50ms."""
    global clock, stop_prog, space_key
    # Abfrage 'q'- und Leer-Taste und Window-Close-Button
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_key = False
        if event.type == pygame.QUIT:
            stop_prog = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                stop_prog = True
            if event.key == pygame.K_SPACE:
                space_key = True

    # zeichnen
    # vor dem Zeichnen das surface heranzoomen
    pygame.transform.scale(surface, screen_wxh, screen)
    pygame.display.flip()
    # Programm auf 20 FPS drosseln
    clock.tick(20)


def main():
    """Simpler Modultest."""
    init_once()

    color_demo_paint_on_surface()

    while not stop_prog:
        event_loop()

    quit_prog()


if __name__ == '__main__':
    main()
