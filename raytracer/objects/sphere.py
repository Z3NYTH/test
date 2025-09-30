
from __future__ import annotations
from math import sqrt, inf
from ..vec3 import Vec3, EPSILON
from ..ray import Ray
from ..hit import Hit
from .base import Object3D


class Sphere(Object3D):
    def __init__(self, center: Vec3, radius: float):
        super().__init__()
        self.center = center
        self.radius = radius

    def Centre(self, p: Vec3): self.center = p

    def SphereRayon(self, r: float): self.radius = r

    def Normale(self, p: Vec3) -> Vec3: return (p - self.center).normalize()

    def intersection(self, ray: Ray) -> Hit:
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        disc = b*b - 4.0*a*c
        h = Hit()
        if disc < 0:
            return h
        sqrt_disc = sqrt(disc)
        t1 = (-b - sqrt_disc)/(2.0*a)
        t2 = (-b + sqrt_disc)/(2.0*a)
        t = inf
        for cand in (t1, t2):
            if cand > EPSILON and cand < t:
                t = cand
        if t is inf:
            return h
        p = ray.origin + ray.direction * t
        n = self.Normale(p)
        h.t = t
        h.point = p
        h.normal = n
        h.obj = self
        if ray.direction.dot(n) > 0:
            n = -n
            h.normal = n
            h.next_medium_ior = self.mat.ior_outside
        else:
            h.next_medium_ior = self.mat.ior_inside
        return h
