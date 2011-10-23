"""A class representing a snowman object for OpenGL."""

__author__ = "Nick Pascucci (npascut1@gmail.com)"

class Snowman(object):
    def __init__(self):
        pass

    def render(self):
        glutSphere(1, 1, 1)
