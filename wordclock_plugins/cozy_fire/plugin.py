# ===========================================================================
#
# WordClock/wordclock_plugins/cozy_fire/plugin.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:13:00  CET   (RB)
#
#
# ===========================================================================

import numpy
import wordclock_tools.wordclock_colors as wcc
from wordclock_layouts.font_dotimatrix3 import L
import colorsys
import random
import os
from color_masks import value_mask, hue_mask


class plugin:

    def __init__(self):
        # Get the plugin name according to the folder its contained in
        self.name = os.path.dirname(__file__).split('/')[-1]

        self.values = numpy.zeros(16*16)
        self.letters = [[row+1, col+1] for col in range(16)
                        for row in range(16)]

    def run(self, wci, wcd, preview=False):

        if preview:
            l1 = [[row, col] for row, col in L['C']]
            l2 = [[row, col+4] for row, col in L['o']]
            l3 = [[row, col+9] for row, col in L['z']]
            l4 = [[row, col+13] for row, col in L['y']]
            l5 = [[row+9, col] for row, col in L['f']]
            l6 = [[row+9, col+4] for row, col in L['i']]
            l7 = [[row+9, col+9] for row, col in L['r']]
            l8 = [[row+9, col+13] for row, col in L['e']]

            ls = l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8

            wcd.setColorForLetters(ls, [wcc.ORANGE]*len(ls))
            wcd.update(transition='fade')
            wcd.refresh()
            return

        while True:

            self.shiftUp()
            self.generateLine()
            self.setValues(wcd)
            wcd.update()
            wcd.refresh()

            event = wci.waitForEvent(0.5)

            if event == wci.EVENT_BUTTON_RETURN:
                # Return to the main menu
                return

    def shiftUp(self):
        X = 16
        Y = 1
        for y in range(15):
            for x in range(16):
                i1 = (15-x)*X + y*Y
                i2 = (15-x)*X + (y+1)*Y
                self.values[i1] = self.values[i2]

    def generateLine(self):
        X = 16
        Y = 1
        y = 15
        for x in range(16):
            i = (15-x)*X + y*Y
            self.values[i] = random.randint(64, 255) / 255.

    def setValues(self, wcd):

        rgb = [colorsys.hsv_to_rgb(h, 1., max(0, v-m)) for h, v, m
               in zip(hue_mask, self.values, value_mask)]

        colors = [[r*255, g*255, b*255] for r, g, b, in rgb]

        wcd.setColorForLetters(self.letters, colors)
