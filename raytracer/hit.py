from __future__ import annotations

from dataclasses import dataclass, field
from math import inf
from typing import Optional

from .vec3 import EPSILON, Vec3


@dataclass(slots=True)
class Hit:
    t: float = inf
    point: Vec3 = field(default_factory=lambda: Vec3(0, 0, 0))
    normal: Vec3 = field(default_factory=lambda: Vec3(0, 0, 0))
    u: float = 0.0  # New texture coordinate
    v: float = 0.0  # New texture coordinate
    obj: Optional[Object3D] = None
    next_medium_ior: float = 1.0

    def valid(self) -> bool:
        return self.obj is not None and self.t > EPSILON
