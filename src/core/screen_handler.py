class ScreenHandler:
    def __init__(self):
        self.current = None

    def draw(self):
        self.current.draw()

    def update(self, dt):
        self.current.update(dt)
