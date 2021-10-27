import math
import time

import numpy as np
import sdl2
import sdl2.ext

# Constanten
BREEDTE = 800
HOOGTE = 600

#
# Globale variabelen
#

# positie van de speler
p_speler = np.array([3 + 1 / math.sqrt(2), 4 - 1 / math.sqrt(2)])
#p_speler = np.array([5,0.75])

# richting waarin de speler kijkt
r_speler = np.array([1 / math.sqrt(2), -1 / math.sqrt(2)])

# cameravlak
r_cameravlak = np.array([r_speler[0], -1 * r_speler[1]])

D_CAMERA = 1/np.tan(np.deg2rad(90)/2)

# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False

# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn
world_map = np.array(
    [[2, 2, 2, 2, 2, 2, 2],
     [2, 0, 0, 0, 1, 1, 2],
     [2, 0, 0, 0, 0, 1, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 2, 2, 2, 2, 2, 2]]
)

# Vooraf gedefinieerde kleuren
kleuren = [
    sdl2.ext.Color(0, 0, 0),  # 0 = Zwart
    sdl2.ext.Color(255, 0, 0),  # 1 = Rood
    sdl2.ext.Color(0, 255, 0),  # 2 = Groen
    sdl2.ext.Color(0, 0, 255),  # 3 = Blauw
    sdl2.ext.Color(64, 64, 64),  # 4 = Donker grijs
    sdl2.ext.Color(128, 128, 128),  # 5 = Grijs
    sdl2.ext.Color(192, 192, 192),  # 6 = Licht grijs
    sdl2.ext.Color(255, 255, 255),  # 7 = Wit
]


#
# Verwerkt alle input van het toetsenbord en de muis
#
# Argumenten:
# @delta       Tijd in milliseconden sinds de vorige oproep van deze functie
#
def verwerk_input(delta):
    global moet_afsluiten

    # Handelt alle input events af die zich voorgedaan hebben sinds de vorige
    # keer dat we de sdl2.ext.get_events() functie hebben opgeroepen
    events = sdl2.ext.get_events()
    for event in events:
        # Een SDL_QUIT event wordt afgeleverd als de gebruiker de applicatie
        # afsluit door bv op het kruisje te klikken
        if event.type == sdl2.SDL_QUIT:
            moet_afsluiten = True
            break
        # Een SDL_KEYDOWN event wordt afgeleverd wanneer de gebruiker een
        # toets op het toetsenbord indrukt.
        # Let op: als de gebruiker de toets blijft inhouden, dan zien we
        # maar 1 SDL_KEYDOWN en 1 SDL_KEYUP event.
        elif event.type == sdl2.SDL_KEYDOWN:
            key = event.key.keysym.sym
            if key == sdl2.SDLK_q:
                moet_afsluiten = True
            break
        # Analoog aan SDL_KEYDOWN. Dit event wordt afgeleverd wanneer de
        # gebruiker een muisknop indrukt
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            button = event.button.button
            if button == sdl2.SDL_BUTTON_LEFT:
                # ...
                continue
        # Een SDL_MOUSEWHEEL event wordt afgeleverd wanneer de gebruiker
        # aan het muiswiel draait.
        elif event.type == sdl2.SDL_MOUSEWHEEL:
            if event.wheel.y > 0:
                # ...
                continue
        # Wordt afgeleverd als de gebruiker de muis heeft bewogen.
        # Aangezien we relative motion gebruiken zijn alle coordinaten
        # relatief tegenover de laatst gerapporteerde positie van de muis.
        elif event.type == sdl2.SDL_MOUSEMOTION:
            # Aangezien we in onze game maar 1 as hebben waarover de camera
            # kan roteren zijn we enkel geinteresseerd in bewegingen over de
            # X-as
            beweging = event.motion.xrel
            continue

    # Polling-gebaseerde input. Dit gebruiken we bij voorkeur om bv het ingedrukt
    # houden van toetsen zo accuraat mogelijk te detecteren
    key_states = sdl2.SDL_GetKeyboardState(None)

    # if key_states[sdl2.SDL_SCANCODE_UP] or key_states[sdl2.SDL_SCANCODE_W]:
    # beweeg vooruit...

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True


def bereken_r_straal(r_speler, kolom):
    r_straal = np.zeros(2)
    r_straal_kolom = (D_CAMERA * r_speler) + (((-1) + ((2 * kolom)/BREEDTE)) * r_cameravlak)
    modulus = r_straal_kolom[0]**2 + r_straal_kolom[1]**2
    modulus = math.fabs(math.sqrt(modulus))
    r_straal = r_straal_kolom / modulus
    return r_straal


