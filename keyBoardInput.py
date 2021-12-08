import sdl2
import sdl2.ext
import sdl2.sdlttf
import time


def keyBoardInput(key_states, pressTime, userInput, setting):

    if time.time() - pressTime > 0.2:
        if key_states[sdl2.SDL_SCANCODE_0 or key_states[sdl2.SDL_SCANCODE_KP_0]]:
            pressTime = time.time()
            userInput += "0"
        if key_states[sdl2.SDL_SCANCODE_1 or key_states[sdl2.SDL_SCANCODE_KP_1]]:
            pressTime = time.time()
            userInput += "1"
        if key_states[sdl2.SDL_SCANCODE_2 or key_states[sdl2.SDL_SCANCODE_KP_2]]:
            pressTime = time.time()
            userInput += "2"
        if key_states[sdl2.SDL_SCANCODE_3 or key_states[sdl2.SDL_SCANCODE_KP_3]]:
            pressTime = time.time()
            userInput += "3"
        if key_states[sdl2.SDL_SCANCODE_4 or key_states[sdl2.SDL_SCANCODE_KP_4]]:
            pressTime = time.time()
            userInput += "4"
        if key_states[sdl2.SDL_SCANCODE_5 or key_states[sdl2.SDL_SCANCODE_KP_5]]:
            pressTime = time.time()
            userInput += "5"
        if key_states[sdl2.SDL_SCANCODE_6 or key_states[sdl2.SDL_SCANCODE_KP_6]]:
            pressTime = time.time()
            userInput += "6"
        if key_states[sdl2.SDL_SCANCODE_7 or key_states[sdl2.SDL_SCANCODE_KP_7]]:
            pressTime = time.time()
            userInput += "7"
        if key_states[sdl2.SDL_SCANCODE_8 or key_states[sdl2.SDL_SCANCODE_KP_8]]:
            pressTime = time.time()
            userInput += "8"
        if key_states[sdl2.SDL_SCANCODE_9 or key_states[sdl2.SDL_SCANCODE_KP_9]]:
            pressTime = time.time()
            userInput += "9"

        if setting.azerty:
            if key_states[sdl2.SDL_SCANCODE_A]:
                pressTime = time.time()
                userInput += "q"
            if key_states[sdl2.SDL_SCANCODE_SEMICOLON]:
                pressTime = time.time()
                userInput += "m"
            if key_states[sdl2.SDL_SCANCODE_Z]:
                pressTime = time.time()
                userInput += "w"
            if key_states[sdl2.SDL_SCANCODE_W]:
                pressTime = time.time()
                userInput += "z"
            if key_states[sdl2.SDL_SCANCODE_Q]:
                pressTime = time.time()
                userInput += "a"

        else:
            if key_states[sdl2.SDL_SCANCODE_A]:
                pressTime = time.time()
                userInput += "a"
            if key_states[sdl2.SDL_SCANCODE_M]:
                pressTime = time.time()
                userInput += "m"
            if key_states[sdl2.SDL_SCANCODE_Z]:
                pressTime = time.time()
                userInput += "z"
            if key_states[sdl2.SDL_SCANCODE_W]:
                pressTime = time.time()
                userInput += "w"
            if key_states[sdl2.SDL_SCANCODE_Q]:
                pressTime = time.time()
                userInput += "q"


        if key_states[sdl2.SDL_SCANCODE_B]:
            pressTime = time.time()
            userInput += "b"
        if key_states[sdl2.SDL_SCANCODE_C]:
            pressTime = time.time()
            userInput += "c"
        if key_states[sdl2.SDL_SCANCODE_D]:
            pressTime = time.time()
            userInput += "d"
        if key_states[sdl2.SDL_SCANCODE_E]:
            pressTime = time.time()
            userInput += "e"
        if key_states[sdl2.SDL_SCANCODE_F]:
            pressTime = time.time()
            userInput += "f"
        if key_states[sdl2.SDL_SCANCODE_G]:
            pressTime = time.time()
            userInput += "g"
        if key_states[sdl2.SDL_SCANCODE_H]:
            pressTime = time.time()
            userInput += "h"
        if key_states[sdl2.SDL_SCANCODE_I]:
            pressTime = time.time()
            userInput += "i"
        if key_states[sdl2.SDL_SCANCODE_J]:
            pressTime = time.time()
            userInput += "j"
        if key_states[sdl2.SDL_SCANCODE_K]:
            pressTime = time.time()
            userInput += "k"
        if key_states[sdl2.SDL_SCANCODE_L]:
            pressTime = time.time()
            userInput += "l"
        if key_states[sdl2.SDL_SCANCODE_N]:
            pressTime = time.time()
            userInput += "n"
        if key_states[sdl2.SDL_SCANCODE_O]:
            pressTime = time.time()
            userInput += "o"
        if key_states[sdl2.SDL_SCANCODE_P]:
            pressTime = time.time()
            userInput += "p"
        if key_states[sdl2.SDL_SCANCODE_R]:
            pressTime = time.time()
            userInput += "r"
        if key_states[sdl2.SDL_SCANCODE_S]:
            pressTime = time.time()
            userInput += "s"
        if key_states[sdl2.SDL_SCANCODE_T]:
            pressTime = time.time()
            userInput += "t"
        if key_states[sdl2.SDL_SCANCODE_U]:
            pressTime = time.time()
            userInput += "u"
        if key_states[sdl2.SDL_SCANCODE_V]:
            pressTime = time.time()
            userInput += "v"
        if key_states[sdl2.SDL_SCANCODE_X]:
            pressTime = time.time()
            userInput += "x"
        if key_states[sdl2.SDL_SCANCODE_Y]:
            pressTime = time.time()
            userInput += "y"

        if key_states[sdl2.SDL_SCANCODE_SPACE]:
            pressTime = time.time()
            userInput += " "

        if key_states[sdl2.SDL_SCANCODE_BACKSPACE]:
            newUserInput = ""
            for i in range(0, len(userInput) - 1):
                newUserInput += userInput[i]
            userInput = newUserInput
            pressTime = time.time()

    return(userInput, pressTime)