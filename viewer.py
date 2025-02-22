import glfw
from OpenGL.GL import GL_LINES, glClearColor, GL_REPEAT, GL_NEAREST
import sys, time

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
    tiles = int(input("Bienvenido a 'Snake v2.0: Electric Boogaloo'.\n" + \
        "A continuación, ingrese las dimensiones del tablero en el que jugará. Este valor debe estar entre 10 y 50.\n" + \
            "Si ingresa un número muy grande, o muy chico, se ajustará al límite más cercano.\n" + \
                "Se recomienda jugar con valores de dimensión entre 10 y 20. Jugar con más de 20 podría provocar una caída de rendimiento.\n"))
    print("Valor seleccionado: ", min(50, max(10, tiles)))
    background = Background(width, height)
    board = Board(width, height, tiles)
    apple = Apple(width, height, tiles)
    snake = Snake(width, height, tiles)
    snake.set_current_apple(apple)
    controlador.set_model(snake)

    t0 = 0
    movement_t0 = 0

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

        if not snake.life_status:
            background.game_over()
            background.draw_game_over(pipeline2, ti%300)

        

        # Movement of our snake
        movement_dt = t0-movement_t0
        if movement_dt >= 0.3 and not controlador.is_paused():
            snake.move_all()
            movement_t0 = t0
            if snake.check_apple():
                apple = Apple(width, height, tiles)
                while(snake.clash(apple.get_current_position())):
                    apple = Apple(width, height, tiles)
                snake.set_current_apple(apple)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()