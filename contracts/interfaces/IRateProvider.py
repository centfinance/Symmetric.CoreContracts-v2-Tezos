import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors
class IRateProvider:
  def getRate(provider):
      return sp.view('getRate', provider, sp.unit, t=sp.TNat).open_some(Errors.GET_RATE_INVALID)