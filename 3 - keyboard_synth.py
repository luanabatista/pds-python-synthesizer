import pygame as pygame
import numpy as numpy 

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont("Impact", 48)

def synth(frequency, duration = 1.5 , sampling_rate = 44100):
    frames = int(duration*sampling_rate)
    arr = numpy.cos(2*numpy.pi*frequency*numpy.linspace(0, duration, frames))
    sound = numpy.asarray([32767*arr, 32767*arr]).T.astype(numpy.int16)
    sound = pygame.sndarray.make_sound(sound.copy())
    
    return sound

keylist = '123456789qwertyuiopasdfghjklzxcvbnm,'
notes_file = open("noteslist.txt")
file_contents = notes_file.read()
notes_file.close()
noteslist = file_contents.splitlines()

keymod = '0-='
notes = {} # dictionary para guardar amostras/samples
freq = 16.3516 # frequência de início

for i in range(len(noteslist)):
    mod = int(i/36)
    key = keylist[i-mod*36]+str(mod)
    sample = synth(freq)
    notes[key] = [sample, noteslist[i], freq]
    notes[key][0].set_volume(0.33)
    notes[key][0].play()
    notes[key][0].fadeout(100)
#    pygame.time.wait(100) # se comentar toca todas as notas uma atrás da outra
    freq = freq * 2 ** (1/12)

running = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            key = str(event.unicode)
            if key in keymod:
                mod = keymod.index(str(event.unicode))
            elif key in keylist:
                key = key+str(mod)
                notes[key][0].play()
        if event.type == pygame.KEYUP and str(event.unicode) != '' and str(event.unicode) in keylist:
            key = str(event.unicode)+str(mod)
            notes[key][0].fadeout(100)
            
pygame.mixer.quit()
pygame.quit()