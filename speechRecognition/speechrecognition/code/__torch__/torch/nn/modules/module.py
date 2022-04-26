op_version_set = 1
class Module(Module):
  __parameters__ = ["weight", "bias", ]
  weight : Tensor
  training : bool
  bias : Tensor
  def forward(self: __torch__.torch.nn.modules.module.Module,
    input: Tensor) -> Tensor:
    _0 = self.bias
    x = torch._convolution(input, self.weight, _0, [2], [5], [1], False, [0], 1, False, False, True)
    return x
