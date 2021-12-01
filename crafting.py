import main
import numpy as np
import equips


class Craftable:
    type = ""
    obj1 = ""
    obj2 = ""
    damage = 0
    hp = 0
    hunger = 0
    image = ""
    image_text = ""
    renderer = ""
    factory = ""
    resources = ""
    consumable = False

    def __init__(self, renderer, factory, resources, image, obj1, obj2, type, damage, hp, hunger):
        self.type = type
        self.obj1 = obj1
        self.obj2 = obj2
        self.damage = damage
        self.hp = hp
        self.hunger = hunger
        self.renderer = renderer
        self.factory = factory
        self.image_text = image
        self.resources = resources
        self.image = factory.from_image(resources.get_path(image))
        if hp > 0 or hunger > 0:
            self.consumable = True

    def checkTypes(self, equip1, equip2):

        if self.obj1 == equip1.type and self.obj2 == equip2.type:
            return(True)

        elif self.obj1 == equip2.type and self.obj2 == equip1.type:
            return(True)

        else:
            return(False)

    def crafted(self):
        equipable = equips.equip(self.factory, self.resources, self.image_text, self.damage, self.hunger, self.hp, self.consumable, self.type)
        return(equipable)
