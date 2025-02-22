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
        self.locationX = int(self.tiles/2)
        self.locationY = int(self.tiles/2)
        self.last_position = [self.locationX, self.locationY]
        self.last_direction = "A"    # "A" means "left" according to our WASD control buttons
        self.next_direction = "A"
        self.face_orientation = "A"
        self.life_status = True
        self.body_queue = []
        self.movement_queue = []
        self.occupied_positions = [[self.last_position]]

        self.recently_added_body = False

        self.gpu_body = es.toGPUShape(bs.createTextureQuad("question_box.png"), GL_CLAMP, GL_NEAREST)
        
        self.current_apple = None
        
        # Aspect ratio
        ar = frame_height/frame_width
        self.dimensions = [ar*0.95 * 2*4/5, 0.95 * 2*4/5]

        gpu_snake = es.toGPUShape(bs.createTextureQuad("boo_l.png"), GL_CLAMP, GL_NEAREST)

        snake_head = sg.SceneGraphNode('snake_head')
        snake_head.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + self.locationX + 0.5, -self.tiles/2 + self.locationY - 0.5, 0)])
        snake_head.childs += [gpu_snake]

        snake = sg.SceneGraphNode('snake')
        snake.childs += [snake_head]

        snake_tr = sg.SceneGraphNode('snake_TR')
        snake_tr.childs += [snake]

        self.model = snake_tr

    def draw(self, pipeline):
        if self.last_direction == "D":
            self.face_orientation = "D"
            new_gpu_snake = es.toGPUShape(bs.createTextureQuad("boo_r.png"), GL_CLAMP, GL_NEAREST)
            sg.findNode(self.model, "snake_head").childs = [new_gpu_snake]
        elif self.last_direction == "A":
            self.face_orientation = "A"
            new_gpu_snake = es.toGPUShape(bs.createTextureQuad("boo_l.png"), GL_CLAMP, GL_NEAREST)
            sg.findNode(self.model, "snake_head").childs = [new_gpu_snake]
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def move_all(self):
        self.check_life()
        if not self.life_status:
            return
        self.move(self.movement_queue)
        movement = tr.identity()
        if self.next_direction == "W":
            movement = tr.translate(0, 1, 0)
            self.locationY += 1
        elif self.next_direction == "A":
            movement = tr.translate(-1, 0, 0)
            self.locationX += -1
        elif self.next_direction == "S":
            movement = tr.translate(0, -1, 0)
            self.locationY += -1
        elif self.next_direction == "D":
            movement = tr.translate(1, 0, 0)
            self.locationX += 1
        self.queue_movement(self.next_direction)
        self.last_direction = self.next_direction
        if self.check_apple():
            self.eat_apple()
        self.last_position = [self.locationX, self.locationY]
        self.occupied_positions = [self.last_position] + self.occupied_positions[1:]
        sg.findNode(self.model, "snake_head").transform = tr.matmul([sg.findTransform(self.model, "snake_head"), movement])

    def set_direction(self, new_direction):
        if self.last_direction == "A" and new_direction == "D":
            pass
        elif self.last_direction == "D" and new_direction == "A":
            pass
        elif self.last_direction == "S" and new_direction == "W":
            pass
        elif self.last_direction == "W" and new_direction == "S":
            pass
        elif self.life_status:
            self.next_direction = new_direction

    def get_direction(self):
        return self.last_direction

    def get_current_location(self):
        return self.locationX, self.locationY

    def check_life(self):
        if self.locationX > (self.tiles - 1) or self.locationX < 0 or self.locationY < 1 or self.locationY > (self.tiles) or self.clash([self.locationX, self.locationY], is_head = True):
            self.die()
        

    def die(self):
        self.life_status = False

    def get_life_status(self):
        return self.life_status

    def check_apple(self):
        if self.get_current_location() == self.current_apple.get_current_position():
            return True
        else:
            return False

    def eat_apple(self):
        self.add_body()

    def set_current_apple(self, apple):
        self.current_apple = apple

    def add_body(self):
        posX = self.body_queue[len(self.body_queue) - 1]["last_position"][0] if len(self.body_queue) > 0 else self.last_position[0]
        posY = self.body_queue[len(self.body_queue) - 1]["last_position"][1] if len(self.body_queue) > 0 else self.last_position[1]
        snake_body = sg.SceneGraphNode(f'snake_body_{len(self.body_queue)}')
        snake_body.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + posX + 0.5, -self.tiles/2 + posY - 0.5, 0)])
        snake_body.childs += [self.gpu_body]

        self.body_queue.append({"name": f'snake_body_{len(self.body_queue)}', "position": [posX, posY], "last_position": [posX, posY]})

        sg.findNode(self.model, "snake").childs += [snake_body]

    def queue_movement(self, direction):
        self.movement_queue.append(direction)

    def move(self, move_Q):
        moveX = 0
        moveY = 0
        movement = tr.identity()
        body_positions = []
        for i in range(len(self.body_queue)):
            direction = move_Q[len(move_Q) - 1 - i]
            if direction == "W":
                movement = tr.translate(0, 1, 0)
                moveY = 1
            elif direction == "A":
                movement = tr.translate(-1, 0, 0)
                moveX = -1
            elif direction == "S":
                movement = tr.translate(0, -1, 0)
                moveY = -1
            elif direction == "D":
                movement = tr.translate(1, 0, 0)
                moveX = 1
            sg.findNode(self.model, self.body_queue[i]["name"]).transform = tr.matmul([sg.findTransform(self.model,  self.body_queue[i]["name"]), movement])
            self.body_queue[i]["last_position"][0] = self.body_queue[i]["position"][0]
            self.body_queue[i]["last_position"][1] = self.body_queue[i]["position"][1]
            self.body_queue[i]["position"][0] = self.body_queue[i]["position"][0] + moveX
            self.body_queue[i]["position"][1] = self.body_queue[i]["position"][1] + moveY
            moveX = 0
            moveY = 0
            body_positions.append(self.body_queue[i]["position"])
        
        self.occupied_positions = self.occupied_positions[0] + body_positions
            
    def clash(self, node_position, is_head = False):
        if is_head:
            if list(node_position) in self.occupied_positions[1:]:
                return True
            else:
                return False
        else:
            if list(node_position) in self.occupied_positions:
                return True
            else:
                return False

class Apple(object):
    def __init__(self, frame_width, frame_height, tiles = 50):
        self.tiles = min(50, max(10, tiles))
        self.frame_dim = [frame_width, frame_height]
        self.locationX = random.randint(0, self.tiles - 1)
        self.locationY = random.randint(1, self.tiles)
        
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
        game_over.transform = tr.matmul([tr.scale(2.3, 1/5, 0), tr.translate(0, 0, 0)])     # traslation to top was 4.5
        game_over.childs += [gpu_game_over]

        game_over_tr = sg.SceneGraphNode('game_over_banner_TR')
        game_over_tr.childs += [game_over]

        self.g_over = game_over_tr
        self.alive = False

    def draw_game_over(self, pipeline, dt):
        sg.findNode(self.g_over, "game_over_banner_TR").transform = tr.matmul([sg.findTransform(self.g_over, "game_over_banner_TR"), tr.rotationZ(dt)])
        sg.drawSceneGraphNode(self.g_over, pipeline, "transform")
