op_version_set = 1
class Module(Module):
  __parameters__ = []
  training : bool
  __annotations__["0"] = __torch__.torch.nn.modules.module.___torch_mangle_4.Module
  __annotations__["1"] = __torch__.torch.nn.modules.module.___torch_mangle_5.Module
  __annotations__["2"] = __torch__.torch.nn.modules.module.___torch_mangle_6.Module
  __annotations__["3"] = __torch__.torch.nn.modules.module.___torch_mangle_7.Module
  __annotations__["4"] = __torch__.torch.nn.modules.module.___torch_mangle_8.Module
  __annotations__["5"] = __torch__.torch.nn.modules.module.___torch_mangle_9.Module
  __annotations__["6"] = __torch__.torch.nn.modules.module.___torch_mangle_10.Module
  __annotations__["7"] = __torch__.torch.nn.modules.module.___torch_mangle_11.Module
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_12.Module,
    argument_1: Tensor) -> Tensor:
    _0 = getattr(self, "1")
    _1 = (getattr(self, "0")).forward(argument_1, )
    _2 = getattr(self, "3")
    _3 = (getattr(self, "2")).forward((_0).forward(_1, ), )
    _4 = getattr(self, "5")
    _5 = (getattr(self, "4")).forward((_2).forward(_3, ), )
    _6 = getattr(self, "7")
    _7 = (getattr(self, "6")).forward((_4).forward(_5, ), )
    return (_6).forward(_7, )
