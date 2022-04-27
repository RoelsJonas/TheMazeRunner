import sdl2
import sdl2.ext
import sdl2.sdlttf
import main
import numpy as np
import text
import sprites
import playsound
import globals
import time




def interactions(hunger, hp, obj, interact, consumableText, p_speler, renderer, world_map, factory, dramController):
    if obj != None:
        if interact and obj.consumable:
            (hunger, hp) = obj.interact(hunger, hp, p_speler, renderer)
            obj = None
            consumableText.textTimer = 10
            playsound.playsound(main.CONSUMESOUND, False)
            interact = False

        if interact and obj.getType() == "KAART":
            statusKaart = True
            muis_pos = np.array([0, 0])
            while statusKaart:
                (statusKaart, muis_pos) = openKaart(renderer, p_speler, world_map, statusKaart, muis_pos, factory,
                                                    dramController)


            interact = False

    return (hunger, hp, consumableText, obj)



class equip:
    type = ""
    damage = 0
    hunger = 0
    healing = 0
    consumable = False
    image = ""
    b = 0
    h = 0
    tekst = ""
    imagetext = ""
    size = (1, 1)
    wat = ""

    def __init__(self, factory, resources, afbeelding, damage, hunger, healing, consumeerbaar, type):
        self.damage = damage
        self.hunger = hunger
        self.healing = healing
        self.consumable = consumeerbaar
        self.type = type
        self.wat = type
        self.imagetext = afbeelding
        self.image = factory.from_image(resources.get_path(afbeelding))
        self.b = int(self.image.size[0])
        self.h = int(self.image.size[1])

    def getType(self):
        return (self.type)

    def render(self, slot, renderer, offset):
        x = offset + 208 + (slot * 75)
        y = main.HOOGTE - 58
        renderer.copy(self.image, srcrect=(0, 0, self.b, self.h), dstrect=(x, y, 40, 40))

    def interact(self, hunger, hp, renderer, factory):
        if self.consumable:
            hp += self.healing
            hunger += self.hunger

            if hp > 100:
                hp = 100
            if hunger > 100:
                hunger = 100

        return (hunger, hp)

    def drop(self, spriteList, p_speler, resources, factory):
        eetbaar = False
        healer = False

        if self.hunger > 0:
            eetbaar = True

        if self.healing > 0:
            healer = True

        spriteList.append(
            sprites.Sprite(p_speler[0] + 0.1, p_speler[1] + .1, 0, 0, self.imagetext, 0.5, 0.5, 0, False, eetbaar,
                           healer, True, self.hunger, self.healing, self.damage, resources, factory, self.tekst))

        return (spriteList)



def openKaart(renderer, p_speler, world_map, statusKaart, muis_pos, factory, dramController):
    p_speler_temp = np.array([p_speler[0] - 20, p_speler[1] - 15])
    renderer.fill((0, 0, main.BREEDTE, main.HOOGTE), main.kleuren[6])
    dramController.readData()
    for i in range(int(p_speler_temp[0]), int(p_speler_temp[0]) + 40):
        for j in range(int(p_speler_temp[1]), int(p_speler_temp[1]) + 30):
            if world_map[j, i] == 1:
                renderer.fill(((i - int(p_speler_temp[0])) * 20, (j - int(p_speler_temp[1])) * 20, 20, 20),
                              main.kleuren[0])
            elif world_map[j, i] > 1:
                renderer.fill(((i - int(p_speler_temp[0])) * 20, (j - int(p_speler_temp[1])) * 20, 20, 20),
                              main.kleuren[1])


    key_states = sdl2.SDL_GetKeyboardState(None)
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

    renderer.copy(factory.from_image("resources/crosshair.png"),
                  srcrect=(0, 0, 50, 50),
                  dstrect=(muis_pos[0] - main.CROSSHAIRGROOTTE // 2, muis_pos[1] - main.CROSSHAIRGROOTTE // 2,
                           main.CROSSHAIRGROOTTE, main.CROSSHAIRGROOTTE))
    if (dramController.NunChuk.buttonC == 1):
        statusKaart = False
    if key_states[sdl2.SDL_SCANCODE_TAB]:
        statusKaart = False
    renderer.fill((main.BREEDTE // 2 + 5, main.HOOGTE // 2 + 5, 10, 10), main.kleuren[3])
    renderer.present()

    return (statusKaart, muis_pos)
