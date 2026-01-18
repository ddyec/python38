"""Rotating hexagon ball physics with mouse grab/throw.

Controls:
- Left mouse button: grab and drag the ball, release to throw.
- Esc or window close: quit.

Dependencies:
- pygame (pip install pygame)
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import pygame


WIDTH, HEIGHT = 900, 700
FPS = 60
GRAVITY = pygame.Vector2(0, 900)  # pixels/s^2
BALL_RADIUS = 18
BALL_MASS = 1.0
RESTITUTION = 0.85
FRICTION = 0.2
HEX_RADIUS = 240
HEX_CENTER = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
ANGULAR_SPEED = math.radians(25)  # rad/s


@dataclass
class Ball:
    pos: pygame.Vector2
    vel: pygame.Vector2

    def apply_force(self, force: pygame.Vector2, dt: float) -> None:
        self.vel += (force / BALL_MASS) * dt

    def integrate(self, dt: float) -> None:
        self.pos += self.vel * dt


@dataclass
class DragState:
    active: bool = False
    grab_offset: pygame.Vector2 = pygame.Vector2(0, 0)
    last_mouse: pygame.Vector2 = pygame.Vector2(0, 0)
    throw_vel: pygame.Vector2 = pygame.Vector2(0, 0)

    def reset(self) -> None:
        self.active = False
        self.grab_offset.update(0, 0)
        self.throw_vel.update(0, 0)


def hexagon_vertices(center: pygame.Vector2, radius: float, angle: float) -> list[pygame.Vector2]:
    vertices = []
    for i in range(6):
        theta = angle + i * math.tau / 6
        vertices.append(pygame.Vector2(
            center.x + radius * math.cos(theta),
            center.y + radius * math.sin(theta),
        ))
    return vertices


def resolve_collision(ball: Ball, vertices: list[pygame.Vector2], angle: float, dt: float) -> None:
    # For each edge, keep the ball inside by pushing it along the inward normal.
    for i in range(6):
        a = vertices[i]
        b = vertices[(i + 1) % 6]
        edge = b - a
        normal = pygame.Vector2(-edge.y, edge.x)
        if normal.length_squared() == 0:
            continue
        normal = normal.normalize()

        # Ensure normal points inward
        to_center = HEX_CENTER - (a + b) * 0.5
        if normal.dot(to_center) < 0:
            normal = -normal

        # Signed distance from ball center to edge line
        dist = (ball.pos - a).dot(normal)
        penetration = BALL_RADIUS - dist
        if penetration > 0:
            # Push ball inward
            ball.pos += normal * penetration

            # Relative velocity against wall including rotational velocity
            wall_point = ball.pos
            radial = wall_point - HEX_CENTER
            wall_vel = pygame.Vector2(-ANGULAR_SPEED * radial.y, ANGULAR_SPEED * radial.x)
            rel_vel = ball.vel - wall_vel

            vn = rel_vel.dot(normal)
            if vn < 0:
                # Reflect normal component with restitution
                ball.vel -= (1 + RESTITUTION) * vn * normal

                # Apply tangential friction
                tangent = pygame.Vector2(-normal.y, normal.x)
                vt = rel_vel.dot(tangent)
                friction_impulse = -vt * FRICTION
                ball.vel += friction_impulse * tangent


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rotating Hexagon Ball")
    clock = pygame.time.Clock()

    ball = Ball(pos=pygame.Vector2(WIDTH * 0.5, HEIGHT * 0.5 - 120), vel=pygame.Vector2(180, 0))
    drag = DragState()
    angle = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.Vector2(event.pos)
                if (mouse - ball.pos).length() <= BALL_RADIUS + 4:
                    drag.active = True
                    drag.grab_offset = ball.pos - mouse
                    drag.last_mouse = mouse
                    drag.throw_vel.update(0, 0)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drag.active:
                    ball.vel = drag.throw_vel
                drag.reset()

        if drag.active:
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            ball.pos = mouse + drag.grab_offset
            drag.throw_vel = (mouse - drag.last_mouse) / max(dt, 1e-6)
            drag.last_mouse = mouse
        else:
            ball.apply_force(GRAVITY, dt)
            ball.integrate(dt)

        angle += ANGULAR_SPEED * dt
        vertices = hexagon_vertices(HEX_CENTER, HEX_RADIUS, angle)
        resolve_collision(ball, vertices, angle, dt)

        screen.fill((18, 18, 24))
        pygame.draw.polygon(screen, (90, 120, 200), vertices, width=4)
        pygame.draw.circle(screen, (240, 200, 120), ball.pos, BALL_RADIUS)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
