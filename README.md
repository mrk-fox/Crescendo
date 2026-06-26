```
   █████████                                                              █████
  ███░░░░░███                                                            ░░███
 ███     ░░░  ████████   ██████   █████   ██████   ██████  ████████    ███████   ██████
░███         ░░███░░███ ███░░███ ███░░   ███░░███ ███░░███░░███░░███  ███░░███  ███░░███
░███          ░███ ░░░ ░███████ ░░█████ ░███ ░░░ ░███████  ░███ ░███ ░███ ░███ ░███ ░███
░░███     ███ ░███     ░███░░░   ░░░░███░███  ███░███░░░   ░███ ░███ ░███ ░███ ░███ ░███
 ░░█████████  █████    ░░██████  ██████ ░░██████ ░░██████  ████ █████░░████████░░██████
  ░░░░░░░░░  ░░░░░      ░░░░░░  ░░░░░░   ░░░░░░   ░░░░░░  ░░░░ ░░░░░  ░░░░░░░░  ░░░░░░


CRESCENDO v1.1
Developed by Mark Scharonow
https://hackclub.com
https://github.com/mrk-fox/Crescendo
```

Carrier-frequency defined, arpeggiated data-to-audio modulation

> [!IMPORTANT]
> This project is under development. Suggestings and testing feedbacks are welcome!

## Introductions
Data transmission over radio requires high rates of reliability and redundancy. The given repository demostrates a redundant method of data transmissions to prevent bit jumping through byte-bound position frequency modulation. The output is currently bound to the OS selected output audio.

Each bit in the set $D$ , being a set of binary data with certain length gets split into 8-bit packets (bytes). Each bit in the byte gets a freqency assigned based on the position inside the byte and the boolean value. 

$F = F_c + b \cdot F_s$

for the 0 state of the bit and

$F = F_c - b \cdot F_s$

for the 1 state of  the bit.

Also, this model imposes certain functional frequencies designating functional elements of the packet.

```
300 Hz - Message Start (MS)
2100 Hz - Message End (ME)
1200 Hz - Bit Separator (BS)
2200 Hz - Checksum announce flag (CF)
```

## Packet structure
```
[MS][byte 1][byte 2]...[byte x][CF][byte 1][ME]
```
## Features

- Redundancy against bit skip
- Checksum check
- Low-level data output
- FTT for dominant frequency analysis
- Center-frequency driven frequency calculation

## Usage

There are already a few commands implemented:
crescendo.exe


-d: Listens for Audio with the audio interface

-e [String]: Encoding the string to the current audio output

-sf [String] -n [Filename].wav: Writes the encoded audio to a file into the ordner crescendo.exe is in

-h: Displays help with this information

-l: Shows the license information


You can run all of these commands by cd'ing into the crescendo.exe folder and typing crescendo.exe [Flags] into the command line.

## Deployment
1. Download the repository and unzip it
2. Download python from python.org
3. `cd [Project Root Directory]/src`
4. `py -m main.py -h` to get the help page with the possible commands

## License

GNU General Public License 3.0
