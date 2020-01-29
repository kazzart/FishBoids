import pygame
import numpy as np
from Boid import Boid
from Stone import Stone
from WildBoid import WildBoid
from Food import Food
from test import *


width = height = 800
herbivores_amount = 35
grass_amount = 10
carnivores_amount = 1
riffs_amount = 10
grass_appearance_delay = 0.35
birth_delay = 2
birth_energy_consumption = 500
food_value = 700

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Boids')
screen = pygame.Surface((width, height))

food = [Food(*np.random.rand(2)*width, width, height)
        for _ in range(grass_amount)]
flock = [Boid(*np.random.rand(2)*width, width, height)
         for _ in range(herbivores_amount)]
carnivores = [WildBoid(*np.random.rand(2)*width, width, height)
              for _ in range(carnivores_amount)]
riff = [Stone(*np.random.rand(2)*width, width, height)
        for _ in range(riffs_amount)]

grass_appearance_delay = int(grass_appearance_delay * 1000)
birth_delay *= 1000
current_time = pygame.time.get_ticks()
pygame.time.set_timer(pygame.USEREVENT, grass_appearance_delay)
done = True
while done:
    pygame.time.delay(25)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # get a list of all sprites that are under the mouse cursor
            clicked_sprites_riff = [s for s in riff
                                    if s.rect.collidepoint(pos)]
            clicked_sprites_food = [s for s in food
                                    if s.rect.collidepoint(pos)]
            if e.button == 1 and clicked_sprites_riff:
                for sprite in clicked_sprites_riff:
                    riff.remove(sprite)
            if e.button == 1 and not clicked_sprites_riff:
                riff.append(Stone(*pos, width, height))
            if e.button == 3 and clicked_sprites_food:
                for sprite in clicked_sprites_food:
                    food.remove(sprite)
            if e.button == 3 and not clicked_sprites_food:
                food.append(Food(*pos, width, height))
            print(clicked_sprites_riff, clicked_sprites_food)
        if e.type == pygame.USEREVENT:
            food.append(Food(*np.random.rand(2)*width, width, height))

    screen.fill((61, 118, 192))

    for stone in riff:
        stone.show(screen)

    for meal in food:
        meal.show(screen)

    for boid in flock:
        boid.show(screen)
        reproduction_perception = boid.apply_behavior(flock, riff,
                                                      carnivores, food)
        boid.update()
        boid.edges()
        eaten, meal = boid.eaten(food)
        if eaten:
            if boid.energy >= 1400:
                boid.satiety = True
                if (pygame.time.get_ticks() - boid.time_of_birth) >\
                        birth_delay and reproduction_perception:
                    flock.append(Boid(boid.position.x, boid.position.x,
                                      width, height))
                    boid.time_of_birth = pygame.time.get_ticks()
                    boid.energy -= birth_energy_consumption
            else:
                boid.satiety = False
                boid.energy += food_value
                food.remove(meal)
        if boid.energy <= 0:
            flock.remove(boid)

    for enemy in carnivores:
        enemy.show(screen)
        enemy.apply_behavior(carnivores, riff, flock)
        enemy.update()
        enemy.edges()
        killed, meal = enemy.killed(flock)
        if killed:
            flock.remove(meal)

    window.blit(screen, (0, 0))
    pygame.display.flip()

test(screen)
