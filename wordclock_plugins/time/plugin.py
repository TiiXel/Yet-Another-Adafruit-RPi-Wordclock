# ===========================================================================
#
# WordClock/wordclock_plugins/time/plugin.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:13:11  CET   (RB)
#
#
# ===========================================================================

from __future__ import print_function
from wordclock_layouts.words import M
import datetime
import os
import random
import wordclock_tools.wordclock_colors as wcc


class plugin:
    '''
    A plugin class to display the current time on the word clock. This plugin
    needs to be adapted to the letters layout on the hardware stencil.
    '''

    def __init__(self):
        # Get the plugin name according to the folder its contained in
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.preview = False
        self.lucky_love_count = 0

    def run(self, wci, wcd, preview=False):
        self.preview = preview
        if not self.preview:
            print('[RUNNING] The time plugin')

        self.lucky_love_count = 0
        # Initialize the "previous" rendering minute
        prev_min = -1

        while True:
            # Get the current time
            now = datetime.datetime.now()

            # Check if the time has changed since the last rendering
            if prev_min < now.minute:
                # Render and display time on the wordclock
                self.showTime(now, wcd)
                if not self.preview:
                    self.showMessage(now, wcd)
                wcd.update(transition='fade')
                wcd.refresh()
                # Update the last rendering time
                prev_min = -1 if now.minute == 59 else now.minute

            if self.preview:
                # Return to the main menu
                return

            event = wci.waitForEvent(2)

            if event == wci.EVENT_BUTTON_RETURN:
                # Return to the main menu
                return

    def test(self, wci, wcd):
        print('[TESTING] The time plugin')
        base = datetime.datetime(2017, 01, 02)

        print('          Testing times of day: hours')
        for i in range(25):
            delta = datetime.timedelta(hours=i)
            now = base + delta
            self.showTime(now, wcd)
            wcd.update()
            wcd.refresh()

            event = wci.waitForEvent(0.5)
            if event == wci.EVENT_BUTTON_RETURN:
                # Return to the main menu
                return

        print('          Testing times of day: minutes')
        for i in range(0, 61, 5):
            delta = datetime.timedelta(minutes=i)
            now = base + delta
            self.showTime(now, wcd)
            wcd.update()
            wcd.refresh()

            event = wci.waitForEvent(0.5)
            if event == wci.EVENT_BUTTON_RETURN:
                # Return to the main menu
                return

        print('          Testing special days')
        days = [[3, 18], [11, 4], [12, 25], [7, 14], [1, 1], [12, 6], [1, 17]]
        for day in days:
            now = datetime.datetime(2017, day[0], day[1])
            self.showTime(now, wcd)
            self.showMessage(now, wcd)
            wcd.update()
            wcd.refresh()

            event = wci.waitForEvent(1.5)
            if event == wci.EVENT_BUTTON_RETURN:
                # Return to the main menu
                return

        print('          Testing self.lucky_love_count')
        self.lucky_love_count = 1
        self.showMessage(base, wcd)
        wcd.update()
        wcd.refresh()
        event = wci.waitForEvent(1.5)
        if event == wci.EVENT_BUTTON_RETURN:
            # Return to the main menu
            return
        return

    def showTime(self, now, wcd):
        if not self.preview:
            print('          Display the time: %02d:%02d:%02d'
                  % (now.hour, now.minute, now.second))

        time_words = self.getWordsForTime(now)
        if not self.preview:
            print('         ', time_words)
        colors = [wcc.RED]*len(time_words)
        self.addWordsOnMatrix(time_words, colors, wcd)

    def showMessage(self, now, wcd):
        message_words = self.getWordsForMessage(now)
        if len(message_words) > 0:
            print('          With message:', message_words)
        colors = [wcc.PURPLE]*len(message_words)
        self.addWordsOnMatrix(message_words, colors, wcd)

    def getWordsForMessage(self, t):
        '''
        Returns the list of words for special message to be displayed,
        based on given time, and random stuff
        '''

        message_words = []

        if t.month == 3 and t.day == 18:
            message_words += ['joyeux', 'anniversaire', 'lise', 'de1',
                              'la', 'part', 'de2', 'remi', 'heart']
        elif t.month == 11 and t.day == 4:
            message_words += ['joyeux', 'anniversaire', 'remi']
        elif t.month == 12 and t.day == 24 and t.hour > 19:
            message_words += ['joyeux', 'noel']
        elif t.month == 12 and t.day == 25:
            message_words += ['joyeux', 'noel']
        elif t.month == 7 and t.day == 14:
            message_words += ['vive', 'la', 'france']
        elif t.month == 1 and t.day == 1:
            message_words += ['bonne', 'annee']
        elif t.month == 12 and t.day == 6:
            message_words += ['joyeuses', 'fetes']
        elif t.month == 1 and t.day == 17:
            message_words += ['joyeuse', 'fete', 'lise']

        r = random.randint(0, 302400)  # About once per week
        if r == 1 and self.lucky_love_count == 0:
            self.lucky_love_count = 10  # For 10 minutes

        if self.lucky_love_count > 0 and message_words == []:
            self.lucky_love_count = self.lucky_love_count - 1
            message_words += ['je', 't', 'aime', 'lise', 'heart']
        elif self.lucky_love_count > 0 and message_words != []:
            self.lucky_love_count = 0

        return message_words

    def getWordsForTime(self, t):
        '''
        Returns the list of words indicating time to be displayed,
        based on given time
        '''

        words = []

        # Greeting in the morning/evening
        if t.hour > 5 and t.hour <= 10:
            words += ['bonjour']
        if t.hour > 17 and t.hour <= 20:
            words += ['bonsoir']

        words += ['il', 'est']

        # Hours
        if t.minute > 32:
                disp_hour = t.hour + 1
        else:
            disp_hour = t.hour

        if disp_hour == 0 or disp_hour == 24:
            words += ['minuit']
        elif disp_hour == 12:
            words += ['midi']
        elif disp_hour == 1 or disp_hour == 13:
            words += ['une']
        elif disp_hour == 2 or disp_hour == 14:
            words += ['deux']
        elif disp_hour == 3 or disp_hour == 15:
            words += ['trois']
        elif disp_hour == 4 or disp_hour == 16:
            words += ['quatre']
        elif disp_hour == 5 or disp_hour == 17:
            words += ['cinq1']
        elif disp_hour == 6 or disp_hour == 18:
            words += ['six']
        elif disp_hour == 7 or disp_hour == 19:
            words += ['sept']
        elif disp_hour == 8 or disp_hour == 20:
            words += ['huit']
        elif disp_hour == 9 or disp_hour == 21:
            words += ['neuf']
        elif disp_hour == 10 or disp_hour == 22:
            words += ['dix1']
        elif disp_hour == 11 or disp_hour == 23:
            words += ['onze']

        # Heure or Heures depending on time
        if disp_hour != 0 and disp_hour != 12 and disp_hour != 24:
            if disp_hour != 1 and disp_hour != 13:
                words += ['heures']
            else:
                words += ['heure']

        # Minutes
        if t.minute > 2 and t.minute <= 7:
            words += ['cinq2']
        elif t.minute > 7 and t.minute <= 12:
            words += ['dix2']
        elif t.minute > 12 and t.minute <= 17:
            words += ['et', 'quart']
        elif t.minute > 17 and t.minute <= 22:
            words += ['vingt']
        elif t.minute > 22 and t.minute <= 27:
            words += ['vingt', 'cinq2']
        elif t.minute > 27 and t.minute <= 32:
            if disp_hour == 0 or disp_hour == 12 or disp_hour == 24:
                words += ['et', 'demi']
            else:
                words += ['et', 'demie']
        elif t.minute > 32 and t.minute <= 37:
            words += ['moins', 'vingt', 'cinq2']
        elif t.minute > 37 and t.minute <= 42:
            words += ['moins', 'vingt']
        elif t.minute > 42 and t.minute <= 47:
            words += ['moins', 'le', 'quart']
        elif t.minute > 47 and t.minute <= 52:
            words += ['moins', 'dix2']
        elif t.minute > 52 and t.minute <= 57:
            words += ['moins', 'cinq2']

        return words

    def addWordsOnMatrix(self, words, colors, wcd):

        for word, color in zip(words, colors):

            row = M[word]["row"]
            col0 = M[word]["start"]
            col1 = M[word]["start"] + M[word]["length"]

            for col in xrange(col0, col1):
                wcd.setColorForLetter(row, col, color)
