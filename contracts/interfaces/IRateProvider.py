import smartpy as sp

class IRateProvider:
  def getRate(provider):
      return sp.view('getRate', provider, sp.unit, t=sp.TNat).open_some('Invalid View')