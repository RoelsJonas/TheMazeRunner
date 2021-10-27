
import math
import time

import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf

hp = 100
stamina = 100
hunger = 100

HUNGERMODIFIER = 0.1 #snelheid waarmee hunger daalt
SPRINTINGHUNGERMODIFIER = 0.15 #snelheid waarmee hunger extra daal tijdens het sprinten
STAMINALOSSMODIFIER = 5 #snelheid waarmee stamina verloren gaat tijdens sprinten
STAMINAREGENMODIFIER = 3 #snelheid waarmee stamina regenereert
HUNGERHPLOSSMODIFIER = 0.1 #snelheid waarmee hp verloren gaat wanneer hunger = 0
CROSSHAIRGROOTTE = 30

DAGTIJD = 60 # aantal seconden dat 1 dag nacht cyclus duurt

# Constanten
BREEDTE = 800
HOOGTE = 600
SPEED = 1
SPRINT_SPEED = 1.75

# Globale variabelen

# positie van de speler
p_speler = np.array([3 + 1 / math.sqrt(2), 4 - 1 / math.sqrt(2)])
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
    [[1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 1, 1],
     [1, 1, 1, 1, 1, 1, 1]])

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




def polling(delta,p_speler,r_speler):
    global moet_afsluiten
    global stamina
    global hunger

    delta_p = np.array([0,0])
    key_states = sdl2.SDL_GetKeyboardState(None)

    if key_states[sdl2.SDL_SCANCODE_LSHIFT] and stamina > 0:
        delta = delta * SPRINT_SPEED
        sprinting = True
    else:
        delta = delta * SPEED
        sprinting = False
        if stamina < 100:
            stamina += delta * STAMINAREGENMODIFIER

    if key_states[sdl2.SDL_SCANCODE_W]:
        delta_p[0] += 1

    if key_states[sdl2.SDL_SCANCODE_S]:
        delta_p[0] -= 1

    if key_states[sdl2.SDL_SCANCODE_A]:
        delta_p[1] += 1

    if key_states[sdl2.SDL_SCANCODE_D]:
        delta_p[1] -= 1

    if delta_p[0] != 0 or delta_p[1] != 0:

        if sprinting:
            stamina -= delta * STAMINALOSSMODIFIER
            hunger -= delta * SPRINTINGHUNGERMODIFIER
        elif stamina < 100:
            stamina += delta * STAMINAREGENMODIFIER

        delta_p = delta_p / np.linalg.norm(delta_p)
        bewegen(delta, delta_p, r_speler)

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True


def bewegen(delta, delta_p, r_speler):
    global p_speler
    p_speler_nieuw = np.array([p_speler[0], p_speler[1]])

    dichtste_afstand = 0.2

    p_speler_nieuw += delta * delta_p[0] * r_speler
    p_speler_nieuw += delta * delta_p[1] * r_cameravlak

    if world_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 0:
        p_speler = p_speler_nieuw

    elif world_map[int(p_speler[1]), int(p_speler_nieuw[0])] == 0:
        p_speler[0] = p_speler_nieuw[0]

    elif world_map[int(p_speler_nieuw[1]), int(p_speler[0])] == 0:
        p_speler[1] = p_speler_nieuw[1]


def draaien():
    events = sdl2.ext.get_events()
    global r_cameravlak
    global r_speler
    global objecten
    for event in events:
        if event.type == sdl2.SDL_MOUSEMOTION:
            beweging = (-1) * event.motion.xrel *0.001
            rot = np.array(((np.cos(beweging), -np.sin(beweging)),
                            (np.sin(beweging), np.cos(beweging))))
            r_speler = np.dot(r_speler, rot)
            r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])




def bereken_r_straal(r_speler, kolom):

    r_straal_kolom = (D_CAMERA * r_speler) + (((-1) + ((2 * kolom)/BREEDTE)) * r_cameravlak)
    modulus = r_straal_kolom[0]**2 + r_straal_kolom[1]**2
    modulus = math.sqrt(modulus)
    r_straal = r_straal_kolom / modulus
    return r_straal


def raycast(p_speler, r_straal):
    d_muur = -1
    k_muur = kleuren[0]
    #stap 0 initialiseer x en y met waarde 0
    x = 0
    y = 0

    #stap 1 bereken delta v en h

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
            i_x = int(intersectie[0])
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
            d_muur = ((intersectie[0] - p_speler[0]) ** 2 + (intersectie[1] - p_speler[1]) ** 2) ** 0.5
            if horizontaal:
                k_muur = sdl2.ext.Color(255, 0, 0)
            else:
                k_muur = sdl2.ext.Color(128, 0, 0)

    return (d_muur, k_muur, intersectie, horizontaal)

def render_lucht_en_vloer(renderer):
    renderer.fill((0, 0, BREEDTE, int(HOOGTE / 2)), sdl2.ext.Color(0, 0, 255))
    renderer.fill((0, HOOGTE, BREEDTE, int(-HOOGTE / 2)), sdl2.ext.Color(192, 192, 192))


