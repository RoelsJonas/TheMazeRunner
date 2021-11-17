import main
import numpy as np
def interactions(hunger, hp, equiped, equiplist, interact):
    if equiplist[equiped] != None:
        if interact and equiplist[equiped].consumable:
            (hunger, hp) = equiplist[equiped].interact(hunger, hp)
            equiplist[equiped] = None
    return(hunger, hp)


class equip:

    type = ""
    damage = 0
    hunger = 0
    healing = 0
    consumable = False
    image = ""
    b = 0
    h = 0

    def __init__(self, factory, resources, afbeelding, type, damage, hunger, healing, consumeerbaar):
        self.type = type
        self.damage = damage
        self.hunger = hunger
        self.healing = healing
        self.consumable = consumeerbaar
        self.image = factory.from_image(resources.get_path(afbeelding))
        self.b = int(self.image.size[0])
        self.h = int(self.image.size[1])

    def render(self, slot, renderer, offset):
        x = offset + 208 + (slot * 75)
        y = main.HOOGTE - 58
        renderer.copy(self.image, srcrect=(0, 0, self.b, self.h), dstrect=(x, y, 40, 40))

    def interact(self, hunger, hp):
        if self.consumable:
            hp += self.healing
            hunger += self.hunger

            if hp > 100:
                hp = 100
            if hunger > 100:
                hunger = 100

        return(hunger, hp)



