op_version_set = 1
class Module(Module):
  __parameters__ = []
  training : bool
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_6.Module,
    argument_1: Tensor) -> Tensor:
    return torch.gelu(argument_1)
