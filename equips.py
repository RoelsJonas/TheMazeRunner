import main
import numpy as np
import text
import sprites
import playsound

def interactions(hunger, hp, equiped, equiplist, interact, consumableText):
    if equiplist[equiped] != None:
        if interact and equiplist[equiped].consumable:
            (hunger, hp) = equiplist[equiped].interact(hunger, hp)
            equiplist[equiped] = None
            consumableText.textTimer = 10
            playsound.playsound(main.CONSUMESOUND, False)
    return(hunger, hp, consumableText)


class equip:

    type = ""
    damage = 0
    hunger = 0
    healing = 0
    consumable = False
    image = ""
    b = 0
    h = 0
    text = ""
    imagetext = ""
    size = (1,1)

    def __init__(self, factory, resources, afbeelding, damage, hunger, healing, *consumeerbaar, **type):
        self.damage = damage
        self.hunger = hunger
        self.healing = healing
        self.consumable = consumeerbaar
        self.type = type
        self.imagetext = afbeelding
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

    def drop(self, spriteList, p_speler, resources, factory):
        eetbaar = False
        healer = False

        if self.hunger > 0:
            eetbaar = True

        if self.healing > 0:
            healer = True

        spriteList.append(sprites.Sprite(p_speler[0]+0.1, p_speler[1]+.1, 0, 0, self.imagetext, self.size[0], self.size[1], 0, False, eetbaar, healer, True, self.hunger, self.healing, self.damage, resources, factory ))

        return(spriteList)

