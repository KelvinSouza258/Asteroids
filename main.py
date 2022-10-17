import pyglet

from globals import space, options
from src.core import Window, load_asteroids
from src.entities import Player, Asteroid, Bullet

window = Window()
main_batch = pyglet.graphics.Batch()

player = Player(
    x=window.width // 2,
    y=window.height // 2,
    width=64,
    batch=main_batch,
)

space.add(player.body, player.shape)

window.push_handlers(player)

counter = pyglet.window.FPSDisplay(window=window)

asteroids = load_asteroids(space=space, batch=main_batch)

destroyed_shapes = []


def collision_begin(arbiter, space, data):
    first_shape, second_shape = arbiter.shapes

    if first_shape.id == "bullet" and second_shape.id == "asteroid":
        destroyed_shapes.extend([first_shape, second_shape])
        return True
    elif first_shape.id == "asteroid" and second_shape.id == "bullet":
        destroyed_shapes.extend([first_shape, second_shape])
        return True

    return True


handler = space.add_default_collision_handler()
handler.begin = collision_begin


@window.event
def on_draw():
    window.clear()
    # space.debug_draw(options)
    main_batch.draw()
    counter.draw()


def update(dt):
    space.step(dt)
    game_objects = [player] + player.shots + asteroids

    for obj in game_objects:
        obj.update(dt)

        if isinstance(obj, Asteroid):
            if (
                obj.x < -400
                or obj.x > window.width + 400
                or obj.y < -400
                or obj.y > window.height + 400
                or obj.shape in destroyed_shapes
            ):
                asteroids.remove(obj)
                space.remove(obj.body, obj.shape)
                del obj
        elif isinstance(obj, Bullet):
            if (
                obj.x < -400
                or obj.x > window.width + 400
                or obj.y < -400
                or obj.y > window.height + 400
                or obj.shape in destroyed_shapes
            ):
                player.shots.remove(obj)
                space.remove(obj.body, obj.shape)
                del obj

        if len(asteroids) < 15:
            asteroids.extend(load_asteroids(space=space, batch=main_batch))


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()
