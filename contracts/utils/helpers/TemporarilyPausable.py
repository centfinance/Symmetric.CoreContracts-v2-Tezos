import smartpy as sp

from contracts.interfaces.SymmetricErrors import Errors

MAX_PAUSE_WINDOW_DURATION = 23328000  # 270 days

MAX_BUFFER_PERIOD_DURATION = 7776000  # 90 days


class TemporarilyPausable:
    def __init__(self, pauseWindowDuration, bufferPeriodDuration):
        sp.verify(pauseWindowDuration <= MAX_PAUSE_WINDOW_DURATION,
                  Errors.MAX_PAUSE_WINDOW_DURATION)
        sp.verify(bufferPeriodDuration <= MAX_BUFFER_PERIOD_DURATION,
                  Errors.MAX_BUFFER_PERIOD_DURATION)

        pauseWindowEndTime = sp.now + pauseWindowDuration

        _pauseWindowEndTime = pauseWindowEndTime
        _bufferPeriodEndTime = pauseWindowEndTime + bufferPeriodDuration

        pass

    def whenNotpaused(self):
        self._ensureNitPaused(self)

    def getPausedState(self):
        state = sp.record(
            paused=~self._isNotPaused(self),
            pauseWindowEndTime=self._getPauseWindowEndTime(self),
            bufferPeriodEndTime=self._getBufferPeriodEndTime(self)
        )

        return state

    def _setPaused(self, paused):
        with sp.if_(paused):
            sp.verify(sp.now < self.data._pauseWindowEndTime,
                      Errors.PAUSE_WINDOW_EXPIRED)
        with sp.else_():
            sp.verify(sp.now < self.data._bufferPeriodEndTime,
                      Errors.BUFFER_PERIOD_EXPIRED)

        self.data._paused = paused
        sp.emit(paused, with_type=True, tag='PauseStateChanged')

    def _ensureNotPaused(self):
        sp.verify(self._isNotPaused(self), Errors.PAUSED)

    def _ensurePaused(self):
        sp.verify(~self._isNotPaused(self), Errors.NOT_PAUSED)

    def _isNotPaused(self):
        return sp.now > self.data._bufferPeriodEndTime | ~self.data._paused

    def _getPauseWindowEndTime(self):
        return self.data._pauseWindowEndTime

    def _getBufferPeriodEndTime(self):
        return self.data._bufferPeriodEndTime
