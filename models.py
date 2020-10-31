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
        
        # Aspect ratio
        ar = frame_height/frame_width
        #aspect_ratio_tr = tr.scale(ar, 1, 0)
        self.dimensions = [ar*0.95 * 2*4/5, 0.95 * 2*4/5]

        gpu_snake = es.toGPUShape(bs.createTextureQuad("question_box.png"), GL_CLAMP_TO_EDGE, GL_NEAREST)

        snake = sg.SceneGraphNode('snake')
        #snake.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + self.locationX + 0.5, self.tiles/2 - self.locationY - 0.5, 0)])
        snake.childs += [gpu_snake]

        snake_tr = sg.SceneGraphNode('snake_TR')
        snake_tr.childs += [snake]

        self.model = snake_tr

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

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
        apple.transform = tr.matmul([tr.scale(self.dimensions[0]/self.tiles, self.dimensions[1]/self.tiles, 0), tr.translate(-self.tiles/2 + self.locationX + 0.5, self.tiles/2 - self.locationY - 0.5, 0)])
        apple.childs += [gpu_apple]

        apple_tr = sg.SceneGraphNode('apple_TR')
        apple_tr.childs += [apple]

        self.model = apple_tr
    
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def current_position(self):
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
    