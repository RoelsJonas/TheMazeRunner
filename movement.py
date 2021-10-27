import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import main

def bewegen(delta, delta_p, r_speler, r_cameravlak, p_speler):

    p_speler_nieuw = np.array([p_speler[0], p_speler[1]])

    dichtste_afstand = 0.2

    p_speler_nieuw += delta * delta_p[0] * r_speler
    p_speler_nieuw += delta * delta_p[1] * r_cameravlak

    if main.world_map[int(p_speler_nieuw[1]), int(p_speler_nieuw[0])] == 0:
        p_speler = p_speler_nieuw

    elif main.world_map[int(p_speler[1]), int(p_speler_nieuw[0])] == 0:
        p_speler[0] = p_speler_nieuw[0]

    elif main.world_map[int(p_speler_nieuw[1]), int(p_speler[0])] == 0:
        p_speler[1] = p_speler_nieuw[1]

    return(p_speler)


def polling(delta,p_speler,r_speler, r_cameravlak, stamina, hunger):
    moet_afsluiten = False

    delta_p = np.array([0,0])
    key_states = sdl2.SDL_GetKeyboardState(None)

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

    if delta_p[0] != 0 or delta_p[1] != 0:

        if sprinting:
            stamina -= delta * main.STAMINALOSSMODIFIER
            hunger -= delta * main.SPRINTINGHUNGERMODIFIER
        elif stamina < 100:
            stamina += delta * main.STAMINAREGENMODIFIER

        delta_p = delta_p / np.linalg.norm(delta_p)
        p_speler = bewegen(delta, delta_p, r_speler, r_cameravlak, p_speler)

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True

    return(p_speler, moet_afsluiten, stamina, hunger)


def draaien(r_speler, r_cameravlak):
    events = sdl2.ext.get_events()

    for event in events:
        if event.type == sdl2.SDL_MOUSEMOTION:
            beweging = (-1) * event.motion.xrel * main.SENSITIVITY
            rot = np.array(((np.cos(beweging), -np.sin(beweging)),
                            (np.sin(beweging), np.cos(beweging))))
            r_speler = np.dot(r_speler, rot)
            r_cameravlak = np.array([r_speler[1], -1 * r_speler[0]])

    return(r_speler, r_cameravlak)
