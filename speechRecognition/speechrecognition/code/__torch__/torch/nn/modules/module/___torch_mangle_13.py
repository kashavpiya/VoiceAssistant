op_version_set = 1
class Module(Module):
  __parameters__ = ["bias_hh_l0", "bias_ih_l0", "weight_ih_l0", "weight_hh_l0", ]
  bias_hh_l0 : Tensor
  training : bool
  bias_ih_l0 : Tensor
  weight_ih_l0 : Tensor
  weight_hh_l0 : Tensor
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_13.Module,
    orig_input: Tensor,
    hx: Tensor,
    hx0: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
    _0 = self.bias_hh_l0
    _1 = self.bias_ih_l0
    _2 = self.weight_hh_l0
    _3 = self.weight_ih_l0
    input, _4, _5 = torch.lstm(orig_input, [hx, hx0], [_3, _2, _1, _0], True, 1, 0., False, False, False)
    return (input, _4, _5)
