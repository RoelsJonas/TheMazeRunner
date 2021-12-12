import math
import time
import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import main
import equips


def render_hud(renderer, hud, stamina, hp, hunger, crosshair, timeCycle, klokImages, equiped, equiplist, timeToAttack):
    offset = ((main.BREEDTE - 800 )//2)
    renderer.fill((0,main.HOOGTE - 75, main.BREEDTE, main.HOOGTE),main.kleuren[5])
    renderer.fill((offset + 69, main.HOOGTE - 60, int(hp), 47), main.kleuren[10])
    renderer.fill((offset + 688, main.HOOGTE - 65, int(stamina), 22), main.kleuren[9])
    renderer.fill((offset + 688, main.HOOGTE - 35, int(hunger), 22), main.kleuren[8])
    renderer.copy(hud, srcrect=(0, 0, 800, 75), dstrect=(offset, main.HOOGTE - 75, 800,75))
    renderer.copy(crosshair, srcrect=(0, 0, 50, 50), dstrect=((main.BREEDTE - main.CROSSHAIRGROOTTE)//2, (main.HOOGTE - main.CROSSHAIRGROOTTE)//2 , main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))
    klok = int(24 * (int(timeCycle)/main.DAGNACHTCYCLUSTIJD))
    if klok >= 12:
        klok -= 12
    renderer.copy(klokImages[klok], srcrect=(0,0,300,300), dstrect=(offset + 505, main.HOOGTE-70, 60, 60))
    #voeg rechthoek om geselecteerd item toe
    renderer.fill((offset + 200 + equiped * 75 , main.HOOGTE - 65, 5, 55), main.kleuren[1])
    renderer.fill((offset + 251 + equiped * 75 , main.HOOGTE - 65, 5, 55), main.kleuren[1])
    renderer.fill((offset + 200 + equiped * 75 , main.HOOGTE - 65, 55, 5), main.kleuren[1])
    renderer.fill((offset + 200 + equiped * 75 , main.HOOGTE - 15, 55, 5), main.kleuren[1])
    for i in range (len(equiplist)):
        if equiplist[i] != None:
            equiplist[i].render(i, renderer, offset)
            if equiplist[i].type in main.weaponList and timeToAttack > 0:
                renderer.fill((offset + 205 + i * 75, main.HOOGTE - 15, 47, int(-45 * timeToAttack)), main.kleuren[1])


def render_kolom(renderer, window, kolom, d_muur, intersectie, horizontaal, texture, r_straal, r_speler):
    d_euclidisch = d_muur
    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

    hoogte = main.MUURHOOGTE*(window.size[1]/d_muur)
    y1 = int((window.size[1]-hoogte)//2) - 100
    textuur_y = 0
    textuur_hoogte = int(texture.size[1])

    schermkolom = main.BREEDTE - 1 - kolom
    if horizontaal:
        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * texture.size[0]))
    else:
        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * texture.size[0]))

    renderer.copy(texture, srcrect=(textuur_x, textuur_y, 1, textuur_hoogte), dstrect=(schermkolom, y1, 2, int(hoogte))) #muur


def render_lucht_en_vloer(renderer, timecycle):
    renderer.fill((0, 0, main.BREEDTE, int(main.HOOGTE / 2)-100), main.kleuren[11])
    renderer.fill((0, main.HOOGTE, main.BREEDTE, int(-main.HOOGTE / 2 -100)), main.kleuren[6])


def render_StartScreen(renderer,factory,muis_pos,resources):
    afsluiten = False
    starten = False
    events=sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_MOUSEMOTION:
            muis_pos[0] += event.motion.xrel
            if muis_pos[0] < 0:
                muis_pos[0] = 0
            elif muis_pos[0] > main.BREEDTE:
                muis_pos[0] = main.BREEDTE

            muis_pos[1] += event.motion.yrel
            if muis_pos[1] < 0:
                muis_pos[1] = 0
            elif muis_pos[1] > main.HOOGTE:
                muis_pos[1] = main.HOOGTE

        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if main.BREEDTE//2 - 125 <= muis_pos[0] <= main.BREEDTE//2 + 125:
                if main.HOOGTE//2 + 25 <= muis_pos[1] <= main.HOOGTE//2 + 225:
                    afsluiten = True
                elif main.HOOGTE//2 - 275 <= muis_pos[1] <= main.HOOGTE//2 - 75:
                    starten = True



    renderer.fill((0, 0, main.BREEDTE, main.HOOGTE), main.kleuren[5])
    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                  srcrect = (0,0,50,50),
                  dstrect = (muis_pos[0] - main.CROSSHAIRGROOTTE//2, muis_pos[1] - main.CROSSHAIRGROOTTE//2,
                             main.CROSSHAIRGROOTTE,main.CROSSHAIRGROOTTE))

    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf",size = 50,color = main.kleuren[7])
    Line1_text = "start"
    Line2_text = "settings"
    Line3_text = "quit"
    StartScreen_render_Line1 = factory.from_text(Line1_text,fontmanager=ManagerFont)
    StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont)
    StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont)

    renderer.copy(StartScreen_render_Line1,dstrect=(main.BREEDTE//2 - 125,main.HOOGTE//2 - 275,250,200))
    renderer.copy(StartScreen_render_Line2, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 125, 250, 200))
    renderer.copy(StartScreen_render_Line3, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 +25, 250, 200))

    return(muis_pos, afsluiten, starten)


