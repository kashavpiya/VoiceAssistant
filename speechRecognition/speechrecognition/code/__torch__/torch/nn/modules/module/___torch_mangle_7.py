op_version_set = 1
class Module(Module):
  __parameters__ = []
  training : bool
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_7.Module,
    argument_1: Tensor) -> Tensor:
    input = torch.dropout(argument_1, 0.10000000000000001, False)
    return input
