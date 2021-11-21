import math
import time
import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import playsound


import rendering
import raycast
import movement
import sprites
import winsound
import imageToMap
import equips
import text
#begin waarden instellen
hp = 100
stamina = 100
hunger = 100

HUNGERMODIFIER = 6 #snelheid waarmee hunger daalt
SPRINTINGHUNGERMODIFIER = 0.15 #snelheid waarmee hunger extra daal tijdens het sprinten
STAMINALOSSMODIFIER = 5 #snelheid waarmee stamina verloren gaat tijdens sprinten
STAMINAREGENMODIFIER = 3 #snelheid waarmee stamina regenereert
HUNGERHPLOSSMODIFIER = 0.1 #snelheid waarmee hp verloren gaat wanneer hunger = 0
CROSSHAIRGROOTTE = 26
SENSITIVITY = 0.001
INTERACTIONDISTANCE = 0.2
HPREPLENISHMODIFIERER = 0,2

CONSUMESOUND = "GameOverSound.wav"



DAGNACHTCYCLUSTIJD = 60 # aantal seconden dat 1 dag nacht cyclus duurt
KLOKINTERVAL = DAGNACHTCYCLUSTIJD / 24     # om te weten om de hoeveel tijd de klok een uur moet opschuiven

MUURHOOGTE = 1.5

# Constanten
BREEDTE = 800
HOOGTE = 600
SPEED = 1.5
SPRINT_SPEED = 2.25

# Globale variabelen

# positie van de speler
p_speler = np.array([30 + 1 / math.sqrt(2), 30 - 1 / math.sqrt(2)])
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

(world_map, doorLocations, door_map) = imageToMap.generateWorld("resources\map6.png")

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
    sdl2.ext.Color(19, 216, 255), #11 = blauw dag skybox
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

    beginText = text.text("Wie ben ik? Wat doe ik hier? IS JONAS SEXY?", 10, 50, 450, 700, 50)
    consumableText = text.text("hmm, that's good stuff", 0, 200, 450, 400, 50)
    (resources, factory, ManagerFont, textures, hud, crosshair, dimmer, klokImages, mist, afbeeldingen_sprites) = rendering.create_resources(renderer)

    damage = 0
    timeToAttack = 0
    interact = False
    pakOp = False
    equiped = 1

    start_time = time.time()
    equiplist = [equips.equip(factory, resources, "medkit.png", 0, 0, 10, True),equips.equip(factory, resources, "medkit.png", 0, 0, 10, True), equips.equip(factory, resources, "medkit.png", 0, 0, 10, True), equips.equip(factory, resources, "medkit.png", 0, 0, 10, True)]
    timeCycle = 26
    #winsound.PlaySound('muziek.wav', winsound.SND_ASYNC | winsound.SND_LOOP)
    spriteList = []
    #spriteList.append(sprites.Sprite(32.0, 32.0, 1, 0, "spellun-sprite.png", 0.5, 0.25, 1, True, False, False, False, 0, 50, 10, resources, factory))
    spriteList.append(sprites.Sprite(28.0, 17.0, 1, 0, "burger.png", 0.5, 0.5, 1, False, False, False, True, 10, 0, 5, resources, factory))
    spriteList.append(sprites.Sprite(25.0, 25.0, 1, 0, "medkit.png", 0.5, 0.5, 1, False, True, True, True, 0, 0, 30, resources, factory))   #doet damage van -30 -> healt en volgt met speed 0, dus volgt niet
    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    while not moet_afsluiten:
        # Onthoud de huidige tijd
        kolom = 0

        # Reset de rendering context
        renderer.clear()

        #maak lege z buffer aan:
        z_buffer = np.zeros(BREEDTE, float)

        rendering.render_lucht_en_vloer(renderer, timeCycle)
        # Render de huidige frame
        for kolom in range(0, window.size[0]):
            r_straal = raycast.bereken_r_straal(r_speler,r_cameravlak, kolom)
            (d_muur, intersectie, horizontaal, z_buffer) = raycast.raycast(p_speler, r_straal, renderer, window, kolom, textures, r_speler, timeCycle, z_buffer)
            if z_buffer[BREEDTE - 1 - kolom] == 0 or z_buffer[BREEDTE - 1 - kolom] > d_muur:
                z_buffer[BREEDTE - 1 - kolom] = d_muur
                rendering.render_kolom(renderer, window, kolom, d_muur, intersectie, horizontaal, textures, r_straal, r_speler, timeCycle, mist)
        # Verwissel de rendering context met de frame buffer=

        end_time = time.time()
        delta = end_time - start_time
        start_time = time.time()
        spriteList = sprites.sortSprites(spriteList, p_speler)
        for sprite in spriteList:
            sprite.render(renderer, r_speler, r_cameravlak, p_speler, z_buffer)
            sprite.moveToPlayer(p_speler, delta)
            (hunger, hp, destroy, timeToAttack, equiplist) = sprite.checkInteractie(hunger, hp, p_speler, delta, damage, timeToAttack, pakOp, equiplist, equiped)
            if destroy:
                spriteList.remove(sprite)

        timeToAttack -= delta

        (hunger, hp, consumableText) = equips.interactions(hunger, hp, equiped, equiplist, interact, consumableText)



        if hunger >= 0:
            hunger -= delta * HUNGERMODIFIER
        elif hp >= 0:
            hp -= delta * HUNGERHPLOSSMODIFIER
        else:
            playsound.playsound('GameOverSound.wav', False)
            rendering.render_GameOVer(renderer, factory)


        timeCycle += delta
        if timeCycle >= DAGNACHTCYCLUSTIJD:
            timeCycle = 0

        (p_speler, moet_afsluiten, stamina, hunger, equiped, interact, pakOp) = movement.polling(delta, p_speler, r_speler, r_cameravlak, stamina, hunger, equiped, door_map)
        (r_speler, r_cameravlak, damage) = movement.draaien(r_speler, r_cameravlak)
        rendering.dim_image(renderer, dimmer, timeCycle)
        rendering.render_hud(renderer, hud, stamina, hp, hunger, crosshair, timeCycle, klokImages, equiped, equiplist)
        beginText.renderText(delta, renderer, factory)
        consumableText.renderText(delta, renderer, factory)
        rendering.render_FPS(delta, renderer, factory, ManagerFont)
        renderer.present()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()