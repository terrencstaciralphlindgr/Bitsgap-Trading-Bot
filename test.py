from time import sleep
import winsound

duration = 500  # milliseconds
freq = 750  # Hz

for _ in range(3):
    winsound.Beep(freq, duration)