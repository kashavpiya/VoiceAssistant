op_version_set = 1
class Module(Module):
  __parameters__ = ["weight", "bias", ]
  weight : Tensor
  training : bool
  bias : Tensor
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_5.Module,
    argument_1: Tensor) -> Tensor:
    _0 = self.bias
    _1 = self.weight
    input = torch.layer_norm(argument_1, [128], _1, _0, 1.0000000000000001e-05, True)
    return input
