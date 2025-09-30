from __future__ import annotations

from ..hit import Hit
from ..ray import Ray
from ..scene import Scene
from ..vec3 import Color
from .base import Light


class AmbientLight(Light):
    def shade(self, ray: Ray, hit: Hit, scene: Scene) -> Color:
        return hit.obj.Ambiante(hit) * self.color.x
