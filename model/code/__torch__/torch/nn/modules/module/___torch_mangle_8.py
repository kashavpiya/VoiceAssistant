op_version_set = 1
class Module(Module):
  __parameters__ = ["weight", "bias", ]
  weight : Tensor
  training : bool
  bias : Tensor
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_8.Module,
    argument_1: Tensor) -> Tensor:
    _0 = self.bias
    output = torch.matmul(argument_1, torch.t(self.weight))
    return torch.add_(output, _0, alpha=1)
