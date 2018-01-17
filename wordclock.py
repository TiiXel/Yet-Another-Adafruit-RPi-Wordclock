#!/usr/bin/env python

# ===========================================================================
#
# WordClock/wordclock.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 17:08:14  CET   (RB)
#
#
# ===========================================================================

from __future__ import print_function
from importlib import import_module
import atexit
import inspect
import os
import signal
import sys
import wordclock_tools.wordclock_colors as wcc
import wordclock_tools.wordclock_display as wcd
import wordclock_interfaces.event_handler as wci
import wordclock_interfaces.gpio_interface as wcigpio
from wordclock_layouts.font_dotimatrix3 import L


class wordclock:

    def __init__(self, testing):

        print('[    ] Initializing wordclock')

        self.testing = testing

        # Get path of the directory where this file is stored
        self.base_path = os.path.dirname(os.path.abspath(
                                    inspect.getfile(inspect.currentframe())))

        # Create object to interact with the wordclock
        self.wci = wci.eventhandler()
        self.gpio = wcigpio.gpiointerface(self.wci)

        # Create object to display light pixels on the wordclock
        self.wcd = wcd.wordclockdisplay(self.testing)

        # Define path to plugin directory
        plugin_dir = os.path.join(self.base_path, 'wordclock_plugins')

        # Assemble list of all available plugins
        plugins = (plugin for plugin in os.listdir(plugin_dir)
                   if os.path.isdir(os.path.join(plugin_dir, plugin)))

        # Helper variable, only imported on successful import
        index = 0
        # Import plugins
        self.plugins = []
        self.credits_plugin = None

        for plugin in plugins:

            print('[    ] Importing plugin: %s' % plugin, end='')
            try:
                # Check if the plugin is valid
                if not os.path.isfile(
                        os.path.join(plugin_dir, plugin, 'plugin.py')):
                    raise ImportError

                temp_plugin = import_module(
                            'wordclock_plugins.' + plugin + '.plugin').plugin()

                if plugin == 'credits':
                    self.credits_plugin = temp_plugin
                    print('\r[DONE] Importing plugin: %s' % plugin)
                    continue

                if not hasattr(temp_plugin, 'name'):
                    raise ImportError

                self.plugins.append(temp_plugin)
                print('\r[DONE] Importing plugin: %s (#%i)' % (plugin, index))

                if plugin == 'time':
                    self.default_plugin_index = index

                index += 1

            except ImportError:
                print('\r[FAIL] Importing plugin: %s' % plugin)

        self.plugin_index = None

        print('[DONE] Initializing wordclock\n')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        '''
        Cleanup everything before leaving
        '''
        print('Cleaning wordclock ....', end=' ')
        self.gpio.__exit__()
        self.wcd.__exit__()
        print('[DONE]')

    def run(self):
        '''
        Run the currently selected plugin
        '''
        self.plugins[self.plugin_index].run(self.wci, self.wcd)

    def preview(self):
        self.plugins[self.plugin_index].run(self.wci, self.wcd, preview=True)

    def test(self):
        self.plugins[self.plugin_index].test(self.wci, self.wcd)

    def loop(self):
        '''
        Make the wordclock run
        '''

        # Run the (opening) credits plugin
        self.credits_plugin.run(self.wci, self.wcd)

        # Select the default plugin
        try:
            self.plugin_index = self.default_plugin_index
        except AttributeError:
            print('[WARNING] No default plugin were detected')

        while True:
            # Run the selected plugin
            if self.plugin_index is not None:
                if self.testing:
                    self.test()
                else:
                    self.run()

            show_menu_indication = True
            # If plugin.run exits, loop through the menu to select next plugin
            while True:

                plugins_list = ''

                for plugin_index in xrange(len(self.plugins)):

                    # Selected plugin will be marked with a *
                    if self.plugin_index == plugin_index:
                        plugins_list += '*'

                    plugins_list += self.plugins[plugin_index].name + ', '

                if show_menu_indication:

                    print('[MENU] Plugins list: ' + plugins_list)

                    l1 = [[row+4, col] for row, col in L['M']]
                    l2 = [[row+4, col+4] for row, col in L['E']]
                    l3 = [[row+4, col+9] for row, col in L['N']]
                    l4 = [[row+4, col+13] for row, col in L['U']]

                    ls = l1 + l2 + l3 + l4

                    self.wcd.setColorForLetters(ls, [wcc.ORANGE]*len(ls))
                    self.wcd.update(transition='fade', tau=0.3)
                    self.wcd.refresh()

                    event = self.wci.waitForEvent(0.3)

                else:
                    if hasattr(self.plugins[self.plugin_index], 'logo'):
                        logo = self.plugins[self.plugin_index].logo
                        self.wcd.setColorForLetters(logo, [wcc.RED]*len(logo))
                        self.wcd.update(transition='fade', tau=0.3)
                        self.wcd.refresh()
                    else:
                        self.preview()

                    event = self.wci.waitForEvent(3)

                if event == self.wci.EVENT_INVALID:
                    show_menu_indication = not show_menu_indication

                if event == self.wci.EVENT_BUTTON_LEFT:
                    self.plugin_index -= 1
                    self.plugin_index %= len(self.plugins)
                    show_menu_indication = False

                if event == self.wci.EVENT_BUTTON_RIGHT:
                    self.plugin_index += 1
                    self.plugin_index %= len(self.plugins)
                    show_menu_indication = False

                if event == self.wci.EVENT_BUTTON_RETURN:
                    # Go back to upper loop, to run selected pluggin
                    # self.wcd.clean(transition='fade')
                    break


def exit_handler(word_clock):
    print('[EXIT] Script aborted. Turning clock off.')


if __name__ == '__main__':
    testing = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            testing = True
    word_clock = wordclock(testing)

    atexit.register(exit_handler, word_clock)
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda x, y: sys.exit(0))

    with word_clock:
        word_clock.loop()
