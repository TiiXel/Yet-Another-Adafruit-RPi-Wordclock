# ===========================================================================
#
# WordClock/wordclock_tools/wordclock_display.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 17:16:43  CET   (RB)
#
#
# ===========================================================================

from __future__ import print_function
from wordclock_interfaces.rgbmatrix import Adafruit_RGBmatrix
import time
import numpy


class wordclockdisplay:

    def __init__(self, testing):
        print('[    ] Initializing wordclock display', end=' ')

        # Physical parameters: width (pixels), height (pixels), color depth
        self.MATRIX_W = 32
        self.MATRIX_H = 32
        self.MATRIX_C = 3

        # Pixel per letter per length dimention
        self.MATRIX_DIV = 2

        # Size of the linearized representation of the physical matrix
        self.ARRAY_DIM = self.MATRIX_W * self.MATRIX_H * self.MATRIX_C

        # We can use this variable to modify the output type. In the future,
        # it might be cool to allow outputing to the command line interface
        # for developping on a computer.
        self.phy_type = 'adafruit-hat'

        # Physical matrix object
        if self.phy_type == 'adafruit-hat':
            self.phy_matrix = Adafruit_RGBmatrix(self.MATRIX_H,
                                                 self.MATRIX_W/self.MATRIX_H)

        if testing:
            self.phy_matrix = None

        # Array (linearized) representation of the physical matrix
        self.matrix = numpy.zeros(self.ARRAY_DIM, dtype=numpy.uint8)
        self.next_matrix = numpy.zeros(self.ARRAY_DIM, dtype=numpy.uint8)

        print('[DONE] Initializing wordclock display')

    def __exit__(self):
        if self.phy_matrix is None:
            return
        self.phy_matrix.Clear()

    def setColorForPixel(self, x, y, color):
        if self.phy_matrix is None:
            return
        X = self.MATRIX_C * self.MATRIX_W
        Y = self.MATRIX_C
        i = (31-x)*X + y*Y
        self.next_matrix[i:i+3] = color

    def getColorForPixel(self, x, y):
        if self.phy_matrix is None:
            return
        X = self.MATRIX_C * self.MATRIX_W
        Y = self.MATRIX_C
        i = (31-x)*X + y*Y
        return self.matrix[i:i+3]

    def setColorForLetter(self, row, col, color):
        '''
        Sets the color for all pixels associated to a given letter (row, col)
        '''
        if self.phy_matrix is None:
            return

        X = self.MATRIX_C * self.MATRIX_W
        Y = self.MATRIX_C

        y0 = (row - 1) * self.MATRIX_DIV
        x0 = (col - 1) * self.MATRIX_DIV

        for x in xrange(x0, x0+self.MATRIX_DIV):
            for y in xrange(y0, y0+self.MATRIX_DIV):
                i = (31-x)*X + y*Y
                self.next_matrix[i:i+3] = color

    def setColorForLetters(self, letters, colors):
        '''
        Sets the color for all pixels associated to a given letter (row, col)
        '''
        if self.phy_matrix is None:
            return

        X = self.MATRIX_C * self.MATRIX_W
        Y = self.MATRIX_C

        for [row, col], color in zip(letters, colors):
            y0 = (row - 1) * self.MATRIX_DIV
            x0 = (col - 1) * self.MATRIX_DIV

            for x in xrange(x0, x0+self.MATRIX_DIV):
                for y in xrange(y0, y0+self.MATRIX_DIV):
                    i = (31-x)*X + y*Y
                    self.next_matrix[i:i+3] = color

    def refresh(self):
        if self.phy_matrix is None:
            return
        self.next_matrix = numpy.zeros(self.ARRAY_DIM, dtype=numpy.uint8)

    def update(self, transition=None, tau=1):
        if self.phy_matrix is None:
            return

        if transition == 'fade':
            diff_matrix = self.next_matrix.astype(numpy.int16) \
                        - self.matrix.astype(numpy.int16)

            delta_time = tau/10.
            steps = 10.0

            for step in xrange(0, int(steps)):
                c = (step*1.0)/steps
                temp_matrix = numpy.uint8(self.matrix + diff_matrix*c)
                self.phy_matrix.SetBuffer(temp_matrix.tolist())
                time.sleep(delta_time)
        else:
            pass

        self.matrix = self.next_matrix
        self.phy_matrix.SetBuffer(self.matrix.tolist())

    def clean(self, transition=None, tau=1):
        if self.phy_matrix is None:
            return
        self.refresh()
        self.update(transition, tau)
