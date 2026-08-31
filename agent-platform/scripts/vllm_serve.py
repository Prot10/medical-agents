"""Wrapper to launch vLLM server with NVML workaround.

On systems with NVIDIA driver/library version mismatch (e.g., CERN lxplus),
pynvml.nvmlInit() fails even though CUDA works fine via PyTorch.
This script patches vLLM's platform detection to force CUDA mode.
"""

import sys


def _patch_platform_detection():
    """Patch vLLM's builtin_platform_plugins before current_platform is resolved."""
    import vllm.platforms as platforms_mod

    original_cuda_plugin = platforms_mod.builtin_platform_plugins["cuda"]

    def patched_cuda_plugin():
        result = original_cuda_plugin()
        if result is not None:
            return result
        # NVML failed — check if CUDA actually works via PyTorch
        try:
            import torch
            if torch.cuda.is_available() and torch.cuda.device_count() > 0:
                print(
                    f"[vllm_serve] NVML unavailable but PyTorch sees "
                    f"{torch.cuda.device_count()} GPU(s): "
                    f"{torch.cuda.get_device_name(0)}. Forcing CUDA platform.",
                    file=sys.stderr,
                )
                return "vllm.platforms.cuda.CudaPlatform"
        except Exception:
            pass
        return None

    platforms_mod.builtin_platform_plugins["cuda"] = patched_cuda_plugin


_patch_platform_detection()

# Now run the normal vLLM OpenAI server __main__ block
import uvloop  # noqa: E402

from vllm.entrypoints.openai.api_server import (  # noqa: E402
    FlexibleArgumentParser,
    cli_env_setup,
    make_arg_parser,
    run_server,
    validate_parsed_serve_args,
)

if __name__ == "__main__":
    cli_env_setup()
    parser = FlexibleArgumentParser(
        description="vLLM OpenAI-Compatible RESTful API server."
    )
    parser = make_arg_parser(parser)
    args = parser.parse_args()
    validate_parsed_serve_args(args)
    uvloop.run(run_server(args))
