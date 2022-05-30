import pygame
import time
import random
import eyed3
import RPi.GPIO as GPIO
from pygame.locals import *
from pygame.compat import geterror
from pygame import mixer
# Define buttons
btn1 = 23 #w
btn2 = 24 #a
btn3 = 25 #s
btn4 = 26 #d
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Window Size
window_x = 800
window_y = 600
# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
cycle1_color = pygame.Color(91,146,229)
cycle2_color = pygame.Color(255,110,74)

#Pygame init
pygame.init()
cycle_speed = 15
cycle1_position = [400, 50]
cycle2_position = [400, 550]
cycle1_body = [[400, 50],[400, 40]]
cycle2_body = [[400, 550],[400, 560]]
cycle1_direction = 'DOWN'   #Initial Direction
cycle2_direction = 'UP'     #Initial Direction
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

class lightCycle ():

    def __init__(self, position, body, direction, change_to, color, hearts):
      self.position = position
      self.body = body
      self.direction = direction
      self.change_to = change_to
      self.color = color
      self.hearts = hearts
      
    def movement_Right(self):
      self.change_to = 'RIGHT'
    
    def movement_Left(self):
      self.change_to = 'LEFT'
      
    def movement_Up(self):
      self.change_to = 'UP'
      
    def movement_Down(self):
      self.change_to = 'DOWN'

    def movement_restriction(self, direction):
      if self.change_to == 'UP' and self.direction != 'DOWN':
          self.direction = 'UP'
      if self.change_to == 'DOWN' and self.direction != 'UP':
          self.direction = 'DOWN'
      if self.change_to == 'LEFT' and self.direction != 'RIGHT':
          self.direction = 'LEFT'
      if self.change_to == 'RIGHT' and self.direction != 'LEFT':
          self.direction = 'RIGHT'
    
    def light(self):
        if self.direction == 'UP':
            self.position[1] -= 10
            self.body.insert(0, list(self.position))
        if self.direction == 'DOWN':
            self.position[1] += 10
            self.body.insert(0, list(self.position))
        if self.direction == 'LEFT':
            self.position[0] -= 10
            self.body.insert(0, list(self.position))
        if self.direction == 'RIGHT':
            self.position[0] += 10
            self.body.insert(0, list(self.position))
            
    def update_cycle(self, position, body, direction, change_to, color):
        pygame.init()
        self.position = position
        self.body = body
        self.direction = direction
        self.change_to = change_to
        self.color = color
        game_window.fill((0,0,0))
        pygame.display.update()
        time.sleep(1)

score = 0
def show_score(choice, color, font, size):  
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)   
    
def game_over(looser):
    cycle1_position = [400, 50]
    cycle2_position = [400, 550]
    cycle1_body = [[400, 50],[400, 40]]
    cycle2_body = [[400, 550],[400, 560]]
    cycle1_direction = 'DOWN'   #Initial Direction
    cycle2_direction = 'UP'     #Initial Direction
    if looser:
        lightCycle2.hearts -= 1
    else:
        lightCycle1.hearts -= 1
    if (lightCycle2.hearts == 0):
        winner(False) #False = jugador 1 ganador
    if (lightCycle1.hearts == 0):
        winner(True) #True = jugador 2 ganador
    lightCycle1.update_cycle(cycle1_position, cycle1_body, cycle1_direction, cycle1_direction, cycle1_color)
    lightCycle2.update_cycle(cycle2_position, cycle2_body, cycle2_direction, cycle1_direction, cycle2_color)
    
def winner(player):
    my_font = pygame.font.SysFont('calibri', 50)
    if player:
        game_over_surface = my_font.render('Winner: Player 2', True, white)
    else:
        game_over_surface = my_font.render('Winner: Player 1', True, white)
    # creating a text surface on which text will be drawn
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/2)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip() 
    time.sleep(5)
    pygame.quit()
    quit()

def button1_callback(channel):
    lightCycle1.movement_Up()
    lightCycle1.movement_restriction(lightCycle1.direction)

