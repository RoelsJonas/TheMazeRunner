import numpy as np
import main

class Sprites:
    p_sprite = np.array([0, 0])
    breedte = 0
    hoogte = 0
    afbeelding = ""
    r_sprite = np.array([0, 0])

    #constructor
    def __init__(self, positie, richting, grootte, afb):
        self.p_sprite = np.array([positie[0], positie[1]])
        self.r_sprite = np.array([richting[0], richting[1]])
        self.breedte = grootte[0]
        self.hoogte = grootte[1]
        self.afbeelding = afb

    def render(self, renderer, r_speler, p_speler, r_cameravlak):

        # bepaal de determinant van de cameramatrix
        det = r_cameravlak[0] * r_speler[1] - r_cameravlak[1] * r_speler[0]
        afbeelding_breedte = self.afbeelding.size[0]

        #render de sprite kolom per kolom:
        for kolom in range(afbeelding_breedte):

            #bepaal de coordinaten van de sprite met de speler als oorsprong:
            p_object =  np.array([self.p_sprite[0]-p_speler[0],self.p_sprite[1]-p_speler[1]])
            #bepaal de coordinaten van de bepaalde kolom van de afbeelding
            p_object -= ((-0.5 + kolom / afbeelding_breedte) * self.breedte) * self.r_sprite

            #bepaal de cameracoordinaten van de sprite aan de hand van de inverse van de cameramatrix
            p_camera = np.array([0,0])
            p_camera[0] = (1/det) * (r_speler[1] * p_object[0] - r_speler[0]*p_object[1])
            p_camera[1] = (1 / det) * (-r_cameravlak[1] * p_object[0] + r_cameravlak[0] * p_object[1])

            #kijk of object voor de camera ligt
            if p_camera[1] > 0:

                #bepaal snijpunt van de straal van de speler naar het object met het cameravlak
                snijpunt = p_camera[0] / p_camera[1]

                #kijk of dit snijpunt of het cameravlak ligt
                if -1 <= snijpunt <= 1:
                    scherm_kolom = int(np.round((((snijpunt + 1)/2)*main.BREEDTE)))
                    #spiegel de schermkolom
                    scherm_kolom = main.BREEDTE - 1 - scherm_kolom

                    #bepaal de grondhoogte en de hoogte van de sprite
                    d_sprite = np.linalg.norm(p_object)
                    h = (main.HOOGTE / d_sprite) * self.hoogte
                    y = int((main.HOOGTE-h)//2)


            #als snijpunt niet op scherm of object achter speler zet schermkolom op -1 (buiten scherm) en y op 0
                else:
                    scherm_kolom = -1
                    y = 0
                    h = 0
            else:
                scherm_kolom = -1
                y = 0
                h = 0

            renderer.copy(self.afbeelding,
                          srcrect=(kolom, 0, 1, self.afbeelding.size[1]),
                          dstrect=(scherm_kolom, int(y), 2, int(h)))