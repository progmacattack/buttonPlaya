from playa import Playa
from time import sleep
import gpiozero

redButton = gpiozero.Button(26)
redLed = gpiozero.LED(21)
blueButton = gpiozero.Button(19)
blueLed = gpiozero.LED(20)

playa = Playa()
while True:
    if redButton.is_pressed:
        redLed.toggle()
        if redLed.is_lit:
            blueLed.off()
            playa.playPlaylist("bach.m3u")
        else:
            playa.stop()
        sleep(0.7)
    if blueButton.is_pressed:
        blueLed.toggle()
        if blueLed.is_lit:
            redLed.off()
            playa.playPlaylist("brahams.m3u")
        else:
            playa.stop()
        sleep(0.7)

