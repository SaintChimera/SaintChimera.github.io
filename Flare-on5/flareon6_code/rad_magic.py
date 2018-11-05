#!/usr/bin/python3

import r2pipe
from itertools import product


# rad_magic_run_until allows us to skip brute forcing strings that we already know and have correct in our input. meaning we can brute force 1 substring at a time or skip substrings that fail.
run_f = open("rad_magic_run_until.txt","r")
run_until = int(run_f.read())
run_f.close()

r2 = r2pipe.open("magic_patched",flags=['-e','dbg.profile=magic_patched.rr2','-d']) #load file
r2.cmd('db 0x402ef9') # break in a spot where both substring start and length are available in the registers
r2.cmd('db 0x402f03') # break before call rcx to dump registers
r2.cmd('db 0x402f08') # break after to compare result and reset registers
r2.cmd('dc')


# skips strings at positions that we already know using rad_magic_run_until
for a in range(1,run_until):
    print("run_until:",a)
    r2.cmd('dc')
    r2.cmd('dc')
    r2.cmd('dc')

start = r2.cmd('dr edx') # grab start of string which is the location in the password that is being compared
length = r2.cmd('dr rsi') # grab the length of substring that it is comparing
print(start, length)

r2.cmd('dc')

# dump all registers right before call to rcx
before_rax = r2.cmd('dr rax')
before_rbx = r2.cmd('dr rbx')
before_rcx = r2.cmd('dr rcx')
before_rdx = r2.cmd('dr rdx')
before_r8 = r2.cmd('dr r8')
before_r9 = r2.cmd('dr r9')
before_r10 = r2.cmd('dr r10')
before_r11 = r2.cmd('dr r11')
before_r12 = r2.cmd('dr r12')
before_r13 = r2.cmd('dr r13')
before_r14 = r2.cmd('dr r14')
before_r15 = r2.cmd('dr r15')
before_rip = r2.cmd('dr rip')
before_rsi = r2.cmd('dr rsi')
before_rdi = r2.cmd('dr rdi')
before_rsp = r2.cmd('dr rsp')
before_rbp = r2.cmd('dr rbp')

local_counter = 0

# guess 0x20 to 0x7f since that is the valid printable ASCII range.
for guess_number in product(range(0x20,0x7f), repeat=int(length,16)):
    
    # print status
    if local_counter != guess_number[0]:
        local_counter = guess_number[0]
        print(guess_number)

    # write values dumped earlier from right before call rcx
    r2.cmd('dr rax={}'.format(before_rax))
    r2.cmd('dr rbx={}'.format(before_rbx))
    r2.cmd('dr rcx={}'.format(before_rcx))
    r2.cmd('dr rdx={}'.format(before_rdx))
    r2.cmd('dr r8={}'.format(before_r8))
    r2.cmd('dr r9={}'.format(before_r9))
    r2.cmd('dr r10={}'.format(before_r10))
    r2.cmd('dr r11={}'.format(before_r11))
    r2.cmd('dr r12={}'.format(before_r12))
    r2.cmd('dr r13={}'.format(before_r13))
    r2.cmd('dr r14={}'.format(before_r14))
    r2.cmd('dr r15={}'.format(before_r15))
    r2.cmd('dr rip={}'.format(before_rip))
    r2.cmd('dr rsi={}'.format(before_rsi))
    r2.cmd('dr rdi={}'.format(before_rdi))
    r2.cmd('dr rsp={}'.format(before_rsp))
    r2.cmd('dr rbp={}'.format(before_rbp))

    # seek to the location of our input string and write our brute force substring
    r2.cmd('s {}'.format((int(before_rax,16))))
    r2.cmd('wx {}'.format(''.join(format(x,'x') for x in guess_number)))

    r2.cmd('dc') # continue through call rcx

    # check result in eax after call rcx.
    result = int(r2.cmd('dr eax'),16)
    if result == 1:
        print("ANSWER:",''.join(chr(x) for x in guess_number))
        print("HEX ANSWER:",','.join(hex(x) for x in guess_number))
        print("POSITION:", start)
        print("LENGTH:", length)
        r2.quit()
        exit()

