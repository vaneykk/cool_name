from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = (153, 204,255)

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if self.rect.x <= 650 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
            platforms_touched = sprite.spritecollide(self, walls, False)
            if self.x_speed > 0: # идём вправо
                for p in platforms_touched:
                    self.rect.right = min(self.rect.right, p.rect.left)
            elif self.x_speed < 0: # идём налево
                for p in platforms_touched:
                    self.rect.left = max(self.rect.left, p.rect.right)
        if self.rect.y <= 450 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
            platforms_touched = sprite.spritecollide(self, walls, False)
            if self.y_speed > 0: # идём вниз
                for p in platforms_touched:
                    self.rect.bottom = min(self.rect.bottom, p.rect.top)
            if self.y_speed < 0: # идём вверх
                for p in platforms_touched:
                    self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.jpg', 15, 15, self.rect.right, self.rect.centery, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):ф
        self.rect.x += self.speed
        if self.rect.x >= 650:
            self.speed *= -1
        if self.rect.x <= 0:
            self.speed *= -1
        
class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        # исчезает, если дойдёт до края экрана
        if self.rect.x > 700:
            self.kill()

wall_1 = GameSprite('wall.jpg', 50, 350, 450, 150)
wall_2 = GameSprite('wall.jpg', 250, 50, 200, 250)
wall_3 = GameSprite('wall.jpg', 125, 50, 500, 275)

walls = sprite.Group()
walls.add(wall_1)
walls.add(wall_2)
walls.add(wall_3)

bullets = sprite.Group()

player = Player('kolobok.jpg', 50, 50, 60, 350, 0, 0)
final = GameSprite('final_okno.jpg', 50, 50, 550, 400)

monster = Enemy('monster.jpg', 50, 50, 600, 40, 2)
monsters = sprite.Group()
monsters.add(monster)

walls.draw(window)

finish = False
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.y_speed = -5
            if e.key == K_s:
                player.y_speed = 5
            if e.key == K_a:
                player.x_speed = -5
            if e.key == K_d:
                player.x_speed = 5
            if e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                player.y_speed = 0
            if e.key == K_s:
                player.y_speed = 0
            if e.key == K_a:
                player.x_speed = 0
            if e.key == K_d:
                player.x_speed = 0
        
    if finish != True:
        window.fill(background)
        walls.draw(window)   
        player.reset()
        monsters.draw(window)
        bullets.update()
        player.update()
        monsters.update()
        bullets.draw(window)
        final.reset()
        sprite.groupcollide(bullets, walls, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
        if sprite.collide_rect(player, final):
            finish = True
            final_picture = transform.scale(image.load('final_picture.jpg'), (700, 500))
            window.blit(final_picture, (0, 0))
        elif sprite.collide_rect(player, monster):
            finish = True
            final_kartinka = transform.scale(image.load('defeat.jpg'), (700, 500))
            window.blit(final_kartinka, (0, 0))
        
    display.update()
