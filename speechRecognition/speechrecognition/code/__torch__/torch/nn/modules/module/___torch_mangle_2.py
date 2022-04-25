op_version_set = 1
class Module(Module):
  __parameters__ = []
  training : bool
  dropout : __torch__.torch.nn.modules.module.___torch_mangle_0.Module
  norm : __torch__.torch.nn.modules.module.___torch_mangle_1.Module
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_2.Module,
    argument_1: Tensor) -> Tensor:
    _0 = self.dropout
    _1 = self.norm
    input = torch.transpose(argument_1, 1, 2)
    input0 = torch.gelu((_1).forward(input, ))
    return (_0).forward(input0, )
