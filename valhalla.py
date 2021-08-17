#!/usr/bin/python
import random
import argparse
import sys,socket
import string
import time


#############################################################################################
#                                                                                           #
#   fuzz                                                                                    #
#   Creates a buffer of increasing length strings and send it.                              #
#   Each string entry can be prepended by the 'before' argument, and contains               #
#   the given 'character' repeated, or a random one if 'randomCharacter' is set.            #
#                                                                                           #
#   bufferEntriesNumber : total number of strings in the buffer                             #
#   growingFactor (=100): string lenght is increased by this number each time,              #
#                         before being added to the buffer                                  #
#   character (='A'): the character to fill strings with                                    #
#   randomCharacter (=False): if set to True, a random character is chosen each time        #
#   before : if set, will be prepended to each buffer buffer entry                          #
#   ip : ip address where program is hosted                                                 #
#   port : port where program is listening                                                  #
#                                                                                           #
#############################################################################################
def fuzz(bufferEntriesNumber, growingFactor = 100, character = "A", randomCharacter = False, before = None, 
        ip = None, port = None):
    buffer = []
    counter = growingFactor

    while len(buffer) < int(bufferEntriesNumber):
        bufferEntry = ''
        if (before):
            bufferEntry = before

        if (randomCharacter):
            rand = random.choice(string.ascii_letters)
            bufferEntry = bufferEntry + (rand * counter)
        else :
            bufferEntry = bufferEntry + (character * counter)

        buffer.append(bufferEntry)
        counter += growingFactor

    send(buffer, ip, port)

#############################################################################################
#                                                                                           #
#   send                                                                                    #
#   Send the given buffer entry by entry, with possibility to break each time               #
#   If ip and port are given, send it via socket, otherwise on stdout                       #
#                                                                                           #
#   buffer : buffer to send as output                                                       #
#   ip : ip address where program is hosted                                                 #
#   port : port where program is listening                                                  #
#                                                                                           #
#############################################################################################
def send(buffer, ip = None, port = None):
    if (ip and port):
        socketSend(buffer, ip, port)
    else:
        stdoutSend(buffer)

#############################################################################################
#                                                                                           #
#   stdoutSend                                                                              #
#   Send the given buffer entry by entry, with possibility to break each time               #
#                                                                                           #
#   buffer : buffer to send on stdout                                                       #
#                                                                                           #
#############################################################################################
def stdoutSend(buffer):
    print('[+] Sending output stdout', file=sys.stderr)
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
#   socketSend                                                                              #
#   Send the given buffer entry by entry, with possibility to break each time               #
#                                                                                           #
#   buffer : buffer to send on the socket (ip, port)                                        #
#   ip : ip address where program is hosted                                                 #
#   port : port where program is listening                                                  #
#                                                                                           #
#############################################################################################
def socketSend(buffer, ip, port):
    print('[+] Sending output on %s:%s' % (ip, port), file=sys.stderr)
    ask = True
    for str in buffer:
        try:
            if (ask):
                print('[+] %s bytes ready to send. Press anything to break after or \'c\' to not ask again' 
                    % len(str), file=sys.stderr)
                userInput = input()
                if (userInput == 'c'):
                    ask = False    
            print('[+] Sending %s bytes...' % len(str), file=sys.stderr)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip,int(port)))
            s.send((str + '\n').encode())
            # Eventually receive data in response from the application
            # s.recv(1024)
            print('[+] Done', file=sys.stderr)
        except Exception as e:
            print(e)
            print('[!] Unable to connect to the application. You may have crashed it.', file=sys.stderr)
            sys.exit(0)
        finally:
            s.close()


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

    # Socket communication options
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
        fuzz(bufferEntriesNumber=args.fuzz, growingFactor=int(grow), character=char, randomCharacter=args.random, before=args.before,
            ip=args.host, port=args.port)