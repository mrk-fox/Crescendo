import numpy as np
import sounddevice as sd

sample_rate = 44100
symbol_duration = 0.1  # 100 ms
center_freq = 1200  

# position of bit * 100 + 400 for 0 and - 400 for 1

text = "HHHH"

binary = ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

waveform = np.array([], dtype=np.float32)

print(binary)

def tone_add(freq, duration):
    global waveform, sample_rate
    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False
    )
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    waveform = np.concatenate((waveform, tone))  # return it

tone_add(1500, 5)  # Start tone

#START BUFFER, DONT DARE TO CHANGE
tone_add(0, 0.1)

#begin msg
duration = symbol_duration
byte = ""
for bit in binary:
    byte += bit
    l = 0
    if len(byte) == 8:
        print(byte) #debug
        l = 0

        for i in byte:
            if i == '0':
                l += 1
                freq = center_freq + 100 * l
            else:
                l += 1
                freq = center_freq - 100 * l
            tone_add(freq, duration)
        byte = ""



tone_add(1000, 3)  # End tone

#BUFFER, DONT DARE TO CHANGE
tone_add(0, 2)

#Debug, u alr bro, free to modify
print("Waveform length:", len(waveform))
print("Max amplitude:", np.max(np.abs(waveform)))

sd.play(waveform, sample_rate)
sd.wait()