"""Built-in computations ("kernels").

A task from the repository is only a kernel name plus parameters. The code
that runs is always one of the modules listed here, shipped inside a signed
release. Tasks cannot add code.

Every kernel module provides:
    VERSION                      integer; a task must ask for exactly this version
    KIND                         "compute" (deterministic) or "ai" (optional, local model)
    validate(params, units)      raises ValueError if the parameters are not acceptable
    run(params, unit, units, ctx) -> JSON-serialisable result
"""

from . import ai_answer, exit_scam_a, lottery_b, selftest

REGISTRY = {
    "selftest": selftest,
    "exit-scam-a": exit_scam_a,
    "lottery-b": lottery_b,
    "ai-answer": ai_answer,
}
