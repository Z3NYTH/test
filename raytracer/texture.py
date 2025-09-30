from __future__ import annotations

import math

import noise
from PIL import Image

from .hit import Hit
from .vec3 import Color


class Texture:
    def value(self, hit: Hit) -> Color:
        raise NotImplementedError


class CheckerboardTexture(Texture):
    def __init__(
        self,
        scale: float = 1.0,
        even: Color = Color(1, 1, 1),
        odd: Color = Color(0, 0, 0),
    ):
        self.scale = scale
        self.even = even
        self.odd = odd

    def value(self, hit: Hit) -> Color:
        x = math.floor(hit.u * self.scale)
        y = math.floor(hit.v * self.scale)
        return self.even if (x + y) % 2 == 0 else self.odd


class SolidColorTexture(Texture):
    def __init__(self, color: Color = Color(1, 1, 1)):
        self.color = color

    def value(self, hit: Hit) -> Color:
        return self.color


class PerlinNoiseTexture(Texture):
    def __init__(
        self,
        scale: float = 1.0,
        octaves: int = 6,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
    ):
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

    def value(self, hit: Hit) -> Color:
        # Use the 3D Perlin noise function. We use the hit point in 3D space.
        x, y, z = hit.point.x, hit.point.y, hit.point.z
        noise_val = noise.pnoise3(
            x * self.scale,
            y * self.scale,
            z * self.scale,
            octaves=self.octaves,
            persistence=self.persistence,
            lacunarity=self.lacunarity,
        )
        # Normalize from [-1, 1] to [0, 1]
        return Color(noise_val, noise_val, noise_val)


class ImageTexture(Texture):
    def __init__(self, image_path: str):
        self.image = Image.open(image_path).convert("RGB")
        self.width, self.height = self.image.size

    def value(self, hit: Hit) -> Color:
        # Map u, v to [0,1] and then to image coordinates
        u = max(0, min(1, hit.u))
        v = max(0, min(1, hit.v))
        x = int(u * (self.width - 1))
        y = int((1 - v) * (self.height - 1))  # Flip v to image coordinates
        r, g, b = self.image.getpixel((x, y))
        return Color(r / 255.0, g / 255.0, b / 255.0)
