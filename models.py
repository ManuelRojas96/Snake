import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import my_shapes
import random

from OpenGL.GL import *
import random
from typing import List

class Snake(object):
    def __init__(self, frame_width, frame_height, tiles = 50):
        self.tiles = min(50, max(10, tiles))
        self.frame_dim = [frame_width, frame_height]
        self.locationX = int(tiles/2)
        self.locationY = int(tiles/2)
        self.direction = "A"    # "A" means "left" according to our WASD control buttons
        self.face_orientation = "A"
        self.life_status = True
        self.movement_queue = []
        self.remaining_moves = []
        self.body_count = 0
        self.last_position = [self.locationX, self.locationY]
        self.gpu_body = es.toGPUShape(bs.createTextureQuad("question_box.png"), GL_CLAMP, GL_NEAREST)
        self.special_counter = 0
        
        # Aspect ratio
        ar = frame_height/frame_width
        #aspect_ratio_tr = tr.scale(ar, 1, 0)
        self.dimensions = [ar*0.95 * 2*4/5, 0.95 * 2*4/5]

        gpu_snake = es.toGPUShape(bs.createTextureQuad("boo_l.png"), GL_CLAMP, GL_NEAREST)
        gpu_body = es.toGPUShape(bs.createTextureQuad("question_box.png"), GL_CLAMP, GL_NEAREST)

        snake_head = sg.SceneGraphNode('snake_head')
        snake_head.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + self.locationX + 0.5, self.tiles/2 - self.locationY - 0.5, 0)])
        snake_head.childs += [gpu_snake]

        #snake_body = sg.SceneGraphNode('snake_body')
        #snake_body.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + self.locationX + 0.5, self.tiles/2 - self.locationY - 0.5, 0)])
        #snake_body.childs += [gpu_body]

        snake = sg.SceneGraphNode('snake')
        snake.childs += [snake_head]

        snake_tr = sg.SceneGraphNode('snake_TR')
        snake_tr.childs += [snake]

        self.model = snake_tr

    def draw(self, pipeline):
        if self.direction == "D":
            self.face_orientation = "D"
            new_gpu_snake = es.toGPUShape(bs.createTextureQuad("boo_r.png"), GL_CLAMP, GL_NEAREST)
            sg.findNode(self.model, "snake").childs = [new_gpu_snake]
        elif self.direction == "A":
            self.face_orientation = "A"
            new_gpu_snake = es.toGPUShape(bs.createTextureQuad("boo_l.png"), GL_CLAMP, GL_NEAREST)
            sg.findNode(self.model, "snake_head").childs = [new_gpu_snake]
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def move(self, apple):
        self.check_life()
        if not self.life_status:
            return
        movement = tr.identity()
        if self.direction == "W":
            movement = tr.translate(0, 1, 0)
            self.locationY += 1
        elif self.direction == "A":
            movement = tr.translate(-1, 0, 0)
            self.locationX += -1
        elif self.direction == "S":
            movement = tr.translate(0, -1, 0)
            self.locationY += -1
        elif self.direction == "D":
            movement = tr.translate(1, 0, 0)
            self.locationX += 1
        sg.findNode(self.model, "snake").transform = tr.matmul([sg.findTransform(self.model, "snake"), movement])

    def set_direction(self, new_direction):
        if self.direction == "A" and new_direction == "D":
            pass
        elif self.direction == "D" and new_direction == "A":
            pass
        elif self.direction == "S" and new_direction == "W":
            pass
        elif self.direction == "W" and new_direction == "S":
            pass
        elif self.life_status:
            self.direction = new_direction

    def get_direction(self):
        return self.direction

    def get_current_location(self):
        return self.locationX, self.locationY

    def check_life(self):
        if self.locationX > 9 or self.locationX < 0:
            self.die()
        if self.locationY < 1 or self.locationY > 10:
            self.die()

    def die(self):
        self.life_status = False

    def get_life_status(self):
        return self.life_status

    def eat_apple(self, apple):
        if self.get_current_location() == apple.get_current_position():
            #self.add_body()
            return True
        else:
            return False

    def body_movement(self):
        for i in range(self.body_count):
            sg.findNode(self.model, f'snake_body_{i}').transform = tr.matmul([sg.findTransform(self.model, f'snake_body_{i}'), (self.remaining_moves[i].pop() if len(self.remaining_moves[i]) != 0 else tr.identity())])


    def update_movement(self, movement):
        for i in range(self.body_count):
            self.remaining_moves[i] = [movement] + self.remaining_moves[i]
    
    def add_body(self, movement):
        print("toy añadiendo body")
        snake_body = sg.SceneGraphNode(f'snake_body_{self.body_count}')
        snake_body.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + self.last_position[0] + 0.5, -self.tiles/2 + self.last_position[1] - 0.5, 0)])
        snake_body.childs += [self.gpu_body]
        self.special_counter = self.body_count
        self.body_count += 1
        

        sg.findNode(self.model, "snake").childs += [snake_body]
        self.remaining_moves.append([])
        for i in range(self.body_count):
            self.remaining_moves[self.body_count - 1] += [tr.identity()]
    
