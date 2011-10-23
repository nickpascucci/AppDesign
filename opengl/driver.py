#! /usr/bin/env python

"""Driver for OpenGL camera/snowmen simulation."""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from scene import Scene
from camera import Camera

__author__ = "Nick Pascucci (npascut1@gmail.com)"

name = "Snowmen"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

class Renderer(object):
    def __init__(self):
        self.scene = Scene()
    
    def setup(self):
        # Initialize the drawing environment (create main windows, etc)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        glutCreateWindow(name)

    def start(self):
        glutDisplayFunc(self.render)
        glutMainLoop()

    def render(self):
        self.scene.render()

def main():
    renderer = Renderer()
    renderer.setup()
    renderer.start()

if __name__ == "__main__":
    main()
