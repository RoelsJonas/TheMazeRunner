import math
import time
import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import main


def render_hud(renderer, hud, stamina, hp, hunger, crosshair, timeCycle, klokImages):

    renderer.fill((69, 540, int(hp), 47), main.kleuren[10])
    renderer.fill((688, 535, int(stamina), 22), main.kleuren[9])
    renderer.fill((688, 565, int(hunger), 22), main.kleuren[8])
    renderer.copy(hud, srcrect=(0, 0, 800, 75), dstrect=(0, 525, main.BREEDTE,75))
    renderer.copy(crosshair, srcrect=(0, 0, 50, 50), dstrect=((main.BREEDTE - main.CROSSHAIRGROOTTE)//2, (main.HOOGTE - main.CROSSHAIRGROOTTE)//2 , main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))
    klok = int(24 * (int(timeCycle)/main.DAGNACHTCYCLUSTIJD))
    if klok >= 12:
        klok -= 12
    print(klok)
    renderer.copy(klokImages[klok], srcrect=(0,0,300,300), dstrect=(505, 530, 60, 60))


def render_kolom(renderer, window, kolom, d_muur, intersectie, horizontaal, textures, r_straal, r_speler, timecycle, mist):
    texture_index = 0
    d_euclidisch = d_muur
    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

    hoogte = main.MUURHOOGTE*(window.size[1]/d_muur)
    y1 = int((window.size[1]-hoogte)//2) - 100
    y2 = window.size[1]-y1
    textuur_y = 0
    textuur_hoogte = int(textures[texture_index].size[1])



    if horizontaal:
        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * textures[texture_index].size[0]))
    else:
        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * textures[texture_index].size[0]))

    renderer.copy(textures[0], srcrect=(textuur_x, textuur_y, 1, textuur_hoogte), dstrect=(main.BREEDTE - 1 - kolom, y1, 2, int(hoogte))) #muur



def render_lucht_en_vloer(renderer, timecycle):
    renderer.fill((0, 0, main.BREEDTE, int(main.HOOGTE / 2)-100), main.kleuren[11])
    renderer.fill((0, main.HOOGTE, main.BREEDTE, int(-main.HOOGTE / 2 -100)), main.kleuren[6])



def render_GameOVer(renderer, factory):
    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(255, 0, 0))
    GameOver_text = "Ge zijt dood"
    GameOver_render = factory.from_text(GameOver_text, fontmanager=ManagerFont)
    renderer.copy(GameOver_render, dstrect=(150, 200, 500, 200))
    renderer.present()
    time.sleep(5)
    sdl2.ext.quit()



def render_FPS(delta, renderer, factory, ManagerFont):
    text_ = "FPS:" + str(np.round(1 / delta))
    text = factory.from_text(text_, fontmanager=ManagerFont)
    renderer.copy(text, dstrect=(0, 0, 50, 25))


def create_resources(renderer):

    resources = sdl2.ext.Resources(__file__, "resources")

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(255, 255, 255))

    muur = factory.from_image(resources.get_path("wall-concrete.png"))
    hud = factory.from_image(resources.get_path("hud.png"))
    crosshair = factory.from_image(resources.get_path("crosshair.png"))
    dimmer = factory.from_image((resources.get_path("dimmer.png")))
    mist = factory.from_image((resources.get_path("tunnelVision.png")))

    klokImages = []
    for i in range(6, 12):
        klokImages.append(factory.from_image((resources.get_path("klok" + str(i+1) + ".png"))))
    for i in range(6):
        klokImages.append(factory.from_image((resources.get_path("klok" + str(i+1) + ".png"))))

    textures = []
    textures.append(muur)

    return(resources, factory, ManagerFont, textures, hud, crosshair, dimmer, klokImages, mist)

def dim_image(renderer, dimmer, timeCycle):

    if (main.DAGNACHTCYCLUSTIJD//2) + 5 <= timeCycle <= ((main.DAGNACHTCYCLUSTIJD//2) + 10):           #avond maken
        for i in range(int(timeCycle*10-((main.DAGNACHTCYCLUSTIJD//2) + 5)*10)):                       # afhankelijk van timeCyclus bepaalde hoeveelheid dimmers toevoegen om langzaam donker te worden, term achter minteken is om offset te maken
            renderer.copy(dimmer, srcrect=(0, 0, 1, 1), dstrect=(0, 0, main.BREEDTE, main.HOOGTE))

    elif timeCycle > ((main.DAGNACHTCYCLUSTIJD//2) + 10):                #nacht
        for i in range(50):
            renderer.copy(dimmer, srcrect=(0, 0, 1, 1), dstrect=(0, 0, main.BREEDTE, main.HOOGTE))

    elif timeCycle <= 5:                        #ochtend maken
        for i in range(int(50-10*timeCycle)):
            renderer.copy(dimmer, srcrect=(0, 0, 1, 1), dstrect=(0, 0, main.BREEDTE, main.HOOGTE))
