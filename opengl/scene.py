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
        """Draw the scene."""
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Adjust the scene to match current camera settings.
        self.camera.adjust()
        
        # Set up lighting.
        light_diffuse = (1, 1, 1, 1)
        light_position = (0, 5, 0, 1)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        for entity in self.entities:
            entity.render()
        glFlush()

    def add(self, entity):
        """Add a new entity to scene."""
        self.entities.append(entity)
