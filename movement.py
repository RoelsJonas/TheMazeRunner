import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import main
import doors

def bewegen(delta, delta_p, r_speler, r_cameravlak, p_speler, door_map):

    p_speler_nieuw = np.array([p_speler[0], p_speler[1]])

    p_speler_nieuw += delta * delta_p[0] * r_speler
    p_speler_nieuw += delta * delta_p[1] * r_cameravlak

    if main.world_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 0:
        p_speler = p_speler_nieuw
        return (p_speler)

    print(door_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])].state)
    if main.world_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 2 and door_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])].state == 0:
        p_speler = p_speler_nieuw

    elif main.world_map[int(p_speler[1]), int(p_speler_nieuw[0])] == 2 and door_map[int(p_speler[1]), int(p_speler_nieuw[0])].state == 0:
        p_speler[0] = p_speler_nieuw[0]

    elif main.world_map[int(p_speler_nieuw[1]), int(p_speler[0])] == 2 and door_map[int(p_speler_nieuw[1]), int(p_speler[0])].state == 0:
        p_speler[1] = p_speler_nieuw[1]

    elif main.world_map[int(p_speler[1]), int(p_speler_nieuw[0])] == 0:
        p_speler[0] = p_speler_nieuw[0]
        return (p_speler)
    elif main.world_map[int(p_speler_nieuw[1]), int(p_speler[0])] == 0:
        p_speler[1] = p_speler_nieuw[1]
        return (p_speler)

    return(p_speler)


def polling(delta,p_speler,r_speler, r_cameravlak, stamina, hunger, equiped, door_map):
    moet_afsluiten = False
    damage = 0
    delta_p = np.array([0,0])
    key_states = sdl2.SDL_GetKeyboardState(None)
    interact = False
    pakOp = False

    if key_states[sdl2.SDL_SCANCODE_LSHIFT] and stamina > 0:
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

    if key_states[sdl2.SDL_SCANCODE_F]:
        pakOp = True

    if delta_p[0] != 0 or delta_p[1] != 0:

        if sprinting:
            stamina -= delta * main.STAMINALOSSMODIFIER
            hunger -= delta * main.SPRINTINGHUNGERMODIFIER
        elif stamina < 100:
            stamina += delta * main.STAMINAREGENMODIFIER

        delta_p = delta_p / np.linalg.norm(delta_p)
        p_speler = bewegen(delta, delta_p, r_speler, r_cameravlak, p_speler, door_map)

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True

    return(p_speler, moet_afsluiten, stamina, hunger, equiped, interact, pakOp)


def draaien(r_speler, r_cameravlak):
    events = sdl2.ext.get_events()
    damage = 0
    for event in events:
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            damage = 15
        if event.type == sdl2.SDL_MOUSEMOTION:
            beweging = (-1) * event.motion.xrel * main.SENSITIVITY
            rot = np.array(((np.cos(beweging), -np.sin(beweging)),
                            (np.sin(beweging), np.cos(beweging))))
            r_speler = np.dot(r_speler, rot)
            r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])

    return(r_speler, r_cameravlak, damage)
