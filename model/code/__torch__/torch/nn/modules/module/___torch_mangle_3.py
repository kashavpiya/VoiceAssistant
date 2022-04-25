op_version_set = 1
class Module(Module):
  __parameters__ = []
  training : bool
  __annotations__["0"] = __torch__.torch.nn.modules.module.Module
  __annotations__["1"] = __torch__.torch.nn.modules.module.___torch_mangle_2.Module
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_3.Module,
    input: Tensor) -> Tensor:
    _0 = getattr(self, "1")
    _1 = (getattr(self, "0")).forward(input, )
    return (_0).forward(_1, )
