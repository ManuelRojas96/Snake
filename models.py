import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

from OpenGL.GL import glClearColor
import random
from typing import List

class Snake(object):
    def __init__(self):
        pass

    def draw(self, pipeline):
        pass

class Apple(object):
    def __init__(self):
        pass
    
    def draw(self, pipeline):
        pass

class Board(object):
    def __init__(self, width, height, tiles = 50):
        # Add warning if width is beyond 50 or under 10
        self.tiles = 50#min(50, max(10, tiles))
        self.width = width
        self.height = height
        
        # Aspect ratio
        ar = height/width
        aspect_ratio_tr = tr.scale(ar, 1, 0)

        gpu_tiles = [es.toGPUShape(bs.createColorQuad(0, 0.93, 0)), es.toGPUShape(bs.createColorQuad(0, 1, 0.2))]

        tiles = []
        count = 0

        test_tile = sg.SceneGraphNode('test_tile')
        test_tile.transform = tr.matmul([aspect_ratio_tr, tr.scale(0.95 * 2*4/5/self.tiles, 0.95 * 2*4/5/self.tiles, 0)])
        test_tile.childs += [gpu_tiles[1]]

        #for x in range(self.tiles):
        #    tiles.append([])
        #    for y in range(self.tiles):
        #        tiles[x][y] = sg.SceneGraphNode(f'tile{x}_{y}')
        #        tiles[x][y].transform = tr.matmul([aspect_ratio_tr, tr.scale(self.width * ar/self.tiles ,self.height*2*4/5/self.tiles, 0)])

        board_TR = sg.SceneGraphNode('board_TR')
        board_TR.childs += [test_tile]

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
    