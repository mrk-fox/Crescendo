import numpy as np

current_fq = 0
center_fq = 1200
curr_bit_p = 0

def read_data(freq):
    global current_fq, center_fq, curr_bit_p
    deviation = -(freq - center_fq)
    byte_rel_bit_pos = np.abs(deviation)/100

    if (freq == 2100):
        return "e", True, -1
    elif (freq == 300):
        return "s", True, -1

    if (deviation < 0) :
        curr_bit_p = curr_bit_p + 1
        return "d", True, byte_rel_bit_pos
    elif (deviation > 0) :
        curr_bit_p = curr_bit_p + 1
        return "d", False, byte_rel_bit_pos
    else:
        curr_bit_p = 0
        return "n", None, byte_rel_bit_pos
    

def check_pos(rel):
    global curr_bit_p
    if(rel != curr_bit_p):
        print()


try:
    while (True):
        fq = float(input())
        print(read_data(fq))
        print("Current bit pointer: " + str(curr_bit_p))
except KeyboardInterrupt:
    print("Stopped.")