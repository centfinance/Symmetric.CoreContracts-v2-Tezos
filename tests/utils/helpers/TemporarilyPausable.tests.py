import smartpy as sp

from contracts.utils.helpers.TemporarilyPausable import TemporarilyPausable


class PausableTest(TemporarilyPausable, sp.Contract):
    def __init__(self, pauseWindowDuration, bufferPeriodDuration):
        sp.Contract.__init__(self)
        TemporarilyPausable.__init__(
            self, pauseWindowDuration, bufferPeriodDuration)

    @sp.entry_point
    def testSetPaused(self, paused):
        self._setPaused(paused)


@sp.add_test(name="TemporarilyPausable_tests", profile=True)
def test():
    acc = sp.test_account("Administrator")

    sc = sp.test_scenario()

    sc.h1("Pausable contract")
    sc.table_of_contents()

    sc.h3("can be initialized with pause window and buffer period duration")
    t1pauseWindowDuration = sp.nat(23332800)
    t1bufferPeriodDuration = sp.nat(7776000)

    c1 = PausableTest(t1pauseWindowDuration, t1bufferPeriodDuration)
    sc += c1
    r1 = c1.getPausedState()
    sc.show(r1)
    sc.verify(r1 == sp.record(paused=False,
              pauseWindowEndTime=23332800, bufferPeriodEndTime=31108800))

    sc.h3("can be initialized with no pause window or buffer period duration")
    t2pauseWindowDuration = sp.nat(0)
    t2bufferPeriodDuration = sp.nat(0)

    c2 = PausableTest(t2pauseWindowDuration, t2bufferPeriodDuration)
    sc += c2
    r2 = c2.getPausedState()
    sc.show(r2)
    sc.verify(r2 == sp.record(paused=False,
              pauseWindowEndTime=0, bufferPeriodEndTime=0))