def render_kolom(renderer, window, kolom, d_muur, k_muur, intersectie, horizontaal, textures, r_straal):
    texture_index = 0
    d_euclidisch = d_muur
    d_muur = d_euclidisch * np.dot(r_speler, r_straal)
    if d_muur > 0:
        hoogte = (window.size[1]/d_muur)
        y1 = int((window.size[1]-hoogte)//2)
        y2 = window.size[1]-y1
        textuur_y = 0
        textuur_hoogte = int(textures[texture_index].size[1])


    if horizontaal:
        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * textures[texture_index].size[0]))
    else:
        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * textures[texture_index].size[0]))

    renderer.copy(textures[0], srcrect=(textuur_x, textuur_y, 1, textuur_hoogte), dstrect=(BREEDTE - 1 - kolom, y1, 2, int(hoogte))) #muur


    return

def render_hud(renderer, hud, stamina, hp, hunger, crosshair):

    renderer.fill((69, 540, int(hp), 47), kleuren[10])
    renderer.fill((688, 535, int(stamina), 22), kleuren[9])
    renderer.fill((688, 565, int(hunger), 22), kleuren[8])
    renderer.copy(hud, srcrect=(0, 0, 800, 75), dstrect=(0, 525, BREEDTE,75))
    renderer.copy(crosshair, srcrect=(0, 0, 50, 50), dstrect=((BREEDTE-CROSSHAIRGROOTTE)//2, (HOOGTE-CROSSHAIRGROOTTE)//2 , CROSSHAIRGROOTTE, CROSSHAIRGROOTTE))





def main():
    # Initialiseer de SDL2 bibliotheek
    sdl2.ext.init()
    global p_speler
    global stamina
    global hp
    global hunger

    # Maak een venster aan om de game te renderen
    window = sdl2.ext.Window("Project Ingenieursbeleving 2", size=(BREEDTE, HOOGTE))
    window.show()

    # Begin met het uitlezen van input van de muis en vraag om relatieve coordinaten
    sdl2.SDL_SetRelativeMouseMode(True)

    # Maak een renderer aan zodat we in ons venster kunnen renderen
    renderer = sdl2.ext.Renderer(window)

    resources = sdl2.ext.Resources(__file__, "resources")

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    ManagerFont = sdl2.ext.FontManager(font_path="OpenSans.ttf", size=50, color=(255, 255, 255))

    muur_texture_dag = factory.from_image(resources.get_path("nee.png"))
    hud = factory.from_image(resources.get_path("hud.png"))
    crosshair = factory.from_image(resources.get_path("crosshair.png"))

    dimmer75 = factory.from_image(resources.get_path("dimmer4.png"))
    dimmer60 = factory.from_image(resources.get_path("dimmer3.png"))
    dimmer45 = factory.from_image(resources.get_path("dimmer2.png"))
    dimmer30 = factory.from_image(resources.get_path("dimmer1.png"))
    dimmer15 = factory.from_image(resources.get_path("dimmer0.png"))
    dimmer0  = factory.from_image(resources.get_path("transparant.png"))

    dimmers = [dimmer75, dimmer60, dimmer45, dimmer30, dimmer15]
    for i in range(DAGTIJD//2 -5):
        dimmers.append(dimmer0)
    dimmers += ([dimmer15, dimmer30, dimmer45, dimmer60, dimmer75])
    for i in range(DAGTIJD//2 -4):
        dimmers.append(dimmer75)

    textures = []
    textures.append(muur_texture_dag)

    timeCycle = 5


    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    while not moet_afsluiten:
        # Onthoud de huidige tijd
        start_time = time.time()
        kolom = 0

        # Reset de rendering context
        renderer.clear()
        render_lucht_en_vloer(renderer)
        # Render de huidige frame
        for kolom in range(0, window.size[0]):
            r_straal = bereken_r_straal(r_speler, kolom)
            (d_muur, k_muur, intersectie, horizontaal) = raycast(p_speler, r_straal)
            render_kolom(renderer, window, kolom, d_muur, k_muur, intersectie, horizontaal, textures, r_straal)
        # Verwissel de rendering context met de frame buffer=

        renderer.copy(dimmers[int(timeCycle)], srcrect=(0,0,1,1), dstrect=(0,0,BREEDTE,HOOGTE))
        render_hud(renderer, hud, stamina, hp, hunger, crosshair)

        end_time = time.time()
        delta = end_time - start_time

        text_ = "FPS:" + str(np.round(1 / delta))
        text = factory.from_text(text_, fontmanager=ManagerFont)
        renderer.copy(text, dstrect=(0, 0, 50, 25))

        if hunger >= 0:
            hunger -= delta * HUNGERMODIFIER
        elif hp > 0:
            hp -= delta * HUNGERHPLOSSMODIFIER
        timeCycle += delta
        if timeCycle >= DAGTIJD:
            timeCycle = 0

        polling(delta,p_speler,r_speler)
        draaien()

        renderer.present()
        window.refresh()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()