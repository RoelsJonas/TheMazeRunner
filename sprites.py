import numpy as np
import main

class Sprite:
    p_sprite = np.array([0, 0])
    hoogte = 0
    breedte = 0
    afbeelding = ""
    r_sprite = np.array([0, 0])
    a = 0
    drawn = False
    def __init__(self, x, y, richting_x,richting_y, png, h, b, resources, factory):
        self.p_sprite = np.array([x, y])
        self.afbeelding = factory.from_image(resources.get_path(png))
        self.hoogte = h
        self.breedte = b
        self.r_sprite = np.array([richting_x, richting_y])


    def move(self, delta_x, delta_y):
        self.p_sprite += np.array([delta_x, delta_y])


    def setGrootte(self, h, b):
        self.hoogte = h
        self.breedte = b


    def render(self, renderer, r_speler, r_cameravlak, p_speler):
        breed = self.afbeelding.size[0]
        determinant = r_cameravlak[0] * r_speler[1] - r_speler[0] * r_cameravlak[1]
        for kolom in range(0, breed):
            p_kolom = np.array([self.p_sprite[0], self.p_sprite[1]])

            #bepaal de coordinaten van de kolom ten opzichte van de speler
            p_kolom[0] -= p_speler[0]
            p_kolom[1] -= p_speler[1]



            #bepaal de coordinaten tov van het camera vlak
            cameraCoordinaten = (1 / determinant) * np.array([r_speler[1] * p_kolom[0] - r_speler[0] * p_kolom[1], r_cameravlak[0] * p_kolom[1] - r_cameravlak[1] * p_kolom[0]])
            cameraCoordinaten[0] += ((-0.5 + kolom / breed) * self.breedte)

            #bepaal het snijpunt met het cameravlak
            snijpunt = cameraCoordinaten[0] * main.D_CAMERA / cameraCoordinaten[1]

            #bepaal in welke kolom van het scherm dit snijpunt valt
            if -1 <= snijpunt <= 1:
                schermKolom = (np.round((snijpunt + 1) * main.BREEDTE/2))
                afstand = np.linalg.norm(p_kolom)
                y1 = 200
            else:
                schermKolom = main.BREEDTE + 1 #render buiten scherm
                y1 = 0

            h = y1 * self.hoogte
            renderer.copy(self.afbeelding,
                          srcrect=(kolom, 0, 1, self.afbeelding.size[1]),
                          dstrect=(int(main.BREEDTE - 1 - schermKolom), int(y1), 1, int(h)))









