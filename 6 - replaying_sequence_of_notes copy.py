import pygame as pygame
import numpy as numpy 

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont("Impact", 48)

def synth(frequency, duration = 1.5 , sampling_rate = 44100):
    frames = int(duration*sampling_rate)
    arr = numpy.cos(2*numpy.pi*frequency*numpy.linspace(0, duration, frames))
#    arr = numpy.clip(10*arr, -1, 1) # ondas quadradas
#    arr = numpy.cumsum(numpy.clip(arr*10, -1,1)) # ondas triangulares pt1
    arr = arr + numpy.cos(4*numpy.pi*frequency*numpy.linspace(0,duration,frames)) # simulando instrumento orgão
    arr = arr + numpy.cos(6*numpy.pi*frequency*numpy.linspace(0,duration,frames)) # simulando instrumento orgão
    arr = arr/max(numpy.abs(arr)) # ajuste de range
    sound = numpy.asarray([32767*arr, 32767*arr]).T.astype(numpy.int16)
    sound = pygame.sndarray.make_sound(sound.copy())
    
    return sound

notes_file = open("noteslist.txt")
file_contents = notes_file.read()
notes_file.close()
noteslist = file_contents.splitlines()

keymod = '0-='
notes = {} # dictionary para guardar amostras/samples
freq = 16.3516 # frequência de início
posx, posy = 25, 25 # posição de início

for i in range(len(noteslist)):
    mod = int(i/36)
    key = noteslist[i]
    sample = synth(freq)
    color = numpy.array([numpy.sin(i/25+1.7)*130+125, numpy.sin(i/30-0.21)*215+40, numpy.sin(i/25+3.7)*130+125])
    color = numpy.clip(color, 0, 255)
    notes[key] = [sample, noteslist[i], freq, (posx, posy), 255*color/max(color)]
    notes[key][0].set_volume(0.33)
    notes[key][0].play()
    notes[key][0].fadeout(100)
#    pygame.time.wait(100) # se comentar toca todas as notas uma atrás da outra
    freq = freq * 2 ** (1/12)
    posx = posx + 140
    if posx > 1220:
        posx, posy = 25, posy+56

    screen.blit(font.render(notes[key][1], 0, notes[key][4]), notes[key][3])
    pygame.display.update()

with open('soundsequence.txt', 'r') as file:
    keypresses = [eval(line.rstrip()) for line in file]
file.close()

running = 1

for i in range(len(keypresses)):
    if not running:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            
    key = keypresses[i][1]
    pygame.time.wait(keypresses[i][2])
    if keypresses[i][0]:
        notes[key][0].play()
        screen.blit(font.render(notes[key][1], 0, (255,255,255)), notes[key][3])
    else:
        notes[key][0].fadeout(100)
        screen.blit(font.render(notes[key][1], 0, notes[key][4]), notes[key][3])
    pygame.display.update()

pygame.mixer.quit()
pygame.quit()