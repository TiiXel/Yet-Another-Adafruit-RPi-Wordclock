# ===========================================================================
#
# WordClock/wordclock_plugins/time_in_numbers/plugin.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:14:28  CET   (RB)
#
#
# ===========================================================================

from wordclock_layouts.font_dotimatrix5 import N
import wordclock_tools.wordclock_colors as wcc
import datetime
import os


class plugin:

    def __init__(self):
        # Get the plugin name according to the folder its contained in
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.offset = 0
        self.preview = False

    def run(self, wci, wcd, preview=False):

        self.preview = preview

        prev_min = -1
        off = False

        while True:

            now = datetime.datetime.now()
            now = now + datetime.timedelta(minutes=self.offset)

            if prev_min < now.minute or off:
                off = False
                # Render and display time on the wordclock
                self.showTime(now, wcd)
                wcd.update(transition='fade')
                wcd.refresh()
                # Update the last rendering time
                prev_min = -1 if now.minute == 59 else now.minute

            if preview:
                # Return to the main menu
                return

            event = wci.waitForEvent(2)

            if event == wci.EVENT_BUTTON_LEFT:
                self.offset -= 1
                off = True

            if event == wci.EVENT_BUTTON_RIGHT:
                self.offset += 1
                off = True

            if event == wci.EVENT_BUTTON_RETURN:
                # Return to the main menu
                return

    def showTime(self, now, wcd):
            if not self.preview:
                print('Display the time: %02d:%02d:%02d'
                      % (now.hour, now.minute, now.second))

            hh = "%02d" % now.hour
            mm = "%02d" % now.minute

            n1 = [[row, col + 2] for (row, col) in N[hh[0]]]
            n2 = [[row, col + 9] for (row, col) in N[hh[1]]]
            n3 = [[row + 9, col + 2] for (row, col) in N[mm[0]]]
            n4 = [[row + 9, col + 9] for (row, col) in N[mm[1]]]

            colors = [wcc.RED] * len(n1) + [wcc.RED] * len(n2)
            colors += [wcc.BLUE] * len(n3) + [wcc.BLUE] * len(n4)

            ns = n1 + n2 + n3 + n4
            wcd.setColorForLetters(ns, colors)
