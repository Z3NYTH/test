from __future__ import annotations
from ..vec3 import Vec3, EPSILON
from ..ray import Ray
from ..hit import Hit
from .base import Object3D
import math

class Plane(Object3D):
    def __init__(self, normal: Vec3, d: float):
        super().__init__()
        self.n = normal.normalize()
        self.d = d
        self._setup_uv_basis()
    
    def _setup_uv_basis(self):
        """Set up basis vectors for proper UV mapping on the plane"""
        # Choose an arbitrary vector that's not parallel to the normal
        if abs(self.n.y) > 0.9:  # If normal is mostly vertical
            self.u_axis = Vec3(1, 0, 0)
        else:
            self.u_axis = Vec3(0, 1, 0)
        
        # Create orthogonal basis
        self.v_axis = self.n.cross(self.u_axis).normalize()
        self.u_axis = self.v_axis.cross(self.n).normalize()
    
    def depuisVetP(self, v: Vec3, p: Vec3):
        self.n = v.normalize()
        self.d = -self.n.dot(p)
        self._setup_uv_basis()

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

        # Calculate proper UV coordinates using the plane's basis vectors
        # Project the hit point onto the plane's UV basis
        u = p.dot(self.u_axis) / 40
        v = p.dot(self.v_axis) / 40

        # Make UV coordinates repeat every unit
        h.u = u % 1.0
        h.v = v % 1.0

        h.t = t
        h.point = p
        h.normal = n
        h.obj = self
        h.next_medium_ior = self.mat.ior_inside if denom < 0 else self.mat.ior_outside
        return h