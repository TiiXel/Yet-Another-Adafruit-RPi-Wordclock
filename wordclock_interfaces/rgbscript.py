# ===========================================================================
#
# WordClock/wordclock_interfaces/rgbscript.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:18:01  CET   (RB)
#
#
# ===========================================================================

import wordclock_tools.wordclock_colors as wcc


class RGBscript:

    def __init__(self, matrix_h, ratio):
        self.MATRIX_H = matrix_h
        self.MATRIX_W = matrix_h * ratio
        self.MATRIX_C = 3

    def Clear(self):
        buffer = [0] * self.MATRIX_H * self.MATRIX_W * self.MATRIX_C
        self.SetBuffer(buffer)

    def SetBuffer(self, buffer):
        pre = 'echo -e "'
        post = '"\n'

        text = ''
        for y in range(self.MATRIX_H):
            line = pre
            for x in range(self.MATRIX_W):
                i = self.getIndex(x, y)
                c = buffer[i:i+3]
                if c == wcc.BLUE:
                    line += '\e[1;34m'
                elif c == wcc.GREEN:
                    line += '\e[1;32m'
                elif c == wcc.PINK:
                    line += '\e[1;31m'
                elif c == wcc.PURPLE:
                    line += '\e[1;35m'
                elif c == wcc.RED:
                    line += '\e[0;31m'
                elif c == wcc.WHITE:
                    line += '\e[1;37m'
                elif c == wcc.WWHITE:
                    line += '\e[1;37m'
                elif c == wcc.YELLOW:
                    line += '\e[1;33m'
                elif c == wcc.ORANGE:
                    line += '\e[0;33m'
                else:
                    line += '\e[0;30m'
                line += '##'
            line += post
            text += line

        file = open('__outputscript.sh', 'w')
        file.write(text)
        file.close()

    def getIndex(self, x, y, c=0):
        X = self.MATRIX_C*self.MATRIX_W
        Y = self.MATRIX_C
        return (31-x)*X + y*Y + c
