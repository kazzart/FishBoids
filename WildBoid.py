from pygame import Vector2, image, transform, time
import numpy as np


class WildBoid:
    # Конструктор
    def __init__(self, x, y, width, height):
        self.original_image = image.load('Fish_3.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.max_speed = 12
        self.max_force = 1

        self.position = Vector2(x, y)
        vec = (np.random.rand(2) - 0.5) * 10
        self.velocity = Vector2(*vec)
        self.angle = Vector2(0, 0).angle_to(self.velocity)

        vec = (np.random.rand(2) - 0.5) / 2
        self.acceleration = Vector2(*vec)

    # Метод отображения
    def show(self, screen):
        screen.blit(self.image, (int(self.position.x), int(self.position.y)))

    # Метод обновления полей
    def update(self):
        self.position += self.velocity
        self.angle = -Vector2(0, -1).angle_to(self.velocity)
        self.image = transform.rotate(self.original_image, self.angle)
        self.velocity += self.acceleration
        # limit
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity)\
                            * self.max_speed
        self.acceleration = Vector2(*np.zeros(2))

    # Метод применения поведения
    def apply_behavior(self, boids, stones, herbivores):
        perception_cycle = self.compute_perceptions(boids)
        alignment = self.align(perception_cycle[2], perception_cycle[3])
        cohesion = self.cohesion(perception_cycle[0], perception_cycle[4])
        separation = self.separation(perception_cycle[2], perception_cycle[5])
        avoidance, near_stone = self.avoid(stones)
        pursuit, near_prey = self.hunt(herbivores)

        self.acceleration += 1.2 * separation
        self.acceleration += 0.8 * alignment
        self.acceleration += 0.8 * cohesion
        if near_stone:
            self.velocity += 1.2 * avoidance
        if near_prey:
            self.acceleration = pursuit
        if self.acceleration == Vector2(*np.zeros(2)):
            self.velocity += 0.09 * self.velocity.rotate(90)\
                             * np.sin(time.get_ticks() / 250)

    # Метод переноса границ
    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    # Метод вычисления радиусов видимости
    def compute_perceptions(self, boids):
        perception_100 = []
        perception_70 = []
        perception_50 = []
        avg_vec_align = Vector2(*np.zeros(2))
        center_of_mass = Vector2(*np.zeros(2))
        avg_vec_separate = Vector2(*np.zeros(2))
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < 100:
                if distance < 70:
                    if distance < 50:
                        perception_50.append(boid)
                        avg_vec_align += boid.velocity
                        diff = self.position - boid.position
                        diff /= distance
                        avg_vec_separate += diff
                    perception_70.append(boid)
                perception_100.append(boid)
                center_of_mass += boid.position
        return [perception_100, perception_70, perception_50,
                avg_vec_align, center_of_mass, avg_vec_separate]

    # Метод выравнивания
    def align(self, boids, avg_vec):
        perception = 50
        steering = Vector2(*np.zeros(2))
        if len(boids) > 0:
            avg_vec /= len(boids)
            avg_vec = Vector2(*avg_vec)
            avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
            steering = avg_vec - self.velocity
        return steering

    # Метод сплочености
    def cohesion(self, boids, center_of_mass):
        perception = 100
        steering = Vector2(*np.zeros(2))
        if len(boids) > 0:
            center_of_mass /= len(boids)
            center_of_mass = Vector2(*center_of_mass)
            vec_to_com = center_of_mass - self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com))\
                             * self.max_speed
            steering = vec_to_com - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering))\
                           * self.max_force
        return steering

    # Метод разделения
    def separation(self, boids, avg_vec):
        perception = 50
        steering = Vector2(*np.zeros(2))
        if len(boids) > 0:
            avg_vec /= len(boids)
            avg_vec = Vector2(*avg_vec)
            if np.linalg.norm(avg_vec) > 0:
                avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
            steering = avg_vec - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering))\
                           * self.max_force
        return steering

    # Метод избегания рифов
    def avoid(self, stones):
        perception = 70
        near = False
        steering = Vector2(*np.zeros(2))
        total = 0
        avg_vec = Vector2(*np.zeros(2))
        side = 0
        for stone in stones:
            distance = np.linalg.norm(stone.position - self.position)
            distance_vec = stone.position - self.position
            distance_vec = Vector2(*distance_vec)
            if distance < perception:
                side += distance_vec.angle_to(self.velocity)
                avg_vec += self.position - stone.position
                total += 1
        if total > 0:
            near = True
            avg_vec /= total
            avg_vec = Vector2(*avg_vec)
            if np.linalg.norm(avg_vec) > 0:
                avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
                avg_vec = Vector2(*avg_vec).rotate(-60 if side >= 0 else 60)
            steering = avg_vec - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering))\
                           * self.max_force * 2
        return steering, near

    # Метод охоты на добычу
    def hunt(self, herbivores):
        perception = 100
        steering = Vector2(*np.zeros(2))
        total = 0
        center_of_mass = Vector2(*np.zeros(2))
        near = False
        for prey in herbivores:
            distance = np.linalg.norm(prey.position - self.position)
            if self.position != prey.position and distance < perception:
                center_of_mass += prey.position
                total += 1
        if total > 0:
            near = True
            center_of_mass /= total
            center_of_mass = Vector2(*center_of_mass)
            vec_to_com = center_of_mass - self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com))\
                             * self.max_speed
            steering = vec_to_com - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering))\
                           * self.max_force
        return steering, near

    # Метод проверки съеденной жертвы
    def killed(self, herbivores):
        for prey in herbivores:
            if self.rect.colliderect(prey.rect):
                return True, prey
        return False, None
