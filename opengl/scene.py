"""Storage and rendering for scene elements."""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from camera import Camera

__author__ = "Nick Pascucci (npascut1@gmail.com)"

class Scene(object):
    def __init__(self):
        self.camera = Camera()
        self.entities = []

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.camera.adjust()
        for entity in self.entities:
            entity.render()
        glFlush()

    def add(self, entity):
        self.entities.append(entity)
