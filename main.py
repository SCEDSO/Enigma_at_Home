import pygame

from keyboard import Keyboard
from plugboard import Plugboard
from rotor import Rotor
from reflector import Reflector
from enigma import Enigma
from draw import draw

# set up pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Enigma simulator")

# create fonts
MONO = pygame.font.SysFont("FreeMono", 25)
BOLD = pygame.font.SysFont("FreeMono", 25, bold = True)

# global variables
WIDTH = 1600
HEIGHT = 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
MARGINS = {"top":200, "bottom":100, "left":100, "right":100}
GAP = 100
INPUT = ''
OUTPUT = ''
PATH = []

# rotors & reflectors
"""
The letter behinds the rotor wiring is a notch
"""
I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J')
V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

# ketboard & plugboard
KB = Keyboard()
"""
Enter the plugbaord routing set
"""
PB = Plugboard(["AB", "CD", "EF"]) 

# define enigma
"""
Select a reflector(A,B,C) and all three rotors(I,II,III,IV,V)
Do not alter PB and KB 
"""
ENIGMA = Enigma(B,I,II,III,PB,KB)

# set rings
"""
Select three rings(1 = A ~ 26 = Z, arranged in ascending alphabetical order)
"""
ENIGMA.set_rings((1,1,1))

# set message key
"""
Select a set of key with only three letters
"""
ENIGMA.set_key("DOG")

animating = True
while animating:

    # background
    SCREEN.fill("#333333")

    # text input
    text = BOLD.render(INPUT, True, "white")
    text_box = text.get_rect(center = (WIDTH/2, MARGINS["top"]/3 - 10))
    SCREEN.blit(text, text_box)

    # text output
    text = MONO.render(OUTPUT, True, "white")
    text_box = text.get_rect(center = (WIDTH/2, MARGINS["top"]/3 + 15))
    SCREEN.blit(text, text_box)

    # draw enigma
    draw(ENIGMA, PATH, SCREEN, WIDTH, HEIGHT, MARGINS, GAP, BOLD)

    # update screen
    pygame.display.flip()

    # track user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                II.rotate()
            elif event.key == pygame.K_SPACE:
                INPUT += ' '
                OUTPUT += ' '
            else:
                key = event.unicode
                if key in "abcdefghijklmnopqrstuvwxyz":
                    letter = key.upper()
                    INPUT += letter
                    PATH, cipher = ENIGMA.encipher(letter)
                    OUTPUT += cipher