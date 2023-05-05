import pygame
import sys
import os


ani=4
ALPHA=(0,255,0)

class Hero(pygame.sprite.Sprite):
    ani = 4
    ALPHA = (0, 255, 0)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.steps=5
        self.movex=0
        self.movey=0
        self.frame=0
        self.HP=100
        self.ATK=10
        self.DEF=10
        self.images=[]
        for i in range(1,17):
            img=pygame.image.load(os.path.join('images','player'+str(i)+'.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image=self.images[0]
            self.rect=self.image.get_rect()

    def control(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.movey-=self.steps
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.movey+=self.steps
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.movex-=self.steps
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.movex+=self.steps

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.movey += self.steps
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.movey -= self.steps
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.movex += self.steps
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.movex -= self.steps

    def update(self,screen):
        self.rect.x=self.rect.x+self.movex
        self.rect.y = self.rect.y + self.movey
        if self.movey<0:
            self.frame+=1
            if self.frame>3*ani:
                self.frame=0
            self.image=self.images[self.frame//ani+12]
        if self.movey>0:
            self.frame+=1
            if self.frame>3*ani:
                self.frame=0
            self.image=self.images[self.frame//ani]
        if self.movex<0:
            self.frame+=1
            if self.frame>3*ani:
                self.frame=0
            self.image=self.images[self.frame//ani+4]
        if self.movex>0:
            self.frame+=1
            if self.frame>3*ani:
                self.frame=0
            self.image=self.images[self.frame//ani+8]