def button2_callback(channel):
    lightCycle1.movement_Left()
    lightCycle1.movement_restriction(lightCycle1.direction)
def button3_callback(channel):
    lightCycle1.movement_Down()
    lightCycle1.movement_restriction(lightCycle1.direction) 
def button4_callback(channel):
    lightCycle1.movement_Right()
    lightCycle1.movement_restriction(lightCycle2.direction)

lightCycle1 = lightCycle(cycle1_position, cycle1_body, cycle1_direction, cycle1_direction, cycle1_color, 3)
lightCycle2 = lightCycle(cycle2_position, cycle2_body, cycle2_direction, cycle1_direction, cycle2_color, 3)

GPIO.add_event_detect(btn1,GPIO.FALLING,callback=button1_callback) #Button pressed event
GPIO.add_event_detect(btn2,GPIO.FALLING,callback=button2_callback) #Button pressed event
GPIO.add_event_detect(btn3,GPIO.FALLING,callback=button3_callback) #Button pressed event
GPIO.add_event_detect(btn4,GPIO.FALLING,callback=button4_callback) #Button pressed event
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                lightCycle1.movement_Up()
                lightCycle1.movement_restriction(lightCycle1.direction)
            if event.key == pygame.K_s:
                lightCycle1.movement_Down()
                lightCycle1.movement_restriction(lightCycle1.direction)
            if event.key == pygame.K_a:
                lightCycle1.movement_Left()
                lightCycle1.movement_restriction(lightCycle1.direction) 
            if event.key == pygame.K_d:
                lightCycle1.movement_Right()
                lightCycle1.movement_restriction(lightCycle1.direction)
              
            if event.key == pygame.K_i:
                lightCycle2.movement_Up()
                lightCycle2.movement_restriction(lightCycle2.direction)           
            if event.key == pygame.K_k:
                lightCycle2.movement_Down()
                lightCycle2.movement_restriction(lightCycle2.direction)
            if event.key == pygame.K_j:
                lightCycle2.movement_Left()
                lightCycle2.movement_restriction(lightCycle2.direction)
            if event.key == pygame.K_l:
                lightCycle2.movement_Right()
                lightCycle2.movement_restriction(lightCycle2.direction)
 # LightCycle movement
    lightCycle1.light()
    lightCycle2.light()
    
    for pos in lightCycle1.body:
        pygame.draw.rect(game_window, lightCycle1.color, pygame.Rect(pos[0], pos[1], 10, 10))
    for pos in lightCycle2.body:
        pygame.draw.rect(game_window, lightCycle2.color, pygame.Rect(pos[0], pos[1], 10, 10))

    # Game Over conditions LightCycle 1
    # 1 False
    # 2 True
    if lightCycle1.position[0] < 0 or lightCycle1.position[0] > window_x-10:
        game_over(False)
    if lightCycle1.position[1] < 0 or lightCycle1.position[1]  > window_y-10:
        game_over(False)
    # Game Over conditions LightCycle 2  
    if lightCycle2.position[0] < 0 or lightCycle2.position[0] > window_x-10:
        game_over(True)
    if lightCycle2.position[1] < 0 or lightCycle2.position[1]  > window_y-10:
        game_over(True)
    
     # Touching the snake body
    for block in lightCycle1.body[1:]:
        if lightCycle1.position[0] == block[0] and lightCycle1.position[1] == block[1]:
            game_over(False)
            break
        if lightCycle2.position[0] == block[0] and lightCycle2.position[1] == block[1]:
            game_over(True)
            break
            
    for block in lightCycle2.body[1:]:
        if lightCycle2.position[0] == block[0] and lightCycle2.position[1] == block[1]:
            game_over(True)
            break
        if lightCycle1.position[0] == block[0] and lightCycle1.position[1] == block[1]:
            game_over(False)
            break
 
    # Refresh game screen
    pygame.display.update()
    # Frame Per Second /Refresh Rate
    fps.tick(cycle_speed)
