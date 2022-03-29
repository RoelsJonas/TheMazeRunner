import math
import time
import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import playsound
import sys
import settings
import rendering
import raycast
import movement
import sprites
import winsound
import imageToMap
import equips
import text
import crafting as crafts
import dramcontroller
import pp
import multiprocessing as mp
import ParallelWrapper
#begin waarden instellen
hp = 100
stamina = 100
hunger = 100

weaponList = ["STICK", "SPEAR"]

spawnLocations = [(139.5, 109.5),
                  (157.5, 115.5),
                  (135.5, 125.0),
                  (133.0, 132.0),
                  (157.0, 118.0),
                  (180.0, 127.5),
                  (178.0, 148.0),
                  (138.5, 149.5),
                  (154.0, 171.0),
                  (128.5, 179.0),
                  (145.0, 192.5),
                  (177.0, 193.0),
                  (177.0, 167.0),
                  (169.0, 161.0),
                  (192.5, 192.5),
                  ]

HUNGERMODIFIER = 0.15 #snelheid waarmee hunger daalt
SPRINTINGHUNGERMODIFIER = 0.1 #snelheid waarmee hunger extra daal tijdens het sprinten
STAMINALOSSMODIFIER = 5 #snelheid waarmee stamina verloren gaat tijdens sprinten
STAMINAREGENMODIFIER = 3 #snelheid waarmee stamina regenereert
HUNGERHPLOSSMODIFIER = 0.5 #snelheid waarmee hp verloren gaat wanneer hunger = 0
CROSSHAIRGROOTTE = 26
SENSITIVITY = 0.001
INTERACTIONDISTANCE = 1.2
HPREPLENISHMODIFIERER = 0,2

CONSUMESOUND = "consumable.wav"
GAMEOVERSOUND = "GameOverSound.wav"
GATESOUND = "GateSound.wav"



DAGNACHTCYCLUSTIJD = 360 # aantal seconden dat 1 dag nacht cyclus duurt
KLOKINTERVAL = DAGNACHTCYCLUSTIJD / 24     # om te weten om de hoeveel tijd de klok een uur moet opschuiven

MUURHOOGTE = 1.5

# Constanten
BREEDTE = 800
HOOGTE = 600
SPEED = 1.5
SPRINT_SPEED = 2.25

# Globale variabelen

# positie van de speler
p_speler = np.array([510 + 1 / math.sqrt(2), 512 - 1 / math.sqrt(2)])
#p_speler = np.array([5,0.75])

# richting waarin de speler kijkt
r_speler = np.array([1 / math.sqrt(2), -1 / math.sqrt(2)])

# cameravlak
r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])

D_CAMERA = 1/np.tan(np.deg2rad(90)/2)

# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False
start = False
settingsbool = False
azertybool = False
difficulty = "normal"
crosshair = "average"
sens = "average"
# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn

#(world_map, doorLocations, door_map) = imageToMap.generateWorld("resources\map6.png")

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
my_file_code = open("codeList.txt", "r")
code_content = my_file_code.read()
codeList = code_content.split(",")
my_file_code.close

