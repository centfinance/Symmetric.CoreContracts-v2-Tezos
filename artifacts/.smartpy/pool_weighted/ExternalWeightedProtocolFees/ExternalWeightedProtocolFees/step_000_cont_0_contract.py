import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(fixedPoint = sp.TBigMap(sp.TNat, sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat))).layout("fixedPoint"))
    self.init(fixedPoint = {20 : sp.build_lambda(lambda _x0: (sp.fst(_x0) * sp.snd(_x0)) // 1000000000000000000), 22 : lambda, 24 : lambda})

sp.add_compilation_target("test", Contract())