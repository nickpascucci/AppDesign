"""This is a Python file."""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

__author__ = "Nick Pascucci (npascut1@gmail.com)"

class Camera(object):
    def __init__(self):
        self.x = 0
        self.y = 0 
        self.z = 0
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0

    def adjust(self):
        """Applies a translation and a rotation to the camera.

        The translation is applied first, placing the camera at
        (x,y,z) in the old coordinate space, and then rotating it to
        point in the direction x_rotation, y_rotation, z_rotation.
        """
        glTranslate(self.x, self.y, self.z)
        glRotate(self.x_rotation, 1, 0, 0)
        glRotate(self.y_rotation, 0, 1, 0)
        glRotate(self.z_rotation, 0, 0, 1)

    # TODO Make this translate relative to current rotation.
    def translate(self, x=0, y=0, z=0):
        """Translate the camera in 3-Space.

        @param x The amount to translate the camera in the x axis.
        @param y The amount to translate the camera in the y axis.
        @param z The amount to translate the camera in the z axis.
        """
        self.x += x
        self.y += y
        self.z += z
        print ("Camera state:\nx: %s\ny: %s\n"
        "z:%s\n" % (self.x, self.y, self.z))

    def rotate(self, x=0, y=0, z=0):
        self.x_rotation += x
        self.y_rotation += y
        self.z_rotation += z
        print ("Camera state:\nx: %s\ny: %s\n"
        "z:%s\n" % (self.x_rotation, self.y_rotation, self.z_rotation))
