import numpy as np
import sounddevice as sd

#Functional Frequencies: 300 - Start, 2100 - Stop, 1200 - Bit Sep, 2200 - Checksum announce. 


sample_rate = 44100
symbol_duration = 0.1  # 100 ms
center_freq = 1200  

# position of bit * 100 + 400 for 0 and - 400 for 1

#text = "Hello! Wow! This is a very long text to transmit!"
text = input()

def str_to_bin(text):
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))
    #return '1111111100000000'


waveform = np.array([], dtype=np.float32)

print(str_to_bin(text)) #debug

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


#begin msg
def write_msg(binary, duration):
    byte = ""
    for bit in binary:
        byte += bit
        l = 0
        if len(byte) == 8:
            print("Byte: " + byte)
            l = 0
            for i in byte:
                if i == '0':
                    l += 1
                    freq = center_freq + 100 * l
                else:
                    l += 1
                    freq = center_freq - 100 * l
                tone_add(freq, duration)
            tone_add(1200, duration)  # closing separator to flush this byte
            byte = ""


def checksum(bin):
    checksum = 0
    for bit in bin:
        checksum ^= int(bit)
    return checksum



tone_add(300, 5)  # Start tone

#START BUFFER, DONT DARE TO CHANGE
tone_add(0, 0.1)


write_msg(str_to_bin(text), symbol_duration)

tone_add(2200, 1)

print("Checksum: " + str(checksum(str_to_bin(text))))
write_msg(format(checksum(str_to_bin(text)), '08b'), symbol_duration)

tone_add(2100, 3)  # End tone

#BUFFER, DONT DARE TO CHANGE
tone_add(0, 2)

#Debug, u alr bro, free to modify
print("Waveform length:", len(waveform))
print("Max amplitude:", np.max(np.abs(waveform)))

sd.play(waveform, sample_rate)
sd.wait()