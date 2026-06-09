import argparse
from crescendo_tools import coder
from crescendo_tools import decoder

parser = argparse.ArgumentParser(description="Crescendo CLI")
parser.add_argument('-e', '--encode', nargs='+', help="Input a string of UTF-8 text to encode.")
parser.add_argument('-d', '--decode', action='store_true', help='Decode input stream. Current audio interace is the default source.')
parser.add_argument('-sf', '--savefile', nargs='+', help='Save the encoded frequencies in a generated audio file.')
parser.add_argument('-n', '--name', help='Filename variable for the -sf flag.')


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


args = parser.parse_args()
if args.encode:
    coder.run(' '.join(args.encode))
elif args.decode:
    decoder.run()
elif args.savefile:
    coder.wav(' '.join(args.savefile), args.name)

