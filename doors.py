import numpy as np
import main
import playsound
import sdl2
import sdl2.ext
import sdl2.sdlttf
import time


def rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, texture, r_straal, r_speler, offset):
    d_euclidisch = d_muur
    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

    hoogte = main.MUURHOOGTE * (window.size[1] / d_muur)
    y1 = int((window.size[1] - hoogte) // 2) - 100
    textuur_y = 0
    textuur_hoogte = int(texture.size[1])

    schermkolom = main.BREEDTE - 1 - kolom
    if horizontaal:
        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * texture.size[0]))
    else:
        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * texture.size[0]))


    renderer.copy(texture, srcrect=(textuur_x + offset, textuur_y, 1, textuur_hoogte),
                  dstrect=(schermkolom, y1, 2, int(hoogte)))

class timedDoor:
    p_door = np.array([0,0])
    state = 1 #definieer hoe gesloten de deur is (1 is dicht, 0 volledig open)
    side = 0 #definieer van welke kant de deur dicht gaat ( 0 is links, 1 is rechts)
    texture = ""

    def __init__(self, p, kant, texture):
        self.p_door = np.array([p[0],p[1]])
        self.side = kant
        self.texture = texture

    def updateState(self, newState):
        self.state = newState


    def timedUpdateState(self, timeCycle):
        #open deur volledig tijdens dag
        if(5 < timeCycle <= main.DAGNACHTCYCLUSTIJD//2 + 5):
            self.state = 0

        #sluit deur volledig tijdens nacht
        elif((main.DAGNACHTCYCLUSTIJD//2 + 10) < timeCycle):
            self.state = 1

        #open de deur gelijdelijk aan tijdens de ochtend
        elif timeCycle <= 5:
            self.state = 1 - timeCycle/5

        #sluit de deur gelijdelijk aan tijdens de avond
        else:
            self.state = (timeCycle - main.DAGNACHTCYCLUSTIJD//2 - 5)/5



    def render(self, renderer, window, kolom, d_muur, intersectie, horizontaal, textures, r_straal, r_speler, timeCycle, z_buffer, p_speler, delta):
        self.timedUpdateState(timeCycle)

        #render niets als deur volledig open is
        if self.state == 0:
            return(z_buffer)

        #render als een muur wanneer de deur volledig gesloten is
        elif self.state == 1:
            z_buffer[main.BREEDTE - 1 - kolom] = d_muur
            rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal, r_speler, 0)

        #kijk of deur rechts/linkssluitend is
        elif self.side == 0:

            if horizontaal:
                #kijk of de intersectie binnen het gesloten deel zit
                if intersectie[0] - int(intersectie[0]) < self.state:
                    offset = int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal, r_speler, offset)
            else:
                if 1 + int(intersectie[1]) - intersectie[1] < self.state:
                    offset = -1 * int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal, r_speler, offset)

        elif self.side == 1:
            if horizontaal:
                if 1 + int(intersectie[0]) - intersectie[0] < self.state:
                    offset = -1 * int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal, r_speler, offset)
            else:
                if intersectie[1] - int(intersectie[1]) < self.state:
                    offset = int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal, r_speler, offset)

        return(z_buffer)


