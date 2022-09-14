import pyglet

window = pyglet.window.Window(
    caption="Simple Animation",
    width=800,
    height=600,
)

walk_images = list(
    map(
        lambda i: pyglet.image.load(f"./assets/zombie/walk/go_{i}.png"),
        range(1, 11),
    )
)

for image in walk_images:
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


animation = pyglet.image.Animation.from_image_sequence(
    walk_images,
    duration=0.1,
)


flipped_animation = animation.get_transform(flip_x=True)

sprite = pyglet.sprite.Sprite(
    flipped_animation,
    x=window.width // 2,
    y=window.height // 2,
)


@window.event
def on_draw():
    window.clear()
    sprite.draw()


pyglet.app.run()
