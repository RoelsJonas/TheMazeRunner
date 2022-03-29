import main
import numpy

class ObjectWrapper:
    renderer = None
    Window = None

    def __init__(self, renderer, window):
        self.renderer = renderer
        self.window = window