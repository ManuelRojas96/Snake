import glfw
import sys
from typing import Union
from models import Apple

class Controller(object):

    def __init__(self):
        self.model = None
        self.pause = False

    def set_model(self, m):
        self.model = m

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        elif key == glfw.KEY_W and action == glfw.PRESS:
            self.model.set_direction("W")

        elif key == glfw.KEY_A and action == glfw.PRESS:
            self.model.set_direction("A")
        
        elif key == glfw.KEY_S and action == glfw.PRESS:
            self.model.set_direction("S")
        
        elif key == glfw.KEY_D and action == glfw.PRESS:
            self.model.set_direction("D")

        elif key == glfw.KEY_ENTER and action == glfw.PRESS:
            self.pause = not self.pause

    def is_paused(self):
        return self.pause