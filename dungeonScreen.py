
import sys
import time
from Guy import*

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
pygame.init()
clock = pygame.time.Clock()

allSpritesList = pygame.sprite.Group()
nonGuySpritesList = pygame.sprite.Group()
g = Guy(BLACK,350,250,nonGuySpritesList)
allSpritesList.add(g)
for i in range(10):
    p = PhysicalObject(BLACK,20,20,random.randint(200,500),100,nonGuySpritesList)
    p.maxSpeed = 7
    p.setDestination(g.rect.x,g.rect.y)
    nonGuySpritesList.add(p)


screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

#pygame.display.set_caption("Hello, Howdy, Mate, and Hi there world!")


lastUpdate = time.clock()
while True:
    FRAME_RATE = 1/30
    LEFT = 1
    RIGHT = 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            g.setDestination(event.pos[0], event.pos[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            pass
    if time.clock()-lastUpdate > FRAME_RATE:
        lastUpdate = time.clock()
        screen.fill(WHITE)
        allSpritesList.draw(screen)
        nonGuySpritesList.draw(screen)
        pygame.display.flip()
        clock.tick(600)
        for i in nonGuySpritesList:
            i.update()
        g.update()
    '''
    for thing in bullets:
        hit_list = pygame.sprite.spritecollide(thing, ogres, True)
        for h in hit_list:
            print ("hit")
    for thing in ogres:
        hit_list = pygame.sprite.spritecollide(thing, bullets, True)
        for h in hit_list:
            print ("hit")
    '''
pygame.quit()
