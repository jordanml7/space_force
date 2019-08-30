import pygame

pygame.mixer.init()

pygame.mixer.music.load("music/Relapse.wav")
pygame.mixer.music.set_volume(1)

intro = pygame.mixer.Sound("music/Darksides.wav")
intro.set_volume(1)

laser_hit = pygame.mixer.Sound("music/explosion.wav")
laser_hit.set_volume(0.3)

crash_sound = pygame.mixer.Sound("music/boom.wav")
crash_sound.set_volume(0.3)

lost_life = pygame.mixer.Sound("music/alarm.wav")
lost_life.set_volume(1)

laser_fire = pygame.mixer.Sound("music/laser.wav")
laser_fire.set_volume(0.5)
