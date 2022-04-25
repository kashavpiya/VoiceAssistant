op_version_set = 1
class Module(Module):
  __parameters__ = []
  training : bool
  def forward(self: __torch__.torch.nn.modules.module.___torch_mangle_0.Module,
    input: Tensor) -> Tensor:
    input0 = torch.dropout(input, 0.10000000000000001, False)
    return input0
