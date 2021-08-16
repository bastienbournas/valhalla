#!/usr/bin/python
import random
import argparse
import sys,socket
import string
import time


#############################################################################################
#                                                                                           #
#   fuzz                                                                                    #
#   Creates a buffer of increasing length strings and send it                               #
#   bufferEntriesNumber : total number of strings in the buffer                             #
#   growingFactor (=100): string lenght is increased by this number each time,              #
#                         before being added to the buffer                                  #
#   character (='A'): the character to fill strings with                                    #
#   randomCharacter (=False): if set to True, a random character is chosen each time        #
#   ip : ip address where program is hosted                                                 #
#   port : port where program is listening                                                  #
#                                                                                           #
#############################################################################################
def fuzz(bufferEntriesNumber, growingFactor = 100, character = "A", randomCharacter = False, before = None, 
        ip = None, port = None):
    buffer = []
    if (before):
        buffer.append(before)
    counter = growingFactor
    while len(buffer) < int(bufferEntriesNumber):
        if (randomCharacter):
            rand = random.choice(string.ascii_letters)
            buffer.append(rand * counter)
        else :
            buffer.append(character * counter)
        counter += growingFactor
    send(buffer)

#############################################################################################
#                                                                                           #
#   send                                                                                    #
#   Creates a buffer of increasing length strings and send it                               #
#   If ip and port are given, send it via socket, otherwize on stdout                       #
#   buffer : buffer to send as output                                                       #
#   ip : ip address where program is hosted                                                 #
#   port : port where program is listening                                                  #
#                                                                                           #
#############################################################################################
def send(buffer, ip = None, port = None):
    if (ip and port):
        try:
            for str in buffer:
                print('[+] Sending %s bytes...' % len(str), file=sys.stderr)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connect=s.connect((ip,port))
                s.send(string + '\r\n')
                s.recv(1024)
                print('[+] Done', file=sys.stderr)
        except:
            print('[!] Unable to connect to the application. You may have crashed it.', file=sys.stderr)
            sys.exit(0)
        finally:
            s.close()
    else:
        ask = True
        for str in buffer:
            if (ask):
                print('[+] %s bytes ready to send. Press anything to break after or \'c\' to not ask again' 
                    % len(str), file=sys.stderr)
                userInput = input()
                if (userInput == 'c'):
                    ask = False
            print('[+] Sending %s bytes...' % len(str), file=sys.stderr)
            print(str)

