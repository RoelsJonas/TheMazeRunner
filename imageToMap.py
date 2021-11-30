from PIL import Image
import numpy as np
import doors
import main

MUUR = 1
TIMEDDEUR = 2
INTERACTABLEDEUR = 3
LEFT = 0
RIGHT = 1

def generateWorld(afbeelding, factory, resources, textures, renderer):
    input_image = Image.open(afbeelding)
    r_image_in, g_image_in, b_image_in = input_image.split()
    r_in = np.uint32(np.array(r_image_in))
    b_in = np.uint32(np.array(b_image_in))
    g_in = np.uint32(np.array(g_image_in))

    world_map = np.zeros((r_in.shape[0], r_in.shape[1]), int)
    door_map = np.empty((r_in.shape[0], r_in.shape[1]), object)
    wall_map = np.empty((r_in.shape[0], r_in.shape[1]), object)
    doorLocation = []


    for i in range(r_in.shape[0]):
        for j in range(r_in.shape[1]):
            #zwarte pixe ==> muur met texture[0]
            if r_in[i, j] == 0 and b_in[i, j] == 0 and g_in[i, j] == 0:
                world_map[i, j] = MUUR
                wall_map[i, j] = Wall(i, j, textures[0])

                #grijze pixel ==> muur met texture[1]
            elif r_in[i, j] == 128 and b_in[i, j] == 128 and g_in[i, j] == 128:
                world_map[i, j] = MUUR
                wall_map[i, j] = Wall(i, j, textures[1])

            #blauwwe pixel ==> timed deur die van links opent
            elif b_in[i, j] == 255 and r_in[i, j] == 0 and g_in[i, j] == 0:
                world_map[i, j] = TIMEDDEUR
                door_map[i, j] = doors.timedDoor((j, i), LEFT, textures[0])
                doorLocation.append((i, j))

            #groene pixel ==> timed deur die van rechts opent
            elif b_in[i, j] == 0 and r_in[i, j] == 0 and g_in[i, j] == 255:
                world_map[i, j] = TIMEDDEUR
                door_map[i, j] = doors.timedDoor((j, i), RIGHT, textures[0])
                doorLocation.append((i, j))

            elif b_in[i, j] == 0 and r_in[i, j] == 255 and g_in[i, j] == 0:
                world_map[i, j] = INTERACTABLEDEUR
                door_map[i, j] = doors.interactableDoor((j, i), RIGHT, textures[1])
                doorLocation.append((i, j))


            #witte pixel ==> openruimte
            else:
                world_map[i, j] = 0

        renderLoadingScreen(resources, factory, renderer, i, r_in.shape[0])

    return(world_map, doorLocation, door_map, wall_map)


class Wall:

    image = ""
    posWorldCoordinates = np.array([0.0, 0.0])

    def __init__(self, x, y, image):
        self.posWorldCoordinates = np.array([x, y])
        self.image = image


def renderLoadingScreen(resources, factory, renderer, waarde, max):
    completion = int(100*waarde/max)
    renderer.clear()
    renderer.fill((0, 0, main.BREEDTE, main.HOOGTE), main.kleuren[5])
    text_ = "Loading: " + str(completion) + "%"
    text = factory.from_text(text_, fontmanager=resources)
    renderer.copy(text, dstrect=(main.BREEDTE//2 - 100, main.HOOGTE//2 - 50, 200, 100))
    renderer.present()