my_file = open("instructionsList.txt", "r")
instructionsList = my_file.readlines()
my_file.close



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
    global start
    global settingsbool
    global azertybool
    global difficulty
    global crosshair
    global sens

    job_server = pp.Server()
    pool = mp.Pool(mp.cpu_count())

    muis_pos = np.array([BREEDTE//2, HOOGTE//2])

    dramController = dramcontroller.DramController()

    # Maak een venster aan om de game te renderen
    window = sdl2.ext.Window("The Maze Runner", size=(BREEDTE, HOOGTE))
    window.show()

    #creer settingsobjectdingetje
    setting = settings.setting(True)

    # Begin met het uitlezen van input van de muis en vraag om relatieve coordinaten
    sdl2.SDL_SetRelativeMouseMode(True)

    # Maak een renderer aan zodat we in ons venster kunnen renderen
    renderer = sdl2.ext.Renderer(window)

    data = ParallelWrapper.ObjectWrapper(renderer, window)

    tekstList = []
    beginText = text.text("Who am I? What am I doing here?!?", BREEDTE//2 - 350, 450, 700, 50)
    consumableText = text.text("Hmm, that's good stuff!", BREEDTE//2 - 200, 450, 400, 50)
    slaapText = text.text("Catching some Z's", BREEDTE//2 - 200, 450, 400, 50)
    completionText = text.text("Congratulations! You have found a way out!", BREEDTE//2 - 350, 450, 700, 60)
    (resources, factory, ManagerFont, textures, hud, crosshair, dimmer, klokImages, mist, afbeeldingen_sprites, stick, rock) = rendering.create_resources(renderer)
    while not start:
        while not settingsbool:
            dramController.readData()
            (muis_pos,afsluiten,start,settingsbool) = rendering.render_StartScreen(renderer, factory, muis_pos, resources, dramController)
            renderer.present()
            if afsluiten:
                sdl2.ext.quit()
                moet_afsluiten = True
                sys.exit()
                break
            if start:
                break
        if start:
            break

        settingsbool = rendering.render_SettingsScreen(renderer,factory,muis_pos,resources,setting)
        renderer.present()

    (world_map, doorLocations, door_map, wall_map, spriteList) = imageToMap.generateWorld("resources\map10.png", factory, resources, textures, renderer, ManagerFont)

    p_speler = np.array([151.5, 137.5])

    delta = 1
    geklikt = False
    timeToAttack = 0
    interact = False
    pakOp = False
    drop = False
    equiped = 1
    muis_pos = np.array([BREEDTE//2, HOOGTE//2])
    craftingIndex1 = None
    craftingIndex2 = None
    beginText.textTimer = 10


    start_time = time.time()                    #wanneer oppakbare sprite wordt opgepakt gaat hij uit de spritelist en in de equiplist
    equiplist = [
                 equips.equip(factory, resources, "burger.png", 0, 25, 0, True, "BURGER"),
                 equips.equip(factory, resources, "medkit.png", 0, 0, 10, True, "H1"), None, None]

    craftables = [crafts.Craftable(renderer, factory, resources, "medkit2.png", "H1", "H1", "H2", 0, 25, 0), #medkit upgrade van level 1 naar level 2 (10 ==> 25 hp regen)
                  crafts.Craftable(renderer, factory, resources, "medkit3.png", "H2", "H2", "H3", 0, 60, 0), #medkit upgrade van level 2 naar level 3 ( 25 ==> 60 hp regen)
                  crafts.Craftable(renderer, factory, resources, "spear.png", "STICK", "ROCK", "SPEAR", 17, 0, 0), #combinatie van stick en rock wordt speer (damage van 10 ==> 17) (van 5 maal slaan naar 3 maal slaan voor monster te vermoorden)
                  ]
    timeCycle = 170
    winsound.PlaySound('muziek.wav', winsound.SND_ASYNC | winsound.SND_LOOP)

    spriteList.append(sprites.Sprite(151.2, 137.2, 1, 1, "bonfire.png", 0.5, 0.5, 1, False, False, False, False, 0, 0, 0, resources, factory, slaapText))

    spriteListNacht = []
    #spriteListNacht.append(sprites.Sprite(510.1, 510.1, 1, 0, "spellun-sprite.png", 4.0, 1.2, 1, True, False, False, False, 0, 50, 10, resources, factory, None))
    for location in spawnLocations:
        if difficulty == "hard":
            spriteListNacht.append(
                sprites.Sprite(location[0], location[1], 1, 0, "spellun-sprite.png", 8.4, 2.4, 1, True, False, False,
                               False, 0, 50, 7, resources, factory, None))
        elif difficulty == "normal":
            spriteListNacht.append(
                sprites.Sprite(location[0], location[1], 1, 0, "spellun-sprite.png", 8.4, 2.4, 1, True, False, False,
                               False, 0, 50, 5, resources, factory, None))
        elif difficulty == 'easy':
            spriteListNacht.append(
                sprites.Sprite(location[0], location[1], 1, 0, "spellun-sprite.png", 8.4, 2.4, 1, True, False, False,
                               False, 0, 50, 3, resources, factory, None))


    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    renderer.clear()
    while not moet_afsluiten:
        #frameStartTime = time.time()

        while not start:
            while not settingsbool:
                dramController.readData()
                (muis_pos, afsluiten, start,settingsbool) = rendering.render_ResumeScreen(renderer, factory, muis_pos, resources,dramController)
                renderer.present()
                start_time = time.time()
                if afsluiten:
                    sdl2.ext.quit()
                    moet_afsluiten = True
                    sys.exit()
                    break
                if start:
                    break
            if start:
                break
            settingsbool = rendering.render_SettingsScreen(renderer, factory, muis_pos, resources,setting)
            renderer.present()

        #maak lege z buffer aan:
        z_buffer = np.zeros(BREEDTE, float)


        rendering.render_lucht_en_vloer(renderer, timeCycle)
        # Render de huidige frame

        #z_buffer[BREEDTE - 1 - kolom] = [pool.apply(raycast.parallel_raycast, args=(r_speler, r_cameravlak, kolom, p_speler, renderer, window, textures, timeCycle, z_buffer, door_map, world_map, delta, wall_map)) for kolom in range(800)]
        #[pool.apply(raycast.parallel_test, args=(number, dramController, z_buffer, data)) for number in range(800)]
        for kolom in range(0, window.size[0]):
            #z_buffer[BREEDTE - 1 - kolom] = raycast.parallel_raycast(r_speler, r_cameravlak, kolom, p_speler, renderer, window, textures, timeCycle, z_buffer, door_map, world_map, delta, wall_map)
            
            r_straal = raycast.bereken_r_straal(r_speler,r_cameravlak, kolom)
            
            (d_muur, intersectie, horizontaal, z_buffer, door_map, texture) = raycast.raycast(p_speler, r_straal, renderer, window, kolom, textures, r_speler, timeCycle, z_buffer, door_map, world_map, delta, wall_map)
            #print("raycast tijd", (time.time() - kolomStart)*1000)
            if z_buffer[BREEDTE - 1 - kolom] == 0 or z_buffer[BREEDTE - 1 - kolom] > d_muur:
                z_buffer[BREEDTE - 1 - kolom] = d_muur
                rendering.render_kolom(renderer, window, kolom, d_muur, intersectie, horizontaal, texture, r_straal, r_speler)
        # Verwissel de rendering context met de frame buffer=

        end_time = time.time()
        delta = end_time - start_time
        start_time = time.time()
        spriteList = sprites.sortSprites(spriteList, p_speler)
        spriteListNacht = sprites.sortSprites(spriteListNacht, p_speler)

        if (int(p_speler[1]), int(p_speler[0])) in doorLocations:
            if door_map[int(p_speler[1]), int(p_speler[0])].state == 1:
                hp = -1

        for i in range(len(doorLocations)):
            if world_map[doorLocations[i][0], doorLocations[i][1]] == 3:
                door_map[doorLocations[i][0], doorLocations[i][1]].interact(renderer, factory, resources, pakOp, p_speler, equiplist, equiped, setting, dramController)
                door_map[doorLocations[i][0], doorLocations[i][1]].updateState(delta)

        for sprite in spriteList:
            if sprite.d_speler <= 10:
                sprite.render(renderer, r_speler, r_cameravlak, p_speler, z_buffer)
            if(dramController.MIC < 200):
                sprite.moveToPlayer(p_speler, delta, world_map)
            (hunger, hp, destroy, equiplist, timeCycle) = sprite.checkInteractie(hunger, hp, p_speler, delta, geklikt or dramController.detectMotion(), timeToAttack, pakOp, equiplist, equiped, factory, timeCycle, resources, renderer)
            if destroy:
                spriteList.remove(sprite)


        if timeCycle > (DAGNACHTCYCLUSTIJD//2) + 10:
            if sprite.d_speler <= 10:
                for sprite in spriteListNacht:
                    sprite.render(renderer, r_speler, r_cameravlak, p_speler, z_buffer)
                    if(dramController.MIC < 200):
                        sprite.moveToPlayer(p_speler, delta, world_map)
                (hunger, hp, destroy, equiplist, timeCycle) = sprite.checkInteractie(hunger, hp, p_speler, delta, geklikt or dramController.detectMotion(), timeToAttack, pakOp, equiplist, equiped, factory, timeCycle, resources, renderer)
                if destroy or timeCycle == 0:
                    spriteListNacht.remove(sprite)

        if (geklikt or dramController.detectMotion()) and timeToAttack < 0 and equiplist[equiped] != None and equiplist[equiped].type in weaponList:
            timeToAttack = 1

        timeToAttack -= delta

        (hunger, hp, consumableText, equiplist[equiped]) = equips.interactions(hunger, hp,  equiplist[equiped], interact, consumableText, p_speler, renderer, world_map, factory)

        dramController.readData()
        dramController.mapStamina(stamina)
        dramController.mapHealth(hp)
        dramController.sendData()


        timeCycle += delta
        if round(timeCycle) == DAGNACHTCYCLUSTIJD/2 + 5:
            playsound.playsound(GATESOUND, False)
        if timeCycle >= DAGNACHTCYCLUSTIJD:
            spriteListNacht = []
            for location in spawnLocations:
                if difficulty == "hard":
                    spriteListNacht.append(
                        sprites.Sprite(location[0], location[1], 1, 0, "spellun-sprite.png", 8.4, 2.4, 1, True, False,
                                       False,
                                       False, 0, 50, 7, resources, factory, None))
                elif difficulty == "normal":
                    spriteListNacht.append(
                        sprites.Sprite(location[0], location[1], 1, 0, "spellun-sprite.png", 8.4, 2.4, 1, True, False,
                                       False,
                                       False, 0, 50, 5, resources, factory, None))
                elif difficulty == 'easy':
                    spriteListNacht.append(
                        sprites.Sprite(location[0], location[1], 1, 0, "spellun-sprite.png", 8.4, 2.4, 1, True, False,
                                       False,
                                       False, 0, 50, 3, resources, factory, None))

            timeCycle = 0
            playsound.playsound(GATESOUND, False)

        if drop and equiplist[equiped] != None:
            equiplist[equiped].drop(spriteList, p_speler, resources, factory)
            equiplist[equiped] = None

        if equiplist[equiped] != None:
            if equiplist[equiped].type in weaponList:
                renderer.copy(equiplist[equiped].image, srcrect=(0, 0, equiplist[equiped].image.size[0], equiplist[equiped].image.size[1]), dstrect=(BREEDTE - 300, HOOGTE - 300, 250, 250))


        (p_speler, moet_afsluiten, stamina, hunger, equiped, interact, pakOp, drop, crafting,start) = movement.polling(delta, p_speler, r_speler, r_cameravlak, stamina, hunger, equiped, door_map, world_map, wall_map, dramController)
        (r_speler, r_cameravlak, geklikt) = movement.draaien(r_speler, r_cameravlak, dramController)


        if hunger > 0:
            hunger -= delta * HUNGERMODIFIER
        else:
            hunger = 0
            hp -=delta * HUNGERHPLOSSMODIFIER

        if hp <= 0:
            rendering.render_GameOVer(renderer, factory)
            playsound.playsound(GAMEOVERSOUND, True)
            moet_afsluiten = True

        if world_map[int(p_speler[1]), int(p_speler[0])] == 10:
            completionText.textTimer = 10


        rendering.dim_image(renderer, dimmer, timeCycle)
        rendering.render_hud(renderer, hud, stamina, hp, hunger, crosshair, timeCycle, klokImages, equiped, equiplist, timeToAttack)
        beginText.renderText(delta, renderer, factory)
        consumableText.renderText(delta, renderer, factory)
        completionText.renderText(delta, renderer, factory)
        rendering.render_FPS(delta, renderer, factory, ManagerFont)
        renderer.present()
        #print("Total frame time", (time.time() - frameStartTime))

        highlighted = [False, False, False, False]
        while crafting:
            dramController.readData()
            dramController.mapStamina(stamina)
            dramController.mapHealth(hp)
            dramController.sendData()
            (muis_pos, equiplist, equiped, crafting, highlighted, craftingIndex1, craftingIndex2) = rendering.render_inventory(renderer, factory, resources, muis_pos, equiplist, equiped, hp, hunger, stamina, highlighted, craftingIndex1, craftingIndex2, craftables,dramController)
            start_time = time.time()


    # Sluit SDL2 af
    sdl2.ext.quit()

#faah
if __name__ == '__main__':
    main()