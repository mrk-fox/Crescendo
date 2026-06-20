# Crescendo: Carrier-frequency defined, arpeggiated data-to-audio modulation
# Copyright (C) 2026  Mark Scharonow

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import sounddevice as sd
import wave
import datetime

# Functional Frequencies: 300 - Start, 2100 - Stop, 1200 - Bit Sep, 2200 - Checksum announce.

sample_rate = 44100
symbol_duration = 0.1  # 100 ms
center_freq = 1200

# position of bit * 100 + 400 for 0 and - 

def tr():
    x = "[" + str(datetime.datetime.now().strftime("%H:%M:%S.%f")) + "]: "
    return x

def str_to_bin(text):
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))
    # return '1111111100000000' #debug

waveform = np.array([], dtype=np.float32)

def tone_add(freq, duration):
    global waveform, sample_rate
    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False
    )
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    waveform = np.concatenate((waveform, tone))

# begin msg
def write_msg(binary, duration):
    byte = ""
    for bit in binary:
        byte += bit
        l = 0
        if len(byte) == 8:
            #print("Byte: " + byte) #debug
            l = 0
            for i in byte:
                if i == '0':
                    l += 1
                    freq = center_freq + 100 * l
                else:
                    l += 1
                    freq = center_freq - 100 * l
                tone_add(freq, duration)
            tone_add(1200, duration)
            byte = ""


def checksum(bin):
    checksum = 0
    for bit in bin:
        checksum ^= int(bit)
    return checksum


def generate(i_text):
    print(tr() + "--------------------Encoding Data--------------------")

    global waveform
    waveform = np.array([], dtype=np.float32)
    binary = str_to_bin(i_text)
    print(tr() + binary)

    tone_add(300, 5)  # Start tone
    tone_add(0, 0.1)
    write_msg(binary, symbol_duration)
    tone_add(2200, 1)

    print("Checksum: " + str(checksum(binary)))
    write_msg(format(checksum(binary), '08b'), symbol_duration)
    tone_add(2100, 3)  # End tone
    tone_add(0, 2)


def run(i_text):
    generate(i_text)
    print(tr() + "-----------------Playing Encoded Data-----------------")
    sd.play(waveform, sample_rate)
    sd.wait()    

def wav(i_text, filename):
    global waveform, sample_rate
    generate(i_text)
    # float32 to int16
    audio_int16 = np.int16(waveform * 32767)
    print(tr() + "--------------------Generating File--------------------")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)      # mono
        wf.setsampwidth(2)      # 2 bytes = 16 bits
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())

    print(tr() + f"Saved {filename}")

def direct():
    try:
        while True:
            direct_input = input("> ")
            run(direct_input)
    except KeyboardInterrupt:
        print(tr() + "Terminating...")