# Import libraries
import pygame
import math

    # Represents an enemy plane in the game.
class PlaneEnemy(pygame.sprite.Sprite):

    # Initialize the properties of the enemy plane.
    def __init__(self, health, animation_list, x, y, speed, shoot_interval):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0 # 0: walk, 1: attack, 2: death
        self.update_time = pygame.time.get_ticks()
        self.shoot_interval = shoot_interval
        self.last_shoot_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    # Update the state of the enemy plane.
    def update(self, surface, target, bullet_group, enemy_bullet_group):
        if self.alive:
            if self.action == 0:
                self.rect.x += self.speed
                if self.rect.right >= target.rect.left - 50:
                    self.action = 1
                    self.speed = 0

            if pygame.sprite.spritecollide(self, bullet_group, True):
                self.health -= 25

            if self.action == 1:
                if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                    target.health -= 25
                    self.shoot(enemy_bullet_group)
                    if target.health < 0:
                        target.health = 0
                    self.last_attack = pygame.time.get_ticks()

            if self.health <= 0:
                target.money += 100
                target.score += 100
                self.update_action(2)
                self.alive = False

            self.update_animation()
            surface.blit(self.image, self.rect)

    # Make the enemy plane shoot bullets.
    def shoot(self, enemy_bullet_group):
        bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
        bullet_img = pygame.transform.scale(bullet_img, (10, 10))
        bullet = EnemyBullet(bullet_img, self.rect.right, self.rect.centery, -10)
        enemy_bullet_group.add(bullet)

    # Update the animation of the enemy plane.
    def update_animation(self):
        ANIMATION_COOLDOWN = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    # Update the action of the enemy plane.
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

# Represents a bullet shoot from the plane
class EnemyBullet(pygame.sprite.Sprite):
    
    # Initialize the properties of the bullet.
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 10
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    # Update the position of the bullet and delete when it hits the target.
    def update(self):
        SCREEN_WIDTH = 800
        if self.rect.x > SCREEN_WIDTH - 250:
            self.kill()
        self.rect.x += self.dx
        self.rect.y += self.dy
