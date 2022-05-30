#Este programa incluye funciones que muestran las vidas de 2 jugadores para el juego Tron
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
i2c = busio.I2C(SCL, SDA)
bits = [28, 64, 32, 16, 8, 4 , 2, 1]
heart = [0, 0, 0, 10, 31, 14, 4, 0]
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
disp.fill(0)
disp.show()
image = Image.new('1', (128, 64))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()


def char(xpos, ypos, pattern):
    for line in range(8):
        for ii in range(5):
            i = ii +  3
            dot = pattern[line] & bits[i]
            if dot:
                draw.point((xpos + i * 2, ypos + line * 2), fill = 255)
                draw.point((xpos + i * 2 + 1, ypos + line * 2),  fill = 255)
                draw.point((xpos + i * 2, ypos + line * 2 + 1),  fill = 255)
                draw.point((xpos + i * 2 + 1, ypos + line * 2 + 1),  fill = 255)

def displayOLED(lives1, lives2):
    # Crea la imagen con las vidas 
    if (lives1 == 0 or lives2 == 0):
        if (lives1 > lives2):
            draw.text((30, 30), 'Player 1 wins', font = font, fill = 255)
        else:
            draw.text((30, 30), 'Player 2 wins', font = font, fill = 255)
    else:
        draw.text((1, 16), 'Player 1', font = font, fill = 255)
        draw.text((80, 16), 'Player 2', font = font, fill = 255)
        if (lives1 == 3):   
            char(1, 30, heart)
            char(13, 30, heart)
            char(26 ,30, heart)
        if (lives1 == 2):
            char(1, 30, heart)
            char(13, 30, heart)
        if (lives1 == 1):
            char(1, 30, heart)
        if (lives2 == 3):   
            char(80, 30, heart)
            char(93, 30, heart)
            char(106, 30, heart)
        if (lives2 == 2):
            char(80, 30, heart)
            char(93, 30, heart)
        if (lives2 == 1):
            char(80, 30, heart)
    # Muestra las vidas
    disp.image(image)
    disp.show()
