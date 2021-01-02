from playa import Playa
from time import sleep
import gpiozero

redButton = gpiozero.Button(26)
redLed = gpiozero.LED(21)
blueButton = gpiozero.Button(19)
blueLed = gpiozero.LED(20)

class Main:
    def __init__(self):
        self.playa = Playa()
        redLed.off()
        blueLed.off()

    def __pauseOtherThan(self, otherThan):
        self.playa.pausePlaylist()

    def start(self):
        while True:
            if redButton.is_pressed:
                redLed.toggle()
                if redLed.is_lit:
                    if blueLed.is_lit:
                        print("turning off blue led")
                        blueLed.off()
                        print("pausing playlists (brahams)")
                        self.playa.pausePlaylist("brahams.m3u")
                    if self.playa.canContinuePlaylist("bach.m3u"):
                        print("continuing bach playlist")
                        self.playa.continuePlaylist("bach.m3u")
                    else:
                        print("starting bach playlist")
                        self.playa.playPlaylist("bach.m3u")
                else:
                    print("pausing bach playlist")
                    self.playa.pausePlaylist("bach.m3u")
                sleep(0.7)
            if blueButton.is_pressed:
                blueLed.toggle()
                if blueLed.is_lit:
                    if redLed.is_lit:
                        print("turning off red led")
                        redLed.off()
                        print("pausing playlists (bach)")
                        self.playa.pausePlaylist("bach.m3u")
                    if self.playa.canContinuePlaylist("brahams.m3u"):
                        print("continuing brahms playlist")
                        self.playa.continuePlaylist("brahams.m3u")
                    else: 
                        print("starting brahms playlist")
                        self.playa.playPlaylist("brahams.m3u")
                else:
                    print("pausing brahms playlist")
                    self.playa.pausePlaylist("brahams.m3u")
                sleep(0.7)

print("Starting button playa main routine")
Main().start()