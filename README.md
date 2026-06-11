```
   █████████                                                              █████
  ███░░░░░███                                                            ░░███
 ███     ░░░  ████████   ██████   █████   ██████   ██████  ████████    ███████   ██████
░███         ░░███░░███ ███░░███ ███░░   ███░░███ ███░░███░░███░░███  ███░░███  ███░░███
░███          ░███ ░░░ ░███████ ░░█████ ░███ ░░░ ░███████  ░███ ░███ ░███ ░███ ░███ ░███
░░███     ███ ░███     ░███░░░   ░░░░███░███  ███░███░░░   ░███ ░███ ░███ ░███ ░███ ░███
 ░░█████████  █████    ░░██████  ██████ ░░██████ ░░██████  ████ █████░░████████░░██████
  ░░░░░░░░░  ░░░░░      ░░░░░░  ░░░░░░   ░░░░░░   ░░░░░░  ░░░░ ░░░░░  ░░░░░░░░  ░░░░░░
```


# Crescendo
Carrier-frequency defined, arpeggiated data-to-audio modulation

## Introductions
Data transmission over radio requires high rates of reliability and redundancy. The given repository demostrates a redundant method of data transmissions to prevent bit jumping through byte-bound position frequency modulation. The output is currently bound to the OS selected output audio.

Each bit in the set $D$ , being a set of binary data with certain length gets split into 8-bit packets (bytes). Each bit in the byte gets a freqency assigned based on the position inside the byte and the boolean value. 

$F = F_c + b \cdot F_s$

for the 0 state of the bit and

$F = F_c - b \cdot F_s$

for the 1 state of  the bit.

Also, this model imposes certain functional frequencies designating functional elements of the packet.
300 Hz - Message Start (MS)
2100 Hz - Message End (ME)
1200 Hz - Bit Separator (BS)
2200 Hz - Checksum announce flag (CF)

## Packet structure

[MS][byte 1][byte 2]...[byte x][CF][byte 1][ME]

## Features

- Redundancy against bit skip
- Checksum check
- Low-level data output
- FTT for dominant frequency analysis
- Center-frequency driven frequency calculation

## License

