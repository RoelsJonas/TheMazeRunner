from PIL import Image
import numpy as np
import doors


MUUR = 1
DEUR = 2
LEFT = 0
RIGHT = 1

def generateWorld(afbeelding):
    input_image = Image.open(afbeelding)
    r_image_in, g_image_in, b_image_in = input_image.split()
    r_in = np.uint32(np.array(r_image_in))
    b_in = np.uint32(np.array(b_image_in))
    g_in = np.uint32(np.array(g_image_in))

    world_map = np.zeros((r_in.shape[0], r_in.shape[1]), int)
    door_map = np.empty((r_in.shape[0], r_in.shape[1]), object)
    doorLocation = []


    for i in range(r_in.shape[0]):
        for j in range(r_in.shape[1]): #zwarte pixe ==> muur
            if r_in[i, j] == 0 and b_in[i, j] == 0 and g_in[i, j] == 0:
                world_map[i, j] = MUUR

            #blauwwe pixel ==> timed deur die van links opent
            elif b_in[i, j] == 255 and r_in[i, j] == 0 and g_in[i, j] == 0:
                world_map[i, j] = DEUR
                door_map[i, j] = doors.timedDoor((j, i), LEFT)
                doorLocation.append((i, j))

            #groene pixel ==> timed deur die van rechts opent
            elif b_in[i, j] == 0 and r_in[i, j] == 0 and g_in[i, j] == 255:
                world_map[i, j] = DEUR
                door_map[i, j] = doors.timedDoor((j, i), RIGHT)
                doorLocation.append((i, j))

            #witte pixel ==> openruimte
            else:
                world_map[i, j] = 0

    return(world_map, doorLocation, door_map)

