#! /usr/bin/env python

"""This is a Python file."""

import os
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

        self.urlBar = window.urlBar
        self.view = window.graphicsView
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.previousButton = window.previousButton
        self.nextButton = window.nextButton
        self.montageButton = window.montageButton

        window.downloadButton.clicked.connect(self.download_images)
        self.previousButton.clicked.connect(self.previous_image)
        self.nextButton.clicked.connect(self.next_image)
        self.montageButton.clicked.connect(self.montage)

        self.previousButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.montageButton.setEnabled(False)

        self.setLayout(layout)
        self.set_text('No images yet... Enter a URL and press'
                      ' "Download".')

    def download_images(self):
        url = self.urlBar.text()
        self.set_text("Working!")
        self.images = download.download_images(url)
        self.set_text("Downloaded %s images from %s." %
                      (len(self.images), url))
        self.index = 0
        self.show_image(self.images[self.index])
        
        self.previousButton.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.montageButton.setEnabled(True)
        
    def show_image(self, image):
        self.scene.clear()
        image = QPixmap(image)
        self.scene.addPixmap(image)
        self.view.show()

    def next_image(self):
        self.index = (self.index + 1) % len(self.images)
        self.show_image(self.images[self.index])

    def previous_image(self):
        length = len(self.images)
        self.index = (self.index - 1 + length) % length
        self.show_image(self.images[self.index])

    def montage(self):
        os.system("montage img/* img/montage.png")
        self.show_image("img/montage")

    def set_text(self, text):
        self.scene.clear()
        self.scene.addText(text)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow(None)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
   main()
