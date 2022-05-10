import math
import time
import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import main
import sprites
import equips

pausecounter = 100
craftingcounter = 100
craftingcounter2 = 0
selected = 0
started = False

selected_X = 0  # omdat ze anders elke frame terug op nul gezet worden omdat de functie telkens opnieuw wordt opgeroepen
selected_Y = 0
selected_X_sens = 1
selected_X_diff = 1
selected_X_cross = 1


def render_hud(renderer, hud, stamina, hp, hunger, crosshair, timeCycle, klokImages, equiped, equiplist, timeToAttack):
    offset = ((main.BREEDTE - 800) // 2)
    renderer.fill((0, main.HOOGTE - 75, main.BREEDTE, main.HOOGTE), main.kleuren[5])
    renderer.fill((offset + 69, main.HOOGTE - 60, int(hp), 47), main.kleuren[10])
    renderer.fill((offset + 688, main.HOOGTE - 65, int(stamina), 22), main.kleuren[9])
    renderer.fill((offset + 688, main.HOOGTE - 35, int(hunger), 22), main.kleuren[8])
    renderer.copy(hud, srcrect=(0, 0, 800, 75), dstrect=(offset, main.HOOGTE - 75, 800, 75))
    renderer.copy(crosshair, srcrect=(0, 0, 50, 50), dstrect=(
    (main.BREEDTE - main.CROSSHAIRGROOTTE) // 2, (main.HOOGTE - main.CROSSHAIRGROOTTE) // 2, main.CROSSHAIRGROOTTE,
    main.CROSSHAIRGROOTTE))
    klok = int(24 * (int(timeCycle) / main.DAGNACHTCYCLUSTIJD))
    if klok >= 12:
        klok -= 12
    renderer.copy(klokImages[klok], srcrect=(0, 0, 300, 300), dstrect=(offset + 505, main.HOOGTE - 70, 60, 60))
    # voeg rechthoek om geselecteerd item toe
    renderer.fill((offset + 200 + equiped * 75, main.HOOGTE - 65, 5, 55), main.kleuren[1])
    renderer.fill((offset + 251 + equiped * 75, main.HOOGTE - 65, 5, 55), main.kleuren[1])
    renderer.fill((offset + 200 + equiped * 75, main.HOOGTE - 65, 55, 5), main.kleuren[1])
    renderer.fill((offset + 200 + equiped * 75, main.HOOGTE - 15, 55, 5), main.kleuren[1])
    for i in range(len(equiplist)):
        if equiplist[i] != None:
            equiplist[i].render(i, renderer, offset)
            if equiplist[i].type in main.weaponList and timeToAttack > 0:
                renderer.fill((offset + 205 + i * 75, main.HOOGTE - 15, 47, int(-45 * timeToAttack)), main.kleuren[1])


def render_kolom(renderer, window, kolom, d_muur, intersectie, horizontaal, texture, r_straal, r_speler):
    d_euclidisch = d_muur
    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

    hoogte = main.MUURHOOGTE * (window.size[1] / d_muur)
    y1 = int((window.size[1] - hoogte) // 2) - 100
    textuur_y = 0
    textuur_hoogte = int(texture.size[1])

    schermkolom = main.BREEDTE - 1 - kolom
    if horizontaal:
        textuur_x = int(round((intersectie[0] - int(intersectie[0])) * texture.size[0]))
    else:
        textuur_x = int(round((intersectie[1] - int(intersectie[1])) * texture.size[0]))

    renderer.copy(texture, srcrect=(textuur_x, textuur_y, 1, textuur_hoogte),
                  dstrect=(schermkolom, y1, 2, int(hoogte)))  # muur


def render_lucht_en_vloer(renderer, timecycle):
    renderer.fill((0, 0, main.BREEDTE, int(main.HOOGTE / 2) - 100), main.kleuren[11])
    renderer.fill((0, main.HOOGTE, main.BREEDTE, int(-main.HOOGTE / 2 - 100)), main.kleuren[6])


def render_StartScreen(renderer, factory, muis_pos, resources, dramController):
    afsluiten = False
    starten = False
    settings = False
    global selected
    global pausecounter
    pausecounter += 1

    events = sdl2.ext.get_events()
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
            if main.BREEDTE // 2 - 125 <= muis_pos[0] <= main.BREEDTE // 2 + 125:
                if main.HOOGTE // 2 + 100 <= muis_pos[1] <= main.HOOGTE // 2 + 175:
                    afsluiten = True
                elif main.HOOGTE // 2 - 75 <= muis_pos[1] <= main.HOOGTE // 2 + 50:
                    settings = True
                elif main.HOOGTE // 2 - 200 <= muis_pos[1] <= main.HOOGTE // 2 - 100:
                    starten = True
    renderer.copy(factory.from_image("resources/background.jpg"),
                  dstrect=(0, 0, main.BREEDTE, main.HOOGTE))
    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                  srcrect=(0, 0, 50, 50),
                  dstrect=(muis_pos[0] - main.CROSSHAIRGROOTTE // 2, muis_pos[1] - main.CROSSHAIRGROOTTE // 2,
                           main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))

    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=main.kleuren[7])
    ManagerFont2 = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=main.kleuren[2])

    Line1_text = "start"
    Line2_text = "settings"
    Line3_text = "quit"

    if (dramController.NunChuk.joyY > 210):
        if (pausecounter > 100):
            if (selected == 0):
                selected = 2
                pausecounter = 0
            else:
                selected -= 1
                pausecounter = 0
    if (dramController.NunChuk.joyY < 60):
        if (pausecounter > 100):
            if (selected == 2):
                selected = 0
                pausecounter = 0
            else:
                selected += 1
                pausecounter = 0

    if (selected == 0):
        StartScreen_render_Line1 = factory.from_text(Line1_text, fontmanager=ManagerFont2)
        StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont)
        StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont)
    if (selected == 1):
        StartScreen_render_Line1 = factory.from_text(Line1_text, fontmanager=ManagerFont)
        StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont2)
        StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont)
    if (selected == 2):
        StartScreen_render_Line1 = factory.from_text(Line1_text, fontmanager=ManagerFont)
        StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont)
        StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont2)


    renderer.copy(StartScreen_render_Line1, dstrect=(main.BREEDTE // 2 - 150, main.HOOGTE // 2 - 275, 300, 200))
    renderer.copy(StartScreen_render_Line2, dstrect=(main.BREEDTE // 2 - 150, main.HOOGTE // 2 - 125, 300, 200))
    renderer.copy(StartScreen_render_Line3, dstrect=(main.BREEDTE // 2 - 150, main.HOOGTE // 2 + 25, 300, 200))



    if (dramController.NunChuk.buttonZ == 1 and pausecounter > 75):
        if (selected == 0):
            starten = True
            started = False
        if (selected == 1):
            settings = True
            started = False
        if (selected == 2):
            afsluiten = True
            started = False
        pausecounter = 0


    return (muis_pos, afsluiten, starten, settings)

def renderBlood(renderer, factory):
    renderer.copy(factory.from_image("resources/BloodOverlay.png"),
                  srcrect=(0, 0, 1280, 800),
                  dstrect=(0, 0, main.BREEDTE, main.HOOGTE))



def render_ResumeScreen(renderer, factory, muis_pos, resources, dramController):
    afsluiten = False
    starten = False
    settings = False
    global pausecounter
    global selected
    pausecounter += 1
    global started

    if (started == False):
        selected = 0
        started = True

    events = sdl2.ext.get_events()
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
            if main.BREEDTE // 2 - 125 <= muis_pos[0] <= main.BREEDTE // 2 + 125:
                if main.HOOGTE // 2 + 100 <= muis_pos[1] <= main.HOOGTE // 2 + 175:
                    afsluiten = True
                    started = False
                elif main.HOOGTE // 2 - 75 <= muis_pos[1] <= main.HOOGTE // 2 + 50:
                    settings = True
                    started = False
                elif main.HOOGTE // 2 - 200 <= muis_pos[1] <= main.HOOGTE // 2 - 100:
                    starten = True
                    started = False

    renderer.copy(factory.from_image("resources/background.jpg"),
                  dstrect=(0, 0, main.BREEDTE, main.HOOGTE))
    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                  srcrect=(0, 0, 50, 50),
                  dstrect=(muis_pos[0] - main.CROSSHAIRGROOTTE // 2, muis_pos[1] - main.CROSSHAIRGROOTTE // 2,
                           main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))


    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=main.kleuren[7])
    ManagerFont2 = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=main.kleuren[2])
    Line1_text = "resume"
    Line2_text = "settings"
    Line3_text = "quit"
    if (dramController.NunChuk.joyY > 210):
        if (pausecounter > 100):
            if (selected == 0):
                selected = 2
                pausecounter = 0
            else:
                selected -= 1
                pausecounter = 0
    if (dramController.NunChuk.joyY < 60):
        if (pausecounter > 100):
            if (selected == 2):
                selected = 0
                pausecounter = 0
            else:
                selected += 1
                pausecounter = 0

    if (selected == 0):
        StartScreen_render_Line1 = factory.from_text(Line1_text, fontmanager=ManagerFont2)
        StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont)
        StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont)
    if (selected == 1):
        StartScreen_render_Line1 = factory.from_text(Line1_text, fontmanager=ManagerFont)
        StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont2)
        StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont)
    if (selected == 2):
        StartScreen_render_Line1 = factory.from_text(Line1_text, fontmanager=ManagerFont)
        StartScreen_render_Line2 = factory.from_text(Line2_text, fontmanager=ManagerFont)
        StartScreen_render_Line3 = factory.from_text(Line3_text, fontmanager=ManagerFont2)

    renderer.copy(StartScreen_render_Line1, dstrect=(main.BREEDTE // 2 - 150, main.HOOGTE // 2 - 275, 300, 200))
    renderer.copy(StartScreen_render_Line2, dstrect=(main.BREEDTE // 2 - 150, main.HOOGTE // 2 - 125, 300, 200))
    renderer.copy(StartScreen_render_Line3, dstrect=(main.BREEDTE // 2 - 150, main.HOOGTE // 2 + 25, 300, 200))

    if (dramController.NunChuk.buttonZ == 1 and pausecounter > 75):
        if (selected == 0):
            starten = True
            started = False
        if (selected == 1):
            settings = True
            started = False
        if (selected == 2):
            afsluiten = True
            started = False
        pausecounter = 0

    return (muis_pos, afsluiten, starten, settings)


def render_SettingsScreen(renderer, factory, muis_pos, resources, setting, dramco, komtVanResumeScreen):
    global pausecounter
    global selected_Y
    global selected_X
    global selected_X_sens
    global selected_X_diff
    global selected_X_cross
    pausecounter += 1

    if (komtVanResumeScreen == True):
        selected_Y = 0
        komtVanResumeScreen = False

    dramco.readData()

    events = sdl2.ext.get_events()
    settings = True

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
            if main.BREEDTE // 2 - 125 <= muis_pos[0] <= main.BREEDTE // 2 + 125:
                if main.HOOGTE // 2 + 150 <= muis_pos[1] <= main.HOOGTE // 2 + 250:
                    settings = False

            if main.BREEDTE // 2 - 125 <= muis_pos[0] <= main.BREEDTE // 2 - 75:
                if main.HOOGTE // 2 + 5 <= muis_pos[1] <= main.HOOGTE // 2 + 55:
                    if main.azertybool:
                        main.azertybool = False
                        setting.azerty = False

                    else:
                        main.azertybool = True
                        setting.azerty = True

            if main.HOOGTE // 2 - 225 <= muis_pos[1] <= main.HOOGTE // 2 - 125:
                if main.BREEDTE // 2 - 125 <= muis_pos[0] <= main.BREEDTE // 2 - 25:
                    main.difficulty = "hard"
                    main.HUNGERMODIFIER = 0.75
                    main.STAMINALOSSMODIFIER = 7
                    main.STAMINAREGENMODIFIER = 2
                    main.HUNGERHPLOSSMODIFIER = 0.75
                    main.HPREPLENISHMODIFIERER = 0.3

                if main.BREEDTE // 2 <= muis_pos[0] <= main.BREEDTE // 2 + 150:
                    main.difficulty = "normal"
                    main.HUNGERMODIFIER = 0.5
                    main.STAMINALOSSMODIFIER = 5
                    main.STAMINAREGENMODIFIER = 3
                    main.HUNGERHPLOSSMODIFIER = 0.5
                    main.HPREPLENISHMODIFIERER = 0.5

                if main.BREEDTE // 2 + 175 <= muis_pos[0] <= main.BREEDTE // 2 + 275:
                    main.difficulty = "easy"
                    main.HUNGERMODIFIER = 0.25
                    main.STAMINALOSSMODIFIER = 3
                    main.STAMINAREGENMODIFIER = 4
                    main.HUNGERHPLOSSMODIFIER = 0.25
                    main.HPREPLENISHMODIFIERER = 0.7

            if main.HOOGTE // 2 - 325 <= muis_pos[1] <= main.HOOGTE // 2 - 225:
                if main.BREEDTE // 2 - 125 <= muis_pos[0] <= main.BREEDTE // 2:
                    main.SENSITIVITY = 0.01
                    main.sens = "high"
                    selected_X_sens = 0

                if main.BREEDTE // 2 + 25 <= muis_pos[0] <= main.BREEDTE // 2 + 225:
                    main.SENSITIVITY = 0.001
                    main.sens = "average"
                    selected_X_sens = 1

                if main.BREEDTE // 2 + 250 <= muis_pos[0] <= main.BREEDTE // 2 + 375:
                    main.SENSITIVITY = 0.0001
                    main.sens = "low"
                    selected_X_sens = 2

            if main.HOOGTE // 2 - 125 <= muis_pos[1] <= main.HOOGTE // 2 - 25:
                if main.BREEDTE // 2 - 125 <= muis_pos[0] <= main.BREEDTE // 2 - 50:
                    main.CROSSHAIRGROOTTE = 50
                    main.crosshair = "big"

                if main.BREEDTE // 2 - 25 <= muis_pos[0] <= main.BREEDTE // 2 + 175:
                    main.CROSSHAIRGROOTTE = 26
                    main.crosshair = "average"

                if main.BREEDTE // 2 + 200 <= muis_pos[0] <= main.BREEDTE // 2 + 325:
                    main.CROSSHAIRGROOTTE = 15
                    main.crosshair = "small"

    if (dramco.NunChuk.joyY > 210):
        if (pausecounter > 25):
            if (selected_Y == 0):
                selected_Y = 3
                pausecounter = 0
            else:
                selected_Y -= 1
                pausecounter = 0
    if (dramco.NunChuk.joyY < 60):
        if (pausecounter > 25):
            if (selected_Y == 3):
                selected_Y = 0
                pausecounter = 0
            else:
                selected_Y += 1
                pausecounter = 0


    if (dramco.NunChuk.joyX > 210):
        if (pausecounter > 25):
            if (selected_Y == 0):
                if (selected_X_sens == 2):
                    selected_X_sens = 0
                    pausecounter = 0
                else:
                    selected_X_sens += 1
                    pausecounter = 0
            if (selected_Y == 1):
                if (selected_X_diff == 2):
                    selected_X_diff = 0
                    pausecounter = 0
                else:
                    selected_X_diff += 1
                    pausecounter = 0
            if (selected_Y == 2):
                if (selected_X_cross == 2):
                    selected_X_cross = 0
                    pausecounter = 0
                else:
                    selected_X_cross += 1
                    pausecounter = 0

    if (dramco.NunChuk.joyX < 60):
        if (pausecounter > 25):
            if (selected_Y == 0):
                if (selected_X_sens == 0):
                    selected_X_sens = 2
                    pausecounter = 0
                else:
                    selected_X_sens -= 1
                    pausecounter = 0
            if (selected_Y == 1):
                if (selected_X_diff == 0):
                    selected_X_diff = 2
                    pausecounter = 0
                else:
                    selected_X_diff -= 1
                    pausecounter = 0
            if (selected_Y == 2):
                if (selected_X_cross == 0):
                    selected_X_cross = 2
                    pausecounter = 0
                else:
                    selected_X_cross -= 1
                    pausecounter = 0


    if (selected_Y == 0):
        if (selected_X_sens == 0):
            main.SENSITIVITY = 0.01
            main.sens = "high"
        if (selected_X_sens == 1):
            main.SENSITIVITY = 0.001
            main.sens = "average"
        if (selected_X_sens == 2):
            main.SENSITIVITY = 0.0001
            main.sens = "low"

    if (selected_Y == 1):
        if (selected_X_diff == 0):
            main.difficulty = "hard"
            main.HUNGERMODIFIER = 0.75
            main.STAMINALOSSMODIFIER = 7
            main.STAMINAREGENMODIFIER = 2
            main.HUNGERHPLOSSMODIFIER = 0.75
            main.HPREPLENISHMODIFIERER = 0.3
        if (selected_X_diff == 1):
            main.difficulty = "normal"
            main.HUNGERMODIFIER = 0.5
            main.STAMINALOSSMODIFIER = 5
            main.STAMINAREGENMODIFIER = 3
            main.HUNGERHPLOSSMODIFIER = 0.5
            main.HPREPLENISHMODIFIERER = 0.5
        if (selected_X_diff == 2):
            main.difficulty = "easy"
            main.HUNGERMODIFIER = 0.25
            main.STAMINALOSSMODIFIER = 3
            main.STAMINAREGENMODIFIER = 4
            main.HUNGERHPLOSSMODIFIER = 0.25
            main.HPREPLENISHMODIFIERER = 0.7

    if (selected_Y == 2):
        if (selected_X_cross == 0):
            main.CROSSHAIRGROOTTE = 50
            main.crosshair = "big"
        if (selected_X_cross == 1):
            main.CROSSHAIRGROOTTE = 26
            main.crosshair = "average"
        if (selected_X_cross == 2):
            main.CROSSHAIRGROOTTE = 15
            main.crosshair = "small"
    if (selected_Y == 3):
        if (dramco.NunChuk.buttonZ == 1):
            settings = False
            pausecounter = 0

    renderer.copy(factory.from_image("resources/background.jpg"),
                  dstrect=(0, 0, main.BREEDTE, main.HOOGTE))

    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=main.kleuren[7])
    ManagerFontGreen = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=main.kleuren[2])
    ManagerFontBlue = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=main.kleuren[1])
    Sensitivity_text = "sensitivity:"
    Difficulty_text = "difficulty:"
    Crosshair_text = "crosshair:"
    Azerty_text = "azerty:"
    Hard_text = "hard"
    Normal_text = "normal"
    Easy_text = "easy"
    High_text = "high"
    Average_text = "average"
    Low_text = "low"
    Big_text = "big"
    AverageCrosshair_text = "average"
    Small_text = "small"
    Back = "back"


    render_Azerty = factory.from_text(Azerty_text, fontmanager=ManagerFont)
    if (selected_Y == 0):
        render_Sensitivity = factory.from_text(Sensitivity_text, fontmanager=ManagerFontBlue)
        render_Difficulty = factory.from_text(Difficulty_text, fontmanager=ManagerFont)
        render_Crosshair = factory.from_text(Crosshair_text, fontmanager=ManagerFont)
        render_Back = factory.from_text(Back, fontmanager=ManagerFont)
    elif (selected_Y == 1):
        render_Sensitivity = factory.from_text(Sensitivity_text, fontmanager=ManagerFont)
        render_Difficulty = factory.from_text(Difficulty_text, fontmanager=ManagerFontBlue)
        render_Crosshair = factory.from_text(Crosshair_text, fontmanager=ManagerFont)
        render_Back = factory.from_text(Back, fontmanager=ManagerFont)
    elif (selected_Y == 2):
        render_Sensitivity = factory.from_text(Sensitivity_text, fontmanager=ManagerFont)
        render_Difficulty = factory.from_text(Difficulty_text, fontmanager=ManagerFont)
        render_Crosshair = factory.from_text(Crosshair_text, fontmanager=ManagerFontBlue)
        render_Back = factory.from_text(Back, fontmanager=ManagerFont)
    elif (selected_Y == 3):
        render_Sensitivity = factory.from_text(Sensitivity_text, fontmanager=ManagerFont)
        render_Difficulty = factory.from_text(Difficulty_text, fontmanager=ManagerFont)
        render_Crosshair = factory.from_text(Crosshair_text, fontmanager=ManagerFont)
        render_Back = factory.from_text(Back, fontmanager=ManagerFontBlue)


    if main.difficulty == "hard":
        render_Hard = factory.from_text(Hard_text, fontmanager=ManagerFontGreen)
    else:
        render_Hard = factory.from_text(Hard_text, fontmanager=ManagerFont)
    if main.difficulty == "normal":
        render_Normal = factory.from_text(Normal_text, fontmanager=ManagerFontGreen)
    else:
        render_Normal = factory.from_text(Normal_text, fontmanager=ManagerFont)
    if main.difficulty == "easy":
        render_Easy = factory.from_text(Easy_text, fontmanager=ManagerFontGreen)
    else:
        render_Easy = factory.from_text(Easy_text, fontmanager=ManagerFont)


    if main.sens == "high":
        render_High = factory.from_text(High_text, fontmanager=ManagerFontGreen)
    else:
        render_High = factory.from_text(High_text, fontmanager=ManagerFont)
    if main.sens == "average":
        render_Average = factory.from_text(Average_text, fontmanager=ManagerFontGreen)
    else:
        render_Average = factory.from_text(Average_text, fontmanager=ManagerFont)
    if main.sens == "low":
        render_Low = factory.from_text(Low_text, fontmanager=ManagerFontGreen)
    else:
        render_Low = factory.from_text(Low_text, fontmanager=ManagerFont)


    if main.crosshair == "big":
        render_Big = factory.from_text(Big_text, fontmanager=ManagerFontGreen)
    else:
        render_Big = factory.from_text(Big_text, fontmanager=ManagerFont)
    if main.crosshair == "average":
        render_AverageCrosshair = factory.from_text(AverageCrosshair_text, fontmanager=ManagerFontGreen)
    else:
        render_AverageCrosshair = factory.from_text(AverageCrosshair_text, fontmanager=ManagerFont)
    if main.crosshair == "small":
        render_Small = factory.from_text(Small_text, fontmanager=ManagerFontGreen)
    else:
        render_Small = factory.from_text(Small_text, fontmanager=ManagerFont)


    renderer.copy(render_Sensitivity, dstrect=(main.BREEDTE // 2 - 400, main.HOOGTE // 2 - 325, 250, 100))
    renderer.copy(render_High, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 325, 125, 100))
    renderer.copy(render_Average, dstrect=(main.BREEDTE // 2 + 25, main.HOOGTE // 2 - 325, 200, 100))
    renderer.copy(render_Low, dstrect=(main.BREEDTE // 2 + 250, main.HOOGTE // 2 - 325, 75, 100))

    renderer.copy(render_Crosshair, dstrect=(main.BREEDTE // 2 - 400, main.HOOGTE // 2 - 125, 250, 100))
    renderer.copy(render_Big, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 125, 75, 100))
    renderer.copy(render_AverageCrosshair, dstrect=(main.BREEDTE // 2 - 25, main.HOOGTE // 2 - 125, 200, 100))
    renderer.copy(render_Small, dstrect=(main.BREEDTE // 2 + 200, main.HOOGTE // 2 - 125, 125, 100))

    renderer.copy(render_Difficulty, dstrect=(main.BREEDTE // 2 - 400, main.HOOGTE // 2 - 225, 250, 100))
    renderer.copy(render_Hard, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 225, 100, 100))
    renderer.copy(render_Normal, dstrect=(main.BREEDTE // 2, main.HOOGTE // 2 - 225, 150, 100))
    renderer.copy(render_Easy, dstrect=(main.BREEDTE // 2 + 175, main.HOOGTE // 2 - 225, 100, 100))

    renderer.copy(render_Azerty, dstrect=(main.BREEDTE // 2 - 400, main.HOOGTE // 2 - 25, 250, 100))

    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 + 5, 5, 55), main.kleuren[7])
    renderer.fill((main.BREEDTE // 2 - 75, main.HOOGTE // 2 + 5, 5, 55), main.kleuren[7])
    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 + 5, 55, 5), main.kleuren[7])
    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 + 55, 55, 5), main.kleuren[7])
    if main.azertybool:
        renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 + 5, 55, 55), main.kleuren[6])

    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                  srcrect=(0, 0, 50, 50),
                  dstrect=(muis_pos[0] - main.CROSSHAIRGROOTTE // 2, muis_pos[1] - main.CROSSHAIRGROOTTE // 2,
                           main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))

    renderer.copy(render_Back, dstrect=(main.BREEDTE // 2 - 125, main.HOOGTE // 2 + 100, 250, 200))


    return (settings, komtVanResumeScreen)




def render_GameOVer(renderer, factory,dramco):
    dramco.vibrator = 0
    dramco.readData()
    dramco.sendData()
    renderer.copy(factory.from_image("resources/background.jpg"),
                  dstrect=(0, 0, main.BREEDTE, main.HOOGTE))
    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(255, 0, 0))
    GameOver_text = "Game Over"
    GameOver_render = factory.from_text(GameOver_text, fontmanager=ManagerFont)
    renderer.copy(GameOver_render, dstrect=(main.BREEDTE//2 - 250, main.HOOGTE//2 -100, 500, 200))

    renderer.present()

def WinningScreen(renderer,factory):
    renderer.copy(factory.from_image("resources/background.jpg"),
                  dstrect=(0, 0, main.BREEDTE, main.HOOGTE))
    ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(255, 0, 0))
    Winning_text = "You have found a way out of the maze!"
    Winning_render = factory.from_text(Winning_text, fontmanager=ManagerFont)
    renderer.copy(Winning_render, dstrect=(main.BREEDTE // 2 - 400, main.HOOGTE // 2 - 100, 800, 100))
    renderer.copy(factory.from_text("Congratulations!", fontmanager=ManagerFont),
                  dstrect=(main.BREEDTE // 2 - 250, main.HOOGTE // 2, 500, 100))
    renderer.present()

def render_FPS(delta, renderer, factory, ManagerFont):
    text_ = "FPS:" + str(int(np.round(1 /- delta)))
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
    rock = factory.from_image((resources.get_path("rock.png")))

    klokImages = []
    for i in range(6, 12):
        klokImages.append(factory.from_image((resources.get_path("klok" + str(i + 1) + ".png"))))
    for i in range(6):
        klokImages.append(factory.from_image((resources.get_path("klok" + str(i + 1) + ".png"))))

    textures = []
    textures.append(muur)
    textures.append(muur2)
    textures.append(craftingBench)

    afbeeldingen_sprites = []
    afbeeldingen_sprites.append(factory.from_image((resources.get_path("spellun-sprite.png"))))

    return (
    resources, factory, ManagerFont, textures, hud, crosshair, dimmer, klokImages, mist, afbeeldingen_sprites, stick,
    rock)


def dim_image(renderer, dimmer, timeCycle):
    if (main.DAGNACHTCYCLUSTIJD // 2) + 5 <= timeCycle <= ((main.DAGNACHTCYCLUSTIJD // 2) + 10):  # avond maken
        for i in range(int(timeCycle * 10 - ((
                                                     main.DAGNACHTCYCLUSTIJD // 2) + 5) * 10)):  # afhankelijk van timeCyclus bepaalde hoeveelheid dimmers toevoegen om langzaam donker te worden, term achter minteken is om offset te maken
            renderer.copy(dimmer, srcrect=(0, 0, 1, 1), dstrect=(0, 0, main.BREEDTE, main.HOOGTE))

    elif timeCycle > ((main.DAGNACHTCYCLUSTIJD // 2) + 10):  # nacht
        for i in range(50):
            renderer.copy(dimmer, srcrect=(0, 0, 1, 1), dstrect=(0, 0, main.BREEDTE, main.HOOGTE))

    elif timeCycle <= 5:  # ochtend maken
        for i in range(int(50 - 10 * timeCycle)):
            renderer.copy(dimmer, srcrect=(0, 0, 1, 1), dstrect=(0, 0, main.BREEDTE, main.HOOGTE))


def render_inventory(renderer, factory, resources, muis_pos, equiplist, equiped, hp, hunger, stamina, highlighted,
                     craftingIndex1, craftingIndex2, craftables, dramco):
    correctRecipe = None
    global craftingcounter
    global craftingcounter2
    craftingcounter += 1
    craftingcounter2 += 1
    offset = ((main.BREEDTE - 800) // 2)
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
                if 200 <= muis_pos[0] - (main.BREEDTE - 800) // 2 <= 255:
                    if craftingIndex1 == 0:
                        craftingIndex1 = None
                    elif craftingIndex2 == 0:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 0
                    elif craftingIndex2 == None:
                        craftingIndex2 = 0

                elif 275 <= muis_pos[0] - (main.BREEDTE - 800) // 2 <= 330:
                    if craftingIndex1 == 1:
                        craftingIndex1 = None
                    elif craftingIndex2 == 1:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 1
                    elif craftingIndex2 == None:
                        craftingIndex2 = 1

                elif 350 <= muis_pos[0] - (main.BREEDTE - 800) // 2 <= 405:
                    if craftingIndex1 == 2:
                        craftingIndex1 = None
                    elif craftingIndex2 == 2:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 2
                    elif craftingIndex2 == None:
                        craftingIndex2 = 2

                elif 425 <= muis_pos[0] - (main.BREEDTE - 800) // 2 <= 480:
                    if craftingIndex1 == 3:
                        craftingIndex1 = None
                    elif craftingIndex2 == 3:
                        craftingIndex2 = None
                    elif craftingIndex1 == None:
                        craftingIndex1 = 3
                    elif craftingIndex2 == None:
                        craftingIndex2 = 3

            if main.HOOGTE // 2 - 50 <= muis_pos[1] <= main.HOOGTE // 2 + 50:
                if main.BREEDTE // 2 - 50 <= muis_pos[0] <= main.BREEDTE // 2 + 50:
                    if correctRecipe != None:
                        equiplist[
                            craftingIndex1] = correctRecipe.crafted()  # equips.equip(correctRecipe.factory, correctRecipe.resources, correctRecipe.image_text, correctRecipe.damage, correctRecipe.hunger, correctRecipe.hp, correctRecipe.consumable, correctRecipe.type)
                        equiplist[craftingIndex2] = None
                        craftingIndex2 = None
                        craftingIndex1 = None
    if (craftingcounter2 >= 100):
        if (dramco.buttonRed):
            if correctRecipe != None:
                equiplist[
                    craftingIndex1] = correctRecipe.crafted()  # equips.equip(correctRecipe.factory, correctRecipe.resources, correctRecipe.image_text, correctRecipe.damage, correctRecipe.hunger, correctRecipe.hp, correctRecipe.consumable, correctRecipe.type)
                equiplist[craftingIndex2] = None
                craftingIndex2 = None
                craftingIndex1 = None
        if (dramco.NunChuk.buttonZ == 1):
            craftingcounter2 = 0
            if (equiped == 0):
                if craftingIndex1 == 0:
                    craftingIndex1 = None
                elif craftingIndex2 == 0:
                    craftingIndex2 = None
                elif craftingIndex1 == None:
                    craftingIndex1 = 0
                elif craftingIndex2 == None:
                    craftingIndex2 = 0
            elif (equiped == 1):
                if craftingIndex1 == 1:
                    craftingIndex1 = None
                elif craftingIndex2 == 1:
                    craftingIndex2 = None
                elif craftingIndex1 == None:
                    craftingIndex1 = 1
                elif craftingIndex2 == None:
                    craftingIndex2 = 1
            elif (equiped == 2):
                if craftingIndex1 == 2:
                    craftingIndex1 = None
                elif craftingIndex2 == 2:
                    craftingIndex2 = None
                elif craftingIndex1 == None:
                    craftingIndex1 = 2
                elif craftingIndex2 == None:
                    craftingIndex2 = 2
            elif (equiped == 3):
                if craftingIndex1 == 3:
                    craftingIndex1 = None
                elif craftingIndex2 == 3:
                    craftingIndex2 = None
                elif craftingIndex1 == None:
                    craftingIndex1 = 3
                elif craftingIndex2 == None:
                    craftingIndex2 = 3
    if (craftingcounter > 100):
        if (dramco.buttonBlue == 1):
            if (equiped == 3):
                equiped = 0
            else:
                equiped += 1
            craftingcounter = 0
        if (dramco.buttonGreen == 1):
            if (equiped == 0):
                equiped = 3
            else:
                equiped -= 1
            craftingcounter = 0

    renderer.fill(((main.BREEDTE - 800) // 2 + 69, main.HOOGTE - 60, int(hp), 47), main.kleuren[10])
    renderer.fill(((main.BREEDTE - 800) // 2 + 688, main.HOOGTE - 65, int(stamina), 22), main.kleuren[9])
    renderer.fill(((main.BREEDTE - 800) // 2 + 688, main.HOOGTE - 35, int(hunger), 22), main.kleuren[8])
    renderer.copy(factory.from_image(resources.get_path("hud.png")), srcrect=(0, 0, 800, 75),
                  dstrect=((main.BREEDTE - 800) // 2, main.HOOGTE - 75, 800, 75))
    renderer.copy(factory.from_image(resources.get_path("+.png")), srcrect=(0, 0, 50, 50),
                  dstrect=(main.BREEDTE // 2 - 15, main.HOOGTE // 2 - 165, 40, 40))
    renderer.copy(factory.from_image(resources.get_path("Larrow.png")), srcrect=(0, 0, 50, 50),
                  dstrect=(main.BREEDTE // 2 - 85, main.HOOGTE // 2 - 95, 40, 40))
    renderer.copy(factory.from_image(resources.get_path("Rarrow.png")), srcrect=(0, 0, 50, 50),
                  dstrect=(main.BREEDTE // 2 + 48, main.HOOGTE // 2 - 95, 40, 40))

    renderer.fill((offset + 200 + equiped * 75, main.HOOGTE - 65, 5, 55), main.kleuren[1])
    renderer.fill((offset + 251 + equiped * 75, main.HOOGTE - 65, 5, 55), main.kleuren[1])
    renderer.fill((offset + 200 + equiped * 75, main.HOOGTE - 65, 55, 5), main.kleuren[1])
    renderer.fill((offset + 200 + equiped * 75, main.HOOGTE - 15, 55, 5), main.kleuren[1])
    for i in range(len(equiplist)):
        if equiplist[i] != None:
            equiplist[i].render(i, renderer, (main.BREEDTE - 800) // 2)

    if craftingIndex1 != None:
        if equiplist[craftingIndex1] != None:
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex1 * 75, main.HOOGTE - 65, 5, 55),
                          main.kleuren[3])
            renderer.fill(((main.BREEDTE - 800) // 2 + 251 + craftingIndex1 * 75, main.HOOGTE - 65, 5, 55),
                          main.kleuren[3])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex1 * 75, main.HOOGTE - 65, 55, 5),
                          main.kleuren[3])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex1 * 75, main.HOOGTE - 15, 55, 5),
                          main.kleuren[3])

    if craftingIndex2 != None:
        if equiplist[craftingIndex2] != None:
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex2 * 75, main.HOOGTE - 65, 5, 55),
                          main.kleuren[2])
            renderer.fill(((main.BREEDTE - 800) // 2 + 251 + craftingIndex2 * 75, main.HOOGTE - 65, 5, 55),
                          main.kleuren[2])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex2 * 75, main.HOOGTE - 65, 55, 5),
                          main.kleuren[2])
            renderer.fill(((main.BREEDTE - 800) // 2 + 200 + craftingIndex2 * 75, main.HOOGTE - 15, 55, 5),
                          main.kleuren[2])

    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[3])
    renderer.fill((main.BREEDTE // 2 - 24, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[3])
    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 200, 105, 5), main.kleuren[3])
    renderer.fill((main.BREEDTE // 2 - 125, main.HOOGTE // 2 - 100, 105, 5), main.kleuren[3])

    renderer.fill((main.BREEDTE // 2 + 25, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[2])
    renderer.fill((main.BREEDTE // 2 + 126, main.HOOGTE // 2 - 200, 5, 105), main.kleuren[2])
    renderer.fill((main.BREEDTE // 2 + 25, main.HOOGTE // 2 - 200, 105, 5), main.kleuren[2])
    renderer.fill((main.BREEDTE // 2 + 25, main.HOOGTE // 2 - 100, 105, 5), main.kleuren[2])

    renderer.fill((main.BREEDTE // 2 - 50, main.HOOGTE // 2 - 50, 5, 105), main.kleuren[1])
    renderer.fill((main.BREEDTE // 2 + 51, main.HOOGTE // 2 - 50, 5, 105), main.kleuren[1])
    renderer.fill((main.BREEDTE // 2 - 50, main.HOOGTE // 2 - 50, 105, 5), main.kleuren[1])
    renderer.fill((main.BREEDTE // 2 - 50, main.HOOGTE // 2 + 50, 105, 5), main.kleuren[1])

    if craftingIndex1 != None:
        if equiplist[craftingIndex1] != None:
            renderer.copy(equiplist[craftingIndex1].image,
                          srcrect=(0, 0, equiplist[craftingIndex1].b, equiplist[craftingIndex1].h),
                          dstrect=(main.BREEDTE // 2 - 113, main.HOOGTE // 2 - 185, 80, 80))

    if craftingIndex2 != None:
        if equiplist[craftingIndex2] != None:
            renderer.copy(equiplist[craftingIndex2].image,
                          srcrect=(0, 0, equiplist[craftingIndex2].b, equiplist[craftingIndex2].h),
                          dstrect=(main.BREEDTE // 2 + 37, main.HOOGTE // 2 - 185, 80, 80))

    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                  srcrect=(0, 0, 50, 50),
                  dstrect=(muis_pos[0] - main.CROSSHAIRGROOTTE // 2, muis_pos[1] - main.CROSSHAIRGROOTTE // 2,
                           main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))

    if (dramco.NunChuk.buttonC == 1):
        inventory = False
        craftingIndex1 = None
        craftingIndex2 = None

    elif key_states[sdl2.SDL_SCANCODE_E] or key_states[sdl2.SDL_SCANCODE_ESCAPE] or key_states[sdl2.SDL_SCANCODE_TAB]:
        inventory = False
        craftingIndex1 = None
        craftingIndex2 = None

    renderer.present()
    return (muis_pos, equiplist, equiped, inventory, highlighted, craftingIndex1, craftingIndex2)