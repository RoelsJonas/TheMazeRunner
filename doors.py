import numpy as np
import main

class timedDoor:
    p_door = np.array([0,0])
    state = 1 #definieer hoe gesloten de deur is (1 is dicht, 0 volledig open)
    side = 0 #definieer van welke kant de deur dicht gaat ( 0 is links, 1 is rechts)

    def __init__(self, p, kant):
        self.p_door = np.array([p[0],p[1]])
        self.side = kant

    def updateState(self, newState):
        self.state = newState


    def timedUpdateState(self, timeCycle):
        #open deur volledig tijdens dag
        if(1 < timeCycle <= main.DAGNACHTCYCLUSTIJD//2):
            self.state = 0

        #sluit deur volledig tijdens nacht
        elif((main.DAGNACHTCYCLUSTIJD//2 + 5) < timeCycle):
            self.state = 1

        #open de deur gelijdelijk aan tijdens de ochtend
        elif timeCycle < 5:
            self.state = 1 - timeCycle

        #sluit de deur gelijdelijk aan tijdens de avond
        else:
            self.state = (timeCycle - main.DAGNACHTCYCLUSTIJD//2)/5



    def render(self, renderer, window, kolom, d_muur, intersectie, horizontaal, textures, r_straal, r_speler, timeCycle, mist):
        self.timedUpdateState(timeCycle)
        print(kolom, d_muur)

        #render niets als deur volledig open is
        if self.state == 0:
            return

        #render als een muur wanneer de deur volledig gesloten is
        elif self.state == 1:

            texture_index = 0
            d_euclidisch = d_muur
            d_muur = d_euclidisch * np.dot(r_speler, r_straal)

            hoogte = main.MUURHOOGTE * (window.size[1] / d_muur)
            y1 = int((window.size[1] - hoogte) // 2) - 100
            textuur_y = 0
            textuur_hoogte = int(textures[texture_index].size[1])

            schermkolom = main.BREEDTE - 1 - kolom
            if horizontaal:
                textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * textures[texture_index].size[0]))
            else:
                textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * textures[texture_index].size[0]))

            renderer.copy(textures[0], srcrect=(textuur_x, textuur_y, 1, textuur_hoogte),
                        dstrect=(schermkolom, y1, 2, int(hoogte)))  # muur

        #
        elif self.side == 0:
            if horizontaal:
                if intersectie[0] - int(intersectie[0]) < self.state:
                    texture_index = 0
                    d_euclidisch = d_muur
                    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

                    hoogte = main.MUURHOOGTE * (window.size[1] / d_muur)
                    y1 = int((window.size[1] - hoogte) // 2) - 100
                    textuur_y = 0
                    textuur_hoogte = int(textures[texture_index].size[1])

                    schermkolom = main.BREEDTE - 1 - kolom
                    if horizontaal:
                        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * textures[texture_index].size[0]))
                    else:
                        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * textures[texture_index].size[0]))

                    renderer.copy(textures[0], srcrect=(textuur_x, textuur_y, 1, textuur_hoogte),
                                dstrect=(schermkolom, y1, 2, int(hoogte)))  # muur
            else:
                if intersectie[1] - int(intersectie[1]) < self.state:
                    texture_index = 0
                    d_euclidisch = d_muur
                    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

                    hoogte = main.MUURHOOGTE * (window.size[1] / d_muur)
                    y1 = int((window.size[1] - hoogte) // 2) - 100
                    textuur_y = 0
                    textuur_hoogte = int(textures[texture_index].size[1])

                    schermkolom = main.BREEDTE - 1 - kolom
                    if horizontaal:
                        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * textures[texture_index].size[0]))
                    else:
                        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * textures[texture_index].size[0]))

                    renderer.copy(textures[0], srcrect=(textuur_x, textuur_y, 1, textuur_hoogte),
                                dstrect=(schermkolom, y1, 2, int(hoogte)))  # muur

        elif self.side == 1:
            if horizontaal:
                if 1 + int(intersectie[0]) - intersectie[0] < self.state:
                    texture_index = 0
                    d_euclidisch = d_muur
                    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

                    hoogte = main.MUURHOOGTE * (window.size[1] / d_muur)
                    y1 = int((window.size[1] - hoogte) // 2) - 100
                    textuur_y = 0
                    textuur_hoogte = int(textures[texture_index].size[1])

                    schermkolom = main.BREEDTE - 1 - kolom
                    if horizontaal:
                        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * textures[texture_index].size[0]))
                    else:
                        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * textures[texture_index].size[0]))

                    renderer.copy(textures[0], srcrect=(textuur_x, textuur_y, 1, textuur_hoogte),
                                dstrect=(schermkolom, y1, 2, int(hoogte)))  # muur
            else:
                if  1 + int(intersectie[1]) - intersectie[1] < self.state:
                    texture_index = 0
                    d_euclidisch = d_muur
                    d_muur = d_euclidisch * np.dot(r_speler, r_straal)

                    hoogte = main.MUURHOOGTE * (window.size[1] / d_muur)
                    y1 = int((window.size[1] - hoogte) // 2) - 100
                    textuur_y = 0
                    textuur_hoogte = int(textures[texture_index].size[1])

                    schermkolom = main.BREEDTE - 1 - kolom
                    if horizontaal:
                        textuur_x = int(np.round((intersectie[0] - int(intersectie[0])) * textures[texture_index].size[0]))
                    else:
                        textuur_x = int(np.round((intersectie[1] - int(intersectie[1])) * textures[texture_index].size[0]))

                    renderer.copy(textures[0], srcrect=(textuur_x, textuur_y, 1, textuur_hoogte),
                                dstrect=(schermkolom, y1, 2, int(hoogte)))  # muur






