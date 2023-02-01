import smartpy as sp

from contracts.utils.helpers.TemporarilyPausable import TemporarilyPausable


class PausableTest(TemporarilyPausable, sp.Contract):
    def __init__(self, pauseWindowDuration, bufferPeriodDuration):
        sp.Contract.__init__(self)
        TemporarilyPausable.__init__(
            self, pauseWindowDuration, bufferPeriodDuration)

    @sp.entry_point
    def setPaused(self, paused):
        self._setPaused(paused)


t1pauseWindowDuration = sp.nat(23332800)

t1bufferPeriodDuration = sp.nat(7776000)


@sp.add_test(name="TemporarilyPausableTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    sc.h1("Pausable contract")
    sc.table_of_contents()

    sc.h3("can be initialized with pause window and buffer period duration")
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


@sp.add_test(name="TemporarilyPausableTest_2", profile=True)
def test():
    sc = sp.test_scenario()
    sc.h3("Before the pause window end date")

    sc.h3("It can be paused-")
    c = PausableTest(t1pauseWindowDuration, t1bufferPeriodDuration)
    sc += c
    c.setPaused(True).run(now=sp.timestamp(11666400))
    r3 = c.getPausedState()
    sc.show(r3)
    sc.verify(r3 == sp.record(paused=True,
              pauseWindowEndTime=23332800, bufferPeriodEndTime=31108800))

    sc.h3("can be paused and unpaused")
    c2 = PausableTest(sp.nat(23332800), sp.nat(
        7776000))
    sc += c2
    c2.setPaused(True).run(now=sp.timestamp(11666400))
    r4 = c2.getPausedState()
    sc.show(r4)
    sc.verify(r4 == sp.record(paused=True,
              pauseWindowEndTime=34999200, bufferPeriodEndTime=42775200))
    c2.setPaused(False).run(now=sp.timestamp(17500000))
    r4 = c2.getPausedState()
    sc.verify(r4 == sp.record(paused=False,
              pauseWindowEndTime=34999200, bufferPeriodEndTime=42775200))


@sp.add_test(name="TemporarilyPausableTest_3", profile=True)
def test():
    sc = sp.test_scenario()
    sc.h3("When the pause window end date has been reached")

    def itIsForeverUnpaused(c, time=0):
        sc.h3("It is unpaused")
        sc.verify(c.data._paused == False)
        sc.h3("Cannot be paused")
        c.setPaused(True).run(now=time, valid=False)

    sc.h3("when unpaused")

    sc.h3('before the buffer period end date')
    c = PausableTest(sp.nat(23332800), sp.nat(
        7776000))
    sc += c
    itIsForeverUnpaused(c, sp.timestamp(23332801))

    sc.h3('after the buffer period end date')
    itIsForeverUnpaused(c, sp.timestamp(31108801))

    sc.h3("when paused")
    sc.h3("before the buffer period end date")
    c.setPaused(True).run(now=sp.timestamp(23332799))
    # is paused
    sc.verify(c.data._paused == True)
    # can be unpaused
    c.setPaused(False).run(now=sp.timestamp(23332801))
    sc.verify(c.data._paused == False)
    # cannot be paused again
    c.setPaused(True).run(now=sp.timestamp(23332801), valid=False)
    sc.verify(c.data._paused == False)

    sc.h3("after the buffer period end date")
    # is unpaused
    sc.verify(c.data._paused == False)
    # cannot be paused
    c.setPaused(True).run(now=sp.timestamp(42775201), valid=False)
    # cannot be unpaused
    c.setPaused(False).run(now=sp.timestamp(42775201), valid=False)
