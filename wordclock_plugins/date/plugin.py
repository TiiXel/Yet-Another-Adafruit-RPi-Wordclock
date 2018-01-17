 ===========================================================================
#
# WordClock/wordclock_plugins/date/plugin.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:10:19  CET   (RB)
#
#
# ===========================================================================

import datetime
import wordclock_tools.wordclock_colors as wcc
import locale
import os
from wordclock_layouts.font_dotimatrix5 import L
from wordclock_layouts.font_dotimatrix3 import N


class plugin:

    def __init__(self):
        # Get the plugin name according to the folder its contained in
        self.name = os.path.dirname(__file__).split('/')[-1]

    def run(self, wci, wcd, preview=False):

        while True:

            now = datetime.datetime.now()

            self.showDate(now, wcd)
            wcd.update(transition='fade')
            wcd.refresh()

            if preview:
                # Return to the main menu
                return

            event = wci.waitForEvent(2)

            if event == wci.EVENT_BUTTON_RETURN:
                # Return to the main menu
                return

    def showDate(self, now, wcd):

        saved = locale.setlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
        aaa = now.strftime('%a').capitalize()
        dd = now.strftime('%d')
        mm = now.strftime('%m')
        locale.setlocale(locale.LC_TIME, saved)

        a = []
        a += [[row, col] for row, col in L[aaa[0]]]
        a += [[row, col+5] for row, col in L[aaa[1]]]
        a += [[row, col+10] for row, col in L[aaa[2]]]

        d = []
        d += [[row+9, col] for row, col in N[dd[0]]]
        d += [[row+9, col+4] for row, col in N[dd[1]]]

        m = []
        m += [[row+9, col+8] for row, col in N[mm[0]]]
        m += [[row+9, col+12] for row, col in N[mm[1]]]

        letters = a + d + m
        colors = [wcc.WHITE]*len(a) + [wcc.RED]*len(d) + [wcc.ORANGE]*len(m)

        wcd.setColorForLetters(letters, colors)
