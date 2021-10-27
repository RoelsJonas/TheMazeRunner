import math
import time
import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import rendering
import raycast
import movement
import sprites
import winsound

#begin waarden instellen
hp = 100
stamina = 100
hunger = 100

HUNGERMODIFIER = 0.15 #snelheid waarmee hunger daalt
SPRINTINGHUNGERMODIFIER = 0.15 #snelheid waarmee hunger extra daal tijdens het sprinten
STAMINALOSSMODIFIER = 5 #snelheid waarmee stamina verloren gaat tijdens sprinten
STAMINAREGENMODIFIER = 3 #snelheid waarmee stamina regenereert
HUNGERHPLOSSMODIFIER = 0.1 #snelheid waarmee hp verloren gaat wanneer hunger = 0
CROSSHAIRGROOTTE = 26
SENSITIVITY = 0.001

DAGNACHTCYCLUSTIJD = 60 # aantal seconden dat 1 dag nacht cyclus duurt
KLOKINTERVAL = DAGNACHTCYCLUSTIJD / 24     # om te weten om de hoeveel tijd de klok een uur moet opschuiven

# Constanten
BREEDTE = 800
HOOGTE = 600
SPEED = 1
SPRINT_SPEED = 1.75

# Globale variabelen

# positie van de speler
p_speler = np.array([9 + 1 / math.sqrt(2), 10 - 1 / math.sqrt(2)])
#p_speler = np.array([5,0.75])

# richting waarin de speler kijkt
r_speler = np.array([1 / math.sqrt(2), -1 / math.sqrt(2)])

# cameravlak
r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])

D_CAMERA = 1/np.tan(np.deg2rad(90)/2)

# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False

# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn
world_map = np.array(
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

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
    sdl2.ext.Color(219, 190, 72), # 8 = hunger
    sdl2.ext.Color(0, 255, 0),  # 9 = stamina
    sdl2.ext.Color(255, 0, 0),  # 10 = Rood
]


def main():
    # Initialiseer de SDL2 bibliotheek
    sdl2.ext.init()
    global p_speler
    global stamina
    global hp
    global hunger
    global moet_afsluiten
    global r_speler
    global r_cameravlak


    # Maak een venster aan om de game te renderen
    window = sdl2.ext.Window("Project Ingenieursbeleving 2", size=(BREEDTE, HOOGTE))
    window.show()

    # Begin met het uitlezen van input van de muis en vraag om relatieve coordinaten
    sdl2.SDL_SetRelativeMouseMode(True)

    # Maak een renderer aan zodat we in ons venster kunnen renderen
    renderer = sdl2.ext.Renderer(window)

    (resources, factory, ManagerFont, textures, hud, crosshair, dimmer, klokImages, mist) = rendering.create_resources(renderer)

    timeCycle = 30
    winsound.PlaySound("resources\muziek.wav", winsound.SND_LOOP | winsound.SND_ASYNC)
    sprite = sprites.Sprite(3.0, 3.0, 1, 0, "spellun-sprite.png", 0.5, 0.25, resources, factory)
    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    while not moet_afsluiten:
        # Onthoud de huidige tijd
        start_time = time.time()
        kolom = 0

        # Reset de rendering context
        renderer.clear()
        rendering.render_lucht_en_vloer(renderer)
        # Render de huidige frame
        for kolom in range(0, window.size[0]):
            r_straal = raycast.bereken_r_straal(r_speler,r_cameravlak, kolom)
            (d_muur, intersectie, horizontaal) = raycast.raycast(p_speler, r_straal)
            rendering.render_kolom(renderer, window, kolom, d_muur, intersectie, horizontaal, textures, r_straal, r_speler, timeCycle, mist)
        # Verwissel de rendering context met de frame buffer=

        rendering.dim_image(renderer, dimmer, timeCycle)
        sprite.render(renderer, r_speler, r_cameravlak, p_speler)

        end_time = time.time()
        delta = end_time - start_time

        rendering.render_FPS(delta, renderer, factory, ManagerFont)


        if hunger >= 0:
            hunger -= delta * HUNGERMODIFIER
        elif hp>=0:
            hp -= delta * HUNGERHPLOSSMODIFIER
        else:
            winsound.PlaySound("resources\GameOverSound.wav", winsound.SND_ASYNC)
            rendering.render_GameOVer(renderer, factory)

        rendering.render_hud(renderer, hud, stamina, hp, hunger, crosshair, timeCycle, klokImages)

        timeCycle += delta
        if timeCycle >= DAGNACHTCYCLUSTIJD:
            timeCycle = 0

        (p_speler, moet_afsluiten, stamina, hunger) = movement.polling(delta,p_speler,r_speler,r_cameravlak, stamina, hunger)
        (r_speler, r_cameravlak) = movement.draaien(r_speler, r_cameravlak)

        renderer.present()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()