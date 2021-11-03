from PIL import Image
import numpy as np


def generateWorld(afbeelding):
    input_image = Image.open(afbeelding)
    r_image_in, g_image_in, b_image_in = input_image.split()
    r_in = np.uint32(np.array(r_image_in))

    world_map = np.zeros((r_in.shape[0], r_in.shape[1]), int)

    for i in range(r_in.shape[0]):
        for j in range(r_in.shape[1]):
            if r_in[i, j] == 0:
                world_map[i, j] = 1
            else:
                world_map[i, j] = 0

    return world_map

