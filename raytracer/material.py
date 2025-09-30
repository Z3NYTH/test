from __future__ import annotations

from dataclasses import dataclass, field

from .texture import SolidColorTexture, Texture
from .vec3 import Color


@dataclass(slots=True)
class Material:
    texture: Texture = field(default_factory=lambda: SolidColorTexture(Color(1, 1, 1)))
    ka: float = 0.3
    kd: float = 0.8
    ks: float = 0.6
    kr: float = 0.0
    kt: float = 0.0
    ior_inside: float = 1.0
    ior_outside: float = 1.0

    def colorTex(self, hit: Hit) -> Color:
        return self.texture.value(hit)
