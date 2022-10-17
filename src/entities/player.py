import pyglet
import pymunk

from math import radians
from globals import space, bullet_category

from .entity import Entity
from .bullet import Bullet


class Player(Entity):
    def __init__(self, x, y, batch=None, width=32):
        image = pyglet.image.load("assets/player.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        self.shots = []

        super().__init__(
            image,
            x,
            y,
            batch=batch,
            width=width,
        )

        self.shape.id = "player"
        self.shape.filter = pymunk.ShapeFilter(bullet_category)

        engine_image = pyglet.image.load("assets/fire01.png")
        engine_image.anchor_x = engine_image.width // 2
        engine_image.anchor_y = int(engine_image.height * 1.65)
        self.engine_sprite = pyglet.sprite.Sprite(
            engine_image,
            x=x,
            y=y,
            batch=batch,
        )

        self.engine_sprite.visible = False
        self.engine_sprite.scale = 1.5

        self.accelerating = False

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 1280 + self.image.width / 2
        max_y = 720 + self.image.height / 2
        if self.x < min_x:
            self.body.position = max_x, self.y
        elif self.x > max_x:
            self.body.position = min_x, self.y
        if self.y < min_y:
            self.body.position = self.x, max_y
        elif self.y > max_y:
            self.body.position = self.x, min_y

    def attack(self):
        bullet = Bullet(
            self.x,
            self.y,
            angle=self.body.angle,
            batch=self.batch,
        )
        self.shots.append(bullet)
        space.add(bullet.body, bullet.shape)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.A:
            self.body.angular_velocity = radians(180)
        elif symbol == pyglet.window.key.D:
            self.body.angular_velocity = radians(-180)
        elif symbol == pyglet.window.key.W:
            self.accelerating = True
        elif symbol == pyglet.window.key.SPACE:
            self.attack()

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.A and self.body.angular_velocity > 0:
            self.body.angular_velocity = 0
        elif symbol == pyglet.window.key.D and self.body.angular_velocity < 0:
            self.body.angular_velocity = 0
        elif symbol == pyglet.window.key.W:
            self.accelerating = False

    def update(self, dt):
        super().update(dt)

        for bullet in self.shots:
            bullet.update(dt)

        self.check_bounds()

        self.engine_sprite.position = self.body.position
        self.engine_sprite.rotation = self.rotation

        # max speed
        velocity_x, velocity_y = self.body.velocity
        if velocity_x > 150:
            velocity_x = 150
        elif velocity_x < -150:
            velocity_x = -150
        if velocity_y > 150:
            velocity_y = 150
        elif velocity_y < -150:
            velocity_y = -150

        self.body.velocity = pymunk.Vec2d(velocity_x, velocity_y)

        if self.accelerating:
            self.engine_sprite.visible = True
            force = pymunk.Vec2d(0, 5)
            force.rotated(self.body.angle)
            self.body.apply_impulse_at_local_point(force)
        else:
            self.engine_sprite.visible = False
