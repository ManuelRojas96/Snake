import glfw
import sys
from typing import Union

class Controller(object):

    def __init__(self):
        self.model = None

    def set_model(self, m):
        self.model = m

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        elif key == glfw.KEY_W and action == glfw.PRESS:
            pass

        elif key == glfw.KEY_S and action == glfw.PRESS:
            pass
        
        elif key == glfw.KEY_A and action == glfw.PRESS:
            pass
        
        elif key == glfw.KEY_D and action == glfw.PRESS:
            pass

        else:
            print('Unknown key')