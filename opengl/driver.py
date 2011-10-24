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
        sn2 = Snowman()
        sn3 = Snowman()
        sn2.x = 3
        sn3.z = 2
        self.scene.add(sn2)
        self.scene.add(sn3)
        self.scene.camera.translate(0, -.5, -4)

    def setup(self):
        # Initialize the drawing environment (create main windows, etc)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        glutCreateWindow(name)

        glShadeModel(GL_SMOOTH)

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)                                # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)                             # Enables Depth Testing
        glShadeModel(GL_SMOOTH)                             # Enables Smooth Color Shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                                    # Reset The Projection Matrix

        # Calculate The Aspect Ratio Of The Window
        gluPerspective(45.0, float(WINDOW_WIDTH)/float(WINDOW_HEIGHT), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)

        # Set up keyboard listeners.
        glutKeyboardFunc(self.on_key)

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
        elif key == "j":
            self.scene.camera.rotate(y=-5)
        elif key == "l":
            self.scene.camera.rotate(y=5)
        elif key == "k":
            self.scene.camera.rotate(x=5)
        elif key == "i":
            self.scene.camera.rotate(x=-5)
        elif key == "u":
            self.scene.camera.rotate(z=5)
        elif key == "o":
            self.scene.camera.rotate(z=-5)

        self.render()

def main():
    renderer = Renderer()
    renderer.setup()
    renderer.start()

if __name__ == "__main__":
    main()
