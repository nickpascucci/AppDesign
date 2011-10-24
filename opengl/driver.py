#! /usr/bin/env python

"""Driver for OpenGL camera/snowmen simulation."""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from scene import Scene
from snowman import Snowman

__author__ = "Nick Pascucci (npascut1@gmail.com)"

name = "Snowmen"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

class Renderer(object):
    def __init__(self):
        self.scene = Scene()
        self.scene.add(Snowman())
    
    def setup(self):
        # Initialize the drawing environment (create main windows, etc)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        glutCreateWindow(name)

        # Set up keyboard listeners.
        glutKeyboardFunc(self.on_key)

        # Set up lighting.
        # TODO Move this to the scene render.
        light_diffuse = (1, 1, 1, 1)
        light_position = (.5, 1, -.5, 1)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def start(self):
        glutDisplayFunc(self.render)
        glutMainLoop()

    def render(self):
        self.scene.render()

    def on_key(self, key, x, y):
        print "Received", key
        if key == "a":
            self.scene.camera.translate(x=0.05)
        elif key == "d":
            self.scene.camera.translate(x=-0.05)
        elif key == "s":
            self.scene.camera.translate(y=0.05)
        elif key == "w":
            self.scene.camera.translate(y=-0.05)
        elif key == "e":
            self.scene.camera.translate(z=0.05)
        elif key == "q":
            self.scene.camera.translate(z=-0.05)
        self.render()

def main():
    renderer = Renderer()
    renderer.setup()
    renderer.start()

if __name__ == "__main__":
    main()
