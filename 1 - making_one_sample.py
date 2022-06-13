import pygame as pygame
import numpy as numpy 

pygame.init()
pygame.mixer.init()

sampling_rate = 44100 # valor padrão do mixer do pygame
frequency = 440 # Hz
duration = 1.5 # s
frames = int(duration*sampling_rate)
arr = numpy.cos(2*numpy.pi*frequency*numpy.linspace(0,duration, frames))
sound = numpy.asarray([32767*arr,32767*arr]).T.astype(numpy.int16)
sound = pygame.sndarray.make_sound(sound.copy())
sound.play()


