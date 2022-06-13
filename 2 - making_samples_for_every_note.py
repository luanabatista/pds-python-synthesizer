# Tocando amostras de 0.1s de cada nota
import pygame as pygame
import numpy as numpy 

pygame.init()
pygame.mixer.init()

sampling_rate = 44100 # valor padrão do mixer do pygame
frequency = 440 # HZ
duration = 1.5 # s

# Transformando o código anterior em uma função
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
    pygame.time.wait(100) # se comentar toca todas as notas uma atrás da outra
    freq = freq * 2 ** (1/12)

pygame.mixer.quit()
pygame.quit()