#############################################################################################
#                                                                                           #
#   banner                                                                                  #
#   Randomly displays a beautiful viking banner                                             #
#                                                                                           #
#############################################################################################
def banner():
    print("\
              .__  .__           .__  .__          \n\
___  _______  |  | |  |__ _____  |  | |  | _____   \n\
\  \/ /\__  \ |  | |  |  \\__  \ |  | |  | \__  \  \n\
 \   /  / __ \|  |_|   Y  \/ __ \|  |_|  |__/ __ \_\n\
  \_/  (____  /____/___|  (____  /____/____(____  /\n\
            \/          \/     \/               \/ \n\
    ", file=sys.stderr)
    randomValue = random.randint(0, 2)
    if (randomValue == 0):
        print("\
    ,   |\ ,__\n\
    |\   \/   `.\n\
    \ `-.:.     `\n\
     `-.__ `\=====|\n\
        /=`'/   ^_\n\
      .'   /\   .=)\n\
   .-'  .'|  '-(/_|\n\
 .'  __(  \  .'`\n\
/_.'`  `.  |`\n\
          \ |\n\
          |/\n\
        ", file=sys.stderr)
    elif (randomValue == 1):
        print("\
     _.-._\n\
   .' | | `.\n\
  /   | |   \n\
 |    | |    |\n\
 |____|_|____|\n\
 |____(_)____|\n\
 /|(o)| |(o)|\\\n\
//|   | |   |\\\\\n\
'/|  (|_|)  |\`\n\
 //.///|\\\\\\.\\\\\n\
 /////---\\\\\\\\\\ \n\
 ////|||||\\\\\\\\\n\
 '//|||||||\\\\`\n\
   '|||||||`\n\
        ", file=sys.stderr)
    elif (randomValue == 2):
        print("\
                                   ||`-.___\n\
                                   ||    _.>\n\
                                   ||_.-'\n\
               ==========================================\n\
                `.:::::::.       `:::::::.       `:::::::.\n\
                  \:::::::.        :::::::.        :::::::\\\n\
                   L:::::::         :::::::         :::::::L\n\
                   J::::::::        ::::::::        :::::::J\n\
                    F:::::::        ::::::::        ::::::::L\n\
                    |:::::::        ::::::::        ::::::::|\n\
                    |:::::::        ::::::::        ::::::::|     .---.\n\
   .'_ \\            |:::::::        ::::::::        ::::::::|     \\ `--'\n\
   (( ) |           |:::::::        ::::::::        ::::::::|      \\ `.\n\
    `/ /            |:::::::        ::::::::        ::::::::|       L  \\\n\
    / /             |:::::::        ::::::::        ::::::::|       |   \\\n\
   J J              |:::::::        ::::::::        ::::::::|       |    L\n\
   | |              |:::::::        ::::::::        ::::::::|       |    |\n\
   | |              |:::::::        ::::::::        ::::::::|       F    |\n\
   | J\             F:::::::        ::::::::        ::::::::F      /     |\n\
   |  L\           J::::::::       .::::::::       .:::::::J      /      F\n\
   J  J `.     .   F:::::::        ::::::::        ::::::::F    .'      J\n\
    L  \  `.  //  /:::::::'      .::::::::'      .::::::::/   .'        F\n\
    J   `.  `//_..---.   .---.   .---.   .---.   .---.   <---<         J\n\
     L    `-//_=/  _  \=/  _  \=/  _  \=/  _  \=/  _  \=/  _  \       /\n\
     J     /|  |  (_)  |  (_)  |  (_)  |  (_)  |  (_)  |  (_)  |     /\n\
      \   / |   \     //\     //\     //\     //\     //\     /    .'\n\
       \ / /     `---//  `---//  `---//  `---//  `---//  `---'   .'\n\
________/_/_________//______//______//______//______//_________.'_________\n\
##########################################################################\n\
        ", file=sys.stderr)


if __name__ == "__main__":
    text = 'Valhalla is a binary exploitation tool allowing to make basic buffer overflow faster and easier.'
    parser = argparse.ArgumentParser(description=text)

    # General options
    parser.add_argument("-V", "--version", help="show program version", action="store_true")
    parser.add_argument("-s", "--silent", help="hide beautiful viking banner", action="store_true")
    parser.add_argument("-H", "--host", help="set the ip address where program is hosted")
    parser.add_argument("-p", "--port", help="set the port where program is listening")

    # Fuzz options
    parser.add_argument("-f", "--fuzz", help="fuzz the output")
    parser.add_argument("-g", "--grow", help="When fuzzing, the lenght is increased by this number each time (100 by default)")
    parser.add_argument("-c", "--char", help="When fuzzing, the buffer is filled with this character ('A' by default)")
    parser.add_argument("-r", "--random", help="When fuzzing, the buffer is filled random character instead", action="store_true")
    parser.add_argument("-b", "--before", help="When fuzzing, this string is send first before the buffer")
    
    args = parser.parse_args()

    if not (args.silent):
        banner()
    if (args.version):
        print ("Valhalla version 0.1")
    elif (args.fuzz):
        grow = args.grow
        if not (grow):
            grow = 100
        char = args.char
        if not (char):
            char = "A"
        fuzz(bufferEntriesNumber=args.fuzz, growingFactor=grow, character=char, randomCharacter=args.random, before=args.before,
            ip=args.host, port=args.port)