class Apple(object):
    def __init__(self, frame_width, frame_height, tiles = 50):
        self.tiles = min(50, max(10, tiles))
        self.frame_dim = [frame_width, frame_height]
        self.locationX = random.randint(0, self.tiles - 1)
        self.locationY = random.randint(0, self.tiles - 1)
        
        # Aspect ratio
        ar = frame_height/frame_width
        #aspect_ratio_tr = tr.scale(ar, 1, 0)
        self.dimensions = [ar*0.95 * 2*4/5, 0.95 * 2*4/5]

        gpu_apple = es.toGPUShape(my_shapes.apple())

        apple = sg.SceneGraphNode('apple')
        apple.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + self.locationX + 0.5, -self.tiles/2 + self.locationY - 0.5, 0)])
        apple.childs += [gpu_apple]

        apple_tr = sg.SceneGraphNode('apple_TR')
        apple_tr.childs += [apple]

        self.model = apple_tr
    
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def get_current_position(self):
        return self.locationX, self.locationY

class Board(object):
    def __init__(self, frame_width, frame_height, tiles = 50):
        # Add warning if width is beyond 50 or under 10
        self.tiles = min(50, max(10, tiles))
        self.frame_dim = [frame_width, frame_height]
        
        # Aspect ratio
        ar = frame_height/frame_width
        #aspect_ratio_tr = tr.scale(ar, 1, 0)
        self.dimensions = [ar*0.95 * 2*4/5, 0.95 * 2*4/5]

        gpu_tiles = [es.toGPUShape(bs.createColorQuad(1, 0.91, 0.84)), es.toGPUShape(bs.createColorQuad(0.99, 0.84, 0.61))]

        tiles = []
        count = 0

        for x in range(self.tiles):
            tiles.append([])
            for y in range(self.tiles):
                tiles[x].append( sg.SceneGraphNode(f'tile{x}_{y}') )
                tiles[x][y].transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + x + 0.5, self.tiles/2 - y - 0.5, 0)])
                tiles[x][y].childs += [gpu_tiles[(x + y)%2]]

        board_TR = sg.SceneGraphNode('board_TR')
        for i in range(len(tiles)):
            board_TR.childs += tiles[i]

        self.model = board_TR

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

class Background(object):
    def __init__(self, width, height):
        # Frame dimensions
        self.width = width
        self.height = height
        self.alive = True
        
        self.g_over = None

        # Outer board dimensions
        self.dimensions = [0.5 * self.width * 9/16 * 16/9 * 2, 0.5 * self.height * 2 * 4/5]
        aspect_ratio_tr = tr.scale(self.height/self.width, 1, 0)

        gpu_bground = es.toGPUShape(bs.createColorQuad(0.05, 0.55, 0.23))

        bground = sg.SceneGraphNode('background')
        bground.transform = tr.matmul([aspect_ratio_tr, tr.scale(2 * self.width/self.height, 2 * 4/5, 0)])
        bground.childs += [gpu_bground]

        bground_tr = sg.SceneGraphNode('background_TR')
        bground_tr.childs += [bground]

        self.model = bground_tr

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
    
    def get_dimensions(self):
        return self.dimensions

    def game_over(self):
        gpu_game_over = es.toGPUShape(bs.createTextureQuad("game_over.png"), GL_CLAMP, GL_NEAREST)

        game_over = sg.SceneGraphNode('game_over_banner')
        game_over.transform = tr.matmul([tr.scale(2, 1/5, 0), tr.translate(0, 4.5, 0)])
        game_over.childs += [gpu_game_over]

        game_over_tr = sg.SceneGraphNode('game_over_banner_TR')
        game_over_tr.childs += [game_over]

        self.g_over = game_over_tr
        self.alive = False

    def draw_game_over(self, pipeline):
        sg.drawSceneGraphNode(self.g_over, pipeline, "transform")