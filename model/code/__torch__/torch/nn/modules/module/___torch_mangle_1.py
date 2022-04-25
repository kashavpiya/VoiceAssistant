op_version_set = 1
class Module(Module):
  __parameters__ = ["weight", "bias", ]
  weight : Tensor
  training : bool
  bias : Tensor
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_1.Module,
    input: Tensor) -> Tensor:
    _0 = self.bias
    _1 = self.weight
    input0 = torch.layer_norm(input, [81], _1, _0, 1.0000000000000001e-05, True)
    return input0
