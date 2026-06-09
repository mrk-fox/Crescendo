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