from pygame import Vector2, draw, sprite, Surface


class Stone(sprite.Sprite):
    # Конструктор
    def __init__(self, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = Surface((30, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.width = width
        self.height = height
        self.position = Vector2(x, y)

    # Метод отображения
    def show(self, screen):
        draw.circle(screen, (50, 50, 50), (int(self.position.x),
                                           int(self.position.y)), 15)
