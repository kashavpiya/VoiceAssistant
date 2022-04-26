op_version_set = 1
class Module(Module):
  __parameters__ = []
  training : bool
  cnn : __torch__.torch.nn.modules.module.___torch_mangle_3.Module
  dense : __torch__.torch.nn.modules.module.___torch_mangle_12.Module
  lstm : __torch__.torch.nn.modules.module.___torch_mangle_13.Module
  layer_norm2 : __torch__.torch.nn.modules.module.___torch_mangle_14.Module
  dropout2 : __torch__.torch.nn.modules.module.___torch_mangle_15.Module
  final_fc : __torch__.torch.nn.modules.module.___torch_mangle_16.Module
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_17.Module,
    x: Tensor,
    argument_2: Tuple[Tensor, Tensor]) -> Tuple[Tensor, Tuple[Tensor, Tensor]]:
    _0 = self.final_fc
    _1 = self.dropout2
    _2 = self.layer_norm2
    _3 = self.lstm
    _4 = self.dense
    _5 = self.cnn
    hx, hx0, = argument_2
    input = torch.squeeze(x, 1)
    _6 = (_4).forward((_5).forward(input, ), )
    orig_input = torch.transpose(_6, 0, 1)
    _7, _8, _9, = (_3).forward(orig_input, hx, hx0, )
    input0 = torch.gelu((_2).forward(_7, ))
    _10 = (_0).forward((_1).forward(input0, ), )
    return (_10, (_8, _9))