def render_ResumeScreen(renderer,factory,muis_pos,resources):
    afsluiten = False
    starten = False
    events=sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_MOUSEMOTION:
            muis_pos[0] += event.motion.xrel
            if muis_pos[0] < 0:
                muis_pos[0] = 0
            elif muis_pos[0] > main.BREEDTE:
                muis_pos[0] = main.BREEDTE

            muis_pos[1] += event.motion.yrel
            if muis_pos[1] < 0:
                muis_pos[1] = 0
            elif muis_pos[1] > main.HOOGTE:
                muis_pos[1] = main.HOOGTE

        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if main.BREEDTE//2 - 125 <= muis_pos[0] <= main.BREEDTE//2 + 125:
                if main.HOOGTE//2 + 25 <= muis_pos[1] <= main.HOOGTE//2 + 225:
                    afsluiten = True
                elif main.HOOGTE//2 - 275 <= muis_pos[1] <= main.HOOGTE//2 - 75:
                    starten = True



    renderer.fill((0, 0, main.BREEDTE, main.HOOGTE), main.kleuren[5])
    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                  srcrect = (0,0,50,50),
                  dstrect = (muis_pos[0] - main.CROSSHAIRGROOTTE//2, muis_pos[1] - main.CROSSHAIRGROOTTE//2,
                             main.CROSSHAIRGROOTTE,main.CROSSHAIRGROOTTE))

    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf",size = 50,color = main.kleuren[7])
    Line1_text = "resume"
    Line2_text = "settings"
    Line3_text = "quit"
    StartScreen_render_Line1 = factory.from_text(Line1_text,fontmanager=ManagerFont)
    StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont)
    StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont)

    renderer.copy(StartScreen_render_Line1,dstrect=(main.BREEDTE//2 - 125,main.HOOGTE//2 - 275,250,200))
    renderer.copy(StartScreen_render_Line2, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 125, 250, 200))
    renderer.copy(StartScreen_render_Line3, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 +25, 250, 200))

    return(muis_pos, afsluiten, starten)



def render_GameOVer(renderer, factory):
    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(255, 0, 0))
    GameOver_text = "Ge zijt dood"
    GameOver_render = factory.from_text(GameOver_text, fontmanager=ManagerFont)
    renderer.copy(GameOver_render, dstrect=(150, 200, 500, 200))
    renderer.present()


def render_FPS(delta, renderer, factory, ManagerFont):
    text_ = "FPS:" + str(np.round(1 / delta))
    text = factory.from_text(text_, fontmanager=ManagerFont)
    renderer.copy(text, dstrect=(0, 0, 50, 25))


def create_resources(renderer):

    resources = sdl2.ext.Resources(__file__, "resources")

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(255, 255, 255))

    muur = factory.from_image(resources.get_path("wall-concrete1.png"))
    muur2 = factory.from_image(resources.get_path("metal.png"))
    craftingBench = factory.from_image(resources.get_path("craftingBench.png"))
    hud = factory.from_image(resources.get_path("hud.png"))
    crosshair = factory.from_image(resources.get_path("crosshair.png"))
    dimmer = factory.from_image((resources.get_path("dimmer.png")))
    mist = factory.from_image((resources.get_path("tunnelVision.png")))
    stick = factory.from_image((resources.get_path("stick.png")))
    rock  = factory.from_image((resources.get_path("rock.png")))

    klokImages = []
    for i in range(6, 12):
        klokImages.append(factory.from_image((resources.get_path("klok" + str(i+1) + ".png"))))
    for i in range(6):
        klokImages.append(factory.from_image((resources.get_path("klok" + str(i+1) + ".png"))))

    textures = []
    textures.append(muur)
    textures.append(muur2)
    textures.append(craftingBench)

    afbeeldingen_sprites = []
    afbeeldingen_sprites.append(factory.from_image((resources.get_path("spellun-sprite.png"))))

    return(resources, factory, ManagerFont, textures, hud, crosshair, dimmer, klokImages, mist, afbeeldingen_sprites, stick, rock)

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


