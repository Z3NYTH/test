
from __future__ import annotations
from ..vec3 import Vec3, EPSILON
from ..ray import Ray
from ..hit import Hit
from .base import Object3D


class Plane(Object3D):
    def __init__(self, normal: Vec3, d: float):
        super().__init__()
        self.n = normal.normalize()
        self.d = d

    def depuisVetP(self, v: Vec3, p: Vec3):
        self.n = v.normalize()
        self.d = -self.n.dot(p)

    def Normale(self) -> Vec3: return self.n

    def Distance(self, p: Vec3) -> float: return self.n.dot(p) + self.d

    def intersection(self, ray: Ray) -> Hit:
        denom = self.n.dot(ray.direction)
        h = Hit()
        if abs(denom) < EPSILON:
            return h
        t = -(self.n.dot(ray.origin) + self.d) / denom
        if t <= EPSILON:
            return h
        p = ray.origin + ray.direction * t
        n = self.n if denom < 0 else -self.n
        h.t = t
        h.point = p
        h.normal = n
        h.obj = self
        h.next_medium_ior = self.mat.ior_inside if denom < 0 else self.mat.ior_outside
        return h
