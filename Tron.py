#Tron game. Created by Diego Garcia and Oskar Villa
#June 2022
import os, pygame
import time
import random
import RPi.GPIO as GPIO
import serial
import IntegradoraMod4OLED
from pygame.locals import *
from pygame.compat import geterror
from pygame import mixer

# Configure GPIO
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

#UART configuration
ser=serial.Serial(
port='/dev/ttyACM0',
baudrate= 9600,
parity= serial.PARITY_NONE,
stopbits= serial.STOPBITS_ONE,
bytesize= serial.EIGHTBITS,timeout=1)

#Music and sounds
pygame.mixer.init() #Starts the mixer
pygame.mixer.music.load("/home/drigor130/Documentos/ActIntegradora/Derezzed.wav")
explosion_sound = pygame.mixer.Sound(r'/home/drigor130/Documentos/ActIntegradora/Explosion_Sound.wav')
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)
pygame.mixer.music.play()

#Image loads
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, '/home/drigor130/Documentos/ActIntegradora')
def loadImage(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
    return image

#Window Size
global window_x
window_x = 1200
global window_y
window_y = 800

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
cycle1_color = pygame.Color(93, 204, 182)
cycle2_color = pygame.Color(255,110,74)
cycle1_sprites = ["cycle1_0.jpeg", "cycle1_1.jpeg", "cycle1_2.jpeg", "cycle1_3.jpeg"]
cycle2_sprites = ["cycle2_0.jpeg", "cycle2_1.jpeg", "cycle2_2.jpeg", "cycle2_3.jpeg"]

#Pygame init
pygame.init()
cube_size = 5 #Size of each body element
cycle_speed = 60
cycle1_position = [window_x//2, 50]
cycle2_position = [window_x//2, window_y - 50]
cycle1_body = [[window_x//2, 50],[window_x//2, 50 - cube_size]]
cycle2_body = [[window_x//2, window_y - 50],[window_x//2, window_y - 50 + cube_size]]
cycle1_direction = 'DOWN'   #Initial Direction
cycle2_direction = 'UP'     #Initial Direction
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

#Player class
class lightCycle (pygame.sprite.Sprite):
   
    def __init__(self, position, body, direction, change_to, color, hearts, cube_size, image_name, sprites):
      pygame.sprite.Sprite.__init__(self) #call Sprite initializer
      self.position = position
      self.body = body
      self.direction = direction
      self.change_to = change_to
      self.color = color
      self.hearts = hearts
      self.cube_size = cube_size
      self.image_name = image_name
      self.image, self.rect = loadImage(self.image_name,-1)
      self.sprites = sprites
      
    def movementRight(self):
        self.change_to = 'RIGHT'
    def movementLeft(self):
      self.change_to = 'LEFT'
    def movementUp(self):
      self.change_to = 'UP'   
    def movementDown(self):
      self.change_to = 'DOWN'

    def movementRestriction(self, direction):
      if self.change_to == 'UP' and self.direction != 'DOWN':
          self.direction = 'UP'
          self.rect.midtop = (self.position[0]+4, self.position[1])
      if self.change_to == 'DOWN' and self.direction != 'UP':
          self.direction = 'DOWN'
          self.rect.midbottom = (self.position[0]+4, self.position[1]+6)
      if self.change_to == 'LEFT' and self.direction != 'RIGHT':
          self.direction = 'LEFT'
          self.rect.midleft = (self.position[0], self.position[1]+18)
      if self.change_to == 'RIGHT' and self.direction != 'LEFT':
          self.direction = 'RIGHT'
          self.rect.midright = (self.position[0]-22, self.position[1]+14)

    def light(self):
        movementSize = 5
        if self.direction == 'UP':
            self.image_name = self.sprites[0]
            self.position[1] -= movementSize
            self.body.insert(0, list(self.position))
            movementX = 0
            movementY = -movementSize  
        if self.direction == 'DOWN':
            self.image_name = self.sprites[2]
            self.position[1] += movementSize
            self.body.insert(0, list(self.position))
            movementX = 0
            movementY = movementSize    
        if self.direction == 'LEFT':
            self.image_name = self.sprites[3]
            self.position[0] -= movementSize
            self.body.insert(0, list(self.position))
            movementX = -movementSize
            movementY = 0     
        if self.direction == 'RIGHT':
            self.image_name = self.sprites[1]
            self.position[0] += movementSize
            self.body.insert(0, list(self.position))
            movementX = movementSize
            movementY = 0 
        self.image = loadImage(self.image_name)
        newpos = self.rect.move((movementX, movementY))
        self.rect = newpos
        game_window.fill(black)
    
    def explosion(self):
        explosion_sound.play()
        self.image = loadImage('ExplosionImage.png')
        newpos = self.rect.move((0, 0))
        self.rect = newpos
        game_window.fill(black)
        allsprites.update()
        game_window.blit(game_window, (0, 0))
        allsprites.draw(game_window)
        # Refresh game screen
        pygame.display.flip()
        
    def verticalLight(self):
        pygame.draw.rect(game_window, self.color, pygame.Rect(pos[0], pos[1], self.cube_size, self.cube_size))
        pygame.draw.rect(game_window, white, pygame.Rect(pos[0] + self.cube_size / 3, pos[1], self.cube_size / 3, self.cube_size))
        
    def horizontalLight(self):
        pygame.draw.rect(game_window, self.color, pygame.Rect(pos[0], pos[1], self.cube_size, self.cube_size))
        pygame.draw.rect(game_window, white, pygame.Rect(pos[0], pos[1] + self.cube_size / 3, self.cube_size, self.cube_size / 3))
        
    def updateCycle(self, position, body, direction, change_to):
        pygame.init()
        self.position = position
        self.body = body
        self.direction = direction
        self.change_to = change_to
        game_window.fill((0,0,0))
        pygame.display.update()


def start():
    my_font = pygame.font.SysFont('liberationsans', 30)
    my_font2 = pygame.font.SysFont('liberationsans', 20)
    title_font = pygame.font.SysFont('liberationsans', 200)
    #Title
    title = title_font.render('T R O N', True, cycle1_color)
    title_rect = title.get_rect()
    title_rect.midtop = (window_x//2, window_y//5 + 10)
    frame1 = Rect(0, 0, 760, 255)
    frame1.midtop = (window_x//2, window_y//5)
    frame2 = Rect(0, 0, 740, 235)
    frame2.midtop = (window_x//2, window_y//5 + 10)
    pygame.draw.rect(game_window, cycle1_color, frame1)
    pygame.draw.rect(game_window, black, frame2)
    game_window.blit(title, title_rect)
    #"Press r"
    press_key_text = my_font.render('PRESS r TO START', True, white)
    press_rect = press_key_text.get_rect()
    press_rect.midtop = (window_x//2, window_y - window_y // 3)
    game_window.blit(press_key_text, press_rect)
    #Authors
    text = my_font2.render('Hand-coded with love by:', True, white)
    text_rect = text.get_rect()
    text_rect.midtop = (window_x//2, window_y - window_y // 4)
    game_window.blit(text, text_rect)
    text = my_font.render('DIEGO GARCIA            OSKAR VILLA', True, white)
    text_rect = text.get_rect()
    text_rect.midtop = (window_x//2, window_y - window_y // 5)
    game_window.blit(text, text_rect)
    #Display
    pygame.display.flip()
    playAgain()

 
    
def gameOver(looser):
    time.sleep(1)
    cycle1_position = [window_x/2, 50]
    cycle2_position = [window_x/2, window_y - 50]
    cycle1_body = [[window_x/2, 50],[window_x/2, 50 - lightCycle1.cube_size]]
    cycle2_body = [[window_x/2, window_y - 50],[window_x/2, window_y - 50 + lightCycle1.cube_size]]
    cycle1_direction = 'DOWN'   #Initial Direction
    cycle2_direction = 'UP'     #Initial Direction
    if looser:
        lightCycle2.hearts -= 1
    else:
        lightCycle1.hearts -= 1
    IntegradoraMod4OLED.displayOLED(lightCycle1.hearts, lightCycle2.hearts)
    if (lightCycle2.hearts == 0):
        winner(False) #False = player 1 winner
    if (lightCycle1.hearts == 0):
        winner(True) #True = player 2 winner
    #Respawn position
    lightCycle1.rect.x = cycle1_position[0]-cube_size
    lightCycle1.rect.y = cycle1_position[1]
    lightCycle2.rect.x = cycle2_position[0]-cube_size
    lightCycle2.rect.y = cycle2_position[1]
    lightCycle1.updateCycle(cycle1_position, cycle1_body, cycle1_direction, cycle1_direction)
    lightCycle2.updateCycle(cycle2_position, cycle2_body, cycle2_direction, cycle1_direction)
    
def playAgain():
    while(1):
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                pygame.mixer.music.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
    
def winner(player):
    my_font = pygame.font.SysFont('liberationsans', 70)
    my_font2 = pygame.font.SysFont('liberationsans', 30)
    game_window.fill(black)
    if player:
        image = pygame.image.load('endOrange.jpg')
        image = pygame.transform.flip(image,1,0)
        #image = pygame.transform.scale(image,(window_x,window_y))
        game_window.blit(image,(0,0))
        pygame.display.update()
        gameOver_surface = my_font.render('PLAYER 2 WINS', True, cycle2_color)
    else:
        image = pygame.image.load('endBlue.jpg')
        #image = pygame.transform.scale(image,(window_x,window_y))
        game_window.blit(image,(0,0))
        pygame.display.update()
        gameOver_surface = my_font.render('PLAYER 1 WINS', True, cycle1_color)
    
    gameOver_rect = gameOver_surface.get_rect()
    gameOver_rect.midtop = (window_x - window_x//3 ,  window_y//7)
    game_window.blit(gameOver_surface, gameOver_rect)
    press_key_text = my_font2.render('PRESS r TO PLAY AGAIN OR q TO QUIT', True, white)
    press_rect = press_key_text.get_rect()
    press_rect.midtop = (window_x - window_x//3, window_y//7 + 70)
    game_window.blit(press_key_text, press_rect)
    pygame.display.flip()
    
    playAgain()      
    lightCycle1.hearts = 3
    lightCycle2.hearts = 3
    IntegradoraMod4OLED.displayOLED(lightCycle1.hearts, lightCycle2.hearts)
    #pygame.quit()
    #quit()

def button1_callback(channel):
    lightCycle1.movementUp()
    lightCycle1.movementRestriction(lightCycle1.direction)
def button2_callback(channel):
    lightCycle1.movementLeft()
    lightCycle1.movementRestriction(lightCycle1.direction)
def button3_callback(channel):
    lightCycle1.movementDown()
    lightCycle1.movementRestriction(lightCycle1.direction) 
def button4_callback(channel):
    lightCycle1.movementRight()
    lightCycle1.movementRestriction(lightCycle2.direction)

lightCycle1 = lightCycle(cycle1_position, cycle1_body, cycle1_direction, cycle1_direction, cycle1_color, 3, cube_size, cycle1_sprites[2], cycle1_sprites)
lightCycle2 = lightCycle(cycle2_position, cycle2_body, cycle2_direction, cycle1_direction, cycle2_color, 3, cube_size, cycle2_sprites[0], cycle2_sprites)

#/////////////////////////////////////////////////////////////////////
allsprites = pygame.sprite.RenderPlain((lightCycle1, lightCycle2))
#Starting positions
lightCycle1.rect.x = cycle1_position[0]-cube_size
lightCycle1.rect.y = cycle1_position[1]
lightCycle2.rect.x = cycle2_position[0]-cube_size
lightCycle2.rect.y = cycle2_position[1]

#/////////////////////////////////////////////////////////////////////
#Event detection for GPIO
GPIO.add_event_detect(btn1,GPIO.FALLING,callback=button1_callback) #Button pressed event
GPIO.add_event_detect(btn2,GPIO.FALLING,callback=button2_callback) #Button pressed event
GPIO.add_event_detect(btn3,GPIO.FALLING,callback=button3_callback) #Button pressed event
GPIO.add_event_detect(btn4,GPIO.FALLING,callback=button4_callback) #Button pressed event

#Main screen
start()

#OLED display
IntegradoraMod4OLED.displayOLED(lightCycle1.hearts, lightCycle2.hearts)

#Main function
def main():
    while True:
        #UART buttons
        player2Button = ser.readline(ser.in_waiting)
        if (player2Button == b'w\r\n'):
            lightCycle2.movementUp()
            lightCycle2.movementRestriction(lightCycle2.direction)           
        if (player2Button == b's\r\n'):
            lightCycle2.movementDown()
            lightCycle2.movementRestriction(lightCycle2.direction)
        if (player2Button == b'a\r\n'):
            lightCycle2.movementLeft()
            lightCycle2.movementRestriction(lightCycle2.direction)
        if (player2Button == b'd\r\n'):
            lightCycle2.movementRight()
            lightCycle2.movementRestriction(lightCycle2.direction)
        #Keyboard control
        for event in pygame.event.get():
            #Play the music again if it stops
            if event.type == MUSIC_END:
                    pygame.mixer.music.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    lightCycle1.movementUp()
                    lightCycle1.movementRestriction(lightCycle1.direction)
                if event.key == pygame.K_s:
                    lightCycle1.movementDown()
                    lightCycle1.movementRestriction(lightCycle1.direction)
                if event.key == pygame.K_a:
                    lightCycle1.movementLeft()
                    lightCycle1.movementRestriction(lightCycle1.direction) 
                if event.key == pygame.K_d:
                    lightCycle1.movementRight()
                    lightCycle1.movementRestriction(lightCycle1.direction)
                  
                if event.key == pygame.K_i or player2Button == "w\r\n":
                    lightCycle2.movementUp()
                    lightCycle2.movementRestriction(lightCycle2.direction)           
                if event.key == pygame.K_k or player2Button == "s\r\n":
                    lightCycle2.movementDown()
                    lightCycle2.movementRestriction(lightCycle2.direction)
                if event.key == pygame.K_j or player2Button == "a\r\n":
                    lightCycle2.movementLeft()
                    lightCycle2.movementRestriction(lightCycle2.direction)
                if event.key == pygame.K_l or player2Button == "d\r\n":
                    lightCycle2.movementRight()
                    lightCycle2.movementRestriction(lightCycle2.direction)
         # LightCycle movement
        lightCycle1.light()
        lightCycle2.light()
        for pos in lightCycle1.body:
            pygame.draw.rect(game_window, lightCycle1.color, pygame.Rect(pos[0], pos[1], cube_size, cube_size))
        for pos in lightCycle2.body:
            pygame.draw.rect(game_window, lightCycle2.color, pygame.Rect(pos[0], pos[1], cube_size, cube_size))
            
        # Game Over conditions LightCycle 1
        # 1 False - 2 True
        if lightCycle1.position[0] < 0 or lightCycle1.position[0] > window_x-cube_size:
            lightCycle1.explosion()
            gameOver(False)
        if lightCycle1.position[1] < 0 or lightCycle1.position[1]  > window_y-cube_size:
            lightCycle1.explosion()
            gameOver(False)
        # Game Over conditions LightCycle 2  
        if lightCycle2.position[0] < 0 or lightCycle2.position[0] > window_x-cube_size:
            lightCycle2.explosion()
            gameOver(True)
        if lightCycle2.position[1] < 0 or lightCycle2.position[1]  > window_y-cube_size:
            lightCycle2.explosion()
            gameOver(True)
        
         # Touching the lightbeam
        for block in lightCycle1.body[1:]:
            if lightCycle1.position[0] == block[0] and lightCycle1.position[1] == block[1]:
                lightCycle1.explosion()
                gameOver(False)
                break
            if lightCycle2.position[0] == block[0] and lightCycle2.position[1] == block[1]:
                lightCycle2.explosion()
                gameOver(True)
                break
        for block in lightCycle2.body[1:]:
            if (lightCycle2.position[0] == block[0]) and lightCycle2.position[1] == block[1]:
                lightCycle2.explosion()
                gameOver(True)
                break
            if lightCycle1.position[0] == block[0] and lightCycle1.position[1] == block[1]:
                lightCycle1.explosion()
                gameOver(False)
                break
            
        #//////////////////////////////////////////////////////////
        allsprites.update()
        game_window.blit(game_window, (0, 0))
        allsprites.draw(game_window)
        #//////////////////////////////////////////////////////////
        # Refresh game screen
        pygame.display.flip()
        # Frame Per Second /Refresh Rate
        fps.tick(cycle_speed)
main()