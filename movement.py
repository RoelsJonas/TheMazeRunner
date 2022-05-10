import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import main
import doors

equipedcounter = 5


def bewegen(delta, delta_p, r_speler, r_cameravlak, p_speler, door_map, world_map):
    p_speler_nieuw = np.array([p_speler[0], p_speler[1]])

    p_speler_nieuw += delta * delta_p[0] * r_speler
    p_speler_nieuw += delta * delta_p[1] * r_cameravlak

    if world_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 0 or world_map[
        int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 10:
        p_speler = p_speler_nieuw
        return (p_speler)

    if (world_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 2 or world_map[
        int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 3) and door_map[
        int(p_speler_nieuw[1]), int(p_speler_nieuw[0])].state != 1:
        p_speler = p_speler_nieuw

    elif (world_map[int(p_speler[1]), int(p_speler_nieuw[0])] == 2 or world_map[
        int(p_speler[1]), int(p_speler_nieuw[0])] == 3) and door_map[
        int(p_speler[1]), int(p_speler_nieuw[0])].state != 1:
        p_speler[0] = p_speler_nieuw[0]

    elif (world_map[int(p_speler_nieuw[1]), int(p_speler[0])] == 2 or world_map[
        int(p_speler_nieuw[1]), int(p_speler[0])] == 3) and door_map[
        int(p_speler_nieuw[1]), int(p_speler[0])].state != 1:
        p_speler[1] = p_speler_nieuw[1]

    elif world_map[int(p_speler[1]), int(p_speler_nieuw[0])] == 0 or world_map[
        int(p_speler[1]), int(p_speler_nieuw[0])] == 10:
        p_speler[0] = p_speler_nieuw[0]
        return (p_speler)
    elif world_map[int(p_speler_nieuw[1]), int(p_speler[0])] == 0 or world_map[
        int(p_speler_nieuw[1]), int(p_speler[0])] == 10:
        p_speler[1] = p_speler_nieuw[1]
        return (p_speler)

    return (p_speler)


def polling(delta, p_speler, r_speler, r_cameravlak, stamina, hunger, equiped, door_map, world_map, wall_map,
            dramController, hp):
    moet_afsluiten = False
    damage = 0
    delta_p = np.array([0, 0])
    key_states = sdl2.SDL_GetKeyboardState(None)
    interact = False
    pakOp = False
    drop = False
    crafting = False
    start = True
    settings = False
    global equipedcounter
    equipedcounter += 1

    if (dramController.NunChuk.joyY > 210):
        delta_p[0] += 1
    if (dramController.NunChuk.joyY < 60):
        delta_p[0] -= 1
    if (dramController.NunChuk.buttonC == 1 and stamina > 0):
        delta = delta * main.SPRINT_SPEED
        sprinting = True
    elif key_states[sdl2.SDL_SCANCODE_LSHIFT] and stamina > 0:
        delta = delta * main.SPRINT_SPEED
        sprinting = True
    else:
        delta = delta * main.SPEED
        sprinting = False
        if stamina < 100:
            stamina += delta * main.STAMINAREGENMODIFIER

    if key_states[sdl2.SDL_SCANCODE_W]:
        delta_p[0] += 1

    if key_states[sdl2.SDL_SCANCODE_S]:
        delta_p[0] -= 1

    if key_states[sdl2.SDL_SCANCODE_A]:
        delta_p[1] += 1

    if key_states[sdl2.SDL_SCANCODE_D]:
        delta_p[1] -= 1

    if key_states[sdl2.SDL_SCANCODE_C]:
        r_speler *= -1

    if key_states[sdl2.SDL_SCANCODE_L]:
        hp = 100
    if key_states[sdl2.SDL_SCANCODE_N]:
        hp = 0
    if equipedcounter >= 5:
        if (dramController.buttonBlue == 1):
            if (equiped == 3):
                equiped = 0
                equipedcounter = 0
            else:
                equiped += 1
                equipedcounter = 0
        if (dramController.buttonGreen == 1):
            if (equiped == 0):
                equiped = 3
                equipedcounter = 0
            else:
                equiped -= 1
                equipedcounter = 0

    if key_states[sdl2.SDL_SCANCODE_1]:
        equiped = 0
    if key_states[sdl2.SDL_SCANCODE_2]:
        equiped = 1
    if key_states[sdl2.SDL_SCANCODE_3]:
        equiped = 2
    if key_states[sdl2.SDL_SCANCODE_4]:
        equiped = 3
    if key_states[sdl2.SDL_SCANCODE_E]:
        interact = True

    if (dramController.NunChuk.buttonZ == 1):
        pakOp = True
        for i in range(-1, 2):
            for j in range(-1, 2):
                if wall_map[int(p_speler[1] + i), int(p_speler[0] + j)] != None:
                    if wall_map[int(p_speler[1] + i), int(p_speler[0] + j)].type == "crafting bench":
                        crafting = True

    elif key_states[sdl2.SDL_SCANCODE_F]:
        pakOp = True
        for i in range(-1, 2):
            for j in range(-1, 2):
                if wall_map[int(p_speler[1] + i), int(p_speler[0] + j)] != None:
                    if wall_map[int(p_speler[1] + i), int(p_speler[0] + j)].type == "crafting bench":
                        crafting = True

    if key_states[sdl2.SDL_SCANCODE_G]:
        drop = True

    if delta_p[0] != 0 or delta_p[1] != 0:

        if sprinting:
            stamina -= delta * main.STAMINALOSSMODIFIER
            hunger -= delta * main.SPRINTINGHUNGERMODIFIER
        elif stamina < 100:
            stamina += delta * main.STAMINAREGENMODIFIER

        delta_p = delta_p / np.linalg.norm(delta_p)
        p_speler = bewegen(delta, delta_p, r_speler, r_cameravlak, p_speler, door_map, world_map)

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        start = False
        settings = False
    if (dramController.buttonRed == 1):
        start = False
        settings = False

    return (p_speler, moet_afsluiten, stamina, hunger, equiped, interact, pakOp, drop, crafting, start, hp)


def draaien(r_speler, r_cameravlak, dramController):
    muisGeklikt = False
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            muisGeklikt = True
        if event.type == sdl2.SDL_MOUSEMOTION:
            beweging = (-1) * event.motion.xrel * main.SENSITIVITY
            rot = np.array(((np.cos(beweging), -np.sin(beweging)),
                            (np.sin(beweging), np.cos(beweging))))
            r_speler = np.dot(r_speler, rot)
            r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])

    if (dramController.NunChuk.joyX > 140):
        beweging = (-1) * np.abs(dramController.NunChuk.joyX - 129) * main.SENSITIVITY * 5
        rot = np.array(((np.cos(beweging), -np.sin(beweging)),
                        (np.sin(beweging), np.cos(beweging))))
        r_speler = np.dot(r_speler, rot)
        r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])

    if (dramController.NunChuk.joyX < 110):
        beweging = np.abs(dramController.NunChuk.joyX - 129) * main.SENSITIVITY * 5
        rot = np.array(((np.cos(beweging), -np.sin(beweging)),
                        (np.sin(beweging), np.cos(beweging))))
        r_speler = np.dot(r_speler, rot)
        r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])

    return (r_speler, r_cameravlak, muisGeklikt)





























