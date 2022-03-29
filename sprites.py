import numpy as np
import main
import equips
import text
import rendering
import playsound


def sortSprites(list, p_speler):
    for sprite in list:
        sprite.updateDistance(p_speler)
    list.sort(key=lambda x: x.d_speler, reverse=True)
    list.sort(key=lambda x: x.d_speler, reverse=True)
    return(list)


class Sprite:
    p_sprite = np.array([0.0, 0.0])
    hoogte = 0
    breedte = 0
    afbeelding = ""
    r_sprite = np.array([0.0, 0.0])
    a = 0
    MOVEMENTSPEED = 0
    drawn = False
    followTime = 0
    volgt = False
    hp = 0
    hungerValue = 5
    eetbaar = False
    healer = False
    DPS = 0
    middensteKolom = 0
    d_speler = 0
    collectible = False
    factory = ""
    renderer = ""
    resources = ""
    afbeeldingLink = ""
    tekst = ""

    def __init__(self, x, y, richting_x,richting_y, png, h, b, speed, volgIk, eet, healer, collectible, waarde, health, damage, resources, factory, tekst):
        self.p_sprite = np.array([[x], [y]])
        self.afbeeldingLink = png
        self.afbeelding = factory.from_image(resources.get_path(png))
        self.hoogte = h
        self.breedte = b
        self.r_sprite = np.array([richting_x, richting_y])
        self.MOVEMENTSPEED = speed
        self.volgt = volgIk
        self.eetbaar = eet
        self.hungerValue = waarde
        self.hp = health
        self.healer = healer
        self.DPS = damage
        self.collectible = collectible
        self.factory = factory
        self.resources = resources
        self.tekst = tekst

    def move(self, delta_x, delta_y):
        self.p_sprite += np.array([delta_x, delta_y])

    def moveToPlayer(self, p_speler, delta, world_map):
        if self.volgt:
            if self.followTime > 0:
                p_sprite = np.array([self.p_sprite[0], self.p_sprite[1]])
                p_sprite[0] -= p_speler[0]
                p_sprite[1] -= p_speler[1]
                p_sprite = np.linalg.norm(p_sprite)
                if p_sprite > .75:
                    afstand = np.array([self.p_sprite[0]-p_speler[0], self.p_sprite[1]-p_speler[1]])
                    norm = np.linalg.norm(afstand)
                    afstand /= norm
                    self.r_sprite = np.array([afstand[1], -1 * afstand[0]])
                    p_sprite_nieuw = np.array([self.p_sprite[0] - delta * self.MOVEMENTSPEED * afstand[0], self.p_sprite[1] - delta * self.MOVEMENTSPEED * afstand[1]])

                #check of nieuwe positie geldig is
                    if world_map[int(p_sprite_nieuw[1]), int(p_sprite_nieuw[0])] == 0:
                        self.p_sprite = p_sprite_nieuw

                    elif world_map[int(self.p_sprite[1]), int(p_sprite_nieuw[0])] == 0:
                        self.p_sprite[0] = p_sprite_nieuw[0]

                    elif world_map[int(p_sprite_nieuw[1]), int(self.p_sprite[0])] == 0:
                        self.p_sprite[1] = p_sprite_nieuw[1]

                self.followTime -= delta
            else:
                self.followTime = 0

    def setGrootte(self, h, b):
        self.hoogte = h
        self.breedte = b

    def render(self, renderer, r_speler, r_cameravlak, p_speler, z_buffer):
        breed = self.afbeelding.size[0]
        determinant = ((r_cameravlak[0] * r_speler[1]) - (r_speler[0] * r_cameravlak[1]))
        adj = np.array([[r_speler[1],-r_speler[0]],[-r_cameravlak[1],r_cameravlak[0]]])
        self.drawn = False
        for kolom in range(0, breed):
            p_kolom = np.array([self.p_sprite[0], self.p_sprite[1]])
            #bepaal de coordinaten van de kolom ten opzichte van de speler
            p_kolom[0] -= p_speler[0]
            p_kolom[1] -= p_speler[1]
            #p_kolom[0] += ((-0.5 + kolom / breed) * self.breedte) # * self.r_sprite[0]
            #p_kolom[1] += ((-0.5 + kolom / breed) * self.breedte) * self.r_sprite[1]

            #bepaal de coordinaten tov van het camera vlak
            cameraCoordinaten = (1 / determinant) * np.dot(adj, p_kolom)

            cameraCoordinaten[0] += ((-0.5 + kolom / breed) * self.breedte)

            #bepaal het snijpunt met het cameravlak
            snijpunt = (cameraCoordinaten[0] * main.D_CAMERA) / cameraCoordinaten[1]

            #bepaal in welke kolom van het scherm dit snijpunt valt
            if -1 <= snijpunt <= 1 and cameraCoordinaten[1] > 0:
                schermKolom = int(np.round((snijpunt + 1) * main.BREEDTE/2))
                d_sprite = np.linalg.norm(p_kolom)
                h = (main.HOOGTE/d_sprite)
                y1 = main.HOOGTE - int((main.HOOGTE-h)//2) - 100
                h = int(self.hoogte * h)
                schermKolom = main.BREEDTE - 1 - schermKolom
                if d_sprite < z_buffer[schermKolom] or z_buffer[schermKolom] == 0:
                    self.drawn = True
                    self.followTime = 7.5
                    renderer.copy(self.afbeelding,
                                srcrect=(kolom, 0, 1, self.afbeelding.size[1]),
                                dstrect=(schermKolom, y1, 2, h))


    def updateDistance(self, p_speler):
        d = np.array([self.p_sprite[0]-p_speler[0], self.p_sprite[1]-p_speler[1]])
        self.d_speler = np.linalg.norm(d)


    def checkInteractie(self, hunger, hp, p_speler, delta, geklikt, timeToAttack, interaction, equiplist, equiped, factory, timeCycle, resources, renderer):
        destroy = False
        spelerDamage = 0

        if (geklikt == True and equiplist[equiped] != None):
            if equiplist[equiped].type in main.weaponList:
                spelerDamage = equiplist[equiped].damage

        if self.eetbaar:
            p_sprite = np.array([self.p_sprite[0], self.p_sprite[1]])
            p_sprite[0] -= p_speler[0]
            p_sprite[1] -= p_speler[1]
            p_sprite = np.linalg.norm(p_sprite)
            if p_sprite < main.INTERACTIONDISTANCE:
                if hunger == 100:
                    hunger = 100
                    destroy = False
                elif hunger + self.hungerValue > 100:
                    hunger = 100
                    destroy = True
                else:
                    hunger += self.hungerValue
                    destroy = True

        if (self.afbeeldingLink == "bonfire.png" and timeCycle > ((main.DAGNACHTCYCLUSTIJD//2) + 10) and geklikt == True):
            p_sprite = np.array([self.p_sprite[0], self.p_sprite[1]])
            p_sprite[0] -= p_speler[0]
            p_sprite[1] -= p_speler[1]
            p_sprite = np.linalg.norm(p_sprite)
            if p_sprite < main.INTERACTIONDISTANCE:
                timeCycle = 0
                playsound.playsound(main.GATESOUND, False)
                self.tekst.textTimer = 10

        if self.volgt:
            if self.hp <= 0:
                destroy = True

            p_sprite = np.array([self.p_sprite[0], self.p_sprite[1]])
            p_sprite[0] -= p_speler[0]
            p_sprite[1] -= p_speler[1]
            p_sprite = np.linalg.norm(p_sprite)
            if self.d_speler < main.INTERACTIONDISTANCE:
                hp -= self.DPS * delta
                if timeToAttack < 0 and geklikt and equiplist[equiped] != None:
                    self.hp -= equiplist[equiped].damage

        if self.collectible and interaction:
            p_sprite = np.array([self.p_sprite[0], self.p_sprite[1]])
            p_sprite[0] -= p_speler[0]
            p_sprite[1] -= p_speler[1]
            p_sprite = np.linalg.norm(p_sprite)
            if equiplist[equiped] == None and p_sprite < 1:
                type = ""
                consum = False

                if self.afbeeldingLink == "medkit.png":
                    type = "H1"
                    consum = True
                elif self.afbeeldingLink == "medkit2.png":
                    type = "H2"
                    consum = True
                elif self.afbeeldingLink == "medkit3.png":
                    type = "H3"
                    consum = True
                elif self.afbeeldingLink == "burger.png":
                    type = "BURGER"
                    consum = True
                elif self.afbeeldingLink == "stick.png":
                    type = "STICK"
                    consum = False
                elif self.afbeeldingLink == "rock.png":
                    type = "ROCK"
                    consum = False
                elif self.afbeeldingLink == "kaart.png":
                    type = "KAART"
                    consum = False

                equiplist[equiped] = equips.equip(self.factory, self.resources, self.afbeeldingLink, self.DPS, self.hungerValue, self.hp, consum, type)
                destroy = True

        return(hunger, hp, destroy, equiplist, timeCycle)












