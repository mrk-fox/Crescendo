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

import argparse
from crescendo_tools import coder
from crescendo_tools import decoder
from crescendo_tools import license_show

parser = argparse.ArgumentParser(description="Crescendo CLI")
parser.add_argument('-e', '--encode', nargs='+', help="Input a string of UTF-8 text to encode.")
parser.add_argument('-d', '--decode', action='store_true', help='Decode input stream. Current audio interace is the default source.')
parser.add_argument('-sf', '--savefile', nargs='+', help='Save the encoded frequencies in a generated audio file.')
parser.add_argument('-n', '--name', help='Filename variable for the -sf flag.')
parser.add_argument('-l', '--license', action='store_true', help='Shows the license Crescendo is under.')


print('   █████████                                                              █████')
print('  ███░░░░░███                                                            ░░███ ')
print(' ███     ░░░  ████████   ██████   █████   ██████   ██████  ████████    ███████   ██████')   
print('░███         ░░███░░███ ███░░███ ███░░   ███░░███ ███░░███░░███░░███  ███░░███  ███░░███')   
print('░███          ░███ ░░░ ░███████ ░░█████ ░███ ░░░ ░███████  ░███ ░███ ░███ ░███ ░███ ░███')  
print('░░███     ███ ░███     ░███░░░   ░░░░███░███  ███░███░░░   ░███ ░███ ░███ ░███ ░███ ░███')
print(' ░░█████████  █████    ░░██████  ██████ ░░██████ ░░██████  ████ █████░░████████░░██████') 
print('  ░░░░░░░░░  ░░░░░      ░░░░░░  ░░░░░░   ░░░░░░   ░░░░░░  ░░░░ ░░░░░  ░░░░░░░░  ░░░░░░')     
                                                               
print("")
print("CRESCENDO v1.1")
print("Developed by Mark Scharonow")
print("https://hackclub.com")
print("https://github.com/mrk-fox/Crescendo")
print("")
print("")
print("Crescendo  Copyright (C) 2025  Mark Scharonow")
print("This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.")
print("This is free software, and you are welcome to redistribute it")
print("under certain conditions; type `show c' for details.")
print("")
print("")

args = parser.parse_args()
if args.encode:
    coder.run(' '.join(args.encode))
elif args.decode:
    decoder.run()
elif args.savefile:
    coder.wav(' '.join(args.savefile), args.name)
elif args.license:
    license_show.run()

