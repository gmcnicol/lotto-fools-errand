"""Generic GA module providing reusable components."""

from .evolver import (
    Evolver,
    default_select,
    never_stop,
    NoImprovement,
    ConvergenceFunc,
)

__all__ = [
    "Evolver",
    "default_select",
    "never_stop",
    "NoImprovement",
    "ConvergenceFunc",
]
