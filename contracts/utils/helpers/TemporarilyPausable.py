import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

MAX_PAUSE_WINDOW_DURATION = 23328000  # 270 days

MAX_BUFFER_PERIOD_DURATION = 7776000  # 90 days


class TemporarilyPausable(sp.Contract):
    def __init__(self, pauseWindowDuration, bufferPeriodDuration):
        pauseWindowEndTime = sp.utils.seconds_of_timestamp(
            sp.now) + pauseWindowDuration

        self.update_initial_storage(_paused=sp.set_type_expr(sp.bool(False), sp.TBool), _pauseWindowEndTime=sp.set_type_expr(
            pauseWindowEndTime, sp.TNat), _bufferPeriodEndTime=sp.set_type_expr((pauseWindowEndTime + bufferPeriodDuration), sp.TNat))

    @sp.onchain_view()
    def getPausedState(self):
        state = sp.record(
            paused=~self._isNotPaused(),
            pauseWindowEndTime=self._getPauseWindowEndTime(),
            bufferPeriodEndTime=self._getBufferPeriodEndTime()
        )

        sp.result(state)

    def _setPaused(self, paused):
        with sp.if_(paused):
            sp.verify(sp.utils.seconds_of_timestamp(sp.now) < self.data._pauseWindowEndTime,
                      Errors.PAUSE_WINDOW_EXPIRED)
        with sp.else_():
            sp.verify(sp.utils.seconds_of_timestamp(sp.now) < self.data._bufferPeriodEndTime,
                      Errors.BUFFER_PERIOD_EXPIRED)

        self.data._paused = paused
        sp.emit(paused, with_type=True, tag='PauseStateChanged')

    def _ensureNotPaused(self):
        sp.verify(_isNotPaused(), Errors.PAUSED)

    def _isNotPaused(self):
        return (sp.utils.seconds_of_timestamp(
            sp.now) > self.data._bufferPeriodEndTime) | ~self.data._paused

    def _getPauseWindowEndTime(self):
        return self.data._pauseWindowEndTime

    def _getBufferPeriodEndTime(self):
        return self.data._bufferPeriodEndTime


sp.add_compilation_target('TemporarilyPausable', TemporarilyPausable(
    MAX_PAUSE_WINDOW_DURATION, MAX_BUFFER_PERIOD_DURATION))
