# ===========================================================================
#
# WordClock/wordclock_plugins/credits/plugin.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:11:27  CET   (RB)
#
#
# ===========================================================================

from wordclock_layouts.words import M
import wordclock_tools.wordclock_colors as wcc
import time
import os


class plugin:

    def __init__(self):
        # Get the plugin name according to the folder its contained in
        self.name = os.path.dirname(__file__).split('/')[-1]

    def run(self, wci, wcd, preview=False):

        words = ['horloge', 'a', 'mots', 'par', 'remi', 'heart']
        color = wcc.YELLOW

        for word in words:
            print('Insterting: ' + word)

            row = M[word]["row"]
            col0 = M[word]["start"]
            col1 = M[word]["start"] + M[word]["length"]

            for col in xrange(col0, col1):
                print ('  Letter at: %02d, %02d' % (row, col))
                wcd.setColorForLetter(row, col, color)
                wcd.update()
                time.sleep(0.2)

        wcd.refresh()
