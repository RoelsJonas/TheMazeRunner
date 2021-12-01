import math
import time
import numpy as np
import sdl2
import sdl2.ext
import sdl2.sdlttf
import main

class text:
    textFile = ""
    textTimer = 0
    font = 0
    x = 0
    y = 0
    b = 0
    h = 0

    def __init__(self, textFile, x, y, b, h):
        self.textFile = textFile
        self.textTimer = 0
        self.font = sdl2.ext.FontManager(font_path="resources/OpenSans.ttf", size=50, color=(0, 0, 0))
        self.x = x
        self.y = y
        self.b = b
        self.h = h

    def renderText(self, delta, renderer, factory):
        if(self.textTimer > 0):
            text = factory.from_text(self.textFile, fontmanager=self.font)
            renderer.copy(text, dstrect=(self.x, self.y, self.b, self.h))
            self.textTimer -= delta


