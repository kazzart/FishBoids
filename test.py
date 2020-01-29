from Food import *
from Boid import *
from WildBoid import *
import numpy as np


def test(screen):
    test_mold_eaten = Food(21, 39, 800, 800)
    test_mold_not_eaten = Food(100, 39, 800, 800)
    test_herbivore_eaten = Boid(21, 39, 800, 800)
    test_herbivore_not_eaten = Boid(201, 39, 800, 800)
    test_carnivore = WildBoid(21, 39, 800, 800)

    test_mold_eaten.rect = test_mold_eaten.rect.move(int(test_mold_eaten.position.x),
                                                     int(test_mold_eaten.position.y))
    screen.blit(test_mold_eaten.image, (int(test_mold_eaten.position.x), int(test_mold_eaten.position.y)))
    test_mold_not_eaten.rect = test_mold_not_eaten.rect.move(int(test_mold_not_eaten.position.x),
                                                             int(test_mold_not_eaten.position.y))
    screen.blit(test_mold_not_eaten.image, (int(test_mold_not_eaten.position.x), int(test_mold_not_eaten.position.y)))
    test_herbivore_eaten.rect = test_herbivore_eaten.rect.move(int(test_herbivore_eaten.position.x),
                                                               int(test_herbivore_eaten.position.y))
    screen.blit(test_herbivore_eaten.image, (int(test_herbivore_eaten.position.x), int(test_herbivore_eaten.position.y)))
    test_herbivore_not_eaten.rect = test_herbivore_not_eaten.rect.move(int(test_herbivore_not_eaten.position.x),
                                                                       int(test_herbivore_not_eaten.position.y))
    screen.blit(test_herbivore_not_eaten.image, (int(test_herbivore_not_eaten.position.x), int(test_herbivore_not_eaten.position.y)))
    test_carnivore.rect = test_carnivore.rect.move(int(test_carnivore.position.x),
                                                   int(test_carnivore.position.y))
    screen.blit(test_carnivore.image, (int(test_carnivore.position.x), int(test_carnivore.position.y)))

    food = [test_mold_eaten, test_mold_not_eaten]
    prey = [test_herbivore_eaten, test_herbivore_not_eaten]

    def test_eaten():
        assert test_herbivore_eaten.eaten(food) ==\
            (True, test_mold_eaten), "Should be (True, test_mold_eaten)"
        print("First test passed")

    def test_killed():
        assert test_carnivore.killed(prey) ==\
            (True, test_herbivore_eaten), "Should be (True, test_herbivore_eaten)"
        print("Second test passed")

    test_eaten()
    test_killed()
