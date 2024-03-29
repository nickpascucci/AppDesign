"""A class representing a snowman object for OpenGL."""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

__author__ = "Nick Pascucci (npascut1@gmail.com)"

class Snowman(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def render(self):
        """Render this snowman."""
        # Set the color (red, green, blue values from 0.0 to 1.0) to
        # paint in
        glColor3f(1, 1, 1)  

        # Translate the current location by x, y, and z
        glTranslatef(self.x, self.y, self.z)  

        # Paint a solid sphere (like a snowball)
        # Arg 1 is the radius of the sphere
        # Arg 2 is the number of subdivisions around Z
        # (number longitude lines)
        # Arg 3 is the number of subdivisions along Z
        # (number latitude lines)
        glutSolidSphere(.4, 90, 90)
        glTranslate(0, .55, 0)  # Move for the second sphere
        
        glutSolidSphere(.25, 90, 90)
        glTranslate(0, .35, 0)  # Move for the third sphere
        
        glutSolidSphere(.18, 90, 90)
        glTranslate(0, -.9, 0)  # Move back
