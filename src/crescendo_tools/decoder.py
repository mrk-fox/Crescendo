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
from scipy.fftpack import fft
import datetime

SAMPLE_RATE = 44100   # hz
DURATION    = 0.1    # sec per chunk
CHUNK_SIZE  = int(SAMPLE_RATE * DURATION)

current_fq = 0
center_fq = 1200
curr_bit_p = 0
byte_array = [None, None, None, None, None, None, None, None]
msg_running = False
checksum = 0
rx_checksum = 0
decoded = ""
cs_c_cpl = False
cs_inb_heard = False
start_rx = False
pass_key = False
reset_todo = False
twoto = 0


def get_dominant_frequency(audio_chunk, sample_rate):
    windowed = audio_chunk * np.hanning(len(audio_chunk))
    fft_result = fft(windowed)
    magnitudes  = np.abs(fft_result[:CHUNK_SIZE // 2])
    frequencies = np.fft.rfftfreq(CHUNK_SIZE, d=1.0 / sample_rate)[:CHUNK_SIZE // 2]

    peak_idx = np.argmax(magnitudes)
    return frequencies[peak_idx], magnitudes[peak_idx]


def read_data(freq):
    global curr_bit_p
    deviation = -(freq - center_fq)
    byte_rel_bit_pos = np.abs(deviation)/100

    if (freq == 2100):
        return "e", True, -1
    elif (freq == 300):
        return "s", True, -1
    elif (freq == 2200):
        return "c", True, -1
    elif (freq == 1200):
        curr_bit_p = 0
        return "n", None, byte_rel_bit_pos


    if (deviation < 0) :
        curr_bit_p = curr_bit_p + 1
        return "d", False, byte_rel_bit_pos
    elif (deviation > 0) :
        curr_bit_p = curr_bit_p + 1
        return "d", True, byte_rel_bit_pos

    

def write_data(data, pos):
    global byte_array
    try:
        byte_array[int(pos)-1] = data
    except Exception:
        pass


def save_data():
    o = ""
    for b in byte_array:
        if(b == True):
            o = o + "1"
        elif(b == False):
            o = o + "0"
        else:
            o = o + str(twoto)
    return o


def calc_checksum(bin):
    checksum = 0
    for bit in bin:
        checksum ^= int(bit)
    return checksum   


def translate(data):
    chars = [data[i:i+8] for i in range(0, len(data), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)


def reset():
    global curr_bit_p, byte_array, msg_running, checksum, rx_checksum, decoded, cs_c_cpl, pass_key, cs_inb_heard, start_rx, reset_todo
    if reset_todo:
        curr_bit_p = 0
        byte_array = [None, None, None, None, None, None, None, None]
        msg_running = False
        checksum = 0
        rx_checksum = 0
        decoded = ""
        cs_c_cpl = False
        cs_inb_heard = False
        start_rx = False
        pass_key = False
        print(tr() + "Internal values reset completed.")
        reset_todo = False
    
def tr():
    x = "[" + str(datetime.datetime.now().strftime("%H:%M:%S.%f")) + "]: "
    return x


def run():
    global decoded, cs_inb_heard, start_rx, pass_key, cs_c_cpl, reset_todo, data

    print(tr() + "Started audio input processing. KeyboardInterrupt: 'CTRL+C'")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
        try:
            while True:
                audio_chunk, _ = stream.read(CHUNK_SIZE)
                audio_mono      = audio_chunk[:, 0]        # flatten to 1-D
                freq, magnitude = get_dominant_frequency(audio_mono, SAMPLE_RATE)

                if magnitude > 0.01:
                    if(read_data(freq)[0] == "s" and start_rx == False): #start
                        reset()
                        start_rx = True
                        pass_key = True
                        reset_todo = True
                        print("")
                        print(tr() + "--------------------Data inbound--------------------")
                    elif(read_data(freq)[0] == "d" and pass_key == True): #data
                        write_data(read_data(freq)[1], read_data(freq)[2])
                    elif(read_data(freq)[0] == "n" and pass_key == True): #new byte
                        data = save_data()
                        decoded = decoded + data
                        print(tr() + "RX: " + data) #+ decoded)
                    elif(read_data(freq)[0] == "c" and cs_inb_heard == False and pass_key == True): #checksum inbound
                        decoded_data = decoded
                        decoded = ""
                        cs_inb_heard = True
                    elif(read_data(freq)[0] == "e" and cs_c_cpl == False): #end
                        if (pass_key == True):
                            try:
                                rx_checksum = int(decoded, 2)
                            except Exception:
                                rx_checksum = 0
                            checksum_val = calc_checksum(decoded_data)
                            print(tr() + "--------------------RX Finished--------------------")

                            if (rx_checksum == checksum_val):
                                print(tr() + "CHECKSUM BLOCK")
                                print("     Checksums match!")
                                print("")
                                cs_c_cpl = True  
                            else:
                                print(tr() + "CHECKSUM BLOCK")
                                print("     Checksums do not match!")
                                print("     Checksum of the data:" + str(checksum_val))
                                print("     Checksum of the ChRX:" + str(rx_checksum))     
                                print("") 
                            print("Final data: " + decoded_data)
                            print("UTF-8 Message: " + translate(decoded_data))
                            print(tr() + "--------------------Cycle End--------------------")
                        reset()
                        
        except KeyboardInterrupt:
            if (len(decoded) != 0):
                print("")
                print(tr() + "--------------------RX Interrupted--------------------")
                print(tr() + "Datastream interrupted! Recovering...")

                print("Final data: " + decoded)
                print(tr() + "--------------------Cycle End--------------------")

            print(tr() + "Stopped.")