def render_inventory(renderer, factory, resources, muis_pos, equiplist, equiped, hp, hunger, stamina, highlighted, craftingIndex1, craftingIndex2, craftables):
    correctRecipe = None

    renderer.clear()
    renderer.fill((0, 0, main.BREEDTE, main.HOOGTE), main.kleuren[5])

    if craftingIndex1 != None and craftingIndex2 != None:
        for craftable in craftables:
            if craftable.checkTypes(equiplist[craftingIndex1], equiplist[craftingIndex2]):
                renderer.copy(craftable.image,
                              srcrect=(0, 0, craftable.image.size[0], craftable.image.size[1]),
                              dstrect=(main.BREEDTE // 2 - 40, main.HOOGTE // 2 - 40, 80, 80))

                correctRecipe = craftable
    inventory = True

    key_states = sdl2.SDL_GetKeyboardState(None)
    events = sdl2.ext.get_events()
    damage = 0
    for event in events:
        if event.type == sdl2.SDL_MOUSEMOTION:
            muis_pos[0] += event.motion.xrel
            if muis_pos[0] < 0:
                muis_pos[0] = 0
            elif muis_pos[0] > main.BREEDTE:
                muis_pos[0] = main.BREEDTE

            muis_pos[1] += event.motion.yrel
            if muis_pos[1] < 0:
                muis_pos[1] = 0
            elif muis_pos[1] > main.HOOGTE:
                muis_pos[1] = main.HOOGTE

        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if main.HOOGTE - 65 <= muis_pos[1] <= main.HOOGTE - 15:
                if 200 <= muis_pos[0] - (main.BREEDTE - 800)//2 <= 255:
                    if craftingIndex1 == 0:
                        craftingIndex1 = None
                    elif craftingIndex2 == 0:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 0
                    elif craftingIndex2 == None:
                        craftingIndex2 = 0

                elif 275 <= muis_pos[0] - (main.BREEDTE - 800)//2 <= 330:
                    if craftingIndex1 == 1:
                        craftingIndex1 = None
                    elif craftingIndex2 == 1:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 1
                    elif craftingIndex2 == None:
                        craftingIndex2 = 1

                elif 350 <= muis_pos[0] - (main.BREEDTE - 800)//2 <= 405:
                    if craftingIndex1 == 2:
                        craftingIndex1 = None
                    elif craftingIndex2 == 2:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 2
                    elif craftingIndex2 == None:
                        craftingIndex2 = 2

                elif 425 <= muis_pos[0] - (main.BREEDTE - 800)//2 <= 480:
                    if craftingIndex1 == 3:
                        craftingIndex1 = None
                    elif craftingIndex2 == 3:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 3
                    elif craftingIndex2 == None:
                        craftingIndex2 = 3

            if main.HOOGTE//2 - 50 <= muis_pos[1] <= main.HOOGTE//2 + 50:
                if main.BREEDTE//2 - 50 <= muis_pos[0] <= main.BREEDTE//2 + 50:
                    if correctRecipe != None:
                        equiplist[craftingIndex1] = correctRecipe.crafted()#equips.equip(correctRecipe.factory, correctRecipe.resources, correctRecipe.image_text, correctRecipe.damage, correctRecipe.hunger, correctRecipe.hp, correctRecipe.consumable, correctRecipe.type)
                        equiplist[craftingIndex2] = None
                        craftingIndex2 = None
                        craftingIndex1 = None

    renderer.fill(((main.BREEDTE - 800) // 2 + 69, main.HOOGTE - 60, int(hp), 47), main.kleuren[10])
    renderer.fill(((main.BREEDTE - 800) // 2 + 688, main.HOOGTE - 65, int(stamina), 22), main.kleuren[9])
    renderer.fill(((main.BREEDTE - 800) // 2 + 688, main.HOOGTE - 35, int(hunger), 22), main.kleuren[8])
    renderer.copy(factory.from_image(resources.get_path("hud.png")), srcrect=(0, 0, 800, 75), dstrect=((main.BREEDTE - 800)//2, main.HOOGTE - 75, 800, 75))
    renderer.copy(factory.from_image(resources.get_path("+.png")), srcrect=(0,0,50,50), dstrect=(main.BREEDTE//2 - 15, main.HOOGTE//2 - 165, 40,40))
    renderer.copy(factory.from_image(resources.get_path("Larrow.png")), srcrect=(0, 0, 50, 50),dstrect=(main.BREEDTE // 2 - 85, main.HOOGTE // 2 - 95, 40, 40))
    renderer.copy(factory.from_image(resources.get_path("Rarrow.png")), srcrect=(0, 0, 50, 50),dstrect=(main.BREEDTE // 2 + 48, main.HOOGTE // 2 - 95, 40, 40))
    for i in range (len(equiplist)):
        if equiplist[i] != None:
            equiplist[i].render(i, renderer, (main.BREEDTE - 800)//2 )

    if craftingIndex1 != None:
        if equiplist[craftingIndex1] != None:
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex1 * 75, main.HOOGTE - 65, 5, 55), main.kleuren[1])
            renderer.fill(((main.BREEDTE - 800) // 2 + 251 + craftingIndex1 * 75, main.HOOGTE - 65, 5, 55), main.kleuren[1])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex1 * 75, main.HOOGTE - 65, 55, 5), main.kleuren[1])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex1 * 75, main.HOOGTE - 15, 55, 5), main.kleuren[1])

    if craftingIndex2 != None:
        if equiplist[craftingIndex2] != None:
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex2 * 75, main.HOOGTE - 65, 5, 55), main.kleuren[2])
            renderer.fill(((main.BREEDTE - 800) // 2 + 251 + craftingIndex2 * 75, main.HOOGTE - 65, 5, 55), main.kleuren[2])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex2 * 75, main.HOOGTE - 65, 55, 5), main.kleuren[2])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex2 * 75, main.HOOGTE - 15, 55, 5), main.kleuren[2])


    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[1])
    renderer.fill((main.BREEDTE // 2 - 24, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[1])
    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 200, 105, 5), main.kleuren[1])
    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 100, 105, 5), main.kleuren[1])

    renderer.fill((main.BREEDTE // 2 + 25, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[2])
    renderer.fill((main.BREEDTE // 2 + 126, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[2])
    renderer.fill((main.BREEDTE // 2 + 25, main.HOOGTE // 2 - 200, 105, 5), main.kleuren[2])
    renderer.fill((main.BREEDTE // 2 + 25, main.HOOGTE // 2 - 100, 105, 5), main.kleuren[2])

    renderer.fill((main.BREEDTE // 2 - 50, main.HOOGTE // 2 - 50, 5, 105), main.kleuren[3])
    renderer.fill((main.BREEDTE // 2 + 51, main.HOOGTE // 2 - 50, 5, 105), main.kleuren[3])
    renderer.fill((main.BREEDTE // 2 - 50, main.HOOGTE // 2 - 50, 105, 5), main.kleuren[3])
    renderer.fill((main.BREEDTE // 2 - 50, main.HOOGTE // 2 + 50, 105, 5), main.kleuren[3])

    if craftingIndex1 != None:
        if equiplist[craftingIndex1] != None:
            renderer.copy(equiplist[craftingIndex1].image, srcrect=(0, 0, equiplist[craftingIndex1].b, equiplist[craftingIndex1].h), dstrect=(main.BREEDTE // 2 - 113, main.HOOGTE // 2 - 185, 80, 80))

    if craftingIndex2 != None:
        if equiplist[craftingIndex2] != None:
            renderer.copy(equiplist[craftingIndex2].image, srcrect=(0, 0, equiplist[craftingIndex2].b, equiplist[craftingIndex2].h), dstrect=(main.BREEDTE // 2 + 37, main.HOOGTE // 2 - 185, 80, 80))

    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                  srcrect=(0, 0, 50, 50),
                  dstrect=(muis_pos[0] - main.CROSSHAIRGROOTTE // 2, muis_pos[1] - main.CROSSHAIRGROOTTE // 2,
                           main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))


    if key_states[sdl2.SDL_SCANCODE_E] or key_states[sdl2.SDL_SCANCODE_ESCAPE] or key_states[sdl2.SDL_SCANCODE_TAB]:
        inventory = False
        craftingIndex1 = None
        craftingIndex2 = None





    renderer.present()
    return(muis_pos, equiplist, equiped, inventory, highlighted, craftingIndex1, craftingIndex2)