def raycast(p_speler, r_straal):
    d_muur = -1
    k_muur = kleuren[0]

    #stap 0 initialiseer x en y met waarde 0
    x = 0
    y = 0

    #stap 1 bereken delta v en h
    if r_straal[0] == 0:
        delta_v = 1
        delta_h = 0
    elif r_straal[1] == 0:
        delta_v = 0
        delta_h = 1
    else:
        delta_v = 1/abs(r_straal[0])
        delta_h = 1/abs(r_straal[1])

    #stap 2 bereken d_horizontaal en d_verticaal
    if r_straal[1] >= 0:
        d_horizontaal = (1 - p_speler[1] + int(p_speler[1])) * delta_h
    else:
        d_horizontaal = (p_speler[1] - int(p_speler[1])) * delta_h

    if r_straal[0] >= 0:
        d_verticaal = (1 - p_speler[0] + int(p_speler[0])) * delta_v
    else:
        d_verticaal = (p_speler[0] - int(p_speler[0])) * delta_v

    #loop van stap 3 tot stap 6
    while d_muur == -1:
        if (d_horizontaal + x * delta_h) <= (d_verticaal + y * delta_v):
            intersectie = p_speler + (d_horizontaal + (x * delta_h)) * r_straal
            horizontaal = True
            x += 1

        else:
            intersectie = p_speler + (d_verticaal + (y * delta_v)) * r_straal
            horizontaal = False
            y += 1

        if horizontaal:
            i_x = int(np.floor(intersectie[0]))
            if r_straal[1] < 0:
                i_y = int(np.round(intersectie[1]))
                i_y -= 1
            else:
                i_y = int(np.round(intersectie[1]))

        else:
            i_y = int(intersectie[1])
            if r_straal[0] >= 0:
                i_x = int(np.round(intersectie[0]))
            else:
                i_x = int(np.round(intersectie[0])) - 1

        if i_x >= 7 or i_x < 0:
            return(0, kleuren[0])

        if i_y >= 7 or i_y < 0:
            return(0, kleuren[0])

        if world_map[i_y, i_x] == 1:
            d_euclidisch = ((intersectie[0] - p_speler[0]) ** 2 + (intersectie[1] - p_speler[1]) ** 2) ** 0.5
            d_muur = d_euclidisch * np.dot(r_speler, r_straal)
            if horizontaal:
                k_muur = sdl2.ext.Color(255, 0, 0)
            else:
                k_muur = sdl2.ext.Color(128, 0, 0)

    return (d_muur, k_muur)


def render_kolom(renderer, window, kolom, d_muur, k_muur):
    if d_muur > D_CAMERA:
        hoogte = (window.size[1]/d_muur)
        y1 = int((window.size[1]-hoogte)//2)
        y2 = window.size[1]-y1
    else:
        y1 = 0
        y2 = HOOGTE
    renderer.draw_line((kolom, int(y1), kolom, int(y2)), k_muur)
    return



def main():
    # Initialiseer de SDL2 bibliotheek
    sdl2.ext.init()
    global p_speler

    # Maak een venster aan om de game te renderen
    window = sdl2.ext.Window("Project Ingenieursbeleving 2", size=(BREEDTE, HOOGTE))
    window.show()

    # Begin met het uitlezen van input van de muis en vraag om relatieve coordinaten
    sdl2.SDL_SetRelativeMouseMode(True)

    # Maak een renderer aan zodat we in ons venster kunnen renderen
    renderer = sdl2.ext.Renderer(window)

    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    while not moet_afsluiten:
        # Onthoud de huidige tijd
        start_time = time.time()
        kolom = 0

        # Reset de rendering context
        renderer.clear()

        # Render de huidige frame
        for kolom in range(0, window.size[0]):
            r_straal = bereken_r_straal(r_speler, kolom)
            (d_muur, k_muur) = raycast(p_speler, r_straal)
            render_kolom(renderer, window, kolom, d_muur, k_muur)
            #print("raycast", kolom)

        # Verwissel de rendering context met de frame buffer
        renderer.present()
        end_time = time.time()
        delta = end_time - start_time
        #print("FPS:", 1/delta)
        #p_speler[1] = p_speler[1] + 0.25

        verwerk_input(delta)
        window.refresh()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()
