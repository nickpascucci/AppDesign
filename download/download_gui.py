#! /usr/bin/env python

"""This is a Python file."""

import sys
from PySide import QtUiTools
from PySide.QtCore import *
from PySide.QtGui import *
import download

__author__ = "Nick Pascucci (npascut1@gmail.com)"

class MainWindow(QWidget):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        ui_file = QFile("form.ui")
        ui_file.open(QFile.ReadOnly)
        window = loader.load(ui_file, self)
        ui_file.close()

        self.resize(400, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(window)
        self.scene = QGraphicsScene()
        window.graphicsView.setScene(self.scene)
        self.setLayout(layout)
        self.scene.addText('No images yet... Enter a URL and press'
                           ' "Download".')

    def download_images(self):
        pass
        
    def show_image(self):
        pass

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow(None)
    main_window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
   main()