class interactableDoor:
    p_door = np.array([0, 0])
    state = 1  # definieer hoe gesloten de deur is (1 is dicht, 0 volledig open)
    side = 1  # definieer van welke kant de deur dicht gaat ( 0 is links, 1 is rechts)
    opening = 0 #definieer wat de deur aan het doen is, 0 = niks, 1 = openenen, 2 is gelijk aan sluiten
    texture = ""
    updated = False
    passCode = "1234"
    instructionText = "Give the password"

    def __init__(self, p, kant, texture):
        self.p_door = np.array([p[0], p[1]])
        self.side = kant
        self.texture = texture

    def updateState(self, delta):
        if self.opening == 1:
            self.state -= delta/5
            #check of deur volledig open is
            if self.state < 0:
                self.state = 0 #stel de deur op volledig open in
                self.opening = 0 #stop het openenen van de deur

        elif self.opening == 2:
            self.state += delta/5
            #check of deur volledig toe is
            if self.state > 1:
                self.state = 1 #stel de deur op volleidg gesloten in
                self.opening = 0 #stop het sluiten van de deur
        self.updated = True

    def setPassCode(self, code, instruction):
        self.passCode = code
        self.instructionText = instruction

    def render(self, renderer, window, kolom, d_muur, intersectie, horizontaal, textures, r_straal, r_speler, timeCycle, z_buffer, p_speler, delta):
        # render niets als deur volledig open is
        if self.state == 0:
            return (z_buffer)

        # render als een muur wanneer de deur volledig gesloten is
        elif self.state == 1:
            z_buffer[main.BREEDTE - 1 - kolom] = d_muur
            rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal, r_speler, 0)

        # kijk of deur rechts/linkssluitend is
        elif self.side == 0:

            if horizontaal:
                # kijk of de intersectie binnen het gesloten deel zit
                if intersectie[0] - int(intersectie[0]) < self.state:
                    offset = int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal,
                              r_speler, offset)
            else:
                if 1 + int(intersectie[1]) - intersectie[1] < self.state:
                    offset = -1 * int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal,
                              r_speler, offset)

        elif self.side == 1:
            if horizontaal:
                if 1 + int(intersectie[0]) - intersectie[0] < self.state:
                    offset = -1 * int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal,
                              r_speler, offset)
            else:
                if intersectie[1] - int(intersectie[1]) < self.state:
                    offset = int((1 - self.state) * self.texture.size[0])
                    z_buffer[main.BREEDTE - 1 - kolom] = d_muur
                    rendering(renderer, window, kolom, d_muur, intersectie, horizontaal, self.texture, r_straal,
                              r_speler, offset)

        return (z_buffer)


    def interact(self, renderer, factory, resources, interaction, p_speler, equiplist, equiped):
        if interaction:
            d_deur = np.array([self.p_door[0], self.p_door[1]])
            d_deur[0] -= p_speler[0]
            d_deur[1] -= p_speler[1]
            d_deur = np.linalg.norm(d_deur)
            playsound.playsound(main.GATESOUND, False)         #sound moet nog geeddit worden

            if d_deur < 1.25:
                inPuzzle = True
                solved = False
                userInput = ""
                ManagerFont = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(255, 255, 255))
                text = self.instructionText
                answerText = factory.from_text("Answer:", fontmanager = ManagerFont)
                textRender = factory.from_text(text, fontmanager = ManagerFont)
                muis_pos = np.array([main.BREEDTE//2, main.HOOGTE//2])
                pressTime = 0
                while inPuzzle:
                    renderer.clear()

                    renderer.fill((0, 0, main.BREEDTE, main.HOOGTE), main.kleuren[4])

                    key_states = sdl2.SDL_GetKeyboardState(None)
                    events = sdl2.ext.get_events()
                    if key_states[sdl2.SDL_SCANCODE_TAB]:
                        inPuzzle = False

                    renderer.copy(textRender, dstrect=(main.BREEDTE//2 - len(text) * 4, 100, len(text) * 8, 60))
                    renderer.copy(answerText, dstrect=(main.BREEDTE//2 - len(text) * 4, 180, len(text) * 8, 60))
                    if userInput == "":
                        inputText = factory.from_text(" ", fontmanager = ManagerFont)
                    else:
                        inputText = factory.from_text(userInput, fontmanager = ManagerFont)
                    renderer.copy(inputText, dstrect=(main.BREEDTE//2 - len(userInput) * 8, 260, len(userInput) * 16, 120))

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
                    if time.time() - pressTime > 0.2:
                        if key_states[sdl2.SDL_SCANCODE_0 or key_states[sdl2.SDL_SCANCODE_KP_0]]:
                            pressTime = time.time()
                            userInput += "0"
                        if key_states[sdl2.SDL_SCANCODE_1 or key_states[sdl2.SDL_SCANCODE_KP_1]]:
                            pressTime = time.time()
                            userInput += "1"
                        if key_states[sdl2.SDL_SCANCODE_2 or key_states[sdl2.SDL_SCANCODE_KP_2]]:
                            pressTime = time.time()
                            userInput += "2"
                        if key_states[sdl2.SDL_SCANCODE_3 or key_states[sdl2.SDL_SCANCODE_KP_3]]:
                            pressTime = time.time()
                            userInput += "3"
                        if key_states[sdl2.SDL_SCANCODE_4 or key_states[sdl2.SDL_SCANCODE_KP_4]]:
                            pressTime = time.time()
                            userInput += "4"
                        if key_states[sdl2.SDL_SCANCODE_5 or key_states[sdl2.SDL_SCANCODE_KP_5]]:
                            pressTime = time.time()
                            userInput += "5"
                        if key_states[sdl2.SDL_SCANCODE_6 or key_states[sdl2.SDL_SCANCODE_KP_6]]:
                            pressTime = time.time()
                            userInput += "6"
                        if key_states[sdl2.SDL_SCANCODE_7 or key_states[sdl2.SDL_SCANCODE_KP_7]]:
                            pressTime = time.time()
                            userInput += "7"
                        if key_states[sdl2.SDL_SCANCODE_8 or key_states[sdl2.SDL_SCANCODE_KP_8]]:
                            pressTime = time.time()
                            userInput += "8"
                        if key_states[sdl2.SDL_SCANCODE_9 or key_states[sdl2.SDL_SCANCODE_KP_9]]:
                            pressTime = time.time()
                            userInput += "9"
                        if key_states[sdl2.SDL_SCANCODE_BACKSPACE]:
                            newUserInput = ""
                            for i in range(0, len(userInput) - 1):
                                newUserInput += userInput[i]
                            userInput = newUserInput
                            pressTime = time.time()

                    renderer.copy(factory.from_image(resources.get_path("crosshair.png")),
                                  srcrect=(0, 0, 50, 50),
                                  dstrect=(muis_pos[0] - main.CROSSHAIRGROOTTE // 2, muis_pos[1] - main.CROSSHAIRGROOTTE // 2,
                                           main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))

                    if(userInput ==  self.passCode):
                        if not solved:
                            solvetime = time.time()
                            solved = True
                        correctText = factory.from_text("Correct!", fontmanager = ManagerFont)
                        renderer.copy(correctText, dstrect=(main.BREEDTE//2 - 100, 400, 200, 100))
                        if time.time() - solvetime > 1:
                            inPuzzle = False

                    renderer.present()


                if solved:
                    if self.state == 0:
                        self.opening = 2
                    if self.state == 1:
                        self.opening = 1




