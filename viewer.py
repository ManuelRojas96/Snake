import glfw
from OpenGL.GL import GL_LINES, glClearColor, GL_REPEAT, GL_NEAREST
import sys

from models import *
from controller import Controller

if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1280
    height = 720

    window = glfw.create_window(width, height, 'Snake v2.0: Electric Boogaloo', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controlador = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
    pipeline2 = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    #glUseProgram(pipeline.shaderProgram)

    # Setting our RGB values (cause the Internet mostly shows integer values)
    r = 153
    g = 255
    b = 255

    # Setting up the clear screen color
    glClearColor(r/255, g/255, b/255, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Building our objects
    # -----
    tiles = 10
    background = Background(width, height)
    board = Board(width, height, tiles)
    apple = Apple(width, height, tiles)
    snake = Snake(width, height, tiles)

    t0 = 0

    while not glfw.window_should_close(window):

        # Defining our dt
        ti = glfw.get_time()
        dt = ti - t0
        t0 = ti

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        
        # Setting every model
        # ----------
        glUseProgram(pipeline.shaderProgram)
        background.draw(pipeline)
        board.draw(pipeline)
        apple.draw(pipeline)
        glUseProgram(pipeline2.shaderProgram)
        snake.draw(pipeline2)
        
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()