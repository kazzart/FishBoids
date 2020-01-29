from pygame import Vector2, image, sprite


class Food(sprite.Sprite):
    # Конструктор
    def __init__(self, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = image.load('Food_1.png')
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.position = Vector2(x, y)

    # Метод отображения
    def show(self, screen):
        self.rect = self.image.get_rect(center=(int(self.position.x),
                                                int(self.position.y)))
        screen.blit(self.image, self.rect)
