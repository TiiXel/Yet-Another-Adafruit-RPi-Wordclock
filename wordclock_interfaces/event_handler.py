# ===========================================================================
#
# WordClock/wordclock_interfaces/event_handler.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:17:34  CET   (RB)
#
#
# ===========================================================================

from monotonic import monotonic
import threading


class eventhandler:

    EVENT_INVALID = -1

    EVENT_BUTTON_LEFT = 0
    EVENT_BUTTON_RETURN = 1
    EVENT_BUTTON_RIGHT = 2

    def __init__(self):
        self.condition = threading.Condition()
        self.event = self.EVENT_INVALID

    def waitForEvent(self, timeout=None):
        self.condition.acquire()
        self.__wait_for(lambda: self.event != self.EVENT_INVALID, timeout)
        event = self.event
        self.event = self.EVENT_INVALID
        self.condition.release()
        return event

    def setEvent(self, event):
        self.condition.acquire()
        self.event = event
        self.condition.notifyAll()
        self.condition.release()

    def __wait_for(self, predicate, timeout=None):
        '''
        Wait until a condition evaluates to True.

        predicate should be a callable which result will be interpreted as a
        bollean value. A timeout can be provided, giving the maximum time to
        wait.
        '''

        endtime = None
        waittime = timeout
        result = predicate()
        while not result:
            if waittime is not None:
                if endtime is None:
                    endtime = monotonic() + waittime
                else:
                    waittime = endtime - monotonic()
                    if waittime <= 0:
                        break
            self.condition.wait(waittime)
            result = predicate()
        return result
