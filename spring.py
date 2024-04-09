from ursina import *

ITERATIONS = 8

class Spring:
    def __init__(self, mass=5, force=50, damping=4, speed=4):
        self.target = Vec3()
        self.position = Vec3()
        self.velocity = Vec3()

        self.mass = mass
        self.force = force
        self.damping = damping
        self.speed = speed

    def shove(self, force):
        self.velocity += force

    def update(self, dt):
        scaledDeltaTime = min(dt, 1) * self.speed / ITERATIONS

        for _ in range(ITERATIONS):
            iterationForce = (self.target - self.position) * (self.force / self.mass)
            acceleration = iterationForce - self.velocity * self.damping

            self.velocity += acceleration * scaledDeltaTime
            self.position += self.velocity * scaledDeltaTime

        return self.position
