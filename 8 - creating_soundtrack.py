import pygame as pygame
import numpy as numpy 

pygame.init()
pygame.mixer.init()

def synth(frequency, duration = 1.5 , sampling_rate = 44100):
    frames = int(duration*sampling_rate)
    arr = numpy.cos(2*numpy.pi*frequency*numpy.linspace(0, duration, frames))
    arr = numpy.clip(10*arr, -1, 1) # ondas quadradas
    fade = list(numpy.ones(frames - 4410)) + list(numpy.linspace(1, 0, 4410))
    arr = numpy.multiply(arr, numpy.asarray(fade))

    return list(arr)

notes_file = open("noteslist.txt")
file_contents = notes_file.read()
notes_file.close()
noteslist = file_contents.splitlines()

freqs = {} 
freq = 16.3516 # frequência de início

for note in noteslist:
    freqs[note] = freq
    freq = freq * 2 ** (1/12)

with open('supermario.txt', 'r') as file:
    notes = [eval(line.rstrip()) for line in file]
file.close()

track = []

for i in range(int(len(notes)/2)):
    track = track + list(numpy.zeros(max(0, int(44.1*(notes[i*2][2]-100)))))
    track = track + synth(freqs[notes[i*2][1]], 1e-3*(notes[i*2+1][2]+100))

arr = 32767*numpy.asarray(track)*0.5
sound = numpy.asarray([arr, arr]).T.astype(numpy.int16)
sound = pygame.sndarray.make_sound(sound.copy())

sound.play()
pygame.time.wait(int(len(arr)/44.1))

pygame.mixer.quit()
pygame.